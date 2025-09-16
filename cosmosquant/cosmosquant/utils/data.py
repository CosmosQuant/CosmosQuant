"""Data utilities for CosmosQuant."""

import pandas as pd
from pathlib import Path
from typing import Optional
from datetime import datetime


def create_sample_data(symbol: str, start_date: str, end_date: str, 
                      initial_price: float = 100.0) -> pd.DataFrame:
    """Create sample OHLCV data for testing."""
    import numpy as np
    
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    n_days = len(dates)
    
    # Generate random price movements
    np.random.seed(42)  # For reproducible results
    returns = np.random.normal(0.001, 0.02, n_days)  # 0.1% daily return, 2% volatility
    
    prices = [initial_price]
    for i in range(1, n_days):
        prices.append(prices[-1] * (1 + returns[i]))
    
    # Create OHLCV data
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = prices[i-1] if i > 0 else close
        volume = int(np.random.normal(1000000, 200000))
        
        data.append({
            'timestamp': date,
            'open': open_price,
            'high': max(open_price, high, close),
            'low': min(open_price, low, close),
            'close': close,
            'volume': max(volume, 1000)  # Ensure positive volume
        })
    
    return pd.DataFrame(data)


def save_sample_data(df: pd.DataFrame, filepath: str):
    """Save DataFrame to Parquet file."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(filepath, index=False)
    print(f"Sample data saved to: {filepath}")


def load_data(filepath: str) -> Optional[pd.DataFrame]:
    """Load data from Parquet file."""
    try:
        df = pd.read_parquet(filepath)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df.sort_values('timestamp')
    except Exception as e:
        print(f"Error loading data from {filepath}: {e}")
        return None


def validate_ohlcv_data(df: pd.DataFrame) -> bool:
    """Validate OHLCV data format."""
    required_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    
    if not all(col in df.columns for col in required_columns):
        print(f"Missing required columns. Expected: {required_columns}")
        return False
    
    # Check for valid OHLC relationships
    invalid_rows = df[
        (df['high'] < df['low']) |
        (df['high'] < df['open']) |
        (df['high'] < df['close']) |
        (df['low'] > df['open']) |
        (df['low'] > df['close'])
    ]
    
    if len(invalid_rows) > 0:
        print(f"Found {len(invalid_rows)} rows with invalid OHLC relationships")
        return False
    
    return True