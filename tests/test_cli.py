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
    # tmp_path is a pytest fixture providing a Path object to a temporary directory
    output_dir = tmp_path / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def test_cli_entrypoint(runner):
    """Test that the CLI runs and shows help without subcommands."""
    result = runner.invoke(cli)
    assert result.exit_code == 0
    assert "Usage: cli [OPTIONS] COMMAND [ARGS]..." in result.output
    assert "Prime Vector Space (PVS) command-line tool." in result.output

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

    # Test auto .parquet extension
    custom_name_no_ext = "another_set_of_primes"
    output_file_no_ext = temp_output_dir / (custom_name_no_ext + ".parquet")
    result = runner.invoke(cli, [
        'generate',
        '--max-n', str(max_n),
        '--output-dir', str(temp_output_dir),
        '--filename', custom_name_no_ext
    ])
    assert result.exit_code == 0
    assert output_file_no_ext.exists()


def test_generate_negative_max_n(runner, temp_output_dir):
    result = runner.invoke(cli, ['generate', '--max-n', '-5', '--output-dir', str(temp_output_dir)])
    assert result.exit_code == 0 # The command itself doesn't exit with error, but prints error to stderr
    assert "Error: --max-n must be a non-negative integer." in result.output
    # Check that no file was created
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


# --- Tests for 'analyse' subcommand ---
@pytest.fixture
def sample_parquet_file(temp_output_dir):
    max_n = 50
    # Generate a sample file using the 'generate' command
    runner = CliRunner()
    parquet_path = temp_output_dir / f"sample_primes_{max_n}.parquet"
    res = runner.invoke(cli, ['generate', '--max-n', str(max_n), '--output-dir', str(temp_output_dir), '--filename', parquet_path.name])
    assert res.exit_code == 0
    assert parquet_path.exists()
    return parquet_path

def test_analyse_basic(runner, sample_parquet_file):
    result = runner.invoke(cli, ['analyse', '--input-file', str(sample_parquet_file)])

    assert result.exit_code == 0, f"CLI Error: {result.output}"
    assert f"Analysing prime vectors from: {sample_parquet_file}" in result.output
    assert "Parameters: k=2, u-factor=0.5, Plotting: Disabled" in result.output
    assert "Computed GPY weights" in result.output
    assert "Placeholder θ angle statistic" in result.output

def test_analyse_custom_params(runner, sample_parquet_file):
    k_val = 3
    u_factor_val = 0.8
    result = runner.invoke(cli, [
        'analyse',
        '--input-file', str(sample_parquet_file),
        '--k', str(k_val),
        '--u-factor', str(u_factor_val)
    ])
    assert result.exit_code == 0
    assert f"Parameters: k={k_val}, u-factor={u_factor_val}, Plotting: Disabled" in result.output
    # Check if u_param in output reflects u_factor, e.g. by checking part of the GPY weights output line
    # This requires knowing max_n from sample_parquet_file (50)
    # u_param = 0.8 * log(50) approx 0.8 * 3.912 = 3.1296
    assert f"u={np.log(50)*u_factor_val:.2f})" in result.output # Check if u calculation is reflected

def test_analyse_missing_input_file(runner):
    result = runner.invoke(cli, ['analyse', '--input-file', 'non_existent_file.parquet'])
    assert result.exit_code == 2 # Click's error code for missing file path
    assert "Error: Invalid value for '--input-file': Path 'non_existent_file.parquet' does not exist." in result.output

def test_analyse_malformed_parquet(runner, temp_output_dir):
    malformed_file = temp_output_dir / "malformed.parquet"
    # Create a dummy file that isn't a valid Parquet file
    # Or a parquet file with wrong schema
    df = pd.DataFrame({'wrong_column': [1,2,3]})
    df.to_parquet(malformed_file)

    result = runner.invoke(cli, ['analyse', '--input-file', str(malformed_file)])
    assert result.exit_code == 0 # Command completes but prints error.
    assert "Error: 'prime_indices' column not found" in result.output


