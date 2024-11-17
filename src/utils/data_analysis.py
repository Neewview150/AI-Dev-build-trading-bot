import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from ..strategies.strategy import AdvancedStrategy
from ..market_data.price_feed import PriceFeed
from ..portfolio.portfolio_manager import PortfolioManager
from ..utils.logger import get_logger

logger = get_logger(__name__)

def calculate_returns(prices: List[float]) -> np.ndarray:
    """Calculate the returns of a price series."""
    returns = np.diff(prices) / prices[:-1]
    return returns

def calculate_volatility(returns: np.ndarray) -> float:
    """Calculate the annualized volatility of returns."""
    return np.std(returns) * np.sqrt(252)  # Assuming daily returns

def backtest_strategy(
    historical_data: List[Dict],
    strategy: AdvancedStrategy,
    initial_balance: float = 10000
) -> Dict:
    """Backtest a trading strategy on historical data."""
    portfolio = PortfolioManager(initial_balance=initial_balance, risk_percentage=1.0)
    price_feed = PriceFeed({'initial_price': historical_data[0]['close'], 'history_size': len(historical_data)})
    price_feed.price_history = historical_data

    for candle in historical_data:
        current_price = candle['close']
        portfolio.update_value(current_price)
        
        signals = strategy.generate_signals(price_feed.get_historical_data())
        
        if signals.should_trade:
            position_size = portfolio.balance * (portfolio.risk_percentage / 100) / current_price
            
            if signals.action == 'buy' and not portfolio.has_position:
                portfolio.execute_buy(current_price, position_size)
            elif signals.action == 'sell' and portfolio.has_position:
                portfolio.execute_sell(current_price)
    
    final_value = portfolio.get_total_value(historical_data[-1]['close'])
    pnl_percentage = (final_value - initial_balance) / initial_balance * 100
    
    logger.info(f"Backtest completed. Final Portfolio Value: ${final_value:.2f}, PnL: {pnl_percentage:+.2f}%")
    
    return {
        'final_value': final_value,
        'pnl_percentage': pnl_percentage,
        'total_trades': portfolio.total_trades,
        'winning_trades': portfolio.winning_trades,
        'win_rate': portfolio.winning_trades / portfolio.total_trades * 100 if portfolio.total_trades > 0 else 0,
        'max_drawdown': portfolio.max_drawdown
    }

def calculate_technical_indicators(data: List[Dict], config: Dict) -> Dict:
    """Calculate various technical indicators for the given data."""
    prices = np.array([candle['close'] for candle in data])
    
    ema_indicator = EMAIndicator(config.get('ema_period', 20))
    rsi_indicator = RSIIndicator(config.get('rsi_period', 14))
    bb_indicator = BollingerBands(config.get('bb_period', 20))
    gchannel_indicator = GChannel(config.get('g_channel_length', 10))
    
    ema = ema_indicator.calculate(prices)
    rsi = rsi_indicator.calculate(prices)
    bb = bb_indicator.calculate(prices)
    gchannel = gchannel_indicator.calculate(prices)
    
    return {
        'ema': ema,
        'rsi': rsi,
        'bollinger_bands': bb,
        'g_channel': gchannel
    }
