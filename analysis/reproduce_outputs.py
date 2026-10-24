import os
from simulate_data import generate_reference_data
from fit_time_series_model import fit_autoregressive_time_series
from fit_bayesian_model import fit_single_patient_bayesian_posterior

def run_reproducibility_pipeline():
    print("======================================================================")
    print("Executing Master Open-Science Reproducibility Data Pipeline Track...")
    print("======================================================================")
    
    # 1. Execute initial data generation step
    generate_reference_data()
    data_path = 'synthetic_example/synthetic_nof1_data.csv'
    
    # 2. Extract calculations across alternative algorithms
    ts_results = fit_autoregressive_time_series(data_path)
    bayes_results = fit_single_patient_bayesian_posterior(data_path)
    
    # 3. Print verified outcomes mapping to Main Table 8
    print("\n======================================================================")
    print("VERIFIED COMPUTATIONAL ESTIMATION SUMMARY OUTLINES FOR VERIFICATION:")
    print("======================================================================")
    print(f"[-] {ts_results['Model']} -> Estimated Delta: {ts_results['Estimated_Effect']} (Rho: {ts_results['Estimated_Autocorrelation_Rho']})")
    print(f"[-] {bayes_results['Model']} -> Posterior Mean: {bayes_results['Posterior_Mean_Effect']} (Pr[B>A]: {bayes_results['Probability_B_Superior']})")
    print("======================================================================\n")

if __name__ == '__main__':
    run_reproducibility_pipeline()
