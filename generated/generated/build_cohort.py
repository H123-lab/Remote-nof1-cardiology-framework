import os
import yaml
import numpy as np
import pandas as pd

def build_complete_ground_truth_cohort():
    print("Generating complete, uncorrupted pre-clinical cohort database arrays...")
    with open('simulation/scenario_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
        
    np.random.seed(config['simulation_metadata']['locked_global_seed'])
    
    n_patients_per_cell = 33
    total_obs = config['global_constants']['total_planned_observations']
    obs_period = config['global_constants']['observations_per_period']
    mu = config['global_constants']['baseline_mu']
    delta = config['global_constants']['true_effect_delta']
    rho = config['global_constants']['autoregressive_rho']
    
    # Pre-build treatment sequence configuration array
    tx_seq = []
    for p in range(config['global_constants']['total_periods']):
        tx_seq.extend([0.0 if p % 2 == 0 else 1.0] * obs_period)
    tx_seq = np.array(tx_seq)
    
    cohort_rows = []
    pat_truth_rows = []
    obs_truth_rows = []
    
    global_patient_idx = 1
    
    for sc in config['scenarios']:
        sc_id = sc['id']
        sc_label = sc['label']
        m_rate = sc['missingness_rate']
        noise_sd = sc['measurement_noise_sd']
        c_coeff = sc['carryover_coefficient']
        art_prob = sc['artifact_probability']
        
        for p_idx in range(n_patients_per_cell):
            if global_patient_idx > 100: break
            pat_id = f"PAT_{global_patient_idx:03d}"
            
            # 1. Populate Participant Ground Truth Entry Registry
            pat_truth_rows.append({
                'Participant_ID': pat_id, 'Scenario_ID': sc_id, 'True_Baseline_Mu': mu,
                'True_Treatment_Effect_Delta': delta, 'True_Noise_SD': noise_sd, 'True_Carryover_Lambda': c_coeff
            })
            
            # Formulate temporal dependency using AR(1) limits
            innovations = np.random.normal(0, noise_sd, total_obs)
            errors = np.zeros(total_obs)
            errors[0] = innovations[0]
            for t in range(1, total_obs):
                errors[t] = rho * errors[t-1] + np.sqrt(1 - rho**2) * innovations[t]
                
            for t in range(total_obs):
                current_tx = tx_seq[t]
                prev_tx = tx_seq[t-1] if t > 0 else 0.0
                
                # Dynamic physiological target trace
                y_latent = mu + (delta * current_tx) + (c_coeff * delta * prev_tx) + errors[t] + (0.002 * (t + 1))
                
                # Check alert and artifact generation loops
                is_artifact = np.random.binomial(1, art_prob)
                artifact_value = np.random.normal(0, 25.0) if is_artifact == 1 else 0.0
                measurement_error = np.random.normal(0, noise_sd)
                
                y_observed_raw = y_latent + measurement_error + artifact_value
                
                # Conditional Missingness Engine Mapping
                is_missing = 0
                missing_reason = "Observed"
                if sc['missingness_mechanism'] == "MCAR":
                    is_missing = np.random.binomial(1, m_rate)
                    if is_missing: missing_reason = "Stochastic_Dropout"
                elif sc['missingness_mechanism'] == "MAR":
                    prob_mar = m_rate * 1.5 if current_tx == 1.0 else m_rate * 0.5
                    is_missing = np.random.binomial(1, min(prob_mar, 0.95))
                    if is_missing: missing_reason = "Phase_Transition_Dropout"
                elif sc['missingness_mechanism'] == "MNAR":
                    prob_mnar = m_rate * 2.0 if y_latent < 119.5 else m_rate * 0.5
                    is_missing = np.random.binomial(1, min(prob_mnar, 0.95))
                    if is_missing: missing_reason = "Symptom_Driven_Dropout"
                    
                y_final_observed = np.nan if is_missing == 1 else y_observed_raw
                
                # Real-time safety hazard evaluation flags
                is_safety_event = 1 if (y_latent < 95.0 or y_latent > 175.0) else 0
                
                # 2. Map full telemetry tracking logs
                cohort_rows.append({
                    'Participant_ID': pat_id, 'Scenario': sc_label, 'Time_Index': t + 1,
                    'Period': (t // obs_period) + 1, 'Assigned_Treatment': 'Strategy_B' if current_tx == 1.0 else 'Strategy_A',
                    'Observed_Outcome': y_final_observed, 'Missingness_Flag': is_missing
                })
                
                # 3. Map Observation Ground Truth Entries
                obs_truth_rows.append({
                    'Participant_ID': pat_id, 'Time_Index': t + 1, 'Latent_Outcome': y_latent,
                    'Measurement_Error': measurement_error, 'Artifact_Flag': is_artifact,
                    'Missingness_Reason': missing_reason, 'True_Safety_Event_Label': is_safety_event
                })
                
            global_patient_idx += 1
            
    # Save target database logs to disk
    os.makedirs('generated', exist_ok=True)
    pd.DataFrame(cohort_rows).to_csv('generated/virtual_cohort_full.csv', index=False)
    pd.DataFrame(pat_truth_rows).to_csv('generated/participant_ground_truth.csv', index=False)
    pd.DataFrame(obs_truth_rows).to_csv('generated/observation_ground_truth.csv', index=False)
    
    # 4. Generate Cohort Accounting Metrics
    df_c = pd.DataFrame(cohort_rows)
    accounting = pd.DataFrame([{
        'Planned_Observations': len(df_c),
        'Missing_Observations': int(df_c['Missingness_Flag'].sum()),
        'Recorded_Observations_Post_Missingness': int(len(df_c) - df_c['Missingness_Flag'].sum()),
        'Flagged_Quality_Control_Rows': int(pd.DataFrame(obs_truth_rows)['Artifact_Flag'].sum()),
        'Analyzed_Observations_Matrix_Rows': int(len(df_c) - df_c['Missingness_Flag'].sum())
    }])
    accounting.to_csv('generated/cohort_accounting.csv', index=False)
    print("[SUCCESS] Pre-clinical Full Database Cohort Generation Execution Sequence Locked.")

if __name__ == '__main__':
    build_complete_ground_truth_cohort()
