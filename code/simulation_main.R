# ======================================================================
# Multi-Language Analytical Wrapper Pipeline: Remote N-of-1 Cardiology
# ======================================================================
# This script bridges R-centric analysis environments with the primary
# Python data engineering architecture deployed in this repository.

cat("Initializing Multi-Language Replication Environment Interface...\n")

# 1. Enforce package installation checks for system routing stability
if (!requireNamespace("reticulate", quietly = TRUE)) {
  install.packages("reticulate", repos = "https://r-project.org")
}
library(reticulate)

# 2. Bind reticulate to the locked virtual environment path bounds
virtualenv_path <- file.path(getwd(), "venv")

if (dir.exists(virtualenv_path)) {
  cat("[-] Synchronizing with isolated local virtualenv space...\n")
  use_virtualenv(virtualenv_path, required = TRUE)
} else {
  cat("[WARNING] Virtual environment path array missing. Falling back to system python definitions.\n")
}

# 3. Import and execute core pipeline orchestrators via wrapper bindings
tryCatch({
  cat("[-] Executing master clinical data generation track...\n")
  source_python("generated/build_cohort.py")
  
  cat("[-] Running repeated Monte Carlo benchmarking arrays...\n")
  source_python("benchmarks/run_repeated_simulations.py")
  
  cat("[SUCCESS] R-to-Python open science compilation executed cleanly.\n")
}, error = function(e) {
  cat("[EXECUTION FAULT] Pipeline mapping exception caught:\n")
  print(e)
})
