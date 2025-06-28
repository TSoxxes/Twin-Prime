# pvs/visualize.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List

def plot_invariant_distributions(
    df: pd.DataFrame,
    invariants: List[str],
    output_path: str
):
    """
    Plots the distributions of geometric invariants, comparing twin prime
    candidates to non-candidates.
    """
    n_invariants = len(invariants)
    fig, axes = plt.subplots(
        nrows=n_invariants, ncols=1, figsize=(10, 6 * n_invariants),
        sharex=False, sharey=False
    )
    if n_invariants == 1:
        axes = [axes] # Make it iterable if there's only one plot

    fig.suptitle('Distribution of Geometric Invariants (p vs. p+2)', fontsize=16)

    # Separate data for plotting
    twin_prime_data = df[df['is_p_plus_2_prime'] == True]
    composite_data = df[df['is_p_plus_2_prime'] == False]

    for i, invariant_name in enumerate(invariants):
        ax = axes[i]

        sns.histplot(
            twin_prime_data[invariant_name], ax=ax, color='blue',
            label='p+2 is Prime', stat='density', kde=True, element='step'
        )
        sns.histplot(
            composite_data[invariant_name], ax=ax, color='red',
            label='p+2 is Composite', stat='density', kde=True, element='step'
        )

        ax.set_title(f'Distribution of {invariant_name}')
        ax.set_xlabel(invariant_name)
        ax.set_ylabel('Density')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.savefig(output_path, dpi=300)
    print(f"Plot saved to {output_path}")
    plt.close()