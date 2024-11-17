import time
from datetime import datetime
from .strategies.combined_strategy import CombinedStrategy
from .risk_management.position_sizer import PositionSizer
from .utils.logger import setup_logger
from .market_data.price_feed import PriceFeed
from .portfolio.portfolio_manager import PortfolioManager
from .config import load_config

class AdvancedTradingBot:
    def __init__(self):
        self.logger = setup_logger()
        self.config = load_config()
        
        self.price_feed = PriceFeed(self.config)
        self.portfolio = PortfolioManager(
            initial_balance=self.config.get('initial_balance', 10000),
            risk_percentage=self.config.get('risk_percentage', 1.0)
        )
        self.strategy = CombinedStrategy(self.config)
        self.position_sizer = PositionSizer(self.config)
        self.running = False
        self.last_update = None

    def fetch_market_data(self):
        current_price = self.price_feed.get_latest_price()
        self.portfolio.update_value(current_price)
        return current_price

    def generate_signals(self):
        historical_data = self.price_feed.get_historical_data()
        signals = self.strategy.generate_signals(historical_data)
        return signals

    def execute_trades(self, signals, current_price):
        if signals.should_trade:
            position_size = self.position_sizer.calculate_position_size(
                self.portfolio.get_balance(),
                current_price,
                signals.risk_score
            )
            
            if signals.action == 'buy' and not self.portfolio.has_position:
                self.portfolio.execute_buy(current_price, position_size)
            elif signals.action == 'sell' and self.portfolio.has_position:
                self.portfolio.execute_sell(current_price)

    def run(self):
        self.logger.info("Starting advanced trading bot...")
        self.running = True
        
        try:
            while self.running:
                current_price = self.fetch_market_data()
                signals = self.generate_signals()
                self.execute_trades(signals, current_price)
                self.log_status(current_price)
                time.sleep(self.config.get('update_interval', 60))
        except KeyboardInterrupt:
            self.logger.info("Shutting down trading bot...")
            self.running = False

    def log_status(self, current_price):
        status = self.portfolio.get_status()
        self.logger.info(
            f"Price: ${current_price:.2f} | "
            f"Portfolio: ${status['total_value']:.2f} | "
            f"PnL: {status['pnl_percentage']:+.2f}% | "
            f"Position: {status['position_type']}"
        )

if __name__ == "__main__":
    bot = AdvancedTradingBot()
    bot.run()