@pytest.mark.skipif(pytest.importorskip("matplotlib") is None, reason="matplotlib not installed")
def test_analyse_with_plot(runner, sample_parquet_file, temp_output_dir):
    # The CLI saves plots to the input file's directory
    plot_output_path = Path(sample_parquet_file.stem + "_analysis_plot.png")

    # Ensure it's cleaned up if it exists from a previous run in the same temp dir session
    if plot_output_path.exists():
        plot_output_path.unlink()

    result = runner.invoke(cli, [
        'analyse',
        '--input-file', str(sample_parquet_file),
        '--plot'
    ])

    assert result.exit_code == 0, f"CLI Error: {result.output}"
    assert "Plotting is enabled." in result.output
    assert f"Plot saved to {plot_output_path.name}" in result.output # Check relative name

    # Check if the plot file was created in the directory of the input file
    # The sample_parquet_file is in temp_output_dir.
    full_plot_path = sample_parquet_file.parent / plot_output_path.name
    assert full_plot_path.exists(), f"Plot file {full_plot_path} was not created."
    if full_plot_path.exists(): # cleanup
        full_plot_path.unlink()


def test_analyse_plot_matplotlib_not_installed(runner, sample_parquet_file, mocker):
    # Mock import matplotlib to simulate it not being installed
    mocker.patch.dict('sys.modules', {'matplotlib.pyplot': None})

    result = runner.invoke(cli, [
        'analyse',
        '--input-file', str(sample_parquet_file),
        '--plot'
    ])

    assert result.exit_code == 0 # Command completes but prints error.
    assert "Matplotlib is not installed." in result.output
    assert "poetry install --extras viz" in result.output

def test_generate_default_output_dir(runner):
    """Test that 'generate' uses ./data/processed if no output-dir is given."""
    max_n = 10
    # Create a temporary working directory for the runner
    with runner.isolated_filesystem():
        # Current working directory for this test is now a temporary one
        expected_default_dir = Path.cwd() / "data" / "processed"
        expected_file = expected_default_dir / f"prime_vector_{max_n}.parquet"

        result = runner.invoke(cli, ['generate', '--max-n', str(max_n)])

        assert result.exit_code == 0, f"CLI Error: {result.output}"
        assert expected_default_dir.exists()
        assert expected_file.exists()
        assert str(expected_file) in result.output # Check if the output message contains the correct path

def test_analyse_empty_prime_file(runner, temp_output_dir):
    # Create a parquet file with empty prime_indices
    empty_df = pd.DataFrame({'prime_indices': []})
    empty_file_path = temp_output_dir / "empty_primes.parquet"
    empty_df.to_parquet(empty_file_path)

    result = runner.invoke(cli, ['analyse', '--input-file', str(empty_file_path)])
    assert result.exit_code == 0
    assert "Warning: No primes found in the input file." in result.output
    # u_param should default to 1.0 when max_n_from_file is 0 or log(0) would occur
    assert "u=1.00)" in result.output # GPY weights output with u=1.00
    assert "Placeholder θ angle statistic: 0.0000" in result.output

def test_analyse_primes_up_to_1(runner, temp_output_dir):
    # Create a parquet file with primes up to 1 (i.e., no primes)
    # build_prime_vector(1) results in [0,0] bool array, so no prime indices
    runner.invoke(cli, ['generate', '--max-n', '1', '--output-dir', str(temp_output_dir), '--filename', 'primes_up_to_1.parquet'])
    file_path = temp_output_dir / "primes_up_to_1.parquet"
    assert file_path.exists()

    df = pd.read_parquet(file_path)
    assert len(df['prime_indices']) == 0

    result = runner.invoke(cli, ['analyse', '--input-file', str(file_path)])
    assert result.exit_code == 0
    assert "Warning: No primes found in the input file." in result.output
    assert "u=1.00)" in result.output # u_param should default to 1.0
    assert "Placeholder θ angle statistic: 0.0000" in result.output
