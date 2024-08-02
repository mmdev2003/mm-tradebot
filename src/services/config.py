import os
from decimal import Decimal

features_1_1 = ['high_change', 'low_change', 'close_change', 'ao', 'apo', 'bop', 'cci', 'cfo', 'cmo', 'coppock',
                'kst', 'kst_signal', 'pgo', 'pvo', 'pvo_hist', 'pvo_signal', 'rvgi', 'rvgi_signal', 'smi',
                'smi_signal', 'smi_osc', 'stoch_k', 'stoch_d', 'tsi', 'tsi_signal', 'qstick', 'cmf'],
features_0_1 = ['rsi', 'inertia', 'stoch_rsi_k', 'stoch_rsi_d', 'willr', 'adx', 'dmp', 'dmn', 'chop', 'vip', 'vim',
                'atr', 'massi', 'rvi', 'ui'],
features_for_train = ['high_change', 'low_change', 'close_change', 'ao', 'stoch_k', 'stoch_d', 'rsi', 'adx', 'dmp',
                      'dmn']

env = {
    # Neural Network
    "FEATURES_1_1": features_1_1,
    "FEATURES_0_1": features_0_1,
    "FEATURES": [features_1_1, features_0_1],
    "FEATURES_FOR_TRAIN": features_for_train,
    "TRAIN_DATA_PATH": os.getenv("TRAIN_DATA_PATH"),

    # Trade
    "MAKER": Decimal(os.getenv("MAKER")),
    "TAKER": Decimal(os.getenv("TAKER")),

    # Credentials
    "BOT_TOKEN": os.getenv("BOT_TOKEN"),
    "API_KEY": os.getenv("API_KEY"),
    "API_SECRET_KEY": os.getenv("API_SECRET_KEY"),

    # Ports
    "DB_PORT": os.getenv("DB_PORT"),
    "OPEN_POSITION_PORT": os.getenv("OPEN_POSITION_PORT"),

    # Domains
    "DOMAIN": os.getenv("DOMAIN"),

    # System
    "ROOT_PATH": os.getenv("ROOT_PATH"),
}


def get(key):
    return env[key]
