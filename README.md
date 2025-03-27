# Minew ESL Cloud API Client

A Python client library for interacting with the Minew Cloud Platform API for Electronic Shelf Label (ESL) systems.

## Overview

This library provides a clean, Pythonic interface to the Minew Cloud Platform API, allowing you to manage ESL devices, gateways, stores, labels, templates, and product data through a simple and intuitive client.

## Features

- Full coverage of Minew Cloud Platform API endpoints
- Resource-based architecture for better code organization
- Strong typing with comprehensive type annotations
- Authentication and token management
- Clean error handling with custom exceptions
- Comprehensive documentation with examples

## Installation

```bash
# Install from source
pip install -e .

# For development (includes test dependencies)
pip install -e ".[dev]"
```

## Quick Start

```python
from minew_api import MinewAPIClient

# Create client instance
client = MinewAPIClient(
    username="your_username",
    password="your_password"
)

# List stores
stores = client.store_get_information()

# List gateways for a store
gateways = client.gateway_list(
    store_id="your_store_id",
    page=1,
    size=10
)

# Add a new label
label_id = client.label_add(
    mac="AC233FC03CEC",
    store_id="your_store_id",
    demo_name="template_name"
)

# Bind a label to product data
result = client.label_binding(
    label_id="your_label_id",
    data_id="your_data_id",
    store_id="your_store_id"
)
```

## Architecture

The client is designed with a modular architecture:

- **Main Client**: `MinewAPIClient` provides a unified interface to all API resources.
- **Base Client**: `BaseClient` handles core functionality like authentication, request handling, and HTTP operations.
- **Resource Classes**: Specialized classes for each API resource area (stores, gateways, labels, templates, data).

This design improves maintainability, separating concerns and organizing code by functional area.

## API Resources

The client supports the following API resources:

### Store Management
- Create, update, and list stores
- Open/close stores
- Get store warnings and operation logs

### Gateway Management
- Add, update, and list gateways
- Delete gateways
- Restart and upgrade gateways

### Label Management
- Add, update, and list labels
- Bind/unbind labels to product data
- Refresh label displays
- Flash LED for visual identification
- Upgrade label firmware
- Find labels by MAC address

### Template Management
- List, add, update, and delete templates
- Preview templates (bound and unbound)

### Product Data Management
- Add, update, and list product data
- Delete product data
- List bound product data

## Error Handling

The client uses custom exceptions for clear error reporting:

```python
from minew_api import MinewAPIClient, APIError

try:
    client = MinewAPIClient("username", "password")
    client.label_refresh(label_ids=["label_id"], store_id="store_id")
except APIError as e:
    print(f"API error occurred: {e}")
```

## Development

### Running Tests

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=minew_api

# Run linting
flake8 minew_api/

# Run type checking
mypy minew_api/
```

## License

This project is licensed under the terms of the MIT license.

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues for bugs, feature requests, or documentation improvements.