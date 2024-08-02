import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv('ROOT_PATH'))

import time
from pybit.unified_trading import WebSocket

import threading
from datetime import datetime
from decimal import Decimal

from src.services import utils, config
from src.services.database import db
from src.services.telegram import telegram_requests


def handle_position(message):
    symbol, open_price, take_price, size, cum_profit_in_dollars, position_sum, mark_price = get_message_data(message)

    try:

        position = db.get_positions(symbol=symbol, state='open_position')
        account = db.get_account()

        if not position.empty:
            balance, start_balance, take_price_db, stop_price_db, take_in_percent, stop_in_percent, open_price_db, size_db, position_side, leverage = get_db_data(
                position, account)

            client = utils.client_init()

            if not take_price_db and size and not take_price:
                print('Открываем позицию')
                position_opened(client, position, account, symbol, balance, start_balance, open_price, open_price_db,
                                take_in_percent, stop_in_percent, position_side, size, leverage, position_sum)
                print('Открыли позицию')

            if take_price_db and size_db < size:
                print('Добираем позицию')
                purchased_position(client, position, account, symbol, balance, start_balance, open_price, open_price_db,
                                   take_price_db, stop_price_db, position_side, size, size_db, leverage, position_sum)
                print('Добрали позицию')

            if take_price_db and not size:
                print('Закрываем позицию')
                position_closed(client, position, account, balance, start_balance, symbol, open_price_db, take_price_db,
                                position_side, size_db, leverage, cum_profit_in_dollars, mark_price)
                print('Закрыли позицию')
    except:
        import traceback
        traceback.print_exc()


def get_message_data(message):

    print(message)

    symbol = message['data'][0]['symbol']
    size = Decimal(message['data'][0]['size']).normalize()
    open_price = Decimal(message['data'][0]['entryPrice']).normalize()
    take_price = Decimal(message['data'][0]['takeProfit']).normalize()
    cum_profit_in_dollars = Decimal(message['data'][0]['cumRealisedPnl'])
    mark_price = Decimal(message['data'][0]['markPrice'])
    position_sum = Decimal(message['data'][0]['positionBalance'])

    return symbol, open_price, take_price, size, cum_profit_in_dollars, position_sum, mark_price


def get_db_data(position, account):
    take_price_db = db.get_value(position, 'take_price')
    stop_price_db = db.get_value(position, 'stop_price')
    take_in_percent = db.get_value(position, 'take_in_percent')
    stop_in_percent = db.get_value(position, 'stop_in_percent')
    position_side = db.get_value(position, 'position_side')
    open_price_db = db.get_value(position, 'open_price')
    leverage = db.get_value(position, 'leverage')
    size_db = db.get_value(position, 'size')

    balance = db.get_value(account, 'balance')
    start_balance = db.get_value(account, 'start_balance')

    return balance, start_balance, take_price_db, stop_price_db, take_in_percent, stop_in_percent, open_price_db, size_db, position_side, leverage


def position_opened(client, position, account, symbol, balance, start_balance, open_price, open_price_db,
                    take_in_percent, stop_in_percent, position_side, size, leverage, position_sum):

    if open_price != open_price_db:
        open_commission_in_percent = config.taker
    else:
        open_commission_in_percent = config.maker

    clear_stop_in_percent = stop_in_percent
    clear_take_in_percent = take_in_percent

    open_commission_in_dollars = utils.calculate_commission(open_commission_in_percent, open_price, size)

    stop_price, take_price, take_in_percent = set_take(client, symbol, open_price, take_in_percent, position_side, size,
                                                       open_commission_in_dollars)

    take_in_percent, _ = utils.calculate_take_and_stop_in_percent(open_price, take_price, 0, position_side)

    potential_profit_in_percent, potential_profit_in_dollars, potential_profit_in_percent_from_account = utils.calculate_profit(
        symbol, open_price, take_price, leverage, position_side, size, start_balance, open_commission_in_dollars)

    price_change = -(position_sum)

    position_data = {
        "update_time": int(datetime.now().timestamp()),
        "open_price": open_price,
        "limit_order_size": 0,
        "take_price": take_price,
        "stop_price": stop_price,
        "take_in_percent": take_in_percent,
        "stop_in_percent": 0,
        "position_sum": position_sum,
        "clear_stop_in_percent": clear_stop_in_percent,
        "clear_take_in_percent": clear_take_in_percent,
        "open_commission_in_dollars": open_commission_in_dollars,
        "potential_profit_in_percent": potential_profit_in_percent,
        "potential_profit_in_dollars": potential_profit_in_dollars,
        "potential_profit_in_percent_from_account": potential_profit_in_percent_from_account,
        "potential_loss_in_percent": 0,
        "potential_loss_in_dollars": 0,
        "potential_loss_in_percent_from_account": 0,
        "prev_balance": balance,
        "current_balance": balance + price_change
    }
    account_data = {
        "count_active_positions": '1',
        "balance": price_change
    }

    db.update_account(account, account_data)
    update_position = db.update_position(position, position_data)
    thread = threading.Thread(target=telegram_requests.position_opened, args=(update_position,))
    thread.start()


