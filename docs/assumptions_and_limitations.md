# Methodological Assumptions and Scope Limitations

This document explicitly catalogs the foundational parameters, design assumptions, and scope boundaries governing the pre-clinical in-silico 100-patient heart failure validation cohort simulation.

## 1. Core Generative Assumptions & Rationale

### A. Autoregressive Error Structure [AR(1)]
- **Assumption:** Within-patient blood pressure fluctuations exhibit first-order temporal autocorrelation ($\rho = 0.50$ baseline, escalating to $0.75$ in stress states).
- **Rationale:** Human cardiovascular physiology is intrinsically non-stationary; serial measurements collected over short intervals (e.g., daily) are strongly dependent on prior states due to neurohormonal and circadian baselines.
- **Dependent Analyses:** Affects all standard errors, confidence/credible interval widths, and coverage calibration models across the parallel pipelines.

### B. Pharmacodynamic Carryover Fractions
- **Assumption:** Phase transitions embed a deterministic decay lag ($\lambda = 0.40$ in Scenario 3) bleeding directly into subsequent crossover blocks.
- **Rationale:** Patients with chronic kidney disease (CKD) or metabolic clearance barriers exhibit significantly prolonged drug equilibration windows when transitioning between active guideline-directed medical therapies (GDMT).
- **Dependent Analyses:** Directly drives the estimation bias inflation tracked in Figure 7 Panel A and Figure S2 Panel A.

### C. Missingness Topography (MAR & MNAR Masks)
- **Assumption:** Patient non-adherence follows a Missing-at-Random (MAR) tracking drop pattern under severe fatigue, or a symptom-driven Missing-Not-at-Random (MNAR) dropout pattern under severe hypotension.
- **Rationale:** Real-world telematic trials face heavy adherence attrition driven directly by physical frailty or acute decompensation events.
- **Dependent Analyses:** Validates the adaptive forward-fill preprocessing filters and imputation boundary checks.

## 2. Permanent Scope Limitations

1. **Pre-Clinical Software Bounding:** These datasets and scripts represent an in-silico computational stress test of mathematical estimators. They do not utilize live human clinical trials, nor do they evaluate absolute clinical efficacy.
2. **Clinical Stability Requirement:** This framework is designed strictly for clinically stable, reversible chronic cardiovascular conditions (e.g., stable HFrEF titration). It cannot be extrapolated to acute unstable syndromes, irreversible interventions, or primary survival endpoints.
