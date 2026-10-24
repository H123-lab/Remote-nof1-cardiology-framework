import pytest
import numpy as np
import pandas as pd
from core_pipeline.analytics import RemoteNof1AnalyticsPipeline
from core_pipeline.safety import ClinicalSafetyOversightEngine

def test_artifact_detection_filter():
    """Verifies that the telemetry data cleaning boundaries catch extreme clinical values."""
    pipeline = RemoteNof1AnalyticsPipeline()
    # Test array containing realistic SBP, severe hypotension, and extreme hyper-crisis
    raw_array = np.array([120.0, 65.0, 140.0, 260.0])
    cleaned_array = pipeline.run_artifact_detection_filter(raw_array)
    
    assert np.isnan(cleaned_array[1]), "Failed to suppress severe hypotension anomaly (<70 mmHg)"
    assert np.isnan(cleaned_array[3]), "Failed to suppress extreme hypertensive crisis anomaly (>250 mmHg)"
    assert cleaned_array[0] == 120.0, "Erroneously filtered a valid baseline systolic blood pressure node"

def test_bayesian_posterior_math():
    """Bayesian update calculation validation engine."""
    pipeline = RemoteNof1AnalyticsPipeline()
    # Mock data vectors: Estimated effect = 1.0, tracking standard deviation = 0.5, observations = 25
    bayes_results = pipeline.compute_bayesian_single_patient_posterior(est_diff=1.0, noise_sd=0.5, n_obs=25)
    
    assert bayes_results['Posterior_Mean'] > 0.0, "Bayesian update calculation calculated an incorrect direction"
    assert 0.0 <= bayes_results['Posterior_Probability_B_Better_Than_A'] <= 1.0, "Probability logic out of bounds"
    assert len(bayes_results['95_Percent_Credible_Interval']) == 2, "Credible boundary configuration incomplete"

def test_safety_oversight_alerts():
    """Verifies Path 1 safety engine isolates clinical hazards from Path 2 quality data cleaning."""
    safety = ClinicalSafetyOversightEngine()
    
    # Test Case 01: Severe Hypotension Hazard
    mock_history_low = pd.DataFrame([{
        'Observation_Day': 1,
        'Observed_Sensor_Value': 84.0  # Path 1 must process this raw, un-imputed clinical value
    }])
    alerts = safety.evaluate_biometric_safety(mock_history_low)
    
    assert len(alerts) == 1, "Safety engine failed to flag a live clinical hazard condition"
    assert alerts[0]['Escalation_Level'] == 'Level_2_Urgent_Dose_Adjustment', "Incorrect triage escalation path mapped"

if __name__ == "__main__":
    print("Running localized clinical platform verification tests...")
    test_artifact_detection_filter()
    test_bayesian_posterior_math()
    test_safety_oversight_alerts()
    print("[PASS] All algorithmic processing and safety evaluation units verified successfully.")


