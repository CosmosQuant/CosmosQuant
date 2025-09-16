"""Base data source interface."""

from abc import ABC, abstractmethod
from typing import Iterator, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import pandas as pd


@dataclass
class Tick:
    """Tick data representation."""
    symbol: str
    timestamp: datetime
    bid: float
    ask: float
    last: float
    volume: int


@dataclass 
class Bar:
    """Bar data representation."""
    symbol: str
    timestamp: datetime
    open: float
    high: float 
    low: float
    close: float
    volume: int


class BaseDataSource(ABC):
    """Base data source interface for both historical and live data."""
    
    def __init__(self, symbol: str):
        self.symbol = symbol
        self._current_bar: Optional[Bar] = None
        self._current_tick: Optional[Tick] = None
    
    @abstractmethod
    def connect(self) -> bool:
        """Connect to the data source."""
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """Disconnect from the data source."""
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """Check if connected to data source."""
        pass
    
    @abstractmethod
    def get_bars(self, start_date: Optional[datetime] = None, 
                end_date: Optional[datetime] = None) -> Iterator[Bar]:
        """Get historical bars."""
        pass
    
    @abstractmethod
    def get_ticks(self, start_date: Optional[datetime] = None,
                 end_date: Optional[datetime] = None) -> Iterator[Tick]:
        """Get historical ticks."""
        pass
    
    @abstractmethod
    def subscribe_bars(self) -> bool:
        """Subscribe to live bar data."""
        pass
    
    @abstractmethod
    def subscribe_ticks(self) -> bool:
        """Subscribe to live tick data."""
        pass
    
    @abstractmethod
    def unsubscribe_bars(self) -> bool:
        """Unsubscribe from live bar data."""
        pass
    
    @abstractmethod
    def unsubscribe_ticks(self) -> bool:
        """Unsubscribe from live tick data."""
        pass
    
    @property
    def current_bar(self) -> Optional[Bar]:
        """Get the current bar."""
        return self._current_bar
    
    @property
    def current_tick(self) -> Optional[Tick]:
        """Get the current tick."""
        return self._current_tick