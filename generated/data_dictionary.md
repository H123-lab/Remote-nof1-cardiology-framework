# Data Dictionary: Simulation Truth and Generated Datasets

## 1. File: `virtual_cohort_full.csv`
- `Participant_ID`: Unique patient alphanumeric identifier (PAT_001 to PAT_100).
- `Scenario`: Neutral scenario string configuration.
- `Observed_Outcome`: Telemetry Systolic Blood Pressure metric (mmHg). Range: [70.0, 250.0]. Missing code: `NaN`.

## 2. File: `observation_status.csv`
- `Is_Missing`: Binary indicator (1 if dropped stochastically/symptomatically via MAR/MNAR; 0 otherwise).
- `Is_Artifact`: Binary indicator (1 if identified as an extreme hardware sensor glitch; 0 otherwise).
- `Analysis_Inclusion_Flag`: Binary indicator (1 if cleared for pipeline estimation; 0 if suppressed).
