# Prespecified Statistical Analysis Plan (SAP)

This document formalizes the operational objective, prespecified targets, and benchmark metrics for the single-patient cardiology estimation suites prior to execution.

## 1. Statistical Estimands & Targets
- **Primary Estimand ($\delta_i$):** The within-patient latent true treatment-effect contrast, measured as the absolute change in Systolic Blood Pressure proxy (mmHg) between Strategy B (Intervention) and Strategy A (Control).
- **Primary Inferential Unit:** The individual patient trial trajectory ($N=1$ multi-period crossover blocks, 84 days tracking footprint).

## 2. Evaluating Estimator Suites
- **Pipeline 1 [Simple Paired Comparison]:** Period-aggregated frequentist arithmetic mean difference. Evaluated as a low-complexity transparent baseline framework.
- **Pipeline 2 [Time-Series Segmented Regression]:** Autoregressive error models adjusting directly for sequential dependencies and day-indexed linear trend terms.
- **Pipeline 3 [Conjugate Bayesian Posterior Update]:** Gaussian-likelihood update rules mapping direct posterior probability curves without structural asymptotic dependencies.

## 3. Core Operational Decision Rules
- **Inclusive Rule Framework:** An active clinical selection is issued if and only if:
  $$\text{Pr}(\delta > 0 \mid \text{Data}) \ge 0.90$$
- **Abstention Mode:** If the posterior probability fails to clear the nominal 90% boundary due to high tracking noise or variance blocks, the system issues an automated `Abstain_Inconclusive` marker, holding treatment unchanged.

## 4. Benchmark Performance Metrics
1. **Signed & Absolute Bias:** $\mathbb{E}[\hat{\delta}] - \delta_{\text{true}}$ (Target: 0.00).
2. **Root Mean Squared Error (RMSE):** Total estimation precision bounds.
3. **95% Interval Coverage Calibration:** The empirical frequency of the true effect falling inside calculated boundaries (Target: 95%).
4. **Treatment-Selection Accuracy:** Proportion of replicates correctly identifying the superior strategy across a 1,000 Monte Carlo repeated run matrix.
