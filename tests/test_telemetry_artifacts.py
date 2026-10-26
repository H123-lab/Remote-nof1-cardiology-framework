import os
import numpy as np
import pandas as pd
from core_pipeline import safety, analytics

def test_systolic_threshold_boundaries():
    """
    TEST 1: Verifies the exact boundary behavior of the Path 2 artifact gate:
    - Suppresses values below the low systolic threshold (< 70 mmHg)
    - Suppresses values above the high systolic threshold (> 250 mmHg)
    - Preserves values exactly at the boundaries
    - Preserves valid observations near the boundaries
    - Safely handles native missing rows (NaN)
    """
    # Define clinical boundary parameters
    low_thresh = 70.0
    high_thresh = 250.0
    
    test_stream = pd.Series([
        69.9,          # Below threshold (Should be masked)
        70.0,          # Exactly at low threshold (Should be preserved)
        70.1,          # Near low threshold (Should be preserved)
        120.0,         # Normal physiology baseline (Should be preserved)
        249.9,         # Near high threshold (Should be preserved)
        250.0,         # Exactly at high threshold (Should be preserved)
        250.1,         # Above threshold (Should be masked)
        np.nan         # Native missing row (Should remain NaN)
    ])
    
    # Run the Path 2 artifact detection filter module logic
    cleaned_stream = analytics.run_artifact_detection_filter(test_stream)
    
    # Verify exact boundary suppression behaviors
    assert np.isnan(cleaned_stream[0]), "Failed to suppress value below low threshold"
    assert cleaned_stream[1] == low_thresh, "Accidentally corrupted value exactly at low threshold"
    assert cleaned_stream[2] == 70.1, "Accidentally corrupted valid observation near low threshold"
    assert cleaned_stream[3] == 120.0, "Accidentally corrupted baseline observation"
    assert cleaned_stream[4] == 249.9, "Accidentally corrupted valid observation near high threshold"
    assert cleaned_stream[5] == high_thresh, "Accidentally corrupted value exactly at high threshold"
    assert np.isnan(cleaned_stream[6]), "Failed to suppress value above high threshold"
    assert np.isnan(cleaned_stream[7]), "Native missing value structure was broken"

def test_two_path_safety_isolation_and_preservation():
    """
    TEST 2: Mathematically proves that extreme artifact data entries are safely 
    preserved within the Path 1 safety surveillance alert engine to trigger clinical 
    triage, while simultaneously being excluded from Path 2 analytical processing.
    """
    # Create a raw telemetry database entry representing an extreme sensor spike
    # that matches a critical clinical hazard criteria (e.g., severe hypotension crisis)
    raw_hazard_data = pd.DataFrame([{
        'Patient_ID': 'PAT_001',
        'Observation_Day': 12,
        'Assigned_Treatment': 'Strategy_A',
        'Observed_Sensor_Value': 65.0  # Raw extreme value (Artifact & Critical Safety Event)
    }])
    
    # --- PATH 1: Real-Time Safety Surveillance Process ---
    # The raw data stream must be processed immediately without cleaning filters
    safety_alerts = safety.evaluate_biometric_safety(raw_hazard_data)
    
    # --- PATH 2: Analytical Quality Control Process ---
    # The data stream is passed independently through artifact suppression filters
    df_analytical = raw_hazard_data.copy()
    df_analytical['Observed_Sensor_Value'] = analytics.run_artifact_detection_filter(df_analytical['Observed_Sensor_Value'])
    
    # --- VERIFICATION CLAIMS ---
    # 1. Verify that Path 1 successfully triggered the critical hypotension alert
    assert len(safety_alerts) > 0, "Safety Engine failed to flag raw physiological hazard"
    assert safety_alerts[0]['Alert_Level'] == 'Level_3_Escalation', "Safety Engine failed to issue appropriate triage priority"
    
    # 2. Verify that Path 2 independently suppressed the artifact to protect estimator stability
    assert np.isnan(df_analytical.loc[0, 'Observed_Sensor_Value']), "Artifact gate failed to isolate row from analytical data"
    
    print("[SUCCESS] Mutual exclusivity of Two-Path Safety and Analytics pipelines confirmed.")
