import pandas as pd
import numpy as np

def generate_formatted_table_9():
    print("Compiling aggregated validation matrices for Manuscript Table 9...")
    
    # Check if simulation engine data is present
    try:
        raw_summary = pd.read_csv('generated/table_9_cohort_summary.csv')
    except FileNotFoundError:
        print("[ERROR] Please execute 'python virtual_cohort_engine.py' first to build raw data arrays.")
        return

    # Map raw rows to professional manuscript layout definitions
    manuscript_table = pd.DataFrame()
    manuscript_table['Clinical Cohort Phenotype'] = [
        'Phenotype A: Stable / Compliant', 
        'Phenotype B: Frail / Wearable Dropout & Artifacts', 
        'Phenotype C: CKD / PK Equilibration Latency'
    ]
    
    manuscript_table['Mean Absolute Bias'] = raw_summary['Calculated_Bias'].abs().round(3)
    manuscript_table['Root Mean Squared Error (RMSE)'] = raw_summary['Calculated_RMSE'].round(3)
    manuscript_table['Clinical Decision Regimen Accuracy (%)'] = (raw_summary['Directional_Accuracy'] * 100).round(1)

    # Save to disk
    manuscript_table.to_csv('generated/manuscript_table_9_final.csv', index=False)
    print("\n======================================================================")
    print("FINAL MANUSCRIPT TABLE 9 STRUCTURAL LAYOUT FOR JAHA INSERTION:")
    print("======================================================================")
    print(manuscript_table.to_string(index=False))
    print("======================================================================\n")

if __name__ == '__main__':
    generate_formatted_table_9()
