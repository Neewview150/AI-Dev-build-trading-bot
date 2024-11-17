import random
import numpy as np
from typing import Dict, List
from datetime import datetime, timedelta

class PriceFeed:
    def __init__(self, config: Dict):
        self.base_price = config.get('initial_price', 2000)
        self.volatility = config.get('volatility', 0.002)
        self.trend = config.get('trend', 0)
        self.history_size = config.get('history_size', 100)
        self.price_history = []
        self._initialize_history()

    def _initialize_history(self) -> None:
        current_price = self.base_price
        for _ in range(self.history_size):
            current_price = self._generate_price(current_price)
            self.price_history.append({
                'timestamp': datetime.now() - timedelta(
                    minutes=self.history_size - len(self.price_history)
                ),
                'open': current_price,
                'high': current_price * (1 + random.uniform(0, self.volatility)),
                'low': current_price * (1 - random.uniform(0, self.volatility)),
                'close': current_price,
                'volume': random.uniform(100, 1000)
            })

    def _generate_price(self, last_price: float) -> float:
        change = np.random.normal(self.trend, self.volatility)
        return last_price * (1 + change)

    def get_latest_price(self) -> float:
        new_price = self._generate_price(self.price_history[-1]['close'])
        
        candle = {
            'timestamp': datetime.now(),
            'open': self.price_history[-1]['close'],
            'high': max(new_price, self.price_history[-1]['close']),
            'low': min(new_price, self.price_history[-1]['close']),
            'close': new_price,
            'volume': random.uniform(100, 1000)
        }
        
        self.price_history.append(candle)
        if len(self.price_history) > self.history_size:
            self.price_history.pop(0)
            
        return new_price

    def get_historical_data(self) -> List[Dict]:
        return self.price_history.copy()