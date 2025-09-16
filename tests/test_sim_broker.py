"""Test SimBroker functionality."""

import pytest
from datetime import datetime

from cosmosquant.cosmosquant.brokers.sim_broker import SimBroker
from cosmosquant.cosmosquant.brokers.base import OrderSide, OrderType, OrderStatus


class TestSimBroker:
    """Test cases for SimBroker."""
    
    def test_broker_initialization(self):
        """Test broker initialization."""
        broker = SimBroker(initial_cash=10000.0)
        assert broker.initial_cash == 10000.0
        assert broker._cash == 10000.0
        assert not broker.is_connected()
    
    def test_connect_disconnect(self):
        """Test broker connection."""
        broker = SimBroker()
        
        # Test connection
        assert broker.connect()
        assert broker.is_connected()
        
        # Test disconnection
        assert broker.disconnect()
        assert not broker.is_connected()
    
    def test_market_order_submission(self):
        """Test market order submission."""
        broker = SimBroker(initial_cash=10000.0)
        broker.connect()
        
        # Update price to enable order filling
        broker.update_price("AAPL", 150.0)
        
        # Submit buy order
        order_id = broker.submit_order("AAPL", OrderSide.BUY, OrderType.MARKET, 10)
        
        assert order_id is not None
        order = broker.get_order(order_id)
        assert order is not None
        assert order.status == OrderStatus.FILLED
        assert order.filled_quantity == 10
        assert order.avg_fill_price == 150.0