import time
from datetime import datetime
from decimal import Decimal

import config
import repository
from telegram import telegram_requests
from logger import logger

MAX_LOSS = config.get("MAX_LOSS")


def open_position(
        lock,
        client,

        symbol,
        size,
        position_side,
        time_frame,
        leverage,

        stop_in_percent,
        take_in_percent,

        interval_stop_in_percent,
        step_move_stop_in_percent,
        part_from_potential_profit,
        max_count_trail_take,

        limit_depth,
        time_to_cancel_order,
        time_to_set_stop
):
    open_price = client.get_open_price(client, symbol, position_side, limit_depth)

    account = repository.get_account()
    total_profit_in_percent = repository.get_value(account, 'total_profit_in_percent').quantize(Decimal('0.001'))

    # Максимальная просадка на аккаунте
    if total_profit_in_percent < Decimal(MAX_LOSS):
        res = "Максимальная просадка"
        logger.info(res)
        # В потоке запустить надо
        telegram_requests.text_alert(res)
        return res

    # Открытые позиции в базе данных
    position_db = repository.get_positions(symbol=symbol, state='open_position')

    # Если в базе есть записи
    if not position_db.empty:
        position_side_db = repository.get_value(position_db, 'position_side')

        # Если данные в базе не равны данным из сигнала
        if position_side_db != position_side:
            is_position_active = repository.get_value(position_db, 'take_price')

            # Если позиция не активна
            if not is_position_active:
                res = "Сигнал проигнорирован"
                logger.info(res)
                # В потоке запустить надо
                telegram_requests.text_alert(res)
                return res

    if position_db.empty:
        logger.info("Нет открытых лимиток")
        limit_order_size = 0
    else:
        logger.info("Есть открытая лимитка")
        limit_order_size = repository.get_value(position_db, 'limit_order_size')

    if limit_order_size:
        logger.info("Есть открытая лимитка")

        size = Decimal(size) + limit_order_size
        balance = repository.get_value(account, 'balance')

        if balance < open_price * size:
            res = "Недостаточно средств"
            logger.info(res)
            # В потоке запустить надо
            telegram_requests.text_alert(res)
            return res

        is_position_active = bool(float(client.get_position(client, symbol=symbol)["size"]))
        if not is_position_active:
            open_time = int(datetime.now().timestamp())
            position_data = {
                "open_price": open_price,
                "size": size,
                "limit_order_size": limit_order_size,
                "open_time": open_time,
                "order_id": open_time
            }

            client.open_features_order(
                client,
                symbol,
                size,
                open_price,
                position_side,
                leverage,
                'Limit',
                order_id=open_time
            )
            position_db = repository.update_position(position_db, position_data)

            res = "Позиция не открыта, переоткрыли лимитку"
            logger.info(res)
            telegram_requests.text_alert(res)
            return res

        open_time = int(datetime.now().timestamp())
        position_data = {
            "purchased_price": open_price,
            "limit_order_size": limit_order_size,
            "order_id": open_time
        }

        client.open_features_order(
            client,
            symbol,
            size,
            open_price,
            position_side,
            leverage,
            'Limit',
            order_id=open_time
        )
        position_db = repository.update_position(position_db, position_data)

        res = "Позиция уже открыта, висела лимитка и мы ее переоткрыли"
        logger.info(res)
        telegram_requests.text_alert(res)
        return res

    if not limit_order_size:
        logger.info("Нет открытых лимиток")
        open_time = int(datetime.now().timestamp())

        if position_db.empty:
            position_data = {
                "symbol": symbol,
                "position_side": position_side,
                "take_in_percent": take_in_percent,
                "stop_in_percent": stop_in_percent,
                "size": size,
                "open_time": open_time,
                "update_time": open_time,
                "limit_order_size": size,
                "open_price": open_price,
                "leverage": leverage,
                "time_frame": time_frame,
                "count_trail_stop": '0',
                "count_trail_take": '0',
                'interval_stop_in_percent': interval_stop_in_percent,
                'step_move_stop_in_percent': step_move_stop_in_percent,
                'part_from_potential_profit': part_from_potential_profit,
                "order_id": open_time,
                "max_count_trail_take": max_count_trail_take,
                "time_to_set_stop": time_to_set_stop,
                "time_to_cancel_order": time_to_cancel_order
            }
            client.open_features_order(
                client,
                symbol,
                size,
                open_price,
                position_side,
                leverage, 'Limit',
                order_id=open_time
            )
            position_db = repository.set_position(position_data, symbol)

            res = "Пришел сигнал, открыли лимитку"
            logger.info(res)
            telegram_requests.text_alert(res)
            return res

        position_side_db = repository.get_value(position_db, 'position_side')
        balance = repository.get_value(account, 'balance')
        if balance < open_price * size / leverage and position_side_db == position_side:
            res = "Недостаточно средств"
            logger.info(res)
            telegram_requests.text_alert(res)
            return res

        position_data = {
            "purchased_price": open_price,
            "limit_order_size": size,
            "order_id": open_time
        }
        client.open_features_order(
            client,
            symbol,
            size,
            open_price,
            position_side,
            leverage,
            'Limit',
            order_id=open_time
        )
        position_db = repository.update_position(position_db, position_data)

        res = "Добираем позицию"
        logger.info(res)
        telegram_requests.text_alert(res)
        return res
