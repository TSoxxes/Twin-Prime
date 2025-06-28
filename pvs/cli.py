# pvs/cli.py
import click
import numpy as np
import pandas as pd
import os
from pathlib import Path

from pvs.geometry import build_prime_vector
# The gpy_weight import is now removed as the 'analyse' command is gone.

# Helper function to ensure data directory exists
def ensure_data_dir(ctx, param, value):
    if value:
        path = Path(value)
        path.mkdir(parents=True, exist_ok=True)
        return path
    # If no path provided, use default ./data/processed
    default_path = Path.cwd() / "data" / "processed"
    default_path.mkdir(parents=True, exist_ok=True)
    return default_path

@click.group(invoke_without_command=True)
def cli():
    """
    Prime Vector Space (PVS) command-line tool.
    Used for generating prime vectors and performing analysis.
    """
    pass

@cli.command()
@click.option('--max-n', type=int, required=True, help="Maximum number (n) to generate prime vectors up to.")
@click.option('--output-dir', type=click.Path(),
              callback=ensure_data_dir, default=None, # Uses cwd/data/processed by default
              help="Directory to save the output Parquet file. Defaults to ./data/processed/")
@click.option('--filename', type=str, default=None, help="Custom filename for the Parquet file. Defaults to prime_vector_<max_n>.parquet.")
def generate(max_n: int, output_dir: Path, filename: str):
    """
    Generates prime vectors up to --max-n and saves them to a Parquet file.
    """
    if max_n < 0:
        click.echo(f"Error: --max-n must be a non-negative integer. Got {max_n}", err=True)
        return

    click.echo(f"Generating prime vector up to n = {max_n}...")

    prime_vector_sparse = build_prime_vector(max_n)
    
    prime_indices = prime_vector_sparse.indices
    df = pd.DataFrame({'prime_indices': prime_indices})

    if filename is None:
        output_filename = f"prime_vector_{max_n}.parquet"
    else:
        if not filename.endswith(".parquet"):
            filename += ".parquet"
        output_filename = filename

    output_path = output_dir / output_filename

    try:
        df.to_parquet(output_path)
        click.echo(f"Successfully saved prime vector to {output_path}")
    except Exception as e:
        click.echo(f"Error saving Parquet file: {e}", err=True)

# The 'analyse' command that used gpy_weight has been removed for now.

if __name__ == '__main__':
    cli()