import logging
import asyncio
import ccxt.async_support as ccxt
from typing import Dict, Tuple

class OrderExecution:
    def __init__(self, config: Dict):
        self.logger = logging.getLogger(__name__)
        self.exchange = ccxt.fbs({
            'apiKey': config['apiKey'],
            'secret': config['apiSecret'],
            'enableRateLimit': True,
        })
        self.max_order_size = config.get('max_order_size', 100)  # Maximum size for a single order
        self.symbol = config['trading_pairs'][0]  # Assuming single pair for simplicity

    async def execute_order(self, order_type: str, amount: float, price: float = None) -> None:
        """Execute an order with smart routing and order splitting."""
        try:
            if amount > self.max_order_size:
                await self.split_order(order_type, amount, price)
            else:
                await self.place_order(order_type, amount, price)
        except Exception as e:
            self.logger.error(f"Error executing order: {e}")

    async def place_order(self, order_type: str, amount: float, price: float = None) -> None:
        """Place a market or limit order."""
        try:
            if order_type == 'buy':
                if price:
                    order = await self.exchange.create_limit_buy_order(self.symbol, amount, price)
                else:
                    order = await self.exchange.create_market_buy_order(self.symbol, amount)
            elif order_type == 'sell':
                if price:
                    order = await self.exchange.create_limit_sell_order(self.symbol, amount, price)
                else:
                    order = await self.exchange.create_market_sell_order(self.symbol, amount)
            self.logger.info(f"Order placed: {order}")
        except Exception as e:
            self.logger.error(f"Error placing order: {e}")

    async def split_order(self, order_type: str, total_amount: float, price: float = None) -> None:
        """Split a large order into smaller chunks."""
        num_orders = int(total_amount // self.max_order_size)
        remainder = total_amount % self.max_order_size

        for _ in range(num_orders):
            await self.place_order(order_type, self.max_order_size, price)
            await asyncio.sleep(0.1)  # Small delay to avoid rate limits

        if remainder > 0:
            await self.place_order(order_type, remainder, price)

    async def modify_order(self, order_id: str, amount: float, price: float = None) -> None:
        """Modify an existing order."""
        try:
            order = await self.exchange.fetch_order(order_id, self.symbol)
            if order['status'] == 'open':
                await self.exchange.cancel_order(order_id, self.symbol)
                await self.place_order(order['side'], amount, price)
                self.logger.info(f"Order modified: {order_id}")
            else:
                self.logger.warning(f"Cannot modify order {order_id} as it is not open.")
        except Exception as e:
            self.logger.error(f"Error modifying order: {e}")

    async def cancel_order(self, order_id: str) -> None:
        """Cancel an existing order."""
        try:
            await self.exchange.cancel_order(order_id, self.symbol)
            self.logger.info(f"Order canceled: {order_id}")
        except Exception as e:
            self.logger.error(f"Error canceling order: {e}")

    async def close(self):
        """Close the exchange connection."""
        await self.exchange.close()

# Example usage
if __name__ == "__main__":
    config = {
        "apiKey": "your_fbs_api_key_here",
        "apiSecret": "your_fbs_api_secret_here",
        "trading_pairs": ["XAU/USD"],
        "max_order_size": 100
    }
    order_execution = OrderExecution(config)

    async def main():
        await order_execution.execute_order('buy', 250, 1800)
        # Example of modifying an order
        await order_execution.modify_order('order_id_example', 150, 1750)
        # Example of canceling an order
        await order_execution.cancel_order('order_id_example')
        await order_execution.close()

    asyncio.run(main())