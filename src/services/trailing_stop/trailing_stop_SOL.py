import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.getenv('ROOT_PATH'))

import pandas as pd
from filelock import Timeout
from pybit.unified_trading import WebSocket

from src.services.database import db
from src.services.trailing_stop.trailing_stop import trailing_stop


ws = WebSocket(
    testnet=False,
    channel_type="linear",
)
symbol = 'SOLUSDT'
position = {
        symbol: pd.DataFrame()
    }
lock = db.get_db_lock()
def trailing_stop_symbol():
    try:
        ws.trade_stream(symbol = symbol, callback = trailing_stop_handler_symbol)
        print('Открыли сокет по: ', symbol)
    
        while True:
            try:
                position_db = db.get_positions(remote=True, symbol=symbol, state='active')
            except Exception:
                continue
            if position_db.empty:
                position[symbol] = pd.DataFrame()
            else:
                position[symbol] = position_db.copy()
    except Exception as e:
        print('error: ', e)
        
        
def trailing_stop_handler_symbol(message):
    last_price = message['data'][0]['p']
    if not position[symbol].empty:
        try:
            with lock.acquire(timeout=0):
                lock.release()
                trailing_stop(position[symbol], last_price, lock)
        except Timeout:
            return False
        except Exception as e:
            print(f'{symbol}: ', e)
    
if __name__ == "__main__":
    trailing_stop_symbol()