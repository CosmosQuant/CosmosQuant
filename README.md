# CosmosQuant

A comprehensive quantitative trading framework for algorithmic trading, backtesting, and financial research.

## Features

- **Trading Engine**: Robust order management and execution system
- **Broker Integrations**: Support for multiple trading platforms and brokers
- **Data Sources**: Unified interface for various market data providers
- **Strategy Framework**: Flexible framework for developing and testing trading strategies
- **Utilities**: Comprehensive set of tools for financial analysis and research

## Installation

```bash
pip install cosmosquant
```

Or install from source:

```bash
git clone https://github.com/CosmosQuant/CosmosQuant.git
cd CosmosQuant
pip install -e .
```

## Quick Start

```python
import cosmosquant as cq

# Initialize the trading engine
engine = cq.engine.TradingEngine()

# Connect to a data source
data_source = cq.datasources.YahooFinance()

# Create a simple strategy
strategy = cq.strategies.SimpleMovingAverage()

# Run backtest
results = engine.backtest(strategy, data_source)
```

## Project Structure

```
cosmosquant/
├── cosmosquant/           # Main package
│   ├── engine/           # Trading engine components
│   ├── brokers/          # Broker integrations
│   ├── datasources/      # Data feed management
│   ├── strategies/       # Trading strategies
│   └── utils/            # Utility functions
├── docs/                 # Documentation
├── examples/             # Example scripts and notebooks
├── datas/               # Sample data files
└── tests/               # Test suite
```

## Documentation

Full documentation is available at [https://github.com/CosmosQuant/CosmosQuant/docs](https://github.com/CosmosQuant/CosmosQuant/docs)

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Disclaimer

⚠️ **Important**: Please read our [DISCLAIMER](DISCLAIMER.md) before using this software. Trading involves substantial risk of loss and is not suitable for all investors.

## Support

- 📫 Issues: [GitHub Issues](https://github.com/CosmosQuant/CosmosQuant/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/CosmosQuant/CosmosQuant/discussions)
- 📧 Email: info@cosmosquant.com