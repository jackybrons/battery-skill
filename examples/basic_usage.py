from pathlib import Path

from battery_skill import ContextBuilder, lint_text


root = Path(__file__).resolve().parents[1]
builder = ContextBuilder(root)

query = "Rewrite the Introduction of an Energy paper on physics-informed cross-chemistry SOH estimation"
bundle = builder.build(query, top_k=6, max_chars=12000)

print("ROUTE:", bundle.route)
print("\nCONTEXT:\n")
print(bundle.render())

sample = "With the rapid development of artificial intelligence, our universal real-time physics-informed model predicts SOH."
print("LINT:")
for warning in lint_text(sample):
    print(f"- {warning.code}: {warning.message}")
