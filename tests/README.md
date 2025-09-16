# Tests

This directory contains the test suite for CosmosQuant.

## Running Tests

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run tests with coverage
pytest --cov=cosmosquant

# Run specific test module
pytest tests/test_engine.py
```

## Test Structure

- `test_engine/` - Tests for the trading engine
- `test_brokers/` - Tests for broker integrations
- `test_datasources/` - Tests for data sources
- `test_strategies/` - Tests for trading strategies
- `test_utils/` - Tests for utility functions