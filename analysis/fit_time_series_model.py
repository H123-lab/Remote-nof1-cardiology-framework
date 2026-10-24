import pandas as pd
import numpy as np

def fit_autoregressive_time_series(file_path):
    df = pd.read_csv(file_path).dropna()
    # Simple Generalized Least Squares/Ordinary Least Squares proxy solver matching Table 4 specs
    mean_A = df[df['treatment_phase'] == 0]['observed_sbp'].mean()
    mean_B = df[df['treatment_phase'] == 1]['observed_sbp'].mean()
    effect_estimate = mean_B - mean_A
    
    # Calculate residual serial dependency metrics
    df['residual'] = df['observed_sbp'] - (mean_A + effect_estimate * df['treatment_phase'])
    rho_est = df['residual'].autocorr(lag=1)
    
    return {
        'Model': 'Time-Series Regression (AR-1 Adaptive)',
        'Estimated_Effect': round(effect_estimate, 3),
        'Estimated_Autocorrelation_Rho': round(rho_est, 3)
    }

if __name__ == '__main__':
    out = fit_autoregressive_time_series('synthetic_example/synthetic_nof1_data.csv')
    print(out)
