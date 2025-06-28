# analyze_results.py (Corrected)
import argparse
from pathlib import Path
import pandas as pd
from pvs.visualize import plot_invariant_distributions

def main():
    parser = argparse.ArgumentParser(description="Analyze and visualize PVS results.")
    parser.add_argument(
        "input_file", type=str,
        help="Path to the Parquet file containing PVS analysis data."
    )
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file not found at {input_path}")
        return
        
    print(f"Loading data from {input_path}...")
    df = pd.read_parquet(input_path)
    
    # This list now correctly separates all the column names
    invariants_to_plot = [
        'l1_norm_p2',
        'signed_l1_norm_p2',
        'l0_norm_p2',
        'delta_l1_norm',
        'sieve_weight_p2',
        'hybrid_weight'
    ]
    
    # Use the max 'p' from the dataframe for a dynamic filename
    max_p_val = df['p'].max()
    plot_output_path = input_path.parent / f"final_analysis_plot_{max_p_val}.png"
    
    print("Generating visualizations...")
    plot_invariant_distributions(df, invariants_to_plot, str(plot_output_path))

if __name__ == "__main__":
    main()