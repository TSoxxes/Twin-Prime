# check_data.py
import pandas as pd

# The path to the data file you created
file_path = "data/processed/pvs_analysis_max_n_10000000.parquet"

print(f"Loading data from {file_path}...")
df = pd.read_parquet(file_path)

# Separate the data into two groups, just like the plot does
composite_data = df[df['is_p_plus_2_prime'] == False]
prime_data = df[df['is_p_plus_2_prime'] == True]

print("\n--- Analysis of the 'Composite' (Red) Data ---")
# This command counts how many times each value appears in the 'l1_norm_p2' column
composite_counts = composite_data['l1_norm_p2'].value_counts().sort_index()
print("Counts of each 'l1_norm_p2' value for composite numbers:")
print(composite_counts)

print("\n--- Analysis of the 'Prime' (Blue) Data ---")
prime_counts = prime_data['l1_norm_p2'].value_counts().sort_index()
print("Counts of each 'l1_norm_p2' value for prime numbers:")
print(prime_counts)

print("\nConclusion: The table above shows the exact numbers used to draw the bars.")