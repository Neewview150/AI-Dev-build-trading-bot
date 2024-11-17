from .core.engine import TradingEngine
from .core.config import load_config
from .utils.logger import setup_logger

def main():
    logger = setup_logger()
    config = load_config()
    
    engine = TradingEngine(config)
    engine.run()

if __name__ == "__main__":
    main()