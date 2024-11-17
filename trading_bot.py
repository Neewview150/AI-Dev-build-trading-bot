import json
import time
import logging
from datetime import datetime
import ccxt
from typing import Dict, List, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

class PoloniexPriceFetcher:
    def __init__(self):
        self.exchange = ccxt.poloniex({
            'enableRateLimit': True,
        })

    def get_price(self) -> float:
        """Fetch real-time price from Poloniex"""
        ticker = self.exchange.fetch_ticker('ETH/USDT')
        return ticker['last']

class TradingBot:
    def __init__(self):
        self.position = {'base_amount': 0, 'quote_amount': 10}  # Starting with 10 USDT
        self.trade_history = []
        self.price_history = []
        self.price_fetcher = PoloniexPriceFetcher()
        self.ema_period = 200
        self.g_channel_length = 10
        self.trade_amount = 2

    def fetch_price(self) -> float:
        """Fetch real-time price"""
        price = self.price_fetcher.get_price()
        self.price_history.append(price)
        if len(self.price_history) > self.ema_period:
            self.price_history = self.price_history[-self.ema_period:]
        return price

    def calculate_ema(self) -> float:
        """Calculate EMA using price history"""
        if len(self.price_history) < 2:
            return self.price_history[0] if self.price_history else None
            
        multiplier = 2 / (self.ema_period + 1)
        ema = self.price_history[0]
        
        for price in self.price_history[1:]:
            ema = (price - ema) * multiplier + ema
            
        return ema

    def calculate_g_channel(self) -> Tuple[str, float]:
        """Calculate G-Channel signal using price history"""
        if len(self.price_history) < self.g_channel_length:
            return 'hold', None

        prices = self.price_history[-self.g_channel_length:]
        a = prices[0]
        b = prices[0]
        
        for price in prices[1:]:
            a = max(price, a) - (a - b) / self.g_channel_length
            b = min(price, b) + (a - b) / self.g_channel_length

        avg = (a + b) / 2
        current_price = prices[-1]
        prev_price = prices[-2]

        if b < prev_price and b > current_price:
            return 'buy', avg
        elif a > prev_price and a < current_price:
            return 'sell', avg
        return 'hold', avg

    def simulate_trade(self, signal: str, price: float) -> None:
        """Simulate trade execution"""
        try:
            if signal == 'buy' and self.position['base_amount'] == 0:
                amount = self.trade_amount / price
                cost = amount * price
                
                if cost <= self.position['quote_amount']:
                    self.position['base_amount'] = amount
                    self.position['quote_amount'] -= cost
                    self.log_trade('buy', price, amount)
                    
            elif signal == 'sell' and self.position['base_amount'] > 0:
                gained = self.position['base_amount'] * price
                self.position['quote_amount'] += gained
                self.position['base_amount'] = 0
                self.log_trade('sell', price, self.position['base_amount'])
                
        except Exception as e:
            logging.error(f"Error simulating trade: {e}")

    def log_trade(self, trade_type: str, price: float, amount: float) -> None:
        """Log trade to history"""
        trade = {
            'timestamp': datetime.now().isoformat(),
            'type': trade_type,
            'price': price,
            'amount': amount,
            'quote_balance': self.position['quote_amount'],
            'base_balance': self.position['base_amount']
        }
        self.trade_history.append(trade)
        logging.info(f"Trade executed: {trade}")

    def calculate_portfolio_value(self, current_price: float) -> float:
        """Calculate total portfolio value in USDT"""
        return self.position['quote_amount'] + (self.position['base_amount'] * current_price)

    def run(self) -> None:
        """Main trading loop"""
        logging.info("Starting trading bot with real-time data...")
        initial_portfolio = self.calculate_portfolio_value(self.price_fetcher.get_price())
        
        while True:
            try:
                price = self.fetch_price()
                ema = self.calculate_ema()
                signal, g_channel_avg = self.calculate_g_channel()

                if ema is not None:
                    if signal == 'buy' and price < ema:
                        logging.info(f"Buy signal detected below EMA: {price} < {ema}")
                        self.simulate_trade('buy', price)
                    elif signal == 'sell' and price > ema:
                        logging.info(f"Sell signal detected above EMA: {price} > {ema}")
                        self.simulate_trade('sell', price)

                current_portfolio = self.calculate_portfolio_value(price)
                pnl_percentage = ((current_portfolio - initial_portfolio) / initial_portfolio) * 100

                logging.info(
                    f"Price: ${price:.2f} | Signal: {signal} | "
                    f"Portfolio: ${current_portfolio:.2f} | "
                    f"PnL: {pnl_percentage:+.2f}%"
                )
                
                time.sleep(1)  # Update every second in simulation
                
            except Exception as e:
                logging.error(f"Error in main loop: {e}")
                time.sleep(1)

if __name__ == "__main__":
    bot = TradingBot()
    bot.run()