def purchased_position(client, position, account, symbol, balance, start_balance, open_price, open_price_db,
                       take_price_db, stop_price_db, position_side, size, size_db, leverage, position_sum):
    open_commission_in_dollars = db.get_value(position, 'open_commission_in_dollars')
    take_in_percent = db.get_value(position, 'clear_take_in_percent')
    purchased_price_db = db.get_value(position, 'purchased_price')
    position_sum_db = db.get_value(position, 'position_sum')
    purchased_price, purchased_size = utils.calculate_purchased_price(client, symbol, size_db, size, open_price_db,
                                                                      open_price)

    if purchased_price != purchased_price_db:
        purchased_commission_in_percent = config.taker
    else:
        purchased_commission_in_percent = config.maker

    purchased_commission_in_dollars = utils.calculate_commission(purchased_commission_in_percent, purchased_price,
                                                                 purchased_size)

    open_commission_in_dollars += purchased_commission_in_dollars

    stop_price, take_price, take_in_percent = set_take(client, symbol, open_price, take_in_percent, position_side, size,
                                                       open_commission_in_dollars, take_price=take_price_db,
                                                       stop_price=stop_price_db)

    take_in_percent, _ = utils.calculate_take_and_stop_in_percent(open_price, take_price, 0, position_side)

    potential_profit_in_percent, potential_profit_in_dollars, potential_profit_in_percent_from_account = utils.calculate_profit(
        symbol, open_price, take_price, leverage, position_side, size, start_balance, open_commission_in_dollars)

    price_change = -(position_sum - position_sum_db)

    position_data = {
        "update_time": int(datetime.now().timestamp()),
        "open_price": open_price,
        "size": size,
        "limit_order_size": 0,
        "stop_price": stop_price,
        "take_price": take_price,
        "take_in_percent": take_in_percent,
        "stop_in_percent": 0,
        "count_trail_take": "0",
        "position_sum": position_sum,
        "open_commission_in_dollars": open_commission_in_dollars,
        "potential_profit_in_percent": potential_profit_in_percent,
        "potential_profit_in_dollars": potential_profit_in_dollars,
        "potential_profit_in_percent_from_account": potential_profit_in_percent_from_account,
        "potential_loss_in_percent": 0,
        "potential_loss_in_dollars": 0,
        "potential_loss_in_percent_from_account": 0,
        "prev_balance": balance,
        "current_balance": balance + price_change
    }
    account_data = {
        "balance": price_change
    }

    db.update_account(account, account_data)
    update_position = db.update_position(position, position_data)
    thread = threading.Thread(target=telegram_requests.purchased_position, args=(update_position,))
    thread.start()


def position_closed(client, position, account, balance, start_balance, symbol, open_price_db, take_price_db,
                    position_side, size_db, leverage, cum_profit_in_dollars, mark_price):
    utils.cancel_all_orders(client, symbol)

    position_sum = db.get_value(position, 'position_sum')
    profit_in_dollars = cum_profit_in_dollars - db.get_value(position, 'cum_profit_in_dollars')

    profit_in_percent = profit_in_dollars / position_sum * Decimal('100')
    profit_in_percent_from_account = profit_in_dollars / start_balance * Decimal('100')

    price_change = position_sum + profit_in_dollars

    account_data = {
        "count_active_positions": "-1",
        "count_closed_positions": "1",
        "total_profit_in_dollars": profit_in_dollars,
        "total_profit_in_percent": profit_in_percent_from_account,
        "balance": price_change
    }
    position_data = {
        "close_price": mark_price,
        "close_time": datetime.now().timestamp(),
        "limit_order_size": 0,
        "profit_in_dollars": profit_in_dollars,
        "profit_in_percent": profit_in_percent,
        "profit_in_percent_from_account": profit_in_percent_from_account,
        "prev_balance": balance,
        "current_balance": balance + price_change
    }

    if profit_in_percent >= Decimal('0'):
        account_data['count_profit_positions'] = "1"
    else:
        account_data['count_loss_positions'] = "1"

    db.update_account(account, account_data)
    update_position = db.update_position(position, position_data)
    thread = threading.Thread(target=telegram_requests.position_closed, args=(update_position,))
    thread.start()


def set_take(client, symbol, open_price, take_in_percent, position_side, size, open_commission_in_dollars,
             take_price=None, stop_price=None):
    try:
        take_price = utils.calculate_take_price(client, symbol, open_price, take_in_percent, position_side, size,
                                                open_commission_in_dollars)
        client.set_trading_stop(
            category="linear",
            symbol=symbol,
            takeProfit=str(take_price),
            stopLoss=str(0),
            positionIdx=0
        )
        stop_price = 0

    except Exception as e:
        print(e.message)

        if e.message != "can not set tp":
            take_in_percent += Decimal('0.15')

        take_price = utils.calculate_take_price(client, symbol, open_price, take_in_percent, position_side, size,
                                                open_commission_in_dollars)
        client.set_trading_stop(
            category="linear",
            symbol=symbol,
            takeProfit=str(take_price),
            positionIdx=0
        )

        stop_price = 0
    finally:
        return stop_price, take_price, take_in_percent


ws_position = WebSocket(
    testnet=False,
    channel_type='private',
    api_key=os.getenv('API_KEY'),
    api_secret=os.getenv('API_SECRET_KEY')
)


def check_account():
    try:
        print('Stream position')
        ws_position.position_stream(callback=callback_fn)

        while True:
            time.sleep(0.1)

    except Exception as e:
        print('error: ', e)


def callback_fn(message):
    lock = db.get_db_lock()
    with lock:
        handle_position(message)


if __name__ == "__main__":
    check_account()
