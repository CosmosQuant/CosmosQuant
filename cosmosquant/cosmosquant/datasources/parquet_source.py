"""Parquet data source for historical data."""

import pandas as pd
from typing import Iterator, Optional
from datetime import datetime
from pathlib import Path

from cosmosquant.cosmosquant.datasources.base import BaseDataSource, Bar, Tick


class ParquetDataSource(BaseDataSource):
    """Data source that reads from Parquet files."""
    
    def __init__(self, symbol: str, data_path: str):
        super().__init__(symbol)
        self.data_path = Path(data_path)
        self._connected = False
        self._data: Optional[pd.DataFrame] = None
    
    def connect(self) -> bool:
        """Connect to the Parquet data source."""
        try:
            if self.data_path.exists():
                self._data = pd.read_parquet(self.data_path)
                # Ensure timestamp column is datetime
                if 'timestamp' in self._data.columns:
                    self._data['timestamp'] = pd.to_datetime(self._data['timestamp'])
                    self._data = self._data.sort_values('timestamp')
                self._connected = True
                return True
            else:
                print(f"Data file not found: {self.data_path}")
                return False
        except Exception as e:
            print(f"Error connecting to Parquet data: {e}")
            return False
    
    def disconnect(self) -> bool:
        """Disconnect from the data source."""
        self._connected = False
        self._data = None
        return True
    
    def is_connected(self) -> bool:
        """Check if connected to data source."""
        return self._connected
    
    def get_bars(self, start_date: Optional[datetime] = None, 
                end_date: Optional[datetime] = None) -> Iterator[Bar]:
        """Get historical bars from Parquet data."""
        if not self._connected or self._data is None:
            return
        
        df = self._data.copy()
        
        # Filter by date range if provided
        if start_date:
            df = df[df['timestamp'] >= start_date]
        if end_date:
            df = df[df['timestamp'] <= end_date]
        
        # Check required columns for bar data
        required_cols = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        if not all(col in df.columns for col in required_cols):
            print(f"Missing required columns for bar data: {required_cols}")
            return
        
        for _, row in df.iterrows():
            bar = Bar(
                symbol=self.symbol,
                timestamp=row['timestamp'],
                open=float(row['open']),
                high=float(row['high']),
                low=float(row['low']),
                close=float(row['close']),
                volume=int(row['volume'])
            )
            self._current_bar = bar
            yield bar
    
    def get_ticks(self, start_date: Optional[datetime] = None,
                 end_date: Optional[datetime] = None) -> Iterator[Tick]:
        """Get historical ticks from Parquet data."""
        if not self._connected or self._data is None:
            return
        
        df = self._data.copy()
        
        # Filter by date range if provided
        if start_date:
            df = df[df['timestamp'] >= start_date]
        if end_date:
            df = df[df['timestamp'] <= end_date]
        
        # Check required columns for tick data
        required_cols = ['timestamp', 'bid', 'ask', 'last', 'volume']
        if not all(col in df.columns for col in required_cols):
            print(f"Missing required columns for tick data: {required_cols}")
            return
        
        for _, row in df.iterrows():
            tick = Tick(
                symbol=self.symbol,
                timestamp=row['timestamp'],
                bid=float(row['bid']),
                ask=float(row['ask']),
                last=float(row['last']),
                volume=int(row['volume'])
            )
            self._current_tick = tick
            yield tick
    
    def subscribe_bars(self) -> bool:
        """Subscribe to live bar data (not supported for Parquet)."""
        print("Live data subscription not supported for Parquet data source")
        return False
    
    def subscribe_ticks(self) -> bool:
        """Subscribe to live tick data (not supported for Parquet)."""
        print("Live data subscription not supported for Parquet data source")
        return False
    
    def unsubscribe_bars(self) -> bool:
        """Unsubscribe from live bar data (not supported for Parquet)."""
        return True
    
    def unsubscribe_ticks(self) -> bool:
        """Unsubscribe from live tick data (not supported for Parquet)."""
        return True