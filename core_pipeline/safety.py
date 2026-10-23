import pandas as pd
import numpy as np

class ClinicalSafetyOversightEngine:
    """
    Implements the real-time threshold monitoring and safety alert escalation pathways
    outlined in Table 5 and Supplementary Appendix Section 7 of the framework.
    """
    def __init__(self):
        # Cardiology-specific risk profile thresholds
        self.alert_thresholds = {
            'weight_gain_3d': 2.0,      # Delta kg over 3 days
            'weight_gain_7d': 3.0,      # Delta kg over 7 days
            'min_systolic_bp': 90.0,    # Hypotension barrier (mmHg)
            'max_systolic_bp': 180.0,   # Hypertensive urgency boundary (mmHg)
            'min_heart_rate': 50.0,     # Severe bradycardia (bpm)
            'max_heart_rate': 120.0     # Severe tachycardia (bpm)
        }

    def evaluate_biometric_safety(self, patient_history_df):
        """Scans continuous home telemetry logs for emergent cardiovascular decompensation signals."""
        df_sorted = patient_history_df.sort_values('Observation_Day').copy()
        alerts_triggered = []
        
        # Extract the most recent physiological parameters
        latest_idx = df_sorted.index[-1]
        latest_sbp = df_sorted.loc[latest_idx, 'Observed_Sensor_Value']
        
        # Verify if blood pressure violations are active
        if not np.isnan(latest_sbp):
            if latest_sbp < self.alert_thresholds['min_systolic_bp']:
                alerts_triggered.append({
                    'Trigger_Node': 'Systolic_BP',
                    'Current_Value': latest_sbp,
                    'Escalation_Level': 'Level_2_Urgent_Dose_Adjustment'
                })
            elif latest_sbp > self.alert_thresholds['max_systolic_bp']:
                alerts_triggered.append({
                    'Trigger_Node': 'Systolic_BP',
                    'Current_Value': latest_sbp,
                    'Escalation_Level': 'Level_3_Emergency_Referral'
                })
                
        return alerts_triggered
