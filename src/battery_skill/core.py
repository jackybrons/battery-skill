from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9-]*|[\u4e00-\u9fff]{1,4}|\d+(?:\.\d+)?")
HEADING_RE = re.compile(r"^(#{1,4})\s+(.+?)\s*$")


@dataclass(frozen=True)
class Route:
    section: str | None = None
    domains: tuple[str, ...] = ()
    journals: tuple[str, ...] = ()
    needs_terminology: bool = True

    @property
    def preferred_paths(self) -> tuple[str, ...]:
        paths: list[str] = []
        if self.needs_terminology:
            paths.append("knowledge/terminology.md")
        if self.section:
            paths.append("knowledge/writing.md")
        mapping = {
            "state-estimation": "knowledge/state-estimation.md",
            "degradation": "knowledge/degradation-physics.md",
            "physics-informed": "knowledge/degradation-physics.md",
            "safety": "knowledge/safety-control.md",
            "fast-charging": "knowledge/safety-control.md",
            "materials-discovery": "knowledge/materials-discovery.md",
        }
        paths.extend(mapping[d] for d in self.domains if d in mapping)
        if self.journals:
            paths.append("knowledge/journals.md")
        return tuple(dict.fromkeys(paths))


@dataclass(frozen=True)
class Chunk:
    path: str
    heading: str
    text: str
    ordinal: int

    @property
    def id(self) -> str:
        return f"{self.path}::{self.ordinal}::{self.heading}"


@dataclass(frozen=True)
class SearchHit:
    chunk: Chunk
    score: float


@dataclass
class ContextBundle:
    root: Path
    query: str
    route: Route
    skill_text: str
    hits: list[SearchHit] = field(default_factory=list)

    def render(self) -> str:
        blocks = ["# Runtime skill\n\n" + self.skill_text.strip(), "# Retrieved battery-writing knowledge"]
        for hit in self.hits:
            blocks.append(f"## Source: {hit.chunk.path} — {hit.chunk.heading}\n\n{hit.chunk.text.strip()}")
        return "\n\n".join(blocks).strip() + "\n"


SECTION_KEYWORDS: dict[str, tuple[str, ...]] = {
    "abstract": ("abstract", "摘要"),
    "introduction": ("introduction", "intro", "引言", "绪论", "related work", "literature review"),
    "methods": ("method", "methods", "methodology", "方法", "experimental", "实验方法", "model architecture"),
    "results-discussion": ("result", "results", "discussion", "结果", "讨论", "ablation", "消融", "interpretability", "可解释"),
}
DOMAIN_KEYWORDS: dict[str, tuple[str, ...]] = {
    "state-estimation": ("soh", "soc", "soe", "sop", "state of health", "state-of-health", "state of charge", "state-of-charge", "rul", "remaining useful life", "lifetime prediction", "capacity estimation", "health estimation"),
    "degradation": ("degradation", "ageing", "aging", "ica", "incremental capacity", "dva", "differential voltage", "eis", "impedance", "lli", "lam", "lithium plating", "sei", "degradation mode", "退化", "老化", "阻抗", "增量容量"),
    "physics-informed": ("physics-informed", "physics informed", "physics-guided", "physics guided", "pinn", "piml", "electrochemical model", "ecm", "dfn", "p2d", "spm", "spme", "物理信息", "物理约束", "电化学模型"),
    "safety": ("thermal runaway", "fault diagnosis", "fault detection", "early warning", "safety", "abuse test", "gas sensor", "thermal propagation", "热失控", "故障诊断", "预警", "安全"),
    "fast-charging": ("fast charging", "fast-charging", "charging optimization", "charging control", "reinforcement learning", "bayesian optimization", "model predictive control", "快速充电", "快充", "强化学习", "贝叶斯优化", "充电控制"),
    "materials-discovery": ("electrolyte", "solid electrolyte", "materials discovery", "material discovery", "active learning", "machine learning potential", "interatomic potential", "dft", "anode-free", "lithium metal", "electrolyte discovery", "材料发现", "电解液", "固态电解质"),
}
JOURNAL_KEYWORDS: dict[str, tuple[str, ...]] = {
    "energy": ("energy journal", "journal energy", "《energy》", "energy期刊"),
    "applied-energy": ("applied energy",),
    "jps": ("journal of power sources", "jps"),
    "esm": ("energy storage materials", "esm"),
}


def _contains(text: str, keyword: str) -> bool:
    if re.fullmatch(r"[a-z0-9-]+", keyword):
        return re.search(rf"(?<![a-z0-9-]){re.escape(keyword)}(?![a-z0-9-])", text) is not None
    return keyword in text


