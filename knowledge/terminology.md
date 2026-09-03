# Battery terminology and claim discipline

## State variables and prognostics

Use `state-of-charge (SOC) estimation`, `state-of-health (SOH) estimation`, `state-of-energy (SOE) estimation`, and `state-of-power (SOP) estimation` for present latent states. Use `remaining useful life (RUL) prediction/prognosis`, `lifetime prediction`, or `degradation trajectory prediction` for future quantities.

Do not say that a model *measures* SOH unless SOH is directly defined by a reference test. A model normally *estimates* SOH from observable signals.

A capacity-based SOH definition often resembles current available capacity divided by a reference capacity, but the exact denominator must follow the study. Never silently assume initial capacity, nominal capacity, or rated capacity.

## Cell, module, and pack

Use the physical scale precisely. Validation on individual cells does not establish module- or pack-level performance. Cell-to-pack transfer must be stated explicitly and validated with pack data.

## Capacity retention and Coulombic efficiency

Capacity retention describes retained discharge/usable capacity relative to a reference. Coulombic efficiency compares charge passed during discharge and charge during charging for a cycle or defined test. They are not interchangeable.

## Charging terminology

Use `constant-current (CC)`, `constant-voltage (CV)`, and `constant-current–constant-voltage (CC–CV)` accurately. Distinguish full charging curves from partial/incomplete/random charging segments. Define fast charging using the actual current/C-rate/protocol rather than the adjective alone.

## ICA and DVA

Incremental capacity analysis (ICA) is typically associated with `dQ/dV`. Differential voltage analysis (DVA) is typically associated with `dV/dQ`. Do not swap them. When smoothing or differentiating experimental curves, report preprocessing choices if they materially affect peaks.

## EIS and resistance

`Electrochemical impedance spectroscopy (EIS)` yields frequency-dependent complex impedance. Do not reduce EIS to a generic scalar “internal resistance” without describing how the feature is derived. `Direct-current internal resistance (DCIR)` is a separate time-domain pulse-based quantity when measured using a specified protocol.

## Degradation language

Use `loss of lithium inventory (LLI)`, `loss of active material (LAM)`, `lithium plating`, `solid electrolyte interphase (SEI) growth`, `electrolyte decomposition`, `particle cracking`, and related mechanisms only when supported by diagnostic, model-based, or experimental evidence.

A statistical feature importance map, attention map, or SHAP value alone does not establish a causal degradation mechanism.

## Electrochemical and equivalent-circuit models

Equivalent circuit models (ECMs) are phenomenological electrical models. They are not the same as electrochemical models such as SPM/SPMe or DFN/P2D. A neural network does not become physics-informed merely because voltage, current, or temperature are inputs.

## Chemistry

Common abbreviations include LFP, NMC, NCA, LCO, LTO, graphite, silicon/graphite, and lithium metal. Preserve the exact chemistry and stoichiometry used by the source study. Do not infer a specific NMC composition such as NMC811 unless reported.

## Lithium-metal and electrolyte studies

Distinguish Li||Cu, Li||Li symmetric cells, Cu||cathode anode-free cells, and practical full cells. Coulombic efficiency from Li||Cu is not a substitute for full-cell capacity retention.

When discussing electrolytes, distinguish salt, solvent, co-solvent, diluent, additive, concentration, solvation structure, and interphase chemistry. A computationally screened molecule is a candidate, not a validated high-performance electrolyte, until experimentally formulated and tested.

## Claim vocabulary

Use `demonstrates` for directly tested findings with adequate evidence; `shows/indicates/supports` for empirical patterns; and `suggests/may/is consistent with` for mechanisms or broader generalizations that were not directly isolated.

Words that require explicit evidence: `generalizable`, `interpretable`, `physics-informed`, `real-time`, `robust`, `universal`, `mechanistic`, `state-of-the-art`, `low-cost`.
