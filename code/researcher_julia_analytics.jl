# ======================================================================
# Standalone Julia Utility Script for External Single-Patient Framework Analysis
# ======================================================================
# Objective: Ingests the 100-patient dataset and executes single-patient
# frequentist and conjugate Bayesian updates natively in Julia.

using DataFrames
using CSV
using Statistics
using Distributions

println("========================================================")
println("Initializing Native Julia Core Single-Patient Evaluation Tool")
println("========================================================")

# 1. Ingest Data Matrix
data_file = "generated/virtual_hf_cohort_validation.csv"

if !isfile(data_file)
    error("[ERROR] Complete dataset missing. Run python engine simulation first.")
end

full_cohort = CSV.read(data_file, DataFrame)

# 2. Extract Data Matrix Array for an Individual Patient Profile (Example: PAT_001)
target_patient = "PAT_001"
pat_data = full_cohort[full_cohort.Patient_ID .== target_patient, :]

# Path 2: Remove missing rows for analytical pipeline inclusion
pat_data_clean = dropmissing(pat_data, :Observed_Sensor_Value)

# 3. Method 1: Execute Classical Paired Comparison Mean Difference Check
val_col = :Observed_Sensor_Value
tx_col = :Assigned_Treatment

mean_A = mean(pat_data_clean[pat_data_clean[!, tx_col] .== "Strategy_A", val_col])
mean_B = mean(pat_data_clean[pat_data_clean[!, tx_col] .== "Strategy_B", val_col])
estimated_delta = mean_B - mean_A

# 4. Method 2: Execute Conjugate Bayesian Posterior Signal Update
prior_mu = 0.0
prior_var = 4.0
sample_var_sigma = var(pat_data_clean[!, val_col])
n_total_obs = nrow(pat_data_clean)

# Bayesian update algebra equations mapping to manuscript Section 2.3
sample_variance_se = sample_var_sigma / n_total_obs
posterior_precision = (1.0 / prior_var) + (1.0 / sample_variance_se)
posterior_variance = 1.0 / posterior_precision
posterior_mean = posterior_variance * ((prior_mu / prior_var) + (estimated_delta / sample_variance_se))

# Compute localized probability that Strategy B achieves clinical superiority
prob_b_superior = cdf(Normal(posterior_mean, sqrt(posterior_variance)), posterior_mean)

# 5. Output Results Summary Vectors to Console
println("\n--- Analytical Metric Summaries for Patient Profile: ", target_patient, " ---")
println("[-] Estimated Frequentist Mean Delta (B - A): ", round(estimated_delta, digits=3), " mmHg")
println("[-] Calculated Single-Patient Bayesian Posterior Mean: ", round(posterior_mean, digits=3), " mmHg")
println("[-] Calculated Probability of Strategy B Efficacy Superiority: ", round(prob_b_superior * 100, digits=1), "%")
println("========================================================\n")
