from dataclasses import dataclass
from typing import List, Dict
import numpy as np

@dataclass
class GChannelResult:
    signal: str
    upper: List[float]
    lower: List[float]
    avg: List[float]

class GChannel:
    def __init__(self, length: int = 10):
        self.length = length

    def calculate(self, prices: np.ndarray) -> GChannelResult:
        upper = np.zeros_like(prices)
        lower = np.zeros_like(prices)
        
        upper[0] = lower[0] = prices[0]
        
        for i in range(1, len(prices)):
            upper[i] = max(prices[i], upper[i-1]) - (
                upper[i-1] - lower[i-1]
            ) / self.length
            
            lower[i] = min(prices[i], lower[i-1]) + (
                upper[i-1] - lower[i-1]
            ) / self.length
        
        avg = (upper + lower) / 2
        
        signal = 'hold'
        if len(prices) >= 2:
            if (lower[-2] < prices[-2] and lower[-1] > prices[-1]):
                signal = 'buy'
            elif (upper[-2] > prices[-2] and upper[-1] < prices[-1]):
                signal = 'sell'
        
        return GChannelResult(
            signal=signal,
            upper=upper.tolist(),
            lower=lower.tolist(),
            avg=avg.tolist()
        )