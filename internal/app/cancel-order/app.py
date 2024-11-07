import sys
import datetime

import time

sys.path.append("/root/service/src")

import utils
from src.services.database import db

client = utils.client_init()

while True:
    lock = db.get_db_lock()
    with lock:
        positions = db.get_positions(state='limit')

        if not positions.empty:
            symbols = positions['symbol'].unique()

            for symbol in symbols:
                position = positions[positions['symbol'] == symbol]

                time_frame = db.get_value(position, 'time_frame')
                open_time = db.get_value(position, 'open_time')
                time_to_cancel_order = db.get_value(position, 'time_to_cancel_order')
                time_to_cancel = utils.get_time_to_cancel(time_frame, open_time, time_to_cancel_order)
                time_now = datetime.now().timestamp()

                if time_to_cancel - time_now < 0:
                    positions = positions[(positions['close_time'].isnull()) & (positions['symbol'] != symbol)]
                    positions.to_csv(db.positions_file, index=False)
                    utils.cancel_all_orders(client, symbol)
                    print('Закрыли лимитку')
    print('Cancel order started!')
    time.sleep(20)