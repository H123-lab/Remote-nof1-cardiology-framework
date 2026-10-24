# Mathematical Specification of the Data-Generating Model

## 1. Core Structural Signal Architecture
For each virtual participant $i$ at tracking observation step $t$ (where $t \in \{1, 2, \dots, 84\}$), the true latent uncorrupted state variable $Y_{i,t}^*$ is generated via the following structural treatment onset, offset, and carryover equations:

$$Y_{i,t}^* = \mu + \delta \cdot X_{i,t} + \lambda \cdot \delta \cdot X_{i,t-1} + \gamma \cdot t + \epsilon_{i,t}$$

Where:
- $\mu = 120.0\text{ mmHg}$ represents the true global baseline reference center.
- $\delta = 0.50\text{ mmHg}$ denotes the true active treatment effect vector.
- $X_{i,t} \in \{0, 1\}$ represents the active binary treatment phase assignment indicator.
- $\lambda \in \{0.00, 0.10, 0.40\}$ characterizes the **dimensionless carryover persistence coefficient**, representing the exact residual fraction of the previous period's treatment effect vector bleeding into day $t$.
- $\gamma = 0.002$ represents a small, non-stationary background linear temporal trend line.

## 2. Stochastic Temporal Autocorrelation Engine
The background tracking error process $\epsilon_{i,t}$ follows a rigid first-order autoregressive structure, **AR(1)**, initialized independently at $t=1$ via an exact stationary variance configuration:

$$\epsilon_{i,1} \sim \mathcal{N}\left(0, \sigma^2_{\text{residual}}\right)$$
$$\epsilon_{i,t} = \rho \cdot \epsilon_{i,t-1} + \sqrt{1 - \rho^2} \cdot \eta_{i,t}, \quad \text{for } t > 1$$

Where:
- $\rho = 0.50$ represents the active temporal autocorrelation coefficient.
- $\eta_{i,t} \sim \mathcal{N}(0, \sigma^2_{\text{noise}})$ represents white-noise innovations.
- $\sigma^2_{\text{residual}}$ represents the target residual noise variance bounded tightly by phenotype tracking properties.

## 3. Observation Contamination, Artifacts, and Missingness
The actual observed telemetry node $Y_{i,t}$ is extracted by corrupting the true latent physiological state through explicit stochastic measurement errors, random sensor spikes, and structured drop-out masking tracks:

$$Y_{i,t} = 
\begin{cases} 
\text{NaN} & \text{if } M_{i,t} = 1 \quad \text{[Missingness Model]} \\
Y_{i,t}^* + \xi_{i,t} + \theta_{i,t} & \text{if } M_{i,t} = 0 \quad \text{[Observed Data Model]}
\end{cases}$$

- **Noise Distribution:** $\xi_{i,t} \sim \mathcal{N}(0, \sigma^2_{\text{measurement}})$, where $\sigma_{\text{measurement}} \in \{0.25, 0.75\}$ parameters model low-noise vs high-noise hardware tracking grids.
- **Sensor Spikes & Artifacts:** $\theta_{i,t} \sim \text{Bernoulli}(\pi_{\text{artifact}}) \times \mathcal{N}(0, 25.0)$ simulates isolated electronic tracking glitches.
- **Missingness Mechanism Architecture:** Data dropouts operate via a combined Missing-at-Random (**MAR**) and Missing-Not-at-Random (**MNAR**) configuration framework. The structural probability of a tracking drop event ($P(M_{i,t} = 1)$) varies dynamically based on active treatment transitions and severe physical symptomatology:

$$\text{logit}\left(P(M_{i,t} = 1)\right) = \beta_0 + \beta_1 \cdot X_{i,t} + \beta_2 \cdot \mathbb{I}(Y_{i,t}^* < 95)$$

This layout enforces conditional missingness dependencies driven by active low blood pressure symptoms or phase adjustments rather than assuming basic completely random data drops (MCAR).
