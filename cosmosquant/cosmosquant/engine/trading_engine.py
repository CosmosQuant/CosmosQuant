"""Trading engine that coordinates strategy execution."""

from typing import Optional, List
from datetime import datetime
import time

from cosmosquant.cosmosquant.brokers.base import BaseBroker
from cosmosquant.cosmosquant.datasources.base import BaseDataSource, Bar, Tick
from cosmosquant.cosmosquant.strategies.base import BaseStrategy


class TradingEngine:
    """Main trading engine that coordinates strategy execution."""
    
    def __init__(self, strategy: BaseStrategy):
        self.strategy = strategy
        self.broker = strategy.broker
        self.data_source = strategy.data_source
        self._running = False
        self._bars_processed = 0
        self._ticks_processed = 0
    
    def run_backtest(self, start_date: Optional[datetime] = None,
                    end_date: Optional[datetime] = None, 
                    use_bars: bool = True) -> dict:
        """Run backtest on historical data."""
        print("Starting backtest...")
        
        # Connect to broker and data source
        if not self.broker.connect():
            raise RuntimeError("Failed to connect to broker")
        
        if not self.data_source.connect():
            raise RuntimeError("Failed to connect to data source")
        
        try:
            # Initialize strategy
            self.strategy.on_start()
            
            if use_bars:
                self._run_bar_backtest(start_date, end_date)
            else:
                self._run_tick_backtest(start_date, end_date)
            
            # Finalize strategy
            self.strategy.on_stop()
            
            # Return performance summary
            return self._get_performance_summary()
            
        finally:
            self.broker.disconnect()
            self.data_source.disconnect()
    
    def run_live(self, use_bars: bool = True, sleep_interval: float = 1.0):
        """Run strategy on live data."""
        print("Starting live trading...")
        
        # Connect to broker and data source
        if not self.broker.connect():
            raise RuntimeError("Failed to connect to broker")
        
        if not self.data_source.connect():
            raise RuntimeError("Failed to connect to data source")
        
        try:
            # Subscribe to live data
            if use_bars:
                self.data_source.subscribe_bars()
            else:
                self.data_source.subscribe_ticks()
            
            # Initialize strategy
            self.strategy.on_start()
            self._running = True
            
            print("Live trading started. Press Ctrl+C to stop.")
            
            while self._running:
                try:
                    if use_bars and self.data_source.current_bar:
                        self.strategy.on_bar(self.data_source.current_bar)
                        self._bars_processed += 1
                    
                    if not use_bars and self.data_source.current_tick:
                        self.strategy.on_tick(self.data_source.current_tick)
                        self._ticks_processed += 1
                    
                    time.sleep(sleep_interval)
                    
                except KeyboardInterrupt:
                    print("\\nStopping live trading...")
                    break
            
            # Finalize strategy
            self.strategy.on_stop()
            
        finally:
            self._running = False
            if use_bars:
                self.data_source.unsubscribe_bars()
            else:
                self.data_source.unsubscribe_ticks()
            
            self.broker.disconnect()
            self.data_source.disconnect()
    
    def _run_bar_backtest(self, start_date: Optional[datetime], end_date: Optional[datetime]):
        """Run backtest using bar data."""
        print("Running bar-based backtest...")
        
        for bar in self.data_source.get_bars(start_date, end_date):
            # Update broker with current price (for simulation broker)
            if hasattr(self.broker, 'update_price'):
                self.broker.update_price(bar.symbol, bar.close)
            
            # Call strategy
            self.strategy.on_bar(bar)
            self._bars_processed += 1
            
            if self._bars_processed % 1000 == 0:
                print(f"Processed {self._bars_processed} bars...")
        
        print(f"Backtest completed. Processed {self._bars_processed} bars.")
    
    def _run_tick_backtest(self, start_date: Optional[datetime], end_date: Optional[datetime]):
        """Run backtest using tick data."""
        print("Running tick-based backtest...")
        
        for tick in self.data_source.get_ticks(start_date, end_date):
            # Update broker with current price (for simulation broker)
            if hasattr(self.broker, 'update_price'):
                self.broker.update_price(tick.symbol, tick.last)
            
            # Call strategy
            self.strategy.on_tick(tick)
            self._ticks_processed += 1
            
            if self._ticks_processed % 10000 == 0:
                print(f"Processed {self._ticks_processed} ticks...")
        
        print(f"Backtest completed. Processed {self._ticks_processed} ticks.")
    
    def _get_performance_summary(self) -> dict:
        """Get performance summary."""
        account = self.broker.get_account_info()
        orders = self.broker.get_orders()
        
        filled_orders = [o for o in orders if o.status.value == "filled"]
        total_trades = len(filled_orders)
        
        return {
            "initial_cash": getattr(self.broker, 'initial_cash', 0.0),
            "final_cash": account.cash,
            "final_portfolio_value": account.total_value,
            "total_return": account.total_value - getattr(self.broker, 'initial_cash', 0.0),
            "total_trades": total_trades,
            "bars_processed": self._bars_processed,
            "ticks_processed": self._ticks_processed,
            "positions": account.positions
        }
    
    def stop(self):
        """Stop the trading engine."""
        self._running = False