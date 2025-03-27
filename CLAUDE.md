# CLAUDE.md - Development Guidelines for Minew API

## Build & Test Commands
```bash
# Install package in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"

# Run linting
flake8 minew_api/

# Run type checking
mypy minew_api/

# Run tests
pytest tests/

# Run tests with coverage
pytest --cov=minew_api tests/

# Generate HTML coverage report
pytest --cov=minew_api --cov-report=html tests/
```

## Architecture Overview

The client library follows a modular, resource-based architecture:

### Core Components
- `MinewAPIClient`: Main client class that provides a unified interface for all API operations
- `BaseClient`: Core functionality for authentication, HTTP requests, and response handling
- Resource classes: Specialized classes for each API resource area

### Directory Structure
```
minew_api/
├── __init__.py         # Package exports and version
├── base.py             # Base client functionality
├── client.py           # Main client class
├── exceptions.py       # Custom exception hierarchy
├── resources/          # Resource-specific implementation
│   ├── __init__.py
│   ├── data.py         # Product data endpoints
│   ├── gateway.py      # Gateway management endpoints
│   ├── label.py        # Label management endpoints
│   ├── store.py        # Store management endpoints
│   └── template.py     # Template management endpoints
```

## Code Style Guidelines

### Formatting & Imports
- 4-space indentation, ~100 character line limit
- Imports: standard library → third-party → local modules → relative imports
- Use relative imports with dot notation (from .exceptions import APIError)
- Group imports by type with a blank line between groups

### Types & Naming
- Use comprehensive type hints in all function signatures (Python 3.6+ annotations)
- Classes: PascalCase (MinewAPIClient, BaseResource)
- Functions/methods/variables: snake_case (authenticate, base_url)
- Constants: UPPER_SNAKE_CASE (BASE_URL, LOGIN_ENDPOINT)
- Private attributes/methods: underscore prefix (_base_client, _handle_response)

### Error Handling & Documentation
- Use custom exception hierarchy from exceptions.py
- Document with Google-style docstrings (Args/Returns sections)
- Validate API responses and raise appropriate exceptions
- Follow RESTful client pattern for API methods
- Include type information in docstrings that matches annotations

## Testing 

### Test Organization
Tests are organized to mirror the library structure:
- `test_client_core.py`: Tests for basic client functionality
- `test_store_endpoints.py`: Tests for store management endpoints
- `test_gateway_endpoints.py`: Tests for gateway management endpoints
- `test_label_endpoints.py`: Tests for label management endpoints
- `test_template_data_endpoints.py`: Tests for template and data endpoints

### Mocking
- Use the `responses` library to mock HTTP requests
- Create reusable fixtures in `conftest.py`
- Mock authentication separately from endpoint tests
- Test error handling and edge cases

### Best Practices
- Keep tests isolated and independent
- Test the public API, not implementation details
- Use parametrized tests for similar test cases
- Ensure high test coverage for critical code paths