def _matches(text: str, mapping: dict[str, tuple[str, ...]]) -> tuple[str, ...]:
    return tuple(label for label, keywords in mapping.items() if any(_contains(text, kw) for kw in keywords))


def route_query(query: str) -> Route:
    text = query.lower()
    sections = _matches(text, SECTION_KEYWORDS)
    domains = tuple(dict.fromkeys(_matches(text, DOMAIN_KEYWORDS)))
    journals = tuple(dict.fromkeys(_matches(text, JOURNAL_KEYWORDS)))
    terminology_triggers = ("term", "terminology", "术语", "wording", "rewrite", "润色", "write", "写", "paper", "论文")
    return Route(
        section=sections[0] if sections else None,
        domains=domains,
        journals=journals,
        needs_terminology=bool(domains) or any(t in text for t in terminology_triggers),
    )


def tokenize(text: str) -> list[str]:
    return [m.group(0).lower() for m in TOKEN_RE.finditer(text)]


def _split_long(text: str, max_chars: int = 1800, overlap: int = 180) -> list[str]:
    text = text.strip()
    if len(text) <= max_chars:
        return [text] if text else []
    pieces: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        if end < len(text):
            boundary = max(text.rfind("\n\n", start, end), text.rfind(". ", start, end))
            if boundary > start + max_chars // 2:
                end = boundary + 1
        pieces.append(text[start:end].strip())
        if end >= len(text):
            break
        start = max(start + 1, end - overlap)
    return [p for p in pieces if p]


def chunk_markdown(path: Path, root: Path) -> list[Chunk]:
    rel = path.relative_to(root).as_posix()
    lines = path.read_text(encoding="utf-8").splitlines()
    chunks: list[Chunk] = []
    heading = path.stem.replace("-", " ")
    buf: list[str] = []
    ordinal = 0

    def flush() -> None:
        nonlocal ordinal, buf
        body = "\n".join(buf).strip()
        if body:
            for piece in _split_long(body):
                chunks.append(Chunk(rel, heading, piece, ordinal))
                ordinal += 1
        buf = []

    for line in lines:
        match = HEADING_RE.match(line)
        if match:
            flush()
            heading = match.group(2).strip()
        else:
            buf.append(line)
    flush()
    return chunks


class BM25Retriever:
    """Heading-aware local retriever. Replace `search()` with embeddings/hybrid search if desired."""

    def __init__(self, root: Path, knowledge_dir: str = "knowledge") -> None:
        self.root = Path(root)
        paths = sorted((self.root / knowledge_dir).rglob("*.md"))
        self.chunks = [chunk for path in paths for chunk in chunk_markdown(path, self.root)]
        self._tokens = [tokenize(f"{c.heading}\n{c.text}") for c in self.chunks]
        self._tfs = [Counter(tokens) for tokens in self._tokens]
        self._lengths = [len(tokens) for tokens in self._tokens]
        self._avgdl = (sum(self._lengths) / len(self._lengths)) if self._lengths else 1.0
        self._dfs: Counter[str] = Counter()
        for tokens in self._tokens:
            self._dfs.update(set(tokens))

    def _idf(self, term: str) -> float:
        n, df = len(self.chunks), self._dfs.get(term, 0)
        return math.log(1.0 + (n - df + 0.5) / (df + 0.5)) if n else 0.0

    def _bm25(self, terms: Iterable[str], i: int, k1: float = 1.5, b: float = 0.75) -> float:
        tf, dl = self._tfs[i], self._lengths[i] or 1
        score = 0.0
        for term in terms:
            freq = tf.get(term, 0)
            if freq:
                denom = freq + k1 * (1 - b + b * dl / self._avgdl)
                score += self._idf(term) * (freq * (k1 + 1) / denom)
        return score

    @staticmethod
    def _route_boost(chunk: Chunk, route: Route) -> float:
        boost = 4.0 if chunk.path in route.preferred_paths else 0.0
        if route.section and chunk.path == "knowledge/writing.md" and route.section.replace("-", " ") in chunk.heading.lower():
            boost += 2.0
        if route.journals and chunk.path == "knowledge/journals.md":
            boost += 1.5
        return boost

    def search(self, query: str, route: Route, k: int = 6) -> list[SearchHit]:
        terms = tokenize(query) or ["battery"]
        query_lower = query.lower()
        hits: list[SearchHit] = []
        for i, chunk in enumerate(self.chunks):
            score = self._bm25(terms, i) + self._route_boost(chunk, route)
            corpus = (chunk.heading + " " + chunk.text).lower()
            for phrase in ("state of health", "remaining useful life", "physics-informed", "thermal runaway", "active learning"):
                if phrase in query_lower and phrase in corpus:
                    score += 1.25
            if score > 0:
                hits.append(SearchHit(chunk, score))
        hits.sort(key=lambda h: (-h.score, h.chunk.path, h.chunk.ordinal))

        selected: list[SearchHit] = []
        selected_ids: set[str] = set()
        seen: set[tuple[str, ...]] = set()

        def add(hit: SearchHit) -> bool:
            signature = tuple(tokenize(hit.chunk.text)[:28])
            if hit.chunk.id in selected_ids or signature in seen:
                return False
            selected.append(hit)
            selected_ids.add(hit.chunk.id)
            seen.add(signature)
            return True

        # Route is a hard hint: guarantee representation from relevant narrow files
        # before filling the remaining slots by global BM25 score.
        for preferred in route.preferred_paths:
            best = next((h for h in hits if h.chunk.path == preferred), None)
            if best is not None:
                add(best)
            if len(selected) >= k:
                return selected

        for hit in hits:
            add(hit)
            if len(selected) >= k:
                break
        return selected


