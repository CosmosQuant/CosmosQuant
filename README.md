# CosmosQuant

A minimal trading engine scaffold for Python 3.11 that supports both backtesting and live trading with Interactive Brokers.

## Features

- 🎯 **Single Symbol MVP**: Focus on one symbol trading for simplicity
- 🔄 **Unified Codebase**: Same code for backtesting and live trading
- 📊 **Simple Event Loop**: Easy onTick/onBar strategy implementation
- 💾 **Parquet Support**: Efficient historical data reading
- 🎭 **Abstract Base Classes**: Clean broker and data source interfaces
- 🤖 **SimBroker**: Full-featured simulation broker for backtesting
- 💼 **IB Integration**: Interactive Brokers live trading skeleton
- ✅ **Testing**: Comprehensive test suite included

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/CosmosQuant/CosmosQuant.git
cd CosmosQuant

# Install the package
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Basic Usage

```python
from cosmosquant.cosmosquant.engine.trading_engine import TradingEngine
from cosmosquant.cosmosquant.brokers.sim_broker import SimBroker
from cosmosquant.cosmosquant.datasources.parquet_source import ParquetDataSource
from cosmosquant.cosmosquant.strategies.base import BaseStrategy

# Create a simple strategy
class MyStrategy(BaseStrategy):
    def on_bar(self, bar):
        if self.get_position_size() == 0:
            self.buy(100)  # Buy 100 shares
    
    def on_tick(self, tick):
        pass  # Not used in this example

# Set up components
broker = SimBroker(initial_cash=10000)
data_source = ParquetDataSource(symbol="AAPL", data_path="data/AAPL.parquet")
strategy = MyStrategy(broker, data_source)

# Run backtest
engine = TradingEngine(strategy)
results = engine.run_backtest()
print(f"Total return: ${results['total_return']:.2f}")
```

### Running Examples

```bash
# Run the example backtest
cd cosmosquant
python examples/run_backtest.py
```

## Architecture

```
cosmosquant/
├── cosmosquant/
│   ├── engine/          # Trading engine core
│   ├── brokers/         # Broker implementations
│   │   ├── base.py      # Abstract broker interface
│   │   ├── sim_broker.py    # Simulation broker
│   │   └── ib_broker.py     # Interactive Brokers
│   ├── datasources/     # Data source implementations
│   │   ├── base.py      # Abstract data source interface
│   │   └── parquet_source.py   # Parquet file reader
│   ├── strategies/      # Strategy base classes
│   │   └── base.py      # Abstract strategy interface
│   └── utils/           # Utility functions
├── examples/            # Example strategies and usage
├── tests/              # Test suite
├── docs/               # Documentation
└── datas/              # Sample data files
```

## Key Components

### Trading Engine
The `TradingEngine` coordinates strategy execution and handles the main event loop for both backtesting and live trading.

### Brokers
- **BaseBroker**: Abstract interface for all brokers
- **SimBroker**: Full-featured simulation broker with order management
- **IBBroker**: Interactive Brokers integration (requires ib-insync)

### Data Sources
- **BaseDataSource**: Abstract interface for data providers
- **ParquetDataSource**: Historical data from Parquet files

### Strategies
- **BaseStrategy**: Abstract base class for trading strategies
- Provides convenient methods for placing orders and accessing account info

## Data Format

The system expects Parquet files with the following columns:
- `timestamp`: DateTime index
- `open`, `high`, `low`, `close`: OHLC prices
- `volume`: Trading volume

For tick data:
- `timestamp`: DateTime index
- `bid`, `ask`, `last`: Price levels
- `volume`: Volume

## Live Trading

To use Interactive Brokers for live trading:

1. Install IB TWS or Gateway
2. Enable API access in TWS
3. Install ib-insync: `pip install ib-insync`
4. Use IBBroker instead of SimBroker

```python
from cosmosquant.cosmosquant.brokers.ib_broker import IBBroker

# Connect to IB (default: localhost:7497)
broker = IBBroker(host="127.0.0.1", port=7497, client_id=1)
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
black cosmosquant/

# Sort imports
isort cosmosquant/

# Type checking
mypy cosmosquant/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Disclaimer

**IMPORTANT**: This software is for educational and research purposes only. See [DISCLAIMER.md](DISCLAIMER.md) for full details regarding financial trading risks.