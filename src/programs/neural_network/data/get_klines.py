import sys
import os
from dotenv import load_dotenv
load_dotenv()
root_path = os.getenv('ROOT_PATH')
os.environ['TZ'] = 'Europe/Moscow'
sys.path.append(root_path)

import time
import pandas as pd
from datetime import datetime, timedelta
from pybit.unified_trading import HTTP

from src.services import utils, config

time.tzset()

def get_klines(symbol, time_frame):
    client = HTTP(testnet=False)
    minutes = 365*24*60
    count_bars = minutes // 3
    
    count_requests = int(round(count_bars / 1000, 0))
    
    time_now = datetime.now()
    start_time = time_now - timedelta(minutes=minutes)
    end_time = start_time + timedelta(minutes=time_frame * 1000)
    kline_list = []
    for request_idx in range(count_requests):
        
        kline = utils.get_klines(client, symbol, time_frame, start_time, end_time)
        start_time += timedelta(minutes=time_frame*1000)
        end_time += timedelta(minutes=time_frame*1000)
        print(kline)
 
        kline_list.append(kline)
    data = pd.concat(kline_list)
    print(len(data))
    print(data.isna().sum())
    
    data.to_csv(f'{config.data_path}/data_{symbol}.csv', index=False)

get_klines('XMRUSDT', 3)