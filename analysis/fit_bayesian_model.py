import pandas as pd
import numpy as np
from scipy.stats import norm

def fit_single_patient_bayesian_posterior(file_path):
    df = pd.read_csv(file_path).dropna()
    n_obs = len(df)
    
    mean_A = df[df['treatment_phase'] == 0]['observed_sbp'].mean()
    mean_B = df[df['treatment_phase'] == 1]['observed_sbp'].mean()
    observed_diff = mean_B - mean_A
    
    # Conjugate Normal Prior Specifications (Framework Supplementary Appendix 8)
    prior_mu = 0.0
    prior_var = 4.0
    sigma_sq = df['observed_sbp'].var()
    sample_var = sigma_sq / n_obs if n_obs > 0 else 1.0
    
    post_precision = (1.0 / prior_var) + (1.0 / sample_var)
    post_var = 1.0 / post_precision
    post_mu = post_var * ((prior_mu / prior_var) + (observed_diff / sample_var))
    
    prob_b_better = norm.cdf(post_mu / np.sqrt(post_var))
    
    return {
        'Model': 'Single-Patient Bayesian Posterior',
        'Posterior_Mean_Effect': round(post_mu, 3),
        'Posterior_Variance': round(post_var, 4),
        'Probability_B_Superior': round(prob_b_better, 4)
    }

if __name__ == '__main__':
    out = fit_single_patient_bayesian_posterior('synthetic_example/synthetic_nof1_data.csv')
    print(out)
