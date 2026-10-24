import os
import numpy as np
import pandas as pd
from scipy.stats import norm

def execute_monte_carlo_benchmarking():
    print("Initializing 1,000 Replicate Repeated Monte Carlo Simulation Benchmarks...")
    np.random.seed(4491001)
    
    n_replicates = 1000
    true_delta = 0.50
    obs_total = 84
    
    scenarios = [
        {'name': 'low-noise_low-missingness', 'noise': 0.25, 'missing': 0.05, 'carryover': 0.00},
        {'name': 'high-noise_high-missingness', 'noise': 0.75, 'missing': 0.30, 'carryover': 0.10},
        {'name': 'prolonged-carryover', 'noise': 0.35, 'missing': 0.10, 'carryover': 0.40}
    ]
    
    tx_arr = np.array((*14 + *14) * 3)
    results = []
    
    for sc in scenarios:
        print(f" Running Simulation Grid Cell Array Track: {sc['name']}")
        bias_accum, rmse_accum, cover_accum, acc_accum = [], [], [], []
        
        for rep in range(n_replicates):
            # Generate local error vector
            innovations = np.random.normal(0, sc['noise'], obs_total)
            errors = innovations.copy()
            for t in range(1, obs_total):
                errors[t] = 0.50 * errors[t-1] + np.sqrt(1 - 0.50**2) * innovations[t]
                
            y_latent = 120.0 + (true_delta * tx_arr) + errors
            mask = np.random.binomial(1, sc['missing'], obs_total).astype(bool)
            
            y_obs = y_latent.copy()
            y_obs[mask] = np.nan
            
            df = pd.DataFrame({'tx': tx_arr, 'y': y_obs}).dropna()
            
            if len(df) > 5:
                mA = df[df['tx'] == 0.0]['y'].mean()
                mB = df[df['tx'] == 1.0]['y'].mean()
                est = mB - mA if (not np.isnan(mA) and not np.isnan(mB)) else 0.0
                
                bias = est - true_delta
                rmse = bias ** 2
                
                # Mock uncertainty bounds for verification testing
                se = sc['noise'] / np.sqrt(len(df))
                ci_low, ci_high = est - 1.96 * se, est + 1.96 * se
                coverage = 1.0 if (ci_low <= true_delta <= ci_high) else 0.0
                
                # Correct selection defined as catching positive benefit direction
                correct_selection = 1.0 if est > 0.0 else 0.0
                
                bias_accum.append(bias)
                rmse_accum.append(rmse)
                cover_accum.append(coverage)
                acc_accum.append(correct_selection)
                
        # Compute Monte Carlo standard error margins
        mc_se_bias = np.std(bias_accum) / np.sqrt(n_replicates)
        mc_se_coverage = np.sqrt((np.mean(cover_accum) * (1 - np.mean(cover_accum))) / n_replicates)
        
        results.append({
            'Scenario': sc['name'],
            'Mean_Bias': np.mean(bias_accum),
            'MC_SE_Bias': mc_se_bias,
            'RMSE': np.sqrt(np.mean(rmse_accum)),
            'Interval_Coverage': np.mean(cover_accum),
            'MC_SE_Coverage': mc_se_coverage,
            'Decision_Accuracy': np.mean(acc_accum)
        })
        
    os.makedirs('benchmarks', exist_ok=True)
    summary_df = pd.DataFrame(results)
    summary_df.to_csv('benchmarks/performance_summary.csv', index=False)
    print("\n--- Benchmark Repeated Testing Complete ---")
    print(summary_df.to_string(index=False))

if __name__ == '__main__':
    execute_monte_carlo_benchmarking()
