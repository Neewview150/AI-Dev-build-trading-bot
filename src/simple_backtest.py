import numpy as np
import logging
from typing import List, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Mock data: Simulated historical price data
mock_data = [
    {'timestamp': '2023-01-01', 'close': 100},
    {'timestamp': '2023-01-02', 'close': 102},
    {'timestamp': '2023-01-03', 'close': 101},
    {'timestamp': '2023-01-04', 'close': 105},
    {'timestamp': '2023-01-05', 'close': 107},
    {'timestamp': '2023-01-06', 'close': 106},
    {'timestamp': '2023-01-07', 'close': 108},
    {'timestamp': '2023-01-08', 'close': 110},
    {'timestamp': '2023-01-09', 'close': 109},
    {'timestamp': '2023-01-10', 'close': 111},
]

def calculate_moving_average(prices: List[float], window: int) -> List[float]:
    """Calculate moving average for a given window size."""
    return np.convolve(prices, np.ones(window), 'valid') / window

def simple_strategy(data: List[Dict], short_window: int, long_window: int) -> Dict:
    """Simple moving average crossover strategy."""
    prices = [entry['close'] for entry in data]
    short_ma = calculate_moving_average(prices, short_window)
    long_ma = calculate_moving_average(prices, long_window)

    signals = []
    for i in range(len(long_ma)):
        if short_ma[i] > long_ma[i]:
            signals.append('buy')
        else:
            signals.append('sell')

    return {'signals': signals, 'prices': prices[len(prices) - len(signals):]}

def calculate_performance(prices: List[float], signals: List[str]) -> Dict:
    """Calculate performance metrics."""
    initial_balance = 10000
    balance = initial_balance
    position = 0  # 0 means no position, 1 means holding the asset

    portfolio_values = []

    for price, signal in zip(prices, signals):
        if signal == 'buy' and position == 0:
            position = balance / price
            balance = 0
        elif signal == 'sell' and position > 0:
            balance = position * price
            position = 0

        portfolio_value = balance + position * price
        portfolio_values.append(portfolio_value)

    total_return = (portfolio_values[-1] - initial_balance) / initial_balance * 100
    max_drawdown = calculate_max_drawdown(portfolio_values)

    return {
        'final_value': portfolio_values[-1],
        'total_return': total_return,
        'max_drawdown': max_drawdown
    }

def calculate_max_drawdown(portfolio_values: List[float]) -> float:
    """Calculate the maximum drawdown."""
    peak = portfolio_values[0]
    max_drawdown = 0

    for value in portfolio_values:
        if value > peak:
            peak = value
        drawdown = (peak - value) / peak * 100
        if drawdown > max_drawdown:
            max_drawdown = drawdown

    return max_drawdown

if __name__ == "__main__":
    short_window = 2
    long_window = 3

    strategy_results = simple_strategy(mock_data, short_window, long_window)
    performance = calculate_performance(strategy_results['prices'], strategy_results['signals'])

    logging.info(f"Final Portfolio Value: ${performance['final_value']:.2f}")
    logging.info(f"Total Return: {performance['total_return']:.2f}%")
    logging.info(f"Max Drawdown: {performance['max_drawdown']:.2f}%")
