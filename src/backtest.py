import json
import logging
import pandas as pd
from datetime import datetime
from typing import Dict, List
from src.core.engine import TradingEngine
from src.config import load_config
from src.utils.logger import setup_logger

class Backtester:
    def __init__(self, historical_data: pd.DataFrame, config: Dict):
        self.historical_data = historical_data
        self.config = config
        self.engine = TradingEngine(config)
        self.logger = setup_logger()
        self.portfolio_value_history = []

    def run_backtest(self) -> None:
        self.logger.info("Starting backtest...")
        initial_portfolio_value = self.config['initial_balance']
        self.portfolio_value_history.append(initial_portfolio_value)

        for index, row in self.historical_data.iterrows():
            current_price = row['close']
            self.engine.price_feed.price_history.append(row.to_dict())
            self.engine.update()

            current_portfolio_value = self.engine.portfolio.get_total_value(current_price)
            self.portfolio_value_history.append(current_portfolio_value)

        self._log_results()

    def _log_results(self) -> None:
        final_portfolio_value = self.portfolio_value_history[-1]
        total_return = ((final_portfolio_value - self.portfolio_value_history[0]) / self.portfolio_value_history[0]) * 100
        max_drawdown = self._calculate_max_drawdown()

        self.logger.info(f"Backtest completed.")
        self.logger.info(f"Final Portfolio Value: ${final_portfolio_value:.2f}")
        self.logger.info(f"Total Return: {total_return:.2f}%")
        self.logger.info(f"Max Drawdown: {max_drawdown:.2f}%")

    def _calculate_max_drawdown(self) -> float:
        peak = self.portfolio_value_history[0]
        max_drawdown = 0

        for value in self.portfolio_value_history:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak * 100
            if drawdown > max_drawdown:
                max_drawdown = drawdown

        return max_drawdown

def load_historical_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path, parse_dates=['timestamp'])

if __name__ == "__main__":
    config = load_config()
    historical_data = load_historical_data('historical_data.csv')
    backtester = Backtester(historical_data, config)
    backtester.run_backtest()
