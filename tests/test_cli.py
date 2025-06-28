# tests/test_cli.py
import pytest
from click.testing import CliRunner
import pandas as pd
import numpy as np
from pathlib import Path

from pvs.cli import cli # Your Click application
from pvs.geometry import sieve_of_eratosthenes # For checking generate output

# Fixture to create a CliRunner instance
@pytest.fixture
def runner():
    return CliRunner()

# Fixture to create a temporary test directory for outputs
@pytest.fixture
def temp_output_dir(tmp_path):
    output_dir = tmp_path / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def test_cli_entrypoint(runner):
    """Test that the CLI runs without error when no subcommand is given."""
    result = runner.invoke(cli)
    assert result.exit_code == 0
    # With invoke_without_command=True, the output is expected to be empty,
    # so we no longer check for the help text.

# --- Tests for 'generate' subcommand ---
def test_generate_basic(runner, temp_output_dir):
    max_n = 30
    output_file = temp_output_dir / f"prime_vector_{max_n}.parquet"

    result = runner.invoke(cli, ['generate', '--max-n', str(max_n), '--output-dir', str(temp_output_dir)])

    assert result.exit_code == 0, f"CLI Error: {result.output}"
    assert f"Generating prime vector up to n = {max_n}" in result.output
    assert f"Successfully saved prime vector to {output_file}" in result.output
    assert output_file.exists()

    # Verify Parquet file content
    df = pd.read_parquet(output_file)
    assert 'prime_indices' in df.columns

    sieve = sieve_of_eratosthenes(max_n)
    expected_primes = np.where(sieve)[0]
    assert np.array_equal(df['prime_indices'].values, expected_primes)

def test_generate_custom_filename(runner, temp_output_dir):
    max_n = 20
    custom_name = "my_primes.parquet"
    output_file = temp_output_dir / custom_name

    result = runner.invoke(cli, [
        'generate',
        '--max-n', str(max_n),
        '--output-dir', str(temp_output_dir),
        '--filename', custom_name
    ])
    assert result.exit_code == 0
    assert output_file.exists()

def test_generate_negative_max_n(runner, temp_output_dir):
    result = runner.invoke(cli, ['generate', '--max-n', '-5', '--output-dir', str(temp_output_dir)])
    assert result.exit_code == 0 
    assert "Error: --max-n must be a non-negative integer." in result.output
    assert not list(temp_output_dir.glob('*.parquet'))

def test_generate_zero_max_n(runner, temp_output_dir):
    max_n = 0
    output_file = temp_output_dir / f"prime_vector_{max_n}.parquet"
    result = runner.invoke(cli, ['generate', '--max-n', str(max_n), '--output-dir', str(temp_output_dir)])
    assert result.exit_code == 0
    assert output_file.exists()
    df = pd.read_parquet(output_file)
    assert 'prime_indices' in df.columns
    assert len(df['prime_indices']) == 0

def test_generate_default_output_dir(runner):
    """Test that 'generate' uses ./data/processed if no output-dir is given."""
    max_n = 10
    with runner.isolated_filesystem():
        expected_default_dir = Path.cwd() / "data" / "processed"
        expected_file = expected_default_dir / f"prime_vector_{max_n}.parquet"
        result = runner.invoke(cli, ['generate', '--max-n', str(max_n)])
        assert result.exit_code == 0, f"CLI Error: {result.output}"
        assert expected_default_dir.exists()
        assert expected_file.exists()