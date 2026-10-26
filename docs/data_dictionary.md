# Tabular Ingestion Schema & Field Data Dictionary

This data dictionary defines every tracking column, status flag, and unit constraint generated across the 100-patient heart failure database.

## 1. File: `generated/virtual_cohort_full.csv` & `generated/analysis_dataset.csv`

| Variable Name | Storage Type | Allowed Range / Codes | Unit / Metric | Field Description & Logical Target |
| :--- | :--- | :--- | :--- | :--- |
| `Participant_ID` | String | `PAT_001` to `PAT_100` | N/A | Unique patient digital twin tracking code. |
| `Scenario_Group` | String | `Scenario_1`, `Scenario_2`, `Scenario_3` | N/A | Evaluation block matrix grouping indicator. |
| `Observation_Day` | Integer | 1 to 84 | Days | Longitudinal trial chronological timeline axis tracker. |
| `CrossOver_Period` | Integer | 1 to 6 | Index | Discrete 14-day tracking blocks within the trial layout. |
| `Assigned_Treatment`| String | `Strategy_A`, `Strategy_B` | N/A | Randomised sequence assignment arm identifier. |
| `Observed_Outcome` | Float | 70.0 to 250.0 (or `NaN`) | mmHg | Telemetric Systolic Blood Pressure proxy outcome. |

## 2. File: `generated/observation_status.csv`

| Status Flag | Storage Type | Valid Values | Operational Meaning & Boundary Filter |
| :--- | :--- | :--- | :--- |
| `Is_Missing` | Boolean | `0` = Active, `1` = Dropped | Indicates a missed transmission due to patient non-adherence. |
| `Is_Artifact` | Boolean | `0` = Valid, `1` = Suppressed | Indicates an extreme sensor glitch outside mmHg limits. |
| `Analysis_Inclusion`| Boolean | `0` = Excluded, `1` = Ingested | Confirms the row cleared all Path 2 data filters. |
