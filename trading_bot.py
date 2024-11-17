import json
import time
import logging
from datetime import datetime
import ccxt
import numpy as np
from typing import Dict, List, Tuple
from src.config import load_config
from src.indicators import calculateEMA, calculateGChannel
from src.risk_management import PositionSizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

class TradingBot:
    def __init__(self, mode='simulation'):
        self.config = load_config()
        self.mode = mode
        self.position = {'base_amount': 0, 'quote_amount': self.config['initial_balance']}
        self.trade_history = []
        self.price_history = []
        self.portfolio_value_history = []
        self.price_fetcher = ccxt.binance({
            'apiKey': self.config['apiKey'],
            'secret': self.config['apiSecret'],
            'enableRateLimit': True,
        })
        self.ema_period = self.config['ema_period']
        self.g_channel_length = self.config['g_channel_length']
        self.position_sizer = PositionSizer(self.config)

    def fetch_price(self) -> float:
        """Fetch real-time price"""
        ticker = self.price_fetcher.fetch_ticker(self.config['symbol'])
        price = ticker['last']
        self.price_history.append(price)
        if len(self.price_history) > self.ema_period:
            self.price_history = self.price_history[-self.ema_period:]
        return price

    def calculate_ema(self) -> float:
        """Calculate EMA using price history"""
        return calculateEMA(self.price_history, self.ema_period)

    def calculate_g_channel(self) -> Tuple[str, float]:
        """Calculate G-Channel signal using price history"""
        return calculateGChannel(self.price_history, self.g_channel_length)

    def execute_trade(self, signal: str, price: float) -> None:
        """Execute trade based on mode"""
        if self.mode == 'simulation':
            self.simulate_trade(signal, price)
        elif self.mode == 'real':
            self.real_trade(signal, price)

    def simulate_trade(self, signal: str, price: float) -> None:
        """Simulate trade execution"""
        try:
            position_size = self.position_sizer.calculate_position_size(
                self.position['quote_amount'], price, signal
            )
            if signal == 'buy' and self.position['base_amount'] == 0:
                cost = position_size * price
                if cost <= self.position['quote_amount']:
                    self.position['base_amount'] = position_size
                    self.position['quote_amount'] -= cost
                    self.log_trade('buy', price, position_size)
                    
            elif signal == 'sell' and self.position['base_amount'] > 0:
                gained = self.position['base_amount'] * price
                self.position['quote_amount'] += gained
                self.position['base_amount'] = 0
                self.log_trade('sell', price, self.position['base_amount'])
                
        except Exception as e:
            logging.error(f"Error simulating trade: {e}")

    def real_trade(self, signal: str, price: float) -> None:
        """Execute real trade using ccxt"""
        try:
            position_size = self.position_sizer.calculate_position_size(
                self.position['quote_amount'], price, signal
            )
            if signal == 'buy':
                order = self.exchange.create_market_buy_order(self.config['symbol'], position_size)
                self.log_trade('buy', price, position_size)
            elif signal == 'sell':
                order = self.exchange.create_market_sell_order(self.config['symbol'], position_size)
                self.log_trade('sell', price, position_size)
        except Exception as e:
            logging.error(f"Error executing real trade: {e}")

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

    def calculate_max_drawdown(self) -> float:
        """Calculate the maximum drawdown from the portfolio value history"""
        if not self.portfolio_value_history:
            return 0.0
        peak = self.portfolio_value_history[0]
        max_drawdown = 0.0
        for value in self.portfolio_value_history:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        return max_drawdown * 100
    def run(self) -> None:
        """Main trading loop"""
        logging.info("Starting trading bot with real-time data...")
        initial_portfolio = self.calculate_portfolio_value(self.fetch_price())
        
        while True:
            try:
                price = self.fetch_price()
                ema = self.calculate_ema()
                signal, g_channel_avg = self.calculate_g_channel()

                if ema is not None:
                    if signal == 'buy' and price < ema:
                        logging.info(f"Buy signal detected below EMA: {price} < {ema}")
                        self.execute_trade('buy', price)
                    elif signal == 'sell' and price > ema:
                        logging.info(f"Sell signal detected above EMA: {price} > {ema}")
                        self.execute_trade('sell', price)

                current_portfolio = self.calculate_portfolio_value(price)
                self.portfolio_value_history.append(current_portfolio)
                pnl_percentage = ((current_portfolio - initial_portfolio) / initial_portfolio) * 100
                max_drawdown = self.calculate_max_drawdown()

                logging.info(
                    f"Price: ${price:.2f} | Signal: {signal} | "
                    f"Portfolio: ${current_portfolio:.2f} | "
                    f"PnL: {pnl_percentage:+.2f}% | "
                    f"Max Drawdown: {max_drawdown:.2f}%"
                )
                
                time.sleep(self.config['update_interval'])  # Update based on config interval
                
            except Exception as e:
                logging.error(f"Error in main loop: {e}")
                time.sleep(self.config['update_interval'])

if __name__ == "__main__":
    bot = TradingBot(mode='simulation')  # Change to 'real' for real trading
    bot.run()
