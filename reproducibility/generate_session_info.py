import os
import sys
import platform
import subprocess
import pandas as pd
import numpy as np
import scipy
import yaml

def capture_system_ecosystem_matrix():
    print("Executing complete system environment audit track...")
    out_file = "environment/session_info.txt"
    os.makedirs("environment", exist_ok=True)
    
    # Query R version metadata proxy
    try:
        r_ver = subprocess.check_output(["R", "--version"], text=True).split('\n')[0]
    except Exception:
        r_ver = "R Environment Node Not Found in Current Path Shell"
        
    # Query Julia version metadata proxy
    try:
        julia_ver = subprocess.check_output(["julia", "--version"], text=True).split('\n')[0]
    except Exception:
        julia_ver = "Julia Environment Node Not Found in Current Path Shell"

    info_log = f"""======================================================================
OPEN-SCIENCE INFRASTRUCTURE: PLATFORM RUNTIME SESSION RECORDS
======================================================================
Execution Timestamp Timestamp Vector : 2026-10-26 (Locked Baseline Run)
Operating System Architecture Engine: {platform.system()} {platform.release()} ({platform.machine()})
Python Core Base Version Allocation : {sys.version.split()[0]}

Locked Python Package Versions Matrix:
[-] numpy   : {np.__version__}
[-] pandas  : {pd.__version__}
[-] scipy   : {scipy.__version__}
[-] pyyaml  : {yaml.__version__}

Cross-Language Compilation Engine Registry:
[-] R Env    : {r_ver}
[-] Julia Env: {julia_ver}
======================================================================
"""
    with open(out_file, "w") as f:
        f.write(info_log)
    print(f"[SUCCESS] System ecosystem signature saved directly to: {out_file}")

if __name__ == '__main__':
    capture_system_ecosystem_matrix()
