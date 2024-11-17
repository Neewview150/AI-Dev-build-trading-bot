# AI-Dev-build-trading-bot

## Introduction

The AI-Dev-build-trading-bot is an advanced trading bot designed to automate cryptocurrency trading using sophisticated strategies and risk management techniques. It integrates various technical indicators and strategies to make informed trading decisions.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Neewview150/AI-Dev-build-trading-bot.git
   cd AI-Dev-build-trading-bot
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The bot uses a configuration file `src/advanced_config.json` to set various parameters:
- `apiKey` and `apiSecret`: Your API credentials for accessing the exchange.
- `symbol`: The trading pair, e.g., "BTC/USDT".
- `initial_balance`: Starting balance for the simulation.
- `risk_percentage`: Percentage of balance to risk per trade.
- `stop_loss_percentage` and `take_profit_percentage`: Risk management settings.
- `max_open_trades`: Maximum number of concurrent trades.

## Usage

To run the trading bot, execute the following command:
```bash
python -m src.advanced_trading_bot
```

The bot will continuously fetch market data, generate trading signals, and execute trades based on the configured strategy.

## Features

- **Advanced Strategy Integration**: Combines multiple indicators like EMA, RSI, Bollinger Bands, and G-Channel for robust signal generation.
- **Risk Management**: Implements stop-loss and take-profit mechanisms to manage risk effectively.
- **Backtesting Capability**: Allows for historical data backtesting to evaluate strategy performance.

[Edit in StackBlitz next generation editor ⚡️](https://stackblitz.com/~/github.com/Neewview150/AI-Dev-build-trading-bot)
