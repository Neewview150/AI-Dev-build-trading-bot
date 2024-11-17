import logging
from src.backtest import Backtester, load_historical_data
from src.config import load_config
from src.utils.logger import setup_logger

def main():
    # Setup logger
    logger = setup_logger()
    
    # Load configuration
    config = load_config()
    
    # Load historical data
    historical_data = load_historical_data('historical_data.csv')
    
    # Initialize Backtester
    backtester = Backtester(historical_data, config)
    
    # Run backtest
    backtester.run_backtest()
    
    # Log results
    logger.info("Backtest for propfirm.py completed.")

if __name__ == "__main__":
    main()
