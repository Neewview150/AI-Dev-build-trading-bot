import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_mock_data(start_date: str, end_date: str, interval: str = '5T') -> pd.DataFrame:
    """Generate mock data for AUD/USD pair."""
    date_range = pd.date_range(start=start_date, end=end_date, freq=interval)
    prices = np.random.lognormal(mean=0, sigma=0.01, size=len(date_range)) * 0.75 + 0.75
    return pd.DataFrame({'timestamp': date_range, 'close': prices})

def simple_moving_average_strategy(data: pd.DataFrame, short_window: int = 40, long_window: int = 100):
    """Simple moving average crossover strategy."""
    signals = pd.DataFrame(index=data.index)
    signals['price'] = data['close']
    signals['short_mavg'] = data['close'].rolling(window=short_window, min_periods=1).mean()
    signals['long_mavg'] = data['close'].rolling(window=long_window, min_periods=1).mean()
    signals['signal'] = 0.0
    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)
    signals['positions'] = signals['signal'].diff()
    return signals

def backtest_strategy(data: pd.DataFrame, initial_balance: float = 10000.0):
    """Backtest the strategy on historical data."""
    signals = simple_moving_average_strategy(data)
    balance = initial_balance
    position = 0.0
    portfolio_value = []

    for i in range(len(signals)):
        if signals['positions'][i] == 1.0:  # Buy signal
            position = balance / signals['price'][i]
            balance = 0.0
        elif signals['positions'][i] == -1.0:  # Sell signal
            balance = position * signals['price'][i]
            position = 0.0
        portfolio_value.append(balance + position * signals['price'][i])

    final_value = portfolio_value[-1]
    pnl_percentage = ((final_value - initial_balance) / initial_balance) * 100
    max_drawdown = calculate_max_drawdown(portfolio_value)
    print(f"Final Portfolio Value: ${final_value:.2f}")
    print(f"Total PnL: {pnl_percentage:.2f}%")
    print(f"Max Drawdown: {max_drawdown:.2f}%")

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
    start_date = '2022-01-01'
    end_date = '2022-12-31'
    mock_data = generate_mock_data(start_date, end_date)
    backtest_strategy(mock_data)