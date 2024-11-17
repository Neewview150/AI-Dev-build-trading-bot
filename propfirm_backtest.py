import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict
from src.strategies.strategy import AdvancedStrategy
from src.portfolio.portfolio_manager import PortfolioManager
from src.utils.logger import get_logger

logger = get_logger(__name__)

def generate_mock_data(start_date: str, periods: int, freq: str = '5T') -> pd.DataFrame:
    """Generate mock trading data for backtesting."""
    date_rng = pd.date_range(start=start_date, periods=periods, freq=freq)
    price_data = np.random.normal(loc=100, scale=5, size=(periods,))
    return pd.DataFrame(date_rng, columns=['timestamp']).assign(close=price_data)

def execute_trades(strategy: AdvancedStrategy, data: pd.DataFrame, initial_balance: float) -> Dict:
    """Execute trades based on the strategy and calculate performance metrics."""
    portfolio = PortfolioManager(initial_balance=initial_balance, risk_percentage=1.0)
    price_feed = data.to_dict('records')

    for candle in price_feed:
        current_price = candle['close']
        portfolio.update_value(current_price)
        
        signals = strategy.generate_signals(price_feed)
        
        if signals.should_trade:
            position_size = portfolio.balance * (portfolio.risk_percentage / 100) / current_price
            
            if signals.action == 'buy' and not portfolio.has_position:
                portfolio.execute_buy(current_price, position_size)
            elif signals.action == 'sell' and portfolio.has_position:
                portfolio.execute_sell(current_price)
    
    final_value = portfolio.get_total_value(price_feed[-1]['close'])
    pnl_percentage = (final_value - initial_balance) / initial_balance * 100
    
    logger.info(f"Backtest completed. Final Portfolio Value: ${final_value:.2f}, PnL: {pnl_percentage:+.2f}%")
    
    return {
        'final_value': final_value,
        'pnl_percentage': pnl_percentage,
        'total_trades': portfolio.total_trades,
        'winning_trades': portfolio.winning_trades,
        'win_rate': portfolio.winning_trades / portfolio.total_trades * 100 if portfolio.total_trades > 0 else 0,
        'max_drawdown': portfolio.max_drawdown
    }

def calculate_max_drawdown(portfolio_values: List[float]) -> float:
    """Calculate the maximum drawdown from the portfolio value history."""
    peak = portfolio_values[0]
    max_drawdown = 0.0
    for value in portfolio_values:
        if value > peak:
            peak = value
        drawdown = (peak - value) / peak
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    return max_drawdown * 100

if __name__ == "__main__":
    # Generate mock data for one year with 5-minute intervals
    mock_data = generate_mock_data(start_date='2022-01-01', periods=365*24*12)
    
    # Initialize strategy
    config = {
        'ema_period': 20,
        'rsi_period': 14,
        'bb_period': 20,
        'g_channel_length': 10,
        'rsi_oversold': 30,
        'rsi_overbought': 70,
        'min_confidence': 0.7
    }
    strategy = AdvancedStrategy(config)
    
    # Execute backtest
    results = execute_trades(strategy, mock_data, initial_balance=10000)
    
    # Log results
    logger.info(f"Backtest Results: {results}")
