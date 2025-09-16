"""Simple buy and hold strategy example."""

from cosmosquant.cosmosquant.strategies.base import BaseStrategy
from cosmosquant.cosmosquant.datasources.base import Bar, Tick


class BuyAndHoldStrategy(BaseStrategy):
    """Simple buy and hold strategy."""
    
    def __init__(self, broker, data_source, initial_quantity: float = 100):
        super().__init__(broker, data_source)
        self.initial_quantity = initial_quantity
        self.bought = False
    
    def on_bar(self, bar: Bar):
        """Buy on the first bar and hold."""
        if not self.bought:
            print(f"Buying {self.initial_quantity} shares of {bar.symbol} at {bar.close}")
            self.buy(self.initial_quantity)
            self.bought = True
    
    def on_tick(self, tick: Tick):
        """Buy on the first tick and hold."""
        if not self.bought:
            print(f"Buying {self.initial_quantity} shares of {tick.symbol} at {tick.last}")
            self.buy(self.initial_quantity)
            self.bought = True


class SimpleMovingAverageStrategy(BaseStrategy):
    """Simple moving average crossover strategy."""
    
    def __init__(self, broker, data_source, short_window: int = 10, long_window: int = 30):
        super().__init__(broker, data_source)
        self.short_window = short_window
        self.long_window = long_window
        self.prices = []
        self.position_size = 100
    
    def on_bar(self, bar: Bar):
        """Execute strategy on each bar."""
        self.prices.append(bar.close)
        
        # Only trade after we have enough data
        if len(self.prices) < self.long_window:
            return
        
        # Calculate moving averages
        short_ma = sum(self.prices[-self.short_window:]) / self.short_window
        long_ma = sum(self.prices[-self.long_window:]) / self.long_window
        
        current_position = self.get_position_size()
        
        # Buy signal: short MA crosses above long MA
        if short_ma > long_ma and current_position <= 0:
            print(f"Buy signal: Short MA ({short_ma:.2f}) > Long MA ({long_ma:.2f})")
            self.buy(self.position_size)
        
        # Sell signal: short MA crosses below long MA
        elif short_ma < long_ma and current_position > 0:
            print(f"Sell signal: Short MA ({short_ma:.2f}) < Long MA ({long_ma:.2f})")
            self.sell(current_position)
    
    def on_tick(self, tick: Tick):
        """Not implemented for tick data."""
        pass