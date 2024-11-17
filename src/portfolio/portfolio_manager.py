from dataclasses import dataclass
from typing import Dict, Optional
from ..utils.logger import get_logger

@dataclass
class Position:
    entry_price: float
    size: float
    timestamp: str

class PortfolioManager:
    def __init__(self, initial_balance: float, risk_percentage: float):
        self.logger = get_logger(__name__)
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.risk_percentage = risk_percentage
        self.current_position: Optional[Position] = None
        self.total_trades = 0
        self.winning_trades = 0
        self.total_pnl = 0
        self.peak_value = initial_balance
        self.max_drawdown = 0

    @property
    def has_position(self) -> bool:
        return self.current_position is not None

    def execute_buy(self, price: float, size: float) -> None:
        if self.has_position:
            self.logger.warning("Attempted to buy while position exists")
            return
            
        cost = price * size
        if cost > self.balance:
            self.logger.warning(
                f"Insufficient funds for trade: {cost} > {self.balance}"
            )
            return
            
        self.balance -= cost
        self.current_position = Position(
            entry_price=price,
            size=size,
            timestamp=str(datetime.now())
        )
        
        self.logger.info(
            f"Opened long position: {size} units at ${price:.2f}"
        )

    def execute_sell(self, price: float) -> None:
        if not self.has_position:
            self.logger.warning("Attempted to sell without position")
            return
            
        position = self.current_position
        self.current_position = None
        
        gained = position.size * price
        self.balance += gained
        
        pnl = gained - (position.size * position.entry_price)
        pnl_percentage = (pnl / (position.size * position.entry_price)) * 100
        
        self.total_trades += 1
        if pnl > 0:
            self.winning_trades += 1
        
        self.total_pnl += pnl
        
        self.logger.info(
            f"Closed position: PnL ${pnl:.2f} ({pnl_percentage:+.2f}%)"
        )

    def update_value(self, current_price: float) -> None:
        total_value = self.get_total_value(current_price)
        
        if total_value > self.peak_value:
            self.peak_value = total_value
        
        drawdown = (self.peak_value - total_value) / self.peak_value * 100
        self.max_drawdown = max(self.max_drawdown, drawdown)

    def get_total_value(self, current_price: float) -> float:
        position_value = (
            self.current_position.size * current_price
            if self.has_position
            else 0
        )
        return self.balance + position_value

    def get_status(self) -> Dict:
        current_value = self.get_total_value(current_price)
        
        return {
            'total_value': current_value,
            'balance': self.balance,
            'position_type': 'long' if self.has_position else 'none',
            'pnl_percentage': (
                (current_value - self.initial_balance) /
                self.initial_balance * 100
            ),
            'win_rate': (
                self.winning_trades / self.total_trades * 100
                if self.total_trades > 0
                else 0
            ),
            'max_drawdown': self.max_drawdown
        }