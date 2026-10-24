# Analytical Pipe Modeling Mappings and Estimator Specifications

## 1. Baseline Ordinary Least Squares Model
Equation: $Y_t = \beta_0 + \beta_1 X_t + \gamma t + \epsilon_t$
- **Unit of Analysis:** Daily structural mean score.
- **Leakage Controls:** No access parameters to hidden baseline simulation fields or future arrays are permitted.

## 2. Conjugate Bayesian Pipeline
Equation Likelihood: $Y_t \sim \mathcal{N}(\mu_t, \sigma^2_{\text{noise}})$
- **Structural Independence Constraint Warning:** The simple conjugate update model assumes conditionally independent tracking coordinates. When analyzing serially dependent sequences ($\rho = 0.50$), standard credible boundaries will exhibit narrowing drift distortions (coverage variance drop as detailed in Main Table 8). This systematic deviation is documented here as an expected performance edge-case boundary rather than an unmodeled software bug.
