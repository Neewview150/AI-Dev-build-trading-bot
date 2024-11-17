import pandas as pd
import numpy as np

def load_historical_data(file_path: str) -> pd.DataFrame:
    """Load historical price data from a CSV file."""
    return pd.read_csv(file_path, parse_dates=['timestamp'])

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
    print(f"Final Portfolio Value: ${final_value:.2f}")
    print(f"Total PnL: {pnl_percentage:.2f}%")

if __name__ == "__main__":
    historical_data = load_historical_data('historical_data.csv')
    backtest_strategy(historical_data)