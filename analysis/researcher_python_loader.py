import os
import pandas as pd
import numpy as np

def extract_and_profile_patient(patient_id="PAT_034"):
    """
    Utility script for future researchers to easily ingest the virtual cohort
    database and extract single-patient telematic data metrics.
    """
    data_path = 'generated/virtual_hf_cohort_validation.csv'
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"[ERROR] Run the data generation script first to create: {data_path}")
        
    # Ingest the full 8,316-row structural cohort database
    df_cohort = pd.read_csv(data_path)
    
    # Isolate a single patient's longitudinal cross-over array records
    df_patient = df_cohort[df_cohort['Patient_ID'] == patient_id].copy()
    
    print(f"======================================================================")
    print(f"Extracting Longitudinal Telematic Logs for Target Profile: {patient_id}")
    print(f"======================================================================")
    print(f"Phenotype Cluster: {df_patient['Phenotype'].iloc[0]}")
    print(f"Total Logged Tracking Observation Points: {len(df_patient)} days")
    print(f"Observed Missingness Rate: {df_patient['Observed_Sensor_Value'].isna().mean() * 100:.1f}%")
    
    # Display snippet of the research dataset table
    print("\n--- Telemetry Log Snippet (First 5 Rows) ---")
    print(df_patient[['Observation_Day', 'Assigned_Treatment', 'Observed_Sensor_Value']].head().to_string(index=False))
    print("======================================================================\n")
    
    return df_patient

if __name__ == '__main__':
    # Default execution verifies data extraction path integrity
    try:
        extract_and_profile_patient()
    except FileNotFoundError:
        # If running in an empty repo path loop, execute the dataset build first automatically
        print("Dataset missing locally. Executing generation engine module first...")
        import sys
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from generated.build_cohort import build_complete_ground_truth_cohort
        build_complete_ground_truth_cohort()
        extract_and_profile_patient()
