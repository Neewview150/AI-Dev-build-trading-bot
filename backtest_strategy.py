import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict
from src.core.engine import TradingEngine
from src.config import load_config
from src.utils.logger import setup_logger

def generate_mock_data(start_date: datetime, periods: int, freq: str) -> pd.DataFrame:
    """Generate mock data for a given period and frequency."""
    date_range = pd.date_range(start=start_date, periods=periods, freq=freq)
    data = {
        'timestamp': date_range,
        'open': np.random.uniform(low=1000, high=2000, size=periods),
        'high': np.random.uniform(low=1000, high=2000, size=periods),
        'low': np.random.uniform(low=1000, high=2000, size=periods),
        'close': np.random.uniform(low=1000, high=2000, size=periods),
        'volume': np.random.uniform(low=100, high=1000, size=periods)
    }
    return pd.DataFrame(data)

def main():
    logger = setup_logger()
    config = load_config()
    
    # Generate mock data for one year with a 5-minute interval
    start_date = datetime.now() - timedelta(days=365)
    mock_data = generate_mock_data(start_date, periods=365*24*12, freq='5T')
    
    # Initialize the trading engine with the configuration
    engine = TradingEngine(config)
    
    # Run backtest
    logger.info("Starting backtest with mock data...")
    initial_portfolio_value = config['initial_balance']
    portfolio_value_history = [initial_portfolio_value]
    
    for index, row in mock_data.iterrows():
        current_price = row['close']
        engine.price_feed.price_history.append(row.to_dict())
        engine.update()
        
        current_portfolio_value = engine.portfolio.get_total_value(current_price)
        portfolio_value_history.append(current_portfolio_value)
    
    # Calculate results
    final_portfolio_value = portfolio_value_history[-1]
    total_return = ((final_portfolio_value - initial_portfolio_value) / initial_portfolio_value) * 100
    max_drawdown = calculate_max_drawdown(portfolio_value_history)
    
    logger.info(f"Backtest completed.")
    logger.info(f"Final Portfolio Value: ${final_portfolio_value:.2f}")
    logger.info(f"Total Return: {total_return:.2f}%")
    logger.info(f"Max Drawdown: {max_drawdown:.2f}%")

def calculate_max_drawdown(portfolio_values: list) -> float:
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
    main()
