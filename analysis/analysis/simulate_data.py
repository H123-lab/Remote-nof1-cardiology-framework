import numpy as np
import pandas as pd
import yaml

def generate_reference_data():
    with open('synthetic_example/simulation_parameters.yaml', 'r') as f:
        params = yaml.safe_load(f)['statistical_constants']
        
    np.random.seed(2026)
    obs = params['total_observations']
    rho = params['autoregressive_rho']
    noise_sd = params['measurement_noise_sd_low']
    effect = params['true_treatment_effect']
    mu = params['baseline_mean_mu']
    
    # Generate crossover array schedule
    tx = np.array(([0]*14 + [1]*14) * 3)
    
    # Compile AR(1) temporal dependency bounds
    innovations = np.random.normal(0, noise_sd, obs)
    errors = np.zeros(obs)
    errors[0] = innovations[0]
    for t in range(1, obs):
        errors[t] = rho * errors[t-1] + np.sqrt(1 - rho**2) * innovations[t]
        
    y_true = mu + (effect * tx) + errors
    mask = np.random.binomial(1, 0.05, obs).astype(bool)
    y_obs = y_true.copy()
    y_obs[mask] = np.nan
    
    df = pd.DataFrame({
        'time_index': np.arange(1, obs + 1),
        'treatment_phase': tx,
        'true_latent_sbp': y_true,
        'observed_sbp': y_obs,
        'autocorrelation_error': errors
    })
    df.to_csv('synthetic_example/synthetic_nof1_data.csv', index=False)
    print("[SUCCESS] Reference N-of-1 Data Array Generated.")

if __name__ == '__main__':
    generate_reference_data()
