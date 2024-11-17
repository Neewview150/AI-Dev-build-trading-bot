import logging
import sys
from typing import Optional

def setup_logger() -> logging.Logger:
    logger = logging.getLogger('TradingBot')
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

def get_logger(name: Optional[str] = None) -> logging.Logger:
    return logging.getLogger(name if name else 'TradingBot')