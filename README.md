# Open-Source Platform Framework: Remote N-of-1 Cardiology Analytics Architecture

This repository hosts the production-ready source code, data dictionaries, and pre-clinical verification data supporting the manuscript: **"Remote N-of-1 Trials for Individualized Cardiovascular Treatment: An Integrated Operational Framework and Synthetic Simulation Stress-Test for Heart Failure Care and Remote Monitoring."**

## Platform Component Architecture
The workspace contains the operational code modules required to execute remote within-patient crossover trials:
1. `/core_pipeline/analytics.py`: Active signal processors executing adaptive missing data imputation and conjugate Bayesian uncertainty calculations.
2. `/core_pipeline/safety.py`: Automatic tracking modules monitoring clinical danger flags (severe telemetry drops or sudden weight spikes).
3. `/data_schemas/patient_log.json`: Production data schema structure mapping trial logs directly to FHIR standard Observation definitions.
4. `virtual_cohort_engine.py`: Pre-clinical digital twin engine generating a heterogeneous 100-patient test population.
5. `process_table_9.py`: Data aggregator script that builds the clinical verification matrix for the paper text.

## Reproducibility & Replication Workflow
Reviewers can build the code tracking environment and run calculations locally via:

```bash
# Initialize isolated python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the exact frozen dependency packages
pip install -r requirements.txt

# Run the 100-patient simulation loop
python virtual_cohort_engine.py

# Aggregate outputs to reconstruct Table 9
python process_table_9.py
```

## Simulated Cohort Definitions
The pipeline tests data metrics against three realistic clinical tracking settings:
- **Phenotype A (Stable)**: 5% data dropouts, low baseline device variance.
- **Phenotype B (Frail)**: 30% random missing data rows modeling patient logging fatigue; high internal noise variance mapping wearable motion artifacts.
- **Phenotype C (CKD)**: 40% active carryover equilibration coefficient modeling prolonged biological clearance lag due to underlying chronic kidney disease.
