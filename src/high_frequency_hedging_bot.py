import numpy as np
import pandas as pd
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

class HighFrequencyHedgingBot:
    def __init__(self, initial_balance=10000, history_size=1000):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.history_size = history_size
        self.mock_data = self._generate_mock_data()
        self.trade_history = []
        self.portfolio_value_history = []

    def _generate_mock_data(self):
        """Generate mock market data."""
        base_price = 100
        volatility = 0.01
        trend = 0.0001
        timestamps = [datetime.now() - timedelta(minutes=i) for i in range(self.history_size)]
        prices = [base_price]

        for _ in range(1, self.history_size):
            change = np.random.normal(trend, volatility)
            new_price = prices[-1] * (1 + change)
            prices.append(new_price)

        data = pd.DataFrame({
            'timestamp': timestamps,
            'open': prices,
            'high': [p * (1 + np.random.uniform(0, volatility)) for p in prices],
            'low': [p * (1 - np.random.uniform(0, volatility)) for p in prices],
            'close': prices,
            'volume': np.random.uniform(100, 1000, size=self.history_size)
        })

        return data

    def run_backtest(self):
        """Run a simple backtest on the mock data."""
        logging.info("Starting backtest...")
        for index, row in self.mock_data.iterrows():
            current_price = row['close']
            self._simulate_trade_decision(current_price)
            self.portfolio_value_history.append(self._calculate_portfolio_value(current_price))

        self._log_results()

    def _simulate_trade_decision(self, current_price):
        """Simulate a simple trading decision."""
        if np.random.rand() > 0.5:
            self._execute_trade('buy', current_price)
        else:
            self._execute_trade('sell', current_price)

    def _execute_trade(self, action, price):
        """Execute a mock trade."""
        if action == 'buy' and self.balance > price:
            self.balance -= price
            self.trade_history.append({'action': 'buy', 'price': price, 'timestamp': datetime.now()})
        elif action == 'sell' and self.balance < self.initial_balance:
            self.balance += price
            self.trade_history.append({'action': 'sell', 'price': price, 'timestamp': datetime.now()})

    def _calculate_portfolio_value(self, current_price):
        """Calculate the current portfolio value."""
        return self.balance

    def _log_results(self):
        """Log the results of the backtest."""
        final_value = self.portfolio_value_history[-1]
        total_return = ((final_value - self.initial_balance) / self.initial_balance) * 100
        max_drawdown = self._calculate_max_drawdown()
        win_rate = self._calculate_win_rate()

        logging.info(f"Backtest completed. Final Portfolio Value: ${final_value:.2f}")
        logging.info(f"Total Return: {total_return:.2f}%")
        logging.info(f"Max Drawdown: {max_drawdown:.2f}%")
        logging.info(f"Win Rate: {win_rate:.2f}%")

    def _calculate_max_drawdown(self):
        """Calculate the maximum drawdown."""
        peak = self.portfolio_value_history[0]
        max_drawdown = 0

        for value in self.portfolio_value_history:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak * 100
            if drawdown > max_drawdown:
                max_drawdown = drawdown

        return max_drawdown

    def _calculate_win_rate(self):
        """Calculate the win rate of trades."""
        wins = sum(1 for trade in self.trade_history if trade['action'] == 'sell')
        total_trades = len(self.trade_history)
        return (wins / total_trades) * 100 if total_trades > 0 else 0

if __name__ == "__main__":
    bot = HighFrequencyHedgingBot()
    bot.run_backtest()
