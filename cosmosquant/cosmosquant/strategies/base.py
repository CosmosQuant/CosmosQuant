"""Base strategy interface."""

from abc import ABC, abstractmethod
from typing import Optional

from cosmosquant.cosmosquant.brokers.base import BaseBroker, OrderSide, OrderType
from cosmosquant.cosmosquant.datasources.base import BaseDataSource, Bar, Tick


class BaseStrategy(ABC):
    """Base strategy class for implementing trading strategies."""
    
    def __init__(self, broker: BaseBroker, data_source: BaseDataSource):
        self.broker = broker
        self.data_source = data_source
        self.symbol = data_source.symbol
        
    @abstractmethod
    def on_bar(self, bar: Bar):
        """Called when a new bar is received."""
        pass
    
    @abstractmethod
    def on_tick(self, tick: Tick):
        """Called when a new tick is received."""
        pass
    
    def on_start(self):
        """Called when the strategy starts."""
        pass
    
    def on_stop(self):
        """Called when the strategy stops."""
        pass
    
    def buy(self, quantity: float, price: Optional[float] = None) -> str:
        """Place a buy order."""
        order_type = OrderType.LIMIT if price is not None else OrderType.MARKET
        return self.broker.submit_order(
            symbol=self.symbol,
            side=OrderSide.BUY,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
    
    def sell(self, quantity: float, price: Optional[float] = None) -> str:
        """Place a sell order."""
        order_type = OrderType.LIMIT if price is not None else OrderType.MARKET
        return self.broker.submit_order(
            symbol=self.symbol,
            side=OrderSide.SELL,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
    
    def get_position_size(self) -> float:
        """Get current position size for the symbol."""
        position = self.broker.get_position(self.symbol)
        return position.quantity if position else 0.0
    
    def get_cash(self) -> float:
        """Get available cash."""
        account = self.broker.get_account_info()
        return account.cash
    
    def get_portfolio_value(self) -> float:
        """Get total portfolio value."""
        account = self.broker.get_account_info()
        return account.total_value