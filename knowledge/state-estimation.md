# State estimation, SOH, and RUL

## Task definitions

SOC, SOH, SOE, and SOP are latent-state estimation problems. RUL and lifetime are prognostic tasks. SOH may be capacity-based, resistance-based, or defined by another health descriptor; reproduce the study definition exactly.

## Practical data limitations

Important issues include partial charging records, nonaligned voltage windows, dynamic duty cycles, temperature changes, sensor noise, sparse reference-capacity tests, cell-to-cell variability, and chemistry/domain shift.

## Validation

For SOH, strong claims are supported by unseen-cell tests, different ageing conditions, multiple temperatures, cross-chemistry datasets, or cell-to-pack validation where relevant. For SOC, use dynamic drive cycles, multiple temperatures, initialization sensitivity, and ageing conditions. For RUL, define the early-life prediction setting and prevent future-data leakage.

## Transfer learning

State source and target domains, target labels available, fine-tuned components, and whether the result is cross-cell, cross-condition, cross-chemistry, cross-dataset, or cell-to-pack transfer.

Testing later cycles from a training cell is not cross-battery generalization.
