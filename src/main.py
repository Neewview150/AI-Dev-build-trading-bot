from .core.engine import TradingEngine
from .core.config import load_config
from .utils.logger import setup_logger
from .new_chat import ChatHandler
import sys

def main():
    logger = setup_logger()
    config = load_config()
    
    if len(sys.argv) > 1 and sys.argv[1] == 'chat':
        chat_handler = ChatHandler()
        chat_handler.run()
    else:
        engine = TradingEngine(config)
        engine.run()

if __name__ == "__main__":
    main()