from dataclasses import dataclass
from typing import List, Dict
import numpy as np
from ..indicators.trend import EMAIndicator
from ..indicators.momentum import RSIIndicator
from ..indicators.volatility import BollingerBands
from ..indicators.custom import GChannel

@dataclass
class SignalResult:
    action: str
    should_trade: bool
    risk_score: float
    confidence: float

class CombinedStrategy:
    def __init__(self, config: Dict):
        self.ema = EMAIndicator(config.get('ema_period', 20))
        self.rsi = RSIIndicator(config.get('rsi_period', 14))
        self.bbands = BollingerBands(config.get('bb_period', 20))
        self.gchannel = GChannel(config.get('g_channel_length', 10))
        
        self.rsi_oversold = config.get('rsi_oversold', 30)
        self.rsi_overbought = config.get('rsi_overbought', 70)
        self.min_confidence = config.get('min_confidence', 0.7)

    def generate_signals(self, data: List[Dict]) -> SignalResult:
        prices = np.array([candle['close'] for candle in data])
        
        ema_signal = self.ema.calculate(prices)
        rsi_value = self.rsi.calculate(prices)
        bb_signal = self.bbands.calculate(prices)
        gchannel_signal = self.gchannel.calculate(prices)
        
        # Trend analysis
        trend_direction = 1 if prices[-1] > ema_signal[-1] else -1
        
        # Momentum check
        momentum_signal = (
            1 if rsi_value[-1] < self.rsi_oversold else
            -1 if rsi_value[-1] > self.rsi_overbought else
            0
        )
        
        # Volatility assessment
        in_bb_range = bb_signal.lower[-1] < prices[-1] < bb_signal.upper[-1]
        
        # Combined signal calculation
        signal_strength = (
            trend_direction +
            momentum_signal +
            (1 if gchannel_signal.signal == 'buy' else
             -1 if gchannel_signal.signal == 'sell' else 0)
        ) / 3
        
        confidence = abs(signal_strength)
        should_trade = confidence >= self.min_confidence and not in_bb_range
        
        action = (
            'buy' if signal_strength > 0 else
            'sell' if signal_strength < 0 else
            'hold'
        )
        
        risk_score = self._calculate_risk_score(
            confidence,
            rsi_value[-1],
            bb_signal,
            prices[-1]
        )
        
        return SignalResult(
            action=action,
            should_trade=should_trade,
            risk_score=risk_score,
            confidence=confidence
        )

    def _calculate_risk_score(
        self,
        confidence: float,
        rsi: float,
        bb_signal: Dict,
        current_price: float
    ) -> float:
        # Risk score between 0 (highest risk) and 1 (lowest risk)
        volatility_risk = abs(current_price - bb_signal.middle[-1]) / (
            bb_signal.upper[-1] - bb_signal.middle[-1]
        )
        
        rsi_risk = abs(50 - rsi) / 50
        
        return (1 - volatility_risk) * confidence * (1 - rsi_risk)