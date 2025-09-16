"""Utility functions for CosmosQuant."""

import pandas as pd
from typing import Dict, Any
from datetime import datetime


def format_currency(amount: float) -> str:
    """Format amount as currency."""
    return f"${amount:,.2f}"


def calculate_returns(prices: pd.Series) -> pd.Series:
    """Calculate returns from price series."""
    return prices.pct_change().dropna()


def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0) -> float:
    """Calculate Sharpe ratio."""
    excess_returns = returns - risk_free_rate / 252  # Daily risk-free rate
    return excess_returns.mean() / excess_returns.std() * (252 ** 0.5)


def calculate_max_drawdown(equity_curve: pd.Series) -> float:
    """Calculate maximum drawdown."""
    peak = equity_curve.expanding().max()
    drawdown = (equity_curve - peak) / peak
    return drawdown.min()


def print_performance_summary(summary: Dict[str, Any]):
    """Print a formatted performance summary."""
    print("\\n" + "=" * 50)
    print("PERFORMANCE SUMMARY")
    print("=" * 50)
    
    initial_cash = summary.get('initial_cash', 0.0)
    final_value = summary.get('final_portfolio_value', 0.0)
    total_return = summary.get('total_return', 0.0)
    
    print(f"Initial Cash:        {format_currency(initial_cash)}")
    print(f"Final Portfolio:     {format_currency(final_value)}")
    print(f"Total Return:        {format_currency(total_return)}")
    
    if initial_cash > 0:
        return_pct = (total_return / initial_cash) * 100
        print(f"Return %:            {return_pct:.2f}%")
    
    print(f"Total Trades:        {summary.get('total_trades', 0)}")
    print(f"Bars Processed:      {summary.get('bars_processed', 0)}")
    print(f"Ticks Processed:     {summary.get('ticks_processed', 0)}")
    
    positions = summary.get('positions', {})
    if positions:
        print("\\nFinal Positions:")
        for symbol, position in positions.items():
            print(f"  {symbol}: {position.quantity:.2f} @ {format_currency(position.avg_price)}")
    
    print("=" * 50)