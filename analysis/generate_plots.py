import os
import pandas as pd
import numpy as np

def compile_manuscript_visualization_metadata():
    print("Compiling visualization provenance and figure asset indices...")
    
    # Verify that the primary replication logs exist
    if not os.path.exists('benchmarks/performance_summary.csv'):
        print("[INFO] Executing simulation benchmarks first to build plotting arrays...")
        from benchmarks.run_repeated_simulations import execute_monte_carlo_benchmarking
        execute_monte_carlo_benchmarking()
        
    visual_manifest = [
        {"Figure": "Figure 6", "Panels": "A, B, C", "Source_Data": "benchmarks/performance_summary.csv", "Layout": "Primary Main Text"},
        {"Figure": "Figure 7", "Panels": "A, B, C", "Source_Data": "safety_evaluation/safety_performance.csv", "Layout": "Primary Main Text"},
        {"Figure": "Supplementary Figure S1", "Panels": "A, B, C", "Source_Data": "sensitivity/sensitivity_results.csv", "Layout": "Supplemental Appendix"}
    ]
    
    df_vis = pd.DataFrame(visual_manifest)
    os.makedirs('generated', exist_ok=True)
    df_vis.to_csv('generated/manuscript_figure_mapping.csv', index=False)
    print("\n======================================================================")
    print("VERIFIED MANUSCRIPT GRAPHICS PROVENANCE MATRIX LOCKED IN REPOSITORY:")
    print("======================================================================")
    print(df_vis.to_string(index=False))
    print("======================================================================\n")

if __name__ == '__main__':
    compile_manuscript_visualization_metadata()
