import os
import numpy as np
import pandas as pd
from core_pipeline.analytics import RemoteNof1AnalyticsPipeline
from core_pipeline.safety import ClinicalSafetyOversightEngine

def run_comprehensive_validation():
    print("======================================================================")
    print("Executing 100-Patient Virtual HFrEF Digital Twin Framework Core Run...")
    print("======================================================================")
    
    os.makedirs('generated', exist_ok=True)
    np.random.seed(2026)
    
    analytics = RemoteNof1AnalyticsPipeline()
    safety = ClinicalSafetyOversightEngine()
    
    n_patients_per_phenotype = 33
    total_target_patients = 100
    
    phenotypes = {
        'Phenotype_A_Stable': {
            'missing_rate': 0.05, 'noise_sd': 0.25, 'carryover': 0.00, 
            'desc': 'Compliant / Stable Reference Persona'
        },
        'Phenotype_B_Frail': {
            'missing_rate': 0.30, 'noise_sd': 0.75, 'carryover': 0.10, 
            'desc': 'Frail / High Wearable Movement Artifacts & Adherence Gaps'
        },
        'Phenotype_C_CKD': {
            'missing_rate': 0.10, 'noise_sd': 0.35, 'carryover': 0.40, 
            'desc': 'Altered Pharmacokinetics / Renal Clearance Equilibration Delay'
        }
    }
    
    periods, obs_per_period = 6, 14
    total_obs = periods * obs_per_period
    rho = 0.50
    
    tx_schedule = []
    for p in range(periods):
        tx_schedule.extend([0.0 if p % 2 == 0 else 1.0] * obs_per_period)
    tx_schedule = np.array(tx_schedule)
    
    database_records = []
    patient_performance_metrics = []
    patient_counter = 1
    
    for pheno_key, params in phenotypes.items():
        m_rate, noise_sd, c_coeff = params['missing_rate'], params['noise_sd'], params['carryover']
        
        for p_idx in range(n_patients_per_phenotype):
            if patient_counter > total_target_patients:
                break
                
            pat_id = f"PAT_{patient_counter:03d}"
            
            # Formulate temporal dependence via AR(1) processes
            innovations = np.random.normal(0, noise_sd, total_obs)
            errors = np.zeros(total_obs)
            errors = innovations
            for t in range(1, total_obs):
                errors[t] = rho * errors[t-1] + np.sqrt(1 - rho**2) * innovations[t]
                
            y_true = np.zeros(total_obs)
            for t in range(total_obs):
                current_tx = tx_schedule[t]
                prev_tx = tx_schedule[t-1] if t > 0 else 0.0
                y_true[t] = analytics.baseline_mu + (analytics.true_effect * current_tx) + (c_coeff * analytics.true_effect * prev_tx) + errors[t]
                
            missing_mask = np.random.binomial(1, m_rate, total_obs).astype(bool)
            y_observed = y_true.copy()
            y_observed[missing_mask] = np.nan
            
            # Process continuous temporal arrays through the system
            df_patient_log = pd.DataFrame()
            for t in range(total_obs):
                row_data = {
                    'Patient_ID': pat_id, 'Phenotype': pheno_key, 'Clinical_Description': params['desc'],
                    'Observation_Day': t + 1, 'Trial_Period': (t // obs_per_period) + 1,
                    'Assigned_Treatment': 'Strategy_B' if tx_schedule[t] == 1.0 else 'Strategy_A',
                    'True_Latent_Signal': y_true[t], 'Observed_Sensor_Value': y_observed[t]
                }
                database_records.append(row_data)
                
                # Check real-time clinical safety boundaries concurrently
                current_history = pd.DataFrame(database_records)[pd.DataFrame(database_records)['Patient_ID'] == pat_id]
                _ = safety.evaluate_biometric_safety(current_history)
                
            # Filter artifact anomalies and impute gaps via core pipeline models
            df_pat_processing = pd.DataFrame({'tx_num': tx_schedule, 'Observed_Sensor_Value': y_observed})
            df_pat_processing['Assigned_Treatment'] = df_pat_processing['tx_num'].map({0.0: 'Strategy_A', 1.0: 'Strategy_B'})
            
            df_pat_processing['Observed_Sensor_Value'] = analytics.run_artifact_detection_filter(df_pat_processing['Observed_Sensor_Value'])
            df_clean = analytics.run_adaptive_imputation(df_pat_processing, 'Observed_Sensor_Value')
            
            # Calculate final pipeline effect estimates
            freq_results = analytics.compute_paired_comparison(df_clean)
            est_diff = freq_results['Estimated_Difference_B_A']
            n_obs_total = freq_results['Sample_Size_A'] + freq_results['Sample_Size_B']
            
            bayes_results = analytics.compute_bayesian_single_patient_posterior(est_diff, noise_sd, n_obs_total)
            
            patient_performance_metrics.append({
                'Patient_ID': pat_id, 'Phenotype': pheno_key,
                'Estimated_Effect': est_diff,
                'Bayesian_Posterior_Mean': bayes_results['Posterior_Mean'],
                'Calculated_Bias': bayes_results['Posterior_Mean'] - analytics.true_effect,
                'Calculated_RMSE': np.abs(bayes_results['Posterior_Mean'] - analytics.true_effect),
                'Directional_Accuracy': 1.0 if bayes_results['Posterior_Probability_B_Better_Than_A'] >= 0.85 else 0.0
            })
            patient_counter += 1

    # Save outputs to disk
    pd.DataFrame(database_records).to_csv('generated/virtual_hf_cohort_validation.csv', index=False)
    pd.DataFrame(patient_performance_metrics).to_csv('generated/table_9_cohort_summary.csv', index=False)
    print("\n[SUCCESS] 100-Patient Longitudinal Engine Simulation Execution Phase Locked.")

if __name__ == '__main__':
    run_comprehensive_validation()
