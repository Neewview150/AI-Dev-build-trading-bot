import numpy as np
from collections import deque
from typing import Tuple, Dict

class DeltaGammaCalculator:
    def __init__(self, config: Dict):
        self.rolling_window_size = config['delta_gamma']['rolling_window_size']
        self.gold_prices = deque(maxlen=self.rolling_window_size)
        self.eurusd_prices = deque(maxlen=self.rolling_window_size)

    def update_prices(self, gold_price: float, eurusd_price: float) -> None:
        """Update the rolling window with the latest prices."""
        self.gold_prices.append(gold_price)
        self.eurusd_prices.append(eurusd_price)

    def calculate(self, gold_price: float, eurusd_price: float) -> Tuple[float, float]:
        """Calculate delta and gamma using the rolling window of historical prices."""
        self.update_prices(gold_price, eurusd_price)

        if len(self.gold_prices) < self.rolling_window_size or len(self.eurusd_prices) < self.rolling_window_size:
            # Not enough data to calculate delta and gamma
            return 0.0, 0.0

        # Convert deque to numpy arrays for calculation
        gold_prices_array = np.array(self.gold_prices)
        eurusd_prices_array = np.array(self.eurusd_prices)

        # Calculate returns
        gold_returns = np.diff(gold_prices_array) / gold_prices_array[:-1]
        eurusd_returns = np.diff(eurusd_prices_array) / eurusd_prices_array[:-1]

        # Calculate delta as the covariance between asset returns
        covariance_matrix = np.cov(gold_returns, eurusd_returns)
        delta = covariance_matrix[0, 1] / covariance_matrix[1, 1]

        # Calculate gamma as the rate of change of delta
        gamma = np.gradient(delta)

        return delta, gamma
