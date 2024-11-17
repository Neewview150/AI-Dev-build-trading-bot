from typing import Dict

class RiskManagement:
    def __init__(self, config: Dict):
        self.risk_percentage = config.get('risk_percentage', 1.0)
        self.stop_loss_percentage = config.get('stop_loss_percentage', 2.0)
        self.take_profit_percentage = config.get('take_profit_percentage', 5.0)
        self.daily_loss_limit_percentage = config['risk_management']['daily_loss_limit_percentage']
        self.overall_loss_limit_percentage = config['risk_management']['overall_loss_limit_percentage']
        self.transaction_costs = config.get('transaction_costs', 0.1)
        self.slippage = config.get('slippage', 0.05)
        self.liquidity_threshold = config.get('liquidity_threshold', 1000)
        self.initial_balance = config.get('initial_balance', 10000)
        self.daily_loss = 0.0
        self.total_loss = 0.0

    def calculate_position_size(self, balance: float, entry_price: float) -> float:
        """
        Calculate the position size based on the risk percentage and account balance.
        Adjust for transaction costs and slippage.
        """
        risk_amount = balance * (self.risk_percentage / 100)
        adjusted_risk_amount = risk_amount * (1 - self.transaction_costs / 100) * (1 - self.slippage / 100)
        position_size = adjusted_risk_amount / entry_price
        return position_size

    def calculate_stop_loss(self, entry_price: float) -> float:
        """
        Calculate the stop-loss price based on the stop-loss percentage.
        """
        stop_loss_price = entry_price * (1 - self.stop_loss_percentage / 100)
        return stop_loss_price

    def enforce_loss_limits(self, current_portfolio_value: float) -> bool:
        """
        Enforce daily and overall loss limits.
        Returns True if trading should continue, False if limits are breached.
        """
        self.daily_loss = max(0, self.initial_balance - current_portfolio_value)
        self.total_loss += self.daily_loss

        daily_loss_limit = self.initial_balance * (self.daily_loss_limit_percentage / 100)
        overall_loss_limit = self.initial_balance * (self.overall_loss_limit_percentage / 100)

        if self.daily_loss > daily_loss_limit or self.total_loss > overall_loss_limit:
            return False
        return True

    def calculate_take_profit(self, entry_price: float) -> float:
        """
        Calculate the take-profit price based on the take-profit percentage.
        """
        take_profit_price = entry_price * (1 + self.take_profit_percentage / 100)
        return take_profit_price