# battery-skill

A retrieval-augmented academic-writing skill for **AI for Battery** research.

The project is deliberately split into two layers:

- `SKILL.md`: a short runtime policy that is safe to include in every request.
- `knowledge/`: domain and writing knowledge that is retrieved only when relevant.

The included Python package implements a lightweight local RAG pipeline with no third-party runtime dependencies: task routing, heading-aware Markdown chunking, BM25-style retrieval, route-aware score boosts, context budgeting, and a battery-specific claim/terminology linter.

## Why this structure

A 40–50k character monolithic skill wastes context and makes instructions compete with one another. This repository instead follows:

```text
user request
    |
    v
TaskRouter --------------------+
    |                           |
    v                           v
SKILL.md                  route metadata
(always loaded)           section/domain/journal
    |                           |
    +------------+--------------+
                 v
           BM25Retriever
      heading-aware knowledge chunks
                 |
                 v
           ContextBuilder
      token/character budget + dedupe
                 |
                 v
                LLM
```

## Repository layout

```text
battery-skill/
├── SKILL.md
├── knowledge/
│   ├── terminology.md
│   ├── writing.md
│   ├── state-estimation.md
│   ├── degradation-physics.md
│   ├── safety-control.md
│   ├── materials-discovery.md
│   ├── journals.md
│   └── references.md
├── src/battery_skill/
│   ├── core.py
│   └── cli.py
├── examples/
└── tests/
```

## Install

Python 3.10+.

```bash
pip install -e .
```

No external vector database or embedding model is required.

## CLI

Inspect routing:

```bash
battery-skill route "Rewrite my physics-informed SOH introduction for Energy"
```

Retrieve relevant knowledge only:

```bash
battery-skill retrieve "cross-chemistry SOH estimation with partial charging curves" -k 6
```

Build the full runtime context that should be supplied to an LLM:

```bash
battery-skill context "Rewrite my physics-informed SOH introduction for Energy" > context.txt
```

Lint a manuscript fragment:

```bash
battery-skill lint draft.txt
```

## Python usage

```python
from pathlib import Path
from battery_skill import ContextBuilder

root = Path(".")
builder = ContextBuilder(root)

bundle = builder.build(
    query="Rewrite this Introduction for an Energy paper on cross-chemistry SOH estimation",
    top_k=6,
    max_chars=12000,
)

# Send bundle.render() as domain context/instructions to your preferred LLM.
print(bundle.route)
print(bundle.render())
```

The package is provider-neutral. You can pass the rendered context to any model or agent framework. For production systems, replace `BM25Retriever` with an embedding/hybrid retriever while keeping the same `search()` contract.

## Retrieval design

The default retriever:

1. chunks Markdown by headings, preserving source path and section title;
2. applies BM25-style lexical scoring;
3. boosts chunks whose path matches the routed section/domain/journal;
4. de-duplicates near-identical chunks;
5. enforces a context budget;
6. always keeps the short `SKILL.md` separate from retrieved knowledge.

This makes the system deterministic, inspectable, cheap, and easy to test. It is also a useful fallback if an embedding service is unavailable.

## Extending the knowledge base

Add Markdown files under `knowledge/`. Prefer narrow documents with meaningful headings. The retriever automatically indexes them.

For new domain files, add routing keywords and path mapping in `src/battery_skill/core.py` so relevant queries receive a path boost.

## Engineering guidance

In a mature deployment, treat retrieved text as reference context rather than unconditional instructions. The hard behavioral constraints live in `SKILL.md`; the knowledge base supplies terminology, domain patterns, validation expectations, and examples.

For literature-dependent or time-sensitive technical claims, perform fresh source verification before drafting. The included literature corpus is a writing/terminology reference, not a substitute for current literature search.

## Tests

```bash
python -m unittest discover -s tests -v
```

## License

MIT.
