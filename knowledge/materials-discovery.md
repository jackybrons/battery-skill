# AI for battery materials and electrolyte discovery

## Scientific narrative

Use the sequence: chemical/design space -> expensive experiment or calculation -> data-efficient surrogate -> candidate selection -> prospective experimental validation -> mechanistic interpretation.

AI is most persuasive when it changes the discovery loop rather than merely fitting an offline property table.

## Electrolytes

Specify chemistry, salt, solvent/co-solvent/diluent/additive, concentration, cell configuration, and target property. Candidate targets include ionic conductivity, viscosity, electrochemical stability, solubility, interphase-forming behavior, Coulombic efficiency, capacity retention, and cycle life.

Do not label a computationally screened molecule a successful electrolyte before formulation and electrochemical testing.

## Active learning and Bayesian optimization

Report the initial dataset, candidate space, acquisition rule, batch size, number of experimental iterations, uncertainty model, and prospective validation. `Data efficient` should be supported by concrete sample or experiment counts.

## Machine-learning potentials

Distinguish a machine-learning interatomic potential from a property predictor. State the reference electronic-structure data, training domain, validation configurations, and extrapolation limits.
