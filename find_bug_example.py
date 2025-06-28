# find_bug_example.py
import pandas as pd

# Make sure this path points to your 10 million results file
file_path = "data/processed/pvs_analysis_max_n_10000000.parquet"

print(f"Loading data from {file_path}...")
try:
    df = pd.read_parquet(file_path)
except FileNotFoundError:
    print(f"Error: Data file not found at {file_path}")
    print("Please make sure the filename is correct and the file exists.")
    exit()

# Find the rows where the bug occurs
# Condition a) p+2 is identified as composite
# Condition b) The L1 norm of p+2 is 1 (which means it's actually prime)
buggy_rows = df[
    (df['is_p_plus_2_prime'] == False) &
    (df['l1_norm_p2'] == 1)
]

print(f"\nFound {len(buggy_rows)} numbers that were incorrectly classified as composite.")

if not buggy_rows.empty:
    # Get the very first example
    first_example = buggy_rows.iloc[0]

    print("\nHere is the first example of the bug:")
    print("---------------------------------------")
    prime_p = int(first_example['p'])
    misclassified_p_plus_2 = prime_p + 2

    print(f"The prime number 'p' is: {prime_p}")
    print(f"The number 'p+2' is: {misclassified_p_plus_2}")
    print("\nAccording to the code's output:")
    print(f"  - 'is_p_plus_2_prime' was marked as: {first_example['is_p_plus_2_prime']}")
    print(f"  - The 'l1_norm_p2' was calculated as: {int(first_example['l1_norm_p2'])}")

    print("\nThis gives us the clue we need to debug the sieve function.")

else:
    print("\nNo buggy rows were found. The bug might have been fixed already.")