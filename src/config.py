import json
from pathlib import Path
from typing import Dict

def load_config() -> Dict:
    config_path = Path(__file__).parent.parent / 'config.json'
    
    default_config = {
        'initial_balance': 10000,
        'risk_percentage': 1.0,
        'update_interval': 60,
        'ema_period': 20,
        'rsi_period': 14,
        'bb_period': 20,
        'g_channel_length': 10,
        'initial_price': 2000,
        'volatility': 0.002,
        'trend': 0,
        'history_size': 100,
        'min_confidence': 0.7,
        'rsi_oversold': 30,
        'rsi_overbought': 70
    }
    
    try:
        with open(config_path) as f:
            user_config = json.load(f)
            return {**default_config, **user_config}
    except FileNotFoundError:
        return default_config