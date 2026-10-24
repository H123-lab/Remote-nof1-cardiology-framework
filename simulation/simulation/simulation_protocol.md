# Statistical Simulation Protocol: Evaluation of Remote N-of-1 Analytic Estimators

This protocol adheres strictly to the **ADEMP** (Aims, Data-generating mechanisms, Estimands, Methods, and Performance measures) reporting framework for statistical simulation designs.

## 1. Aims (A)
The structural objective is to quantify the estimation error, uncertainty calibration, and decision accuracy profiles of three distinct single-patient analytical pipelines under controlled, non-stationary longitudinal data tracking environments.

## 2. Data-Generating Mechanisms (D)
- **Primary Outcome & Measurement Units:** Simulated continuous physiological output variable representing Systolic Blood Pressure (SBP) tracking metrics, measured in millimeters of mercury (mmHg).
- **Target Experimental Cohort Size:** $N = 100$ independent virtual micro-trial units across all prespecified evaluation tracks.
- **Planned Tracking Observations:** Each individual micro-trial executes a 6-period structural cross-over timeline ($ABABAB$). Every discrete period lasts exactly 14 days, yielding $T = 84$ scheduled longitudinal observation nodes per participant block ($100 \times 84 = 8,400$ total planned observations globally across the experimental unit matrix).
- **Randomization Procedure:** Assignment to structural treatment tracks follows a counterbalanced, block-randomized allocation table pre-locked at initialization to guarantee equal tracking sequence balances.

## 3. Estimands (E)
The primary target estimand is the true individual within-patient treatment effect vector ($\delta_i$), set uniformly to a known simulated ground truth constant of $\delta_i = 0.50$ standardized units across the generation grid.

## 4. Methods (M)
The computational framework evaluates three isolated mathematical pipelines:
1. **Simple Paired Comparison:** Simple arithmetic mean difference engine operating on period-aggregated arrays.
2. **Time-Series Regression:** Autoregressive Ordinary Least Squares (OLS) model structure adjusted for temporal trend lines.
3. **Conjugate Bayesian Estimation:** Normal-Normal update structure operating on continuous conditional sequences.

## 5. Performance Measures (P)
The performance landscape maps mathematical estimators across signed bias, Root Mean Squared Error (RMSE), nominal 95% interval coverage thresholds, and absolute directional decision accuracy counts.
