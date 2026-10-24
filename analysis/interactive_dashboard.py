import os
import pandas as pd
import numpy as np
from scipy.stats import norm

def simulate_dashboard_metrics(patient_id="PAT_034", scenario_type="prolonged-carryover_scenario"):
    """
    Simulates the backend data engine for an interactive web dashboard interface,
    allowing reviewers to visualize individual tracking analytics instantly.
    """
    data_path = 'generated/virtual_hf_cohort_validation.csv'
    
    if not os.path.exists(data_path):
        print("[INFO] Target database missing. Re-running core generation script engine...")
        from generated.build_cohort import build_complete_ground_truth_cohort
        build_complete_ground_truth_cohort()
        
    df_full = pd.read_csv(data_path)
    
    # Filter dataset based on interactive user selections
    df_filtered = df_full[(df_full['Patient_ID'] == patient_id) | (df_full['Scenario'] == scenario_type)].copy()
    df_patient = df_full[df_full['Patient_ID'] == patient_id].copy()
    
    print("======================================================================")
    print("   REMOTE CARDIOLOGY N-OF-1 TRIAL INTERACTIVE TELEMETRY DASHBOARD    ")
    print("======================================================================")
    print(f"[Selected Active View] Patient: {patient_id} | Core Persona Profile: {scenario_type}")
    print("----------------------------------------------------------------------")
    print(f"[-] Total Planned Logging Data Inputs: {len(df_patient)} days")
    print(f"[-] Real-Time Missingness Disruption Rate: {df_patient['Observed_Sensor_Value'].isna().mean() * 100:.1f}%")
    
    # Execute on-the-fly analytical updates matching framework settings
    df_clean = df_patient.dropna(subset=['Observed_Sensor_Value'])
    mean_A = df_clean[df_clean['Assigned_Treatment'] == 'Strategy_A']['Observed_Sensor_Value'].mean()
    mean_B = df_clean[df_clean['Assigned_Treatment'] == 'Strategy_B']['Observed_Sensor_Value'].mean()
    delta_est = mean_B - mean_A if (not np.isnan(mean_A) and not np.isnan(mean_B)) else 0.0
    
    # Conjugate Normal-Normal updates math loop
    prior_mu, prior_var = 0.0, 4.0
    sigma_sq = df_clean['Observed_Sensor_Value'].var() if len(df_clean) > 1 else 1.0
    se_sq = sigma_sq / len(df_clean) if len(df_clean) > 0 else 1.0
    
    post_precision = (1.0 / prior_var) + (1.0 / se_sq)
    post_var = 1.0 / post_precision
    post_mu = post_var * ((prior_mu / prior_var) + (delta_est / se_sq))
    prob_b_better = norm.cdf(post_mu / np.sqrt(post_var))
    
    print("\n--- Real-Time Derived Pipeline Analytics Dashboard Summary ---")
    print(f" [*] Estimated Frequentist Treatment Effect: {delta_est:+.3f} mmHg")
    print(f" [*] Derived Bayesian Posterior Mean Effect: {post_mu:+.3f} mmHg")
    print(f" [*] Calculated Posterior Probability [Strategy B > A]: {prob_b_better * 100:.1f}%")
    
    # Render structured diagnostic ascii plot matrix tracking curves for review check
    print("\n--- Telemetry Trajectory Profiling (First 10 Days Sample Tracking Grid) ---")
    for idx, row in df_patient.head(10).iterrows():
        val_str = f"{row['Observed_Sensor_Value']:.1f} mmHg" if not np.isnan(row['Observed_Sensor_Value']) else "[MISSING NODE]"
        tx_indicator = "[Tx: B]" if row['Assigned_Treatment'] == 'Strategy_B' else "[Tx: A]"
        print(f"  Day {int(row['Observation_Day']):02d} | {tx_indicator} | Observed Value: {val_str}")
    print("======================================================================\n")

if __name__ == '__main__':
    simulate_dashboard_metrics()
