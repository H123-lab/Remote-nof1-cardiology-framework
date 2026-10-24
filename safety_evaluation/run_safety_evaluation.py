import os
import pandas as pd
import numpy as np

def run_isolated_safety_pipeline_checks():
    print("Evaluating Safety Surveillance Logic Performance Against Test Matrix...")
    
    # Load standardized safety test case rows
    test_cases = [
        {'id': 'CASE_01', 'val': 84.0, 'symptom': 'Severe Dizziness', 'true_hazard': 1},
        {'id': 'CASE_02', 'val': 245.0, 'symptom': 'Asymptomatic', 'true_hazard': 0},
        {'id': 'CASE_03', 'val': np.nan, 'symptom': 'Worsening Dyspnea', 'true_hazard': 1}
    ]
    
    alert_logs = []
    
    for tc in test_cases:
        triggered_alert = 0
        # Path 1: Pure Clinical Threshold Safety Screening
        if not np.isnan(tc['val']) and (tc['val'] < 90.0 or tc['val'] > 180.0):
            triggered_alert = 1
        elif np.isnan(tc['val']) and tc['symptom'] == 'Worsening Dyspnea':
            triggered_alert = 1
            
        alert_logs.append({
            'Case_ID': tc['id'],
            'True_Hazard_Label': tc['true_hazard'],
            'System_Alert_Triggered': triggered_alert,
            'Detection_Status': 'SUCCESS' if triggered_alert == tc['true_hazard'] else 'MISSED_EVENT'
        })
        
    os.makedirs('safety_evaluation', exist_ok=True)
    performance_df = pd.DataFrame(alert_logs)
    performance_df.to_csv('safety_evaluation/safety_performance.csv', index=False)
    print("\n--- Safety System Performance Logs Table ---\n", performance_df.to_string(index=False))

if __name__ == '__main__':
    run_isolated_safety_pipeline_checks()
