# ======================================================================
# Standalone R Utility Script for External Single-Patient Framework Analysis
# ======================================================================
# Objective: Allows external teams to import our generated database 
# and execute within-patient treatment effect estimation calculations natively.

cat("========================================================\n")
cat("Initializing Native R Core Single-Patient Evaluation Tool\n")
cat("========================================================\n")

# 1. Ingest Data Matrix
data_file <- "generated/virtual_hf_cohort_validation.csv"

if (!file.exists(data_file)) {
  stop("[ERROR] Complete dataset missing. Run python engine simulation first.")
}

full_cohort <- read.csv(data_file)

# 2. Extract Data Matrix Array for an Individual Patient Profile (Example: PAT_001)
target_patient <- "PAT_001"
pat_data <- full_cohort[full_cohort$Patient_ID == target_patient, ]
pat_data_clean <- na.omit(pat_data) # Path 2: Remove missing rows for analytical pipeline

# 3. Method 1: Execute Classical Paired Comparison Mean Difference Check
mean_A <- mean(pat_data_clean$Observed_Sensor_Value[pat_data_clean$Assigned_Treatment == "Strategy_A"])
mean_B <- mean(pat_data_clean$Observed_Sensor_Value[pat_data_clean$Assigned_Treatment == "Strategy_B"])
estimated_delta <- mean_B - mean_A

# 4. Method 2: Execute Conjugate Bayesian Posterior Signal Update
prior_mu <- 0.0
prior_var <- 4.0
sample_var_sigma <- var(pat_data_clean$Observed_Sensor_Value)
n_total_obs <- nrow(pat_data_clean)

# Bayesian update algebra equations mapping to manuscript Section 2.3
sample_variance_se <- sample_var_sigma / n_total_obs
posterior_precision <- (1.0 / prior_var) + (1.0 / sample_variance_se)
posterior_variance <- 1.0 / posterior_precision
posterior_mean <- posterior_variance * ((prior_mu / prior_var) + (estimated_delta / sample_variance_se))

# Compute localized probability that Strategy B achieves clinical superiority
probability_b_superior <- pnorm(posterior_mean / sqrt(posterior_variance))

# 5. Output Results Summary Vectors to Console Console
cat("\n--- Analytical Metric Summaries for Patient Profile:", target_patient, "---\n")
cat("[-] Estimated Frequentist Mean Delta (B - A): ", round(estimated_delta, 3), " mmHg\n")
cat("[-] Calculated Single-Patient Bayesian Posterior Mean: ", round(posterior_mean, 3), " mmHg\n")
cat("[-] Calculated Probability of Strategy B Efficacy Superiority: ", round(probability_b_superior * 100, 1), "%\n")
cat("========================================================\n")
