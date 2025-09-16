"""Example of running a backtest with CosmosQuant."""

import sys
from pathlib import Path

# Add the cosmosquant package to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cosmosquant.cosmosquant.engine.trading_engine import TradingEngine
from cosmosquant.cosmosquant.brokers.sim_broker import SimBroker
from cosmosquant.cosmosquant.datasources.parquet_source import ParquetDataSource
from cosmosquant.cosmosquant.utils.performance import print_performance_summary
from cosmosquant.cosmosquant.utils.data import create_sample_data, save_sample_data
from examples.simple_strategies import BuyAndHoldStrategy, SimpleMovingAverageStrategy


def create_sample_data_file():
    """Create sample data for testing."""
    print("Creating sample data...")
    
    # Create sample data
    df = create_sample_data(
        symbol="AAPL",
        start_date="2023-01-01", 
        end_date="2023-12-31",
        initial_price=150.0
    )
    
    # Save to parquet file
    data_dir = Path(__file__).parent.parent / "datas"
    data_dir.mkdir(exist_ok=True)
    data_file = data_dir / "AAPL_2023.parquet"
    save_sample_data(df, str(data_file))
    
    return str(data_file)


def run_buy_and_hold_backtest():
    """Run a buy and hold backtest."""
    print("\\n" + "=" * 60)
    print("RUNNING BUY AND HOLD BACKTEST")
    print("=" * 60)
    
    # Create sample data
    data_file = create_sample_data_file()
    
    # Initialize components
    broker = SimBroker(initial_cash=10000.0)
    data_source = ParquetDataSource(symbol="AAPL", data_path=data_file)
    strategy = BuyAndHoldStrategy(broker, data_source, initial_quantity=50)
    
    # Create and run engine
    engine = TradingEngine(strategy)
    summary = engine.run_backtest()
    
    # Print results
    print_performance_summary(summary)


def run_moving_average_backtest():
    """Run a moving average crossover backtest."""
    print("\\n" + "=" * 60)
    print("RUNNING MOVING AVERAGE CROSSOVER BACKTEST")
    print("=" * 60)
    
    # Create sample data
    data_file = create_sample_data_file()
    
    # Initialize components
    broker = SimBroker(initial_cash=10000.0)
    data_source = ParquetDataSource(symbol="AAPL", data_path=data_file)
    strategy = SimpleMovingAverageStrategy(broker, data_source, short_window=5, long_window=20)
    
    # Create and run engine
    engine = TradingEngine(strategy)
    summary = engine.run_backtest()
    
    # Print results
    print_performance_summary(summary)


if __name__ == "__main__":
    try:
        # Run both examples
        run_buy_and_hold_backtest()
        run_moving_average_backtest()
        
        print("\\n" + "=" * 60)
        print("BACKTEST EXAMPLES COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\\nError running backtests: {e}")
        import traceback
        traceback.print_exc()