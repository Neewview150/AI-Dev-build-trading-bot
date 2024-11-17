import logging
import sys
from typing import Optional

RATE_LIMIT_LEVEL = 25

def setup_logger() -> logging.Logger:
    logging.addLevelName(RATE_LIMIT_LEVEL, "RATE_LIMIT")
    logger = logging.getLogger('TradingBot')
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

def log_rate_limit(logger: logging.Logger, message: str) -> None:
    logger.log(RATE_LIMIT_LEVEL, message)

def get_logger(name: Optional[str] = None) -> logging.Logger:
    return logging.getLogger(name if name else 'TradingBot')