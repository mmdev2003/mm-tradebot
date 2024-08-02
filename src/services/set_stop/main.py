import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv('ROOT_PATH'))

import time
from datetime import datetime

from src.services import utils
from src.services.database import db
from src.services.telegram import telegram_requests


def set_stop(client, position):
    size = db.get_value(position, 'size')
    symbol = db.get_value(position, 'symbol')
    leverage = db.get_value(position, 'leverage')
    open_price = db.get_value(position, 'open_price')
    position_side = db.get_value(position, 'position_side')
    stop_in_percent = db.get_value(position, 'clear_stop_in_percent')
    open_commission_in_dollars = db.get_value(position, 'open_commission_in_dollars')

    stop_price = utils.calculate_stop_price(client, symbol, open_price, stop_in_percent, position_side, size,
                                            open_commission_in_dollars)

    _, stop_in_percent = utils.calculate_take_and_stop_in_percent(open_price, 0, stop_price, position_side)

    potential_loss_in_percent, potential_loss_in_dollars, potential_loss_in_percent_from_account = utils.calculate_profit(
        symbol, open_price, stop_price, leverage, position_side, size, start_balance, open_commission_in_dollars)
    try:
        client.set_trading_stop(
            category="linear",
            symbol=symbol,
            stopLoss=str(stop_price),
            positionIdx=0
        )
        print('Выставили стоп')

        position_data = {
            "potential_loss_in_percent": potential_loss_in_percent,
            "potential_loss_in_dollars": potential_loss_in_dollars,
            "potential_loss_in_percent_from_account": potential_loss_in_percent_from_account,
            "stop_price": stop_price,
            "stop_in_percent": stop_in_percent
        }

        update_position = db.update_position(position, position_data)
        telegram_requests.set_stop(update_position)
    except Exception as e:
        print('Set stop: ', e.message)
        if position_side == 'Buy':
            position_side = 'Sell'
        else:
            position_side = 'Buy'
        if e.message != 'can not set tp/sl/ts for zero position':
            client.place_order(
                symbol=symbol,
                category='linear',
                side=position_side,
                orderType='Market',
                qty=str(size)
            )
            print('Закрыли позицию по маркету')
        else:
            pass
        update_position = db.update_position(position, {"stop_price": 1})


client = utils.client_init()
account = db.get_account()
start_balance = db.get_value(account, 'start_balance')
lock = db.get_db_lock()
time.sleep(20)
telegram_requests.text_alert('Бот перезапущен')

while True:
    with lock:
        positions = db.get_positions(state='without_stop')
        symbols = positions['symbol'].unique()
        if not positions.empty:
            for symbol in symbols:
                position = positions[positions['symbol'] == symbol]
                update_time = db.get_value(position, 'update_time')
                time_to_set_stop = int(str(db.get_value(position, 'time_to_set_stop')))
                time_to_set_stop = utils.get_time_to_set_stop(update_time, time_to_set_stop)
                time_now = datetime.now().timestamp()

                if time_to_set_stop - time_now < 0:
                    set_stop(client, position)
    print('запустились')
    time.sleep(20)
