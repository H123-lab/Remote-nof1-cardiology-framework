#!/usr/bin/env bash
set -e

echo "======================================================================"
echo "Starting Master Open-Science Replication Sequence Framework..."
echo "======================================================================"

# 1. Execute cohort building data traces
python generated/build_cohort.py

# 2. Run repeated statistical benchmarking modules
python benchmarks/run_repeated_simulations.py

# 3. Evaluate critical care safety validation checks
python safety_evaluation/run_safety_evaluation.py

# 4. Compile sensitivity analysis grid cells
python sensitivity/run_sensitivity.py

echo "======================================================================"
echo "[SUCCESS] Total Manuscript Pipeline Assets Regenerated Cleanly."
echo "======================================================================"
