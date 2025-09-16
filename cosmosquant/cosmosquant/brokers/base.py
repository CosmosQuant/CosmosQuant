"""Base broker interface."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class OrderType(Enum):
    """Order types."""
    MARKET = "market"
    LIMIT = "limit"


class OrderSide(Enum):
    """Order sides."""
    BUY = "buy"
    SELL = "sell"


class OrderStatus(Enum):
    """Order status."""
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


@dataclass
class Order:
    """Order representation."""
    id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: Optional[float] = None
    status: OrderStatus = OrderStatus.PENDING
    filled_quantity: float = 0.0
    avg_fill_price: float = 0.0
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass 
class Position:
    """Position representation."""
    symbol: str
    quantity: float
    avg_price: float
    market_value: float
    unrealized_pnl: float


@dataclass
class AccountInfo:
    """Account information."""
    cash: float
    total_value: float
    positions: Dict[str, Position]


class BaseBroker(ABC):
    """Base broker interface for both simulation and live trading."""
    
    def __init__(self):
        self._orders: Dict[str, Order] = {}
        self._next_order_id = 1
    
    @abstractmethod
    def connect(self) -> bool:
        """Connect to the broker."""
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """Disconnect from the broker."""
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """Check if connected to broker."""
        pass
    
    @abstractmethod
    def submit_order(self, symbol: str, side: OrderSide, order_type: OrderType, 
                    quantity: float, price: Optional[float] = None) -> str:
        """Submit an order and return order ID."""
        pass
    
    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order."""
        pass
    
    @abstractmethod
    def get_order(self, order_id: str) -> Optional[Order]:
        """Get order by ID."""
        pass
    
    @abstractmethod
    def get_orders(self) -> List[Order]:
        """Get all orders."""
        pass
    
    @abstractmethod
    def get_account_info(self) -> AccountInfo:
        """Get account information."""
        pass
    
    @abstractmethod
    def get_position(self, symbol: str) -> Optional[Position]:
        """Get position for a symbol."""
        pass
    
    def _generate_order_id(self) -> str:
        """Generate a unique order ID."""
        order_id = f"ORD_{self._next_order_id:06d}"
        self._next_order_id += 1
        return order_id