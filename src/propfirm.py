import asyncio
import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from arch import arch_model
import ccxt.async_support as ccxt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PropFirmBot:
    def __init__(self, config):
        self.config = config
        self.exchange = ccxt.fbs({
            'apiKey': config['apiKey'],
            'secret': config['apiSecret'],
            'enableRateLimit': True,
        })
        self.symbols = ['XAU/USD', 'EUR/USD']
        self.position = {symbol: {'base_amount': 0, 'quote_amount': config['initial_balance']} for symbol in self.symbols}
        self.trade_history = {symbol: [] for symbol in self.symbols}
        self.price_history = {symbol: [] for symbol in self.symbols}
        self.portfolio_value_history = {symbol: [] for symbol in self.symbols}
        self.daily_loss_limit = config['daily_loss_limit']
        self.overall_loss_limit = config['overall_loss_limit']
        self.start_balance = config['initial_balance']

    async def fetch_price(self, symbol):
        ticker = await self.exchange.fetch_ticker(symbol)
        price = ticker['last']
        self.price_history[symbol].append(price)
        if len(self.price_history[symbol]) > self.config['rolling_window']:
            self.price_history[symbol] = self.price_history[symbol][-self.config['rolling_window']:]
        return price

    def calculate_delta_gamma(self, prices):
        returns = np.diff(prices) / prices[:-1]
        delta = np.mean(returns)
        gamma = np.std(returns)
        return delta, gamma

    def calculate_volatility(self, prices):
        returns = np.diff(prices) / prices[:-1]
        model = arch_model(returns, vol='Garch', p=1, q=1)
        model_fit = model.fit(disp='off')
        forecast = model_fit.forecast(horizon=1)
        return forecast.variance.values[-1, :][0]

    def risk_management(self, symbol, current_price):
        current_value = self.calculate_portfolio_value(symbol, current_price)
        daily_loss = (self.start_balance - current_value) / self.start_balance * 100
        if daily_loss > self.daily_loss_limit:
            logging.warning(f"Daily loss limit exceeded for {symbol}: {daily_loss:.2f}%")
            return False
        overall_loss = (self.start_balance - current_value) / self.start_balance * 100
        if overall_loss > self.overall_loss_limit:
            logging.warning(f"Overall loss limit exceeded for {symbol}: {overall_loss:.2f}%")
            return False
        return True

    def calculate_portfolio_value(self, symbol, current_price):
        return self.position[symbol]['quote_amount'] + (self.position[symbol]['base_amount'] * current_price)

    async def execute_trade(self, symbol, signal, price):
        if not self.risk_management(symbol, price):
            return
        position_size = self.config['trade_amount']
        if signal == 'buy' and self.position[symbol]['base_amount'] == 0:
            cost = position_size * price
            if cost <= self.position[symbol]['quote_amount']:
                self.position[symbol]['base_amount'] = position_size
                self.position[symbol]['quote_amount'] -= cost
                self.log_trade(symbol, 'buy', price, position_size)
        elif signal == 'sell' and self.position[symbol]['base_amount'] > 0:
            gained = self.position[symbol]['base_amount'] * price
            self.position[symbol]['quote_amount'] += gained
            self.position[symbol]['base_amount'] = 0
            self.log_trade(symbol, 'sell', price, self.position[symbol]['base_amount'])

    def log_trade(self, symbol, trade_type, price, amount):
        trade = {
            'timestamp': datetime.now().isoformat(),
            'type': trade_type,
            'price': price,
            'amount': amount,
            'quote_balance': self.position[symbol]['quote_amount'],
            'base_balance': self.position[symbol]['base_amount']
        }
        self.trade_history[symbol].append(trade)
        logging.info(f"Trade executed for {symbol}: {trade}")

    async def run(self):
        while True:
            try:
                for symbol in self.symbols:
                    price = await self.fetch_price(symbol)
                    delta, gamma = self.calculate_delta_gamma(self.price_history[symbol])
                    volatility = self.calculate_volatility(self.price_history[symbol])
                    logging.info(f"{symbol} - Price: {price}, Delta: {delta}, Gamma: {gamma}, Volatility: {volatility}")

                    # Example strategy logic
                    if delta > 0.01 and gamma < 0.02:
                        await self.execute_trade(symbol, 'buy', price)
                    elif delta < -0.01 and gamma < 0.02:
                        await self.execute_trade(symbol, 'sell', price)

                    current_portfolio = self.calculate_portfolio_value(symbol, price)
                    self.portfolio_value_history[symbol].append(current_portfolio)
                    pnl_percentage = ((current_portfolio - self.start_balance) / self.start_balance) * 100
                    logging.info(f"{symbol} - Portfolio: ${current_portfolio:.2f}, PnL: {pnl_percentage:+.2f}%")

                await asyncio.sleep(self.config['update_interval'])
            except Exception as e:
                logging.error(f"Error in main loop: {e}")
                await asyncio.sleep(self.config['update_interval'])

if __name__ == "__main__":
    config = {
        'apiKey': 'your_api_key_here',
        'apiSecret': 'your_api_secret_here',
        'initial_balance': 10000,
        'rolling_window': 100,
        'trade_amount': 1,
        'daily_loss_limit': 4.0,
        'overall_loss_limit': 10.0,
        'update_interval': 60
    }
    bot = PropFirmBot(config)
    asyncio.run(bot.run())