class ContextBuilder:
    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.skill_path = self.root / "SKILL.md"
        if not self.skill_path.exists():
            raise FileNotFoundError(f"SKILL.md not found under {self.root}")
        self.retriever = BM25Retriever(self.root)

    def build(self, query: str, top_k: int = 6, max_chars: int = 12000) -> ContextBundle:
        route = route_query(query)
        skill_text = self.skill_path.read_text(encoding="utf-8")
        augmented = " ".join([query, route.section or "", *route.domains, *route.journals]).strip()
        candidates = self.retriever.search(augmented, route, k=max(top_k * 3, top_k))
        selected: list[SearchHit] = []
        used = len(skill_text)
        for hit in candidates:
            cost = len(hit.chunk.text) + len(hit.chunk.heading) + len(hit.chunk.path) + 80
            if selected and used + cost > max_chars:
                continue
            selected.append(hit)
            used += cost
            if len(selected) >= top_k:
                break
        return ContextBundle(self.root, query, route, skill_text, selected)


@dataclass(frozen=True)
class LintWarning:
    code: str
    message: str


LINT_RULES = (
    ("ICA_DVA", re.compile(r"incremental capacity.{0,80}dV\s*/\s*dQ|dV\s*/\s*dQ.{0,80}incremental capacity", re.I | re.S), "Incremental capacity analysis is typically associated with dQ/dV; verify that ICA and DVA were not swapped."),
    ("DVA_ICA", re.compile(r"differential voltage.{0,80}dQ\s*/\s*dV|dQ\s*/\s*dV.{0,80}differential voltage", re.I | re.S), "Differential voltage analysis is typically associated with dV/dQ; verify that DVA and ICA were not swapped."),
    ("GEN_CLAIM", re.compile(r"\b(generaliz\w*|universal)\b", re.I), "Generalization claim detected. Check evaluation on unseen cells/domains/conditions appropriate to the claim."),
    ("REALTIME_CLAIM", re.compile(r"\breal[- ]?time\b", re.I), "Real-time claim detected. Verify latency/hardware/deployment evidence."),
    ("INTERPRET_CLAIM", re.compile(r"\binterpretab\w*\b|\bexplainab\w*\b", re.I), "Interpretability claim detected. Do not imply causality from attention/SHAP alone."),
    ("PHYSICS_CLAIM", re.compile(r"\bphysics[- ]informed\b", re.I), "Physics-informed claim detected. Identify the physical source, where it enters, and a data-only comparison."),
    ("AI_BOILERPLATE", re.compile(r"with the rapid development of (artificial intelligence|machine learning)|has attracted widespread attention|plays a crucial role", re.I), "Generic academic boilerplate detected. Replace it with the concrete battery problem and consequence."),
)


def lint_text(text: str) -> list[LintWarning]:
    warnings = [LintWarning(code, message) for code, pattern, message in LINT_RULES if pattern.search(text)]
    if re.search(r"\bthermal runaway prediction\b", text, re.I) and re.search(r"after (failure|runaway)|post[- ]event", text, re.I):
        warnings.append(LintWarning("TR_TIMING", "Verify event timing; post-event classification should usually be described as detection/diagnosis rather than prediction."))
    return warnings
