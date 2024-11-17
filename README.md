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
- `trailing_stop_loss_percentage`: Percentage for trailing stop-loss to protect profits.

## Usage

To run the trading bot, execute the following command:
```bash
python -m src.advanced_trading_bot
```

The bot will continuously fetch market data, generate trading signals, and execute trades based on the configured strategy.

## Features

- **Advanced Strategy Integration**: Combines multiple indicators like EMA, RSI, Bollinger Bands, and G-Channel for robust signal generation.
- **Risk Management**: Implements stop-loss, take-profit, and trailing stop-loss mechanisms to manage risk effectively.
- **Backtesting Capability**: Allows for historical data backtesting to evaluate strategy performance.

[Edit in StackBlitz next generation editor ⚡️](https://stackblitz.com/~/github.com/Neewview150/AI-Dev-build-trading-bot)

## Chat Feature

The chat feature allows real-time communication using WebSockets. It is designed to facilitate interaction between users and the trading bot.

### Configuration

The chat feature uses a configuration file `src/chat_config.json` to set various parameters:
- `server_address`: The WebSocket server address.
- `port`: The port on which the chat server will run.

### Usage

To run the chat server, execute the following command:
```bash
python -m src.new_chat
```

To interact with the chat feature, connect to the WebSocket server using a WebSocket client and send messages. The server will log incoming and outgoing messages.

## High-Frequency Hedging Bot

The High-Frequency Hedging Bot is designed to execute trades at high frequency, capitalizing on price fluctuations in gold and EUR/USD pairs. It adheres to prop firm rules by enforcing strict loss limits and dynamically rebalancing the portfolio based on delta and gamma calculations.

### Features

- **Delta and Gamma Monitoring**: Continuously calculates delta and gamma to dynamically rebalance the portfolio.
- **Volatility Forecasting**: Utilizes GARCH models to predict changes in volatility.
- **Smart Order Execution**: Implements smart order routing and order splitting to minimize market impact.
- **Risk Management**: Enforces daily and overall loss limits as per prop firm rules.

### Configuration

The bot uses a configuration file `src/hedging_bot_config.json` to set various parameters:
- `apiKey` and `apiSecret`: Your API credentials for accessing the FBS broker.
- `trading_pairs`: The pairs to trade, e.g., "XAU/USD" and "EUR/USD".
- `risk_management`: Settings for daily and overall loss limits.
- `delta_gamma`: Parameters for delta and gamma calculations.
- `volatility_forecasting`: Parameters for the GARCH model.

### Usage

To run the high-frequency hedging bot, execute the following command:
```bash
python high_frequency_hedging_bot.py
```

The bot will continuously fetch market data, calculate delta and gamma, forecast volatility, and execute trades based on the configured strategy.

## High-Frequency Hedging Bot

The High-Frequency Hedging Bot is designed to execute trades at high frequency, capitalizing on price fluctuations in gold and EUR/USD pairs. It adheres to prop firm rules by enforcing strict loss limits and dynamically rebalancing the portfolio based on delta and gamma calculations.

### Features

- **Delta and Gamma Monitoring**: Continuously calculates delta and gamma to dynamically rebalance the portfolio.
- **Volatility Forecasting**: Utilizes GARCH models to predict changes in volatility.
- **Smart Order Execution**: Implements smart order routing and order splitting to minimize market impact.
- **Risk Management**: Enforces daily and overall loss limits as per prop firm rules.

### Configuration

The bot uses a configuration file `src/hedging_bot_config.json` to set various parameters:
- `apiKey` and `apiSecret`: Your API credentials for accessing the FBS broker.
- `trading_pairs`: The pairs to trade, e.g., "XAU/USD" and "EUR/USD".
- `risk_management`: Settings for daily and overall loss limits.
- `delta_gamma`: Parameters for delta and gamma calculations.
- `volatility_forecasting`: Parameters for the GARCH model.

### Usage

To run the high-frequency hedging bot, execute the following command:
```bash
python high_frequency_hedging_bot.py
```

The bot will continuously fetch market data, calculate delta and gamma, forecast volatility, and execute trades based on the configured strategy.