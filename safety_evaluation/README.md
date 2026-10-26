# Subdirectory Module: Path 1 Clinical Safety Surveillance

This directory houses the hazard definitions, expected alert rules, and automated testing evaluation tracking networks used to validate the isolated system triage pathways.

## 🛠️ Automated Evaluation Command Track
To execute the safety audit suite locally and recalculate the continuous false alert burden metrics directly from the raw database rows, run the following script:

```bash
python safety_evaluation/run_safety_evaluation.py
```

All data properties, true simulated tracking parameters, and delayed system response latencies match the results section text of the primary manuscript file.
