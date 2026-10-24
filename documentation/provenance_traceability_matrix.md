# Manuscript-to-Output Provenance and Traceability Matrix

This open-science reference matrix maps text items inside the paper directly to the code modules, parameter configurations, and generated file structures within this repository.

| Manuscript Target Asset | Ingest Source File Path | Generating Software Script | Exported Target Asset File |
| :--- | :--- | :--- | :--- |
| **Main Text Table 8** | `simulation/scenario_config.yaml` | `benchmarks/run_repeated_simulations.py` | `benchmarks/performance_summary.csv` |
| **Main Text Table 9** | `simulation/scenario_config.yaml` | `generated/build_cohort.py` | `generated/cohort_accounting.csv` |
| **Main Text Table 10** | Replicate decision logs | `benchmarks/run_repeated_simulations.py` | `benchmarks/performance_summary.csv` |
| **Supplemental Table S8** | Labelled hazard test rows | `safety_evaluation/run_safety_evaluation.py` | `safety_evaluation/safety_performance.csv` |
| **Supplemental Table S9** | Multi-cell configuration grid | `sensitivity/run_sensitivity.py` | `sensitivity/sensitivity_results.csv` |
