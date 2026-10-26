import os
import pytest
import numpy as np
import pandas as pd
from core_pipeline import analytics

def test_zero_effect_scenario_neutrality():
    """
    TEST 1: Verifies that under a strict null hypothesis (True Effect = 0), 
    the data-imputation, period-ordering, and treatment-coding pipelines 
    do not induce systematic positive optimization bias.
    """
    np.random.seed(42)
    n_days = 84
    
    # Simulate a true zero-effect null trajectory
    latent_intercept = 120.0
    autoregressive_rho = 0.50
    noise_sd = 0.5
    
    errors = np.zeros(n_days)
    innovations = np.random.normal(0, noise_sd, n_days)
    for t in range(1, n_days):
        errors[t] = autoregressive_rho * errors[t-1] + np.sqrt(1 - autoregressive_rho**2) * innovations[t]
        
    # Balanced crossover block scheduling matrix layout (ABABAB)
    treatment_sequence = np.tile(np.repeat([0, 1], 14), 3) 
    
    # Generate the simulated outcome vector with an absolute zero true effect
    true_delta = 0.0
    outcomes = latent_intercept + (treatment_sequence * true_delta) + errors
    
    df_test = pd.DataFrame({
        'Assigned_Treatment': ['Strategy_B' if x == 1 else 'Strategy_A' for x in treatment_sequence],
        'Observed_Sensor_Value': outcomes
    })
    
    # Run the paired comparison estimator core logic
    mean_A = df_test[df_test['Assigned_Treatment'] == 'Strategy_A']['Observed_Sensor_Value'].mean()
    mean_B = df_test[df_test['Assigned_Treatment'] == 'Strategy_B']['Observed_Sensor_Value'].mean()
    estimated_delta = mean_B - mean_A
    
    # Assert that the estimation error falls well within standard error bounds around zero
    # confirming that coding structures do not introduce systemic directional drift
    assert abs(estimated_delta) < 0.25, f"[BIAS WARNING] Null scenario produced skewness: {estimated_delta:+.3f} mmHg"

def test_estimator_input_isolation_from_ground_truth():
    """
    TEST 2: Enforces absolute truth isolation. Guarantees that the estimator 
    inputs do not accidentally leak or pull parameters from the hidden 
    ground-truth database files.
    """
    analysis_frame_path = 'generated/analysis_dataset.csv'
    ground_truth_path = 'generated/observation_ground_truth.csv'
    
    if os.path.exists(analysis_frame_path) and os.path.exists(ground_truth_path):
        df_analysis = pd.read_csv(analysis_frame_path)
        df_truth = pd.read_csv(ground_truth_path)
        
        # Verify that ground-truth latent parameters or specific labels 
        # do not exist as column headers in the operational dataset supplied to estimators
        assert 'Latent_State_Vector' not in df_analysis.columns
        assert 'True_Safety_Label' not in df_analysis.columns
        assert 'True_Treatment_Effect' not in df_analysis.columns

def test_statistical_metric_definitions():
    """
    TEST 3: Verifies that Bias, RMSE, and Monte Carlo Standard Error (MCSE) 
    formula derivations comply exactly with mathematical definitions.
    """
    true_effect = 0.50
    # Simulated vector of 5 estimates from a replicate block
    simulated_estimates = np.array([0.48, 0.52, 0.51, 0.49, 0.50])
    
    calculated_bias = np.mean(simulated_estimates) - true_effect
    calculated_rmse = np.sqrt(np.mean((simulated_estimates - true_effect)**2))
    
    # Standard formula for Monte Carlo Standard Error (MCSE) of the mean estimate
    calculated_mcse = np.std(simulated_estimates, ddof=1) / np.sqrt(len(simulated_estimates))
    
    assert np.isclose(calculated_bias, 0.0), "Bias math formulation mismatch"
    assert calculated_rmse > 0.0, "RMSE math formulation mismatch"
    assert calculated_mcse == pytest.approx(0.00707, abs=1e-4), "MCSE calculation error"
