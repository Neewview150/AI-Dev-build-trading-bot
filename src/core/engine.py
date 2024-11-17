import time
from datetime import datetime
from typing import Dict, Optional
from ..strategies.combined_strategy import CombinedStrategy
from ..risk_management.position_sizer import PositionSizer
from ..utils.logger import get_logger
from ..market_data.price_feed import PriceFeed
from ..portfolio.portfolio_manager import PortfolioManager

class TradingEngine:
    def __init__(self, config: Dict):
        self.logger = get_logger(__name__)
        self.config = config
        self.price_feed = PriceFeed(config)
        self.portfolio = PortfolioManager(
            initial_balance=config.get('initial_balance', 10000),
            risk_percentage=config.get('risk_percentage', 1.0)
        )
        self.strategy = CombinedStrategy(config)
        self.position_sizer = PositionSizer(config)
        self.running = False
        self.last_update = None

    def update(self) -> None:
        try:
            current_price = self.price_feed.get_latest_price()
            self.portfolio.update_value(current_price)
            
            if self._should_update_signals():
                signals = self.strategy.generate_signals(
                    self.price_feed.get_historical_data()
                )
                
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
            
            self._log_status(current_price)
            
        except Exception as e:
            self.logger.error(f"Error in trading update: {e}", exc_info=True)

    def _should_update_signals(self) -> bool:
        now = datetime.now()
        if not self.last_update:
            self.last_update = now
            return True
            
        update_interval = self.config.get('update_interval', 60)
        should_update = (now - self.last_update).seconds >= update_interval
        
        if should_update:
            self.last_update = now
            
        return should_update

    def _log_status(self, current_price: float) -> None:
        status = self.portfolio.get_status()
        self.logger.info(
            f"Price: ${current_price:.2f} | "
            f"Portfolio: ${status['total_value']:.2f} | "
            f"PnL: {status['pnl_percentage']:+.2f}% | "
            f"Position: {status['position_type']}"
        )

    def run(self) -> None:
        self.logger.info("Starting trading engine...")
        self.running = True
        
        try:
            while self.running:
                self.update()
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Shutting down trading engine...")
            self.running = False