import numpy as np
import pandas as pd
from arch import arch_model
from collections import deque
from typing import Dict
import logging

class VolatilityForecaster:
    def __init__(self, config: Dict):
        self.logger = logging.getLogger(__name__)
        self.model_params = config['volatility_forecasting']['parameters']
        self.rolling_window_size = config['delta_gamma']['rolling_window_size']
        self.price_history = deque(maxlen=self.rolling_window_size)

    def update_price_history(self, price: float) -> None:
        """Update the rolling window with the latest price."""
        self.price_history.append(price)
        self.logger.debug(f"Updated price history: {list(self.price_history)}")

    def forecast(self) -> float:
        """Forecast volatility using the GARCH model."""
        if len(self.price_history) < self.rolling_window_size:
            self.logger.warning("Not enough data to forecast volatility.")
            return 0.0

        # Convert price history to returns
        prices_array = np.array(self.price_history)
        returns = np.diff(prices_array) / prices_array[:-1]

        # Fit GARCH model
        model = arch_model(returns, vol='Garch', p=self.model_params['p'], q=self.model_params['q'])
        model_fit = model.fit(disp='off')

        # Forecast volatility
        forecast = model_fit.forecast(horizon=1)
        volatility = forecast.variance.values[-1, 0]
        self.logger.info(f"Forecasted volatility: {volatility}")

        return volatility
