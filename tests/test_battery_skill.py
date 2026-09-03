import unittest
from pathlib import Path

from battery_skill import BM25Retriever, ContextBuilder, lint_text, route_query

ROOT = Path(__file__).resolve().parents[1]


class BatterySkillTests(unittest.TestCase):
    def test_route_physics_soh_energy_introduction(self):
        route = route_query("Rewrite my physics-informed SOH Introduction for Energy journal")
        self.assertEqual(route.section, "introduction")
        self.assertIn("state-estimation", route.domains)
        self.assertIn("physics-informed", route.domains)
        self.assertIn("energy", route.journals)

    def test_material_route_and_retrieval(self):
        query = "Write an abstract on active learning for electrolyte discovery"
        route = route_query(query)
        self.assertEqual(route.section, "abstract")
        self.assertIn("materials-discovery", route.domains)
        hits = BM25Retriever(ROOT).search(query, route, k=4)
        self.assertTrue(any("materials-discovery.md" in h.chunk.path for h in hits))

    def test_physics_retrieval(self):
        query = "cross-chemistry physics-informed SOH with partial charging curves"
        route = route_query(query)
        hits = BM25Retriever(ROOT).search(query, route, k=5)
        paths = [h.chunk.path for h in hits]
        self.assertIn("knowledge/state-estimation.md", paths)
        self.assertIn("knowledge/degradation-physics.md", paths)

    def test_context_budget(self):
        bundle = ContextBuilder(ROOT).build("Rewrite my SOH introduction using partial charging curves", top_k=5, max_chars=9000)
        rendered = bundle.render()
        self.assertIn("# Runtime skill", rendered)
        self.assertIn("Retrieved battery-writing knowledge", rendered)
        self.assertLess(len(rendered), 11000)

    def test_lint(self):
        codes = {w.code for w in lint_text("With the rapid development of artificial intelligence, our universal real-time physics-informed model predicts SOH.")}
        self.assertTrue({"AI_BOILERPLATE", "GEN_CLAIM", "REALTIME_CLAIM", "PHYSICS_CLAIM"}.issubset(codes))


if __name__ == "__main__":
    unittest.main()
