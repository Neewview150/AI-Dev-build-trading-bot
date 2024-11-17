from typing import Dict

class RiskManagement:
    def __init__(self, config: Dict):
        self.risk_percentage = config.get('risk_percentage', 1.0)
        self.stop_loss_percentage = config.get('stop_loss_percentage', 2.0)
        self.take_profit_percentage = config.get('take_profit_percentage', 5.0)

    def calculate_position_size(self, balance: float, entry_price: float) -> float:
        """
        Calculate the position size based on the risk percentage and account balance.
        """
        risk_amount = balance * (self.risk_percentage / 100)
        position_size = risk_amount / entry_price
        return position_size

    def calculate_stop_loss(self, entry_price: float) -> float:
        """
        Calculate the stop-loss price based on the stop-loss percentage.
        """
        stop_loss_price = entry_price * (1 - self.stop_loss_percentage / 100)
        return stop_loss_price

    def calculate_take_profit(self, entry_price: float) -> float:
        """
        Calculate the take-profit price based on the take-profit percentage.
        """
        take_profit_price = entry_price * (1 + self.take_profit_percentage / 100)
        return take_profit_price
