"""Simulation broker for backtesting."""

from typing import Dict, List, Optional
from datetime import datetime

from cosmosquant.cosmosquant.brokers.base import (
    BaseBroker, Order, Position, AccountInfo, OrderType, OrderSide, OrderStatus
)


class SimBroker(BaseBroker):
    """Simulation broker for backtesting."""
    
    def __init__(self, initial_cash: float = 100000.0):
        super().__init__()
        self.initial_cash = initial_cash
        self._cash = initial_cash
        self._positions: Dict[str, Position] = {}
        self._connected = False
        self._current_prices: Dict[str, float] = {}
    
    def connect(self) -> bool:
        """Connect to the simulation broker."""
        self._connected = True
        return True
    
    def disconnect(self) -> bool:
        """Disconnect from the simulation broker."""
        self._connected = False
        return True
    
    def is_connected(self) -> bool:
        """Check if connected to broker."""
        return self._connected
    
    def update_price(self, symbol: str, price: float):
        """Update current market price for a symbol."""
        self._current_prices[symbol] = price
        
        # Update position market values and unrealized PnL
        if symbol in self._positions:
            position = self._positions[symbol]
            position.market_value = position.quantity * price
            position.unrealized_pnl = (price - position.avg_price) * position.quantity
    
    def submit_order(self, symbol: str, side: OrderSide, order_type: OrderType, 
                    quantity: float, price: Optional[float] = None) -> str:
        """Submit an order and return order ID."""
        if not self._connected:
            raise RuntimeError("Broker not connected")
        
        order_id = self._generate_order_id()
        order = Order(
            id=order_id,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            status=OrderStatus.PENDING
        )
        
        self._orders[order_id] = order
        
        # For simulation, immediately try to fill market orders
        if order_type == OrderType.MARKET:
            self._try_fill_order(order)
        
        return order_id
    
    def _try_fill_order(self, order: Order):
        """Try to fill an order based on current market conditions."""
        current_price = self._current_prices.get(order.symbol)
        if current_price is None:
            order.status = OrderStatus.REJECTED
            return
        
        # For simulation, assume all market orders fill immediately
        if order.order_type == OrderType.MARKET:
            fill_price = current_price
        elif order.order_type == OrderType.LIMIT:
            # Limit order logic
            if order.side == OrderSide.BUY and current_price <= order.price:
                fill_price = order.price
            elif order.side == OrderSide.SELL and current_price >= order.price:
                fill_price = order.price
            else:
                return  # Order not filled
        else:
            return
        
        # Calculate order value
        order_value = order.quantity * fill_price
        
        # Check if we have enough cash for buy orders
        if order.side == OrderSide.BUY and order_value > self._cash:
            order.status = OrderStatus.REJECTED
            return
        
        # Check if we have enough shares for sell orders
        if order.side == OrderSide.SELL:
            current_position = self._positions.get(order.symbol)
            if current_position is None or current_position.quantity < order.quantity:
                order.status = OrderStatus.REJECTED
                return
        
        # Fill the order
        order.status = OrderStatus.FILLED
        order.filled_quantity = order.quantity
        order.avg_fill_price = fill_price
        
        # Update cash and positions
        if order.side == OrderSide.BUY:
            self._cash -= order_value
            self._update_position(order.symbol, order.quantity, fill_price)
        else:  # SELL
            self._cash += order_value
            self._update_position(order.symbol, -order.quantity, fill_price)
    
    def _update_position(self, symbol: str, quantity_change: float, price: float):
        """Update position for a symbol."""
        if symbol not in self._positions:
            self._positions[symbol] = Position(
                symbol=symbol,
                quantity=0.0,
                avg_price=0.0,
                market_value=0.0,
                unrealized_pnl=0.0
            )
        
        position = self._positions[symbol]
        
        if quantity_change > 0:  # Adding to position
            if position.quantity >= 0:  # Same direction
                total_cost = position.quantity * position.avg_price + quantity_change * price
                position.quantity += quantity_change
                position.avg_price = total_cost / position.quantity if position.quantity > 0 else 0.0
            else:  # Reducing short position
                position.quantity += quantity_change
                if position.quantity == 0:
                    position.avg_price = 0.0
        else:  # Reducing position
            if position.quantity > 0:  # Reducing long position
                position.quantity += quantity_change
                if position.quantity == 0:
                    position.avg_price = 0.0
            else:  # Adding to short position
                total_cost = position.quantity * position.avg_price + quantity_change * price
                position.quantity += quantity_change
                position.avg_price = total_cost / position.quantity if position.quantity < 0 else 0.0
        
        # Update market value and unrealized PnL
        current_price = self._current_prices.get(symbol, price)
        position.market_value = position.quantity * current_price
        position.unrealized_pnl = (current_price - position.avg_price) * position.quantity
        
        # Remove position if quantity is zero
        if position.quantity == 0:
            del self._positions[symbol]
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order."""
        if order_id in self._orders:
            order = self._orders[order_id]
            if order.status == OrderStatus.PENDING:
                order.status = OrderStatus.CANCELLED
                return True
        return False
    
    def get_order(self, order_id: str) -> Optional[Order]:
        """Get order by ID."""
        return self._orders.get(order_id)
    
    def get_orders(self) -> List[Order]:
        """Get all orders."""
        return list(self._orders.values())
    
    def get_account_info(self) -> AccountInfo:
        """Get account information."""
        total_value = self._cash + sum(pos.market_value for pos in self._positions.values())
        
        return AccountInfo(
            cash=self._cash,
            total_value=total_value,
            positions=self._positions.copy()
        )
    
    def get_position(self, symbol: str) -> Optional[Position]:
        """Get position for a symbol."""
        return self._positions.get(symbol)