# Battery-AI manuscript writing

## Abstract

Use six moves: task importance -> concrete bottleneck -> proposed approach -> essential components and why they are needed -> validation plus quantitative results -> scientific/engineering implication.

Prefer: `Most existing SOH models are trained within a single chemistry, limiting transfer to cells with different voltage characteristics and ageing trajectories.`

Avoid: `Existing methods still have some limitations in practical applications.`

Mention only architecture components that explain the novelty. Report the number of independent cells, chemistries, conditions, labels, or experimental iterations when they support the main claim. A percentage improvement must identify the metric and baseline.

## Introduction

Start from the battery task and consequence, not from the popularity of AI. Organize existing work by scientific solution family: direct diagnostics, model-based estimation, data-driven learning, hybrid/physics-informed methods, or other task-specific families.

Acknowledge what current methods solve, then identify testable gaps such as dependence on complete cycles, label scarcity, chemistry-specific training, cell-to-pack domain shift, temperature sensitivity, sensor missingness, lack of physical consistency, uncertainty, unrealistic evaluation splits, or deployment cost.

Group literature by the problem addressed rather than listing CNN/LSTM/GRU/Transformer. Compare assumptions, data requirements, validation domains, and unresolved limitations.

Contributions should map one-to-one to gaps and contain `what + why + evidence/setting`. Replace `A novel Transformer is proposed` with a scientifically specific contribution such as `A transferable temporal representation is developed to learn degradation features shared across chemistries, reducing dependence on target-domain labels.`

## Methods

Describe the data/experiment before neural-network equations: chemistry, form factor, capacity, voltage/current protocol, temperature, ageing conditions, reference tests, target definition, and dataset organization when available.

Use cell-independent or domain-independent validation when claiming generalization. Random cycle-level splitting can leak information because adjacent cycles from the same cell are correlated.

For each feature, explain extraction, physical relevance, operational availability, and sensitivity to noise/temperature/partial data when relevant. Describe architecture in information-flow order and map each component to a battery problem.

For physics-informed losses, state the data-fitting term, physical residual/constraint, regularization, weighting strategy, and physical interpretation. Report reproducibility details where available.

## Results and Discussion

Organize around questions rather than figure order: unseen-cell accuracy, cross-chemistry transfer, effect of physics constraints, robustness to partial/noisy data, degradation interpretation, or deployment cost.

Potential evidence includes in-domain performance, unseen-cell testing, cross-condition/temperature validation, cross-chemistry/external validation, small-data behavior, noise/missing-data robustness, ablation, physical consistency, uncertainty, and computational cost.

Keep four levels separate: observation -> interpretation -> mechanistic evidence -> generalization. Attention/SHAP/saliency indicates association unless independent evidence supports a causal electrochemical interpretation.

## Conclusion

Answer: what battery problem was solved, what methodological idea mattered, what evidence supports it, and what boundary remains. Prefer a concrete limitation such as additional chemistries, pack validation, low-temperature ageing, field data, uncertainty calibration, or embedded inference over a generic future-work sentence.
