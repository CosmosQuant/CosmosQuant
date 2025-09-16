"""Interactive Brokers broker implementation."""

from typing import Dict, List, Optional
from datetime import datetime
import asyncio

from cosmosquant.cosmosquant.brokers.base import (
    BaseBroker, Order, Position, AccountInfo, OrderType, OrderSide, OrderStatus
)

try:
    from ib_insync import IB, Stock, MarketOrder, LimitOrder, Contract
    IB_AVAILABLE = True
except ImportError:
    IB_AVAILABLE = False
    print("ib-insync not available. IB broker functionality will be limited.")


class IBBroker(BaseBroker):
    """Interactive Brokers broker implementation."""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 7497, client_id: int = 1):
        super().__init__()
        self.host = host
        self.port = port
        self.client_id = client_id
        
        if not IB_AVAILABLE:
            raise ImportError("ib-insync is required for IBBroker. Install with: pip install ib-insync")
        
        self.ib = IB()
        self._connected = False
        self._positions: Dict[str, Position] = {}
        self._account_info: Optional[AccountInfo] = None
    
    def connect(self) -> bool:
        """Connect to Interactive Brokers."""
        try:
            self.ib.connect(self.host, self.port, self.client_id)
            self._connected = self.ib.isConnected()
            
            if self._connected:
                self._update_account_info()
                self._update_positions()
            
            return self._connected
        except Exception as e:
            print(f"Error connecting to IB: {e}")
            return False
    
    def disconnect(self) -> bool:
        """Disconnect from Interactive Brokers."""
        try:
            if self._connected:
                self.ib.disconnect()
            self._connected = False
            return True
        except Exception as e:
            print(f"Error disconnecting from IB: {e}")
            return False
    
    def is_connected(self) -> bool:
        """Check if connected to broker."""
        return self._connected and self.ib.isConnected()
    
    def _create_contract(self, symbol: str) -> Contract:
        """Create IB contract for a symbol."""
        # This is a simple implementation for US stocks
        # In practice, you might want more sophisticated contract creation
        return Stock(symbol, 'SMART', 'USD')
    
    def submit_order(self, symbol: str, side: OrderSide, order_type: OrderType, 
                    quantity: float, price: Optional[float] = None) -> str:
        """Submit an order and return order ID."""
        if not self._connected:
            raise RuntimeError("Broker not connected")
        
        try:
            contract = self._create_contract(symbol)
            
            # Create IB order
            if order_type == OrderType.MARKET:
                ib_order = MarketOrder(
                    action="BUY" if side == OrderSide.BUY else "SELL",
                    totalQuantity=quantity
                )
            elif order_type == OrderType.LIMIT:
                if price is None:
                    raise ValueError("Price required for limit orders")
                ib_order = LimitOrder(
                    action="BUY" if side == OrderSide.BUY else "SELL",
                    totalQuantity=quantity,
                    lmtPrice=price
                )
            else:
                raise ValueError(f"Unsupported order type: {order_type}")
            
            # Submit order to IB
            trade = self.ib.placeOrder(contract, ib_order)
            
            # Create our order object
            order_id = str(trade.order.orderId)
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
            return order_id
            
        except Exception as e:
            print(f"Error submitting order: {e}")
            raise
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order."""
        try:
            if order_id in self._orders:
                # Find the IB trade
                for trade in self.ib.trades():
                    if str(trade.order.orderId) == order_id:
                        self.ib.cancelOrder(trade.order)
                        self._orders[order_id].status = OrderStatus.CANCELLED
                        return True
            return False
        except Exception as e:
            print(f"Error cancelling order: {e}")
            return False
    
    def get_order(self, order_id: str) -> Optional[Order]:
        """Get order by ID."""
        return self._orders.get(order_id)
    
    def get_orders(self) -> List[Order]:
        """Get all orders."""
        return list(self._orders.values())
    
    def _update_account_info(self):
        """Update account information from IB."""
        try:
            account_values = self.ib.accountValues()
            cash = 0.0
            total_value = 0.0
            
            for value in account_values:
                if value.tag == 'CashBalance' and value.currency == 'USD':
                    cash = float(value.value)
                elif value.tag == 'NetLiquidation' and value.currency == 'USD':
                    total_value = float(value.value)
            
            self._account_info = AccountInfo(
                cash=cash,
                total_value=total_value,
                positions=self._positions.copy()
            )
        except Exception as e:
            print(f"Error updating account info: {e}")
    
    def _update_positions(self):
        """Update positions from IB."""
        try:
            ib_positions = self.ib.positions()
            self._positions.clear()
            
            for pos in ib_positions:
                if pos.position != 0:  # Only include non-zero positions
                    symbol = pos.contract.symbol
                    current_price = self._get_current_price(symbol)
                    
                    position = Position(
                        symbol=symbol,
                        quantity=pos.position,
                        avg_price=pos.avgCost / abs(pos.position) if pos.position != 0 else 0.0,
                        market_value=pos.position * current_price,
                        unrealized_pnl=pos.unrealizedPNL
                    )
                    self._positions[symbol] = position
        except Exception as e:
            print(f"Error updating positions: {e}")
    
    def _get_current_price(self, symbol: str) -> float:
        """Get current market price for a symbol."""
        try:
            contract = self._create_contract(symbol)
            ticker = self.ib.reqMktData(contract, '', False, False)
            self.ib.sleep(1)  # Wait for data
            
            if ticker.last and ticker.last > 0:
                return ticker.last
            elif ticker.close and ticker.close > 0:
                return ticker.close
            else:
                return 0.0
        except Exception as e:
            print(f"Error getting current price for {symbol}: {e}")
            return 0.0
    
    def get_account_info(self) -> AccountInfo:
        """Get account information."""
        if self._connected:
            self._update_account_info()
        
        if self._account_info is None:
            return AccountInfo(cash=0.0, total_value=0.0, positions={})
        
        return self._account_info
    
    def get_position(self, symbol: str) -> Optional[Position]:
        """Get position for a symbol."""
        if self._connected:
            self._update_positions()
        
        return self._positions.get(symbol)