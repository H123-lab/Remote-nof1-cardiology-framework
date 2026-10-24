# Mathematical Blueprints and Execution Data-Flow Matrix

This document provides the definitive mathematical blueprints, execution dimensions, and data-flow verification equations governing the **remote-nof1-cardiology-framework** platform ecosystem.

## 1. Primary Framework Data Dimensions & Accounting
Reviewers can trace the exact matrix properties of the generated pre-clinical dataset vectors using this structural accounting blueprint:

| Data Property Node | Calculated Metric Value | Mathematical Definition / Accounting Logic |
| :--- | :--- | :--- |
| **Total Cohort Patient Units ($N$)** | `100` Patients | 33 Patients per Scenario Block + 1 Master Pilot Unit |
| **Structural Cross-Over Periods ($P$)** | `6` Crossover Periods | Alternating treatment blocks structured as an $ABABAB$ sequence |
| **Observations per Period ($t_p$)** | `14` Tracking Days | 14 consecutive daily telemetry nodes per crossover phase |
| **Total Micro-Trial Tracking Slots ($T$)** | `84` Total Days | Mapped exactly as: $6 \text{ Periods} \times 14 \text{ Days} = 84 \text{ Observation rows}$ |
| **Total Database Matrix Rows** | `8,316` Observations | **Planned Raw Observations:** $99 \text{ Patients} \times 84 \text{ Days} = 8,316 \text{ rows}$ |
| **Global Data Record Inventory** | `8,400` Rows | Total framework storage footprint, including the master pilot tracking block |

## 2. Core Generative & Estimator Equations Blueprint
The processing pipelines execute data cleaning and inference using three isolated mathematical modules:

### A. Autoregressive Noise Engine [AR(1)]
The continuous temporal tracking error variable ($\epsilon_{t}$) accounts for day-to-day background telemetry serial dependency:
$$\epsilon_{t} = \rho \cdot \epsilon_{t-1} + \sqrt{1 - \rho^2} \cdot \eta_{t}$$
- **Autocorrelation Coefficient ($\rho$):** Locked uniformly at `0.50`.
- **Innovation Vector ($\eta_{t}$):** White-noise innovations sampled via $\eta_{t} \sim \mathcal{N}(0, \sigma^2_{\text{noise}})$.

### B. Conjugate Bayesian Normal-Normal Update Pipeline
The engine integrates single-patient observations with an objective clinical prior distribution without leaking future ground-truth data structures:
$$\mu_{\text{posterior}} = \sigma^2_{\text{posterior}} \left( \frac{\mu_{\text{prior}}}{\sigma^2_{\text{prior}}} + \frac{\hat{\delta}}{\frac{\sigma^2_{\text{telemetry}}}{n}} \right)$$

$$\frac{1}{\sigma^2_{\text{posterior}}} = \frac{1}{\sigma^2_{\text{prior}}} + \frac{n}{\sigma^2_{\text{telemetry}}}$$
- **Weakly Informative Prior Configuration:** $\mu_{\text{prior}} = 0.0$, $\sigma^2_{\text{prior}} = 4.0$.
- **Likelihood Information Set ($n$):** Equal to the count of actual recorded tracking rows after filtering artifacts and processing adaptive missingness fill loops.

### C. Signal Quality Filter [Path 2 Artifact Gate]
Hard physiological data cleaning thresholds isolate tracking errors before analytical processing:
$$\text{Suppression Rule} = \begin{cases} \text{NaN (Suppressed)} & \text{if } Y_{\text{observed}} < 70.0 \text{ or } Y_{\text{observed}} > 250.0 \\ Y_{\text{observed}} & \text{if } 70.0 \le Y_{\text{observed}} \le 250.0 \end{cases}$$
