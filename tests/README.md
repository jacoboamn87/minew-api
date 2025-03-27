# Testing the Minew API Client

This directory contains tests for the Minew API client library.

## Setup

To install the package and test dependencies:

```bash
# Install the package in development mode with test dependencies
pip install -e ".[dev]"
```

## Running Tests

Run the tests using pytest:

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=minew_api

# Generate a coverage report
pytest --cov=minew_api --cov-report=html
```

## Test Structure

The tests are organized by the API's functional areas:

1. `test_client_core.py`: Tests for core client functionality (authentication, headers, request methods)
2. `test_store_endpoints.py`: Tests for store management endpoints
3. `test_gateway_endpoints.py`: Tests for gateway management endpoints
4. `test_label_endpoints.py`: Tests for label management endpoints
5. `test_template_data_endpoints.py`: Tests for template and data management endpoints

## Adding New Tests

When adding new functionality to the API client, add corresponding tests:

1. If adding a new method to an existing category, add tests to the relevant file
2. If adding a new category of functionality, create a new test file
3. Follow the existing pattern of mocking requests and responses

## Mock Fixtures

The `conftest.py` file contains shared fixtures for mocking the API:

- `mock_responses`: Provides a `responses` object for mocking HTTP requests
- `mock_client`: Provides a pre-authenticated client instance for testing