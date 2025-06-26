# This file is used by pytest to share fixtures, hooks, and plugins among multiple test files.
# For example, you can define a fixture here that sets up a database connection
# or creates some common test data.

import pytest

# Example of a shared fixture:
# @pytest.fixture(scope="session")
# def db_connection():
#     """A fixture to set up and tear down a database connection for the test session."""
#     # Setup code: connect to the database
#     conn = ...
#     yield conn
#     # Teardown code: close the connection
#     conn.close()


# Example of how to make a fixture available to all tests:
# @pytest.fixture
# def common_data():
#     """Provides some common data to tests."""
#     return {"key": "value", "numbers": [1, 2, 3]}

# You can also define hooks, e.g., to modify pytest's behavior or reporting.
# def pytest_report_header(config):
#     """Add a header to the pytest report."""
#     return "PVS Library - Custom Test Report Header"

# For this project, specific fixtures are defined in individual test files (e.g., test_cli.py)
# or are provided by pytest itself (e.g., tmp_path).
# This conftest.py can be expanded as the test suite grows and shared fixtures become necessary.

# Pytest will automatically discover and use fixtures and hooks defined in this file.
# No explicit imports are needed in the test files for fixtures defined here.

# If using pytest custom markers, they can be registered in pyproject.toml or pytest.ini
# Example (if not in pyproject.toml):
# def pytest_configure(config):
# config.addinivalue_line(
# "markers", "slow: marks tests as slow to run"
# )
# config.addinivalue_line(
# "markers", "integration: marks integration tests"
# )

# Currently, the primary custom marker 'slow' is used in test_geometry.py and
# is expected to be registered in pyproject.toml under [tool.pytest.ini_options].
# If not, pytest will issue a PytestUnknownMarkWarning.
# Let's ensure it's defined in pyproject.toml:
# [tool.pytest.ini_options]
# markers = [
#     "slow: marks tests as slow to run",
# ]
# (This is already handled in the pyproject.toml created earlier)
