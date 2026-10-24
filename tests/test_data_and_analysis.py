import os
import pandas as pd
import numpy as np

def test_data_integrity_bounds():
    data_file = 'synthetic_example/synthetic_nof1_data.csv'
    assert os.path.exists(data_file), "Data array node missing. Run analysis/simulate_data.py first."
    
    df = pd.read_csv(data_file)
    assert len(df) == 84, "Total rows do not match the pre-specified 84 observation slots."
    assert set(df['treatment_phase'].unique()).issubset({0, 1}), "Treatment configuration out of bounds."
    print("[PASS] Open-Science Reference Dataset Verification Checks Successful.")

if __name__ == '__main__':
    test_data_integrity_bounds()
