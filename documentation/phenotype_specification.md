# Clinical and Pharmacological Parameterization of Simulation Scenarios

This document provides the clinical rationale, pathophysiology links, and telematic profiling justifications for the three primary scenarios evaluated in the **remote-nof1-cardiology-framework** simulation stress test.

## 1. Low-Noise, Low-Missingness Scenario (Phenotype A Calibration)
- **Clinical Persona:** The Stable, High-Compliance Patient.
- **Pathophysiological Context:** Represents a clinically stable NYHA Class II Heart Failure patient with preserved digital literacy and high health motivation. The patient exhibits stable hemodynamics with minimal spontaneous blood pressure volatility.
- **Telematic Parameters & Gaps:**
  - *Missingness Rate:* 5% stochastic dropout mapping routine accidental omissions (e.g., occasional missed morning transmission).
  - *Measurement Noise SD:* 0.25 mmHg, representing high-fidelity telemetry capture (validated clinical-grade upper-arm oscillometric cuffs under quiet resting conditions).
  - *Carryover ($\lambda$):* 0.00, assuming immediate equilibration or adequate physiological clearing between adjustments.

## 2. High-Noise, High-Missingness Scenario (Phenotype B Calibration)
- **Clinical Persona:** The Frail Patient experiencing Tracking Fatigue and Motion Interference.
- **Pathophysiological Context:** Represents an elderly, multimorbid patient facing advanced frailty or mild cognitive burden. Physical tremors or changes in tissue perfusion increase baseline sensor tracking variance.
- **Telematic Parameters & Gaps:**
  - *Missingness Rate:* 30% structured Missing-at-Random (MAR) data loss mapping severe tracking fatigue, technical battery management failures, or intentional device non-wear during active titration phases.
  - *Measurement Noise SD:* 0.75 mmHg, mathematically capturing dense motion artifacts, improper arm cuff positioning, or photoplethysmography (PPG) signal degradation due to poor sensor-to-skin contact during daily movement.
  - *Carryover ($\lambda$):* 0.10, modeling minor background physiological carryover latency.

## 3. Prolonged-Carryover Scenario (Phenotype C Calibration)
- **Clinical Persona:** The Patient with Impaired Renal Clearance (Chronic Kidney Disease / CKD Complex).
- **Pathophysiological Context:** Represents a high-risk HFrEF patient with co-existing Stage 3 Chronic Kidney Disease (eGFR 30–59 mL/min/1.73m²). In heart failure care, neurohormonal antagonists (like ACE inhibitors, ARBs, or ARNIs) rely on stable renal clearance pathways. When clearance is structurally impaired, active drug metabolites remain in the system much longer.
- **Telematic Parameters & Gaps:**
  - *Carryover ($\lambda$):* **0.40 (40% Delay Lag)**. This value means that **40% of the true therapeutic response from the preceding treatment phase structurally persists into the daily measurements of the next crossover block**. This models prolonged pharmacological equilibration delays rather than immediate clearance.
  - *Autocorrelation vs. Carryover Separation:* The pipeline isolates true pharmacological persistence ($\lambda = 0.40$) from simple day-to-day background telematic serial dependency (autocorrelation $\rho = 0.50$), preventing mathematical conflation during analytical updates.
  - *Missingness Rate:* 10% Missing-Not-at-Random (MNAR), configured to drop observation rows preferentially when simulated outcomes cross symptomatic hypotension barriers ($SBP < 95\text{ mmHg}$).
