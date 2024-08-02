import os
import time
import requests

from io import StringIO
from decimal import Decimal

import pandas as pd

import models
import client
import config

DB_HOST = config.get("DOMAIN")


def get_lock():
    from filelock import FileLock
    lock = FileLock(models.db_lock)
    return lock


def reset_db():
    is_telegram_init = os.path.exists(models.telegram_chat_id_file)
    is_account_init = os.path.exists(models.account_file)
    is_positions_init = os.path.exists(models.positions_file)

    if not is_account_init or not is_telegram_init or not is_positions_init:
        Telegram = pd.DataFrame(columns=models.telegram_columns)
        Telegram.to_csv(models.telegram_chat_id_file, index=False)

        Position = pd.DataFrame(columns=models.telegram_columns)
        Position.to_csv(models.positions_file, index=False)

        Account = pd.DataFrame(columns=models.telegram_columns)
        Account.to_csv(models.account_file, index=False)

    Account = pd.DataFrame(columns=models.account_columns)
    balance = client.get_account()['result']['list'][0]['coin'][0]['walletBalance']
    account_data = {
        "balance": balance,
        "start_balance": balance,
        "total_profit_in_percent": "0",
        "total_profit_in_dollars": "0",
        "count_profit_positions": "0",
        "count_loss_positions": "0",
        "count_active_positions": "0",
        "count_closed_positions": "0"
    }
    Account.loc[len(Account)] = account_data
    Account.to_csv(models.account_file, index=False)

    Position = pd.DataFrame(columns=models.position_columns)
    Position.to_csv(models.positions_file, index=False)


def get_account(remote=False):
    try:
        if remote:
            response = requests.get(
                f'{DB_HOST}/db/get_account'
            )
            Account = pd.read_csv(StringIO(response.text))
        else:
            Account = pd.read_csv(models.account_file)
        return Account.astype(str)
    except:
        time.sleep(0.2)
        get_account(remote=remote)


def get_positions(remote=False, symbol=None, state=None):
    try:

        if remote:
            response = requests.get(
                f'{DB_HOST}/db/get_positions'
            )
            Position = pd.read_csv(StringIO(response.text))
        else:
            Position = pd.read_csv(models.positions_file)

        if not Position.empty:
            if symbol:
                Position = Position[Position['symbol'] == symbol]

            if state == 'open_position':
                Position = Position[Position['close_time'].isnull()]

            if state == 'limit':
                Position = Position[Position['take_price'].isnull()]

            if state == 'close':
                Position = Position[Position['close_price'] > 0]

            if state == 'without_stop':
                Position = Position[Position['stop_price'] == 0]

            if state == 'active':
                Position = Position[(Position['take_price'] > 0) & (Position['close_time'].isnull())]

        return Position.astype(str)
    except:
        time.sleep(0.2)
        return get_positions(remote=remote, symbol=symbol, state=state)


def get_balance(account):
    return account['balance']


def update_account(account, account_data, remote=False):
    if remote:
        account_csv = {
            "account_csv": ('account.csv', account.to_csv(index=True), 'text/csv')
        }

        response = requests.post(
            f'{DB_HOST}/db/update_account',
            data=account_data,
            files=account_csv
        )

        account = pd.read_csv(StringIO(response.text), dtype=str)
    else:
        Account = get_account()

        for column in account_data:
            value = get_value(account, column)
            account[column].iloc[0] = str(value + Decimal(str(account_data[column])))

            Account.update(account)
            Account.to_csv(models.account_file, index=False)

    return account


def set_position(position_data, symbol, remote=False):
    Position = get_positions()

    for column in position_data:
        position_data[column] = str(position_data[column])

    Position.loc[len(Position)] = position_data
    position = Position[(Position['symbol'] == symbol) & (Position['close_time'].isnull())]

    Position.to_csv(models.positions_file, index=False)
    return position


def update_position(position, position_data, remote=False):
    if remote:
        position_csv = {
            "position_csv": ('position.csv', position.to_csv(index=True), 'text/csv')
        }

        response = requests.post(
            f'{models}/db/update_position',
            data=position_data,
            files=position_csv
        )

        position = pd.read_csv(StringIO(response.text), dtype=str)
    else:
        Position = get_positions()
        position_idx = position.index[0]
        position = Position.loc[[position_idx]]

        for column in position_data:
            position[column].iloc[0] = str(position_data[column])
            Position.update(position)
            Position.to_csv(models.positions_file, index=False)

    return position


def get_telegram():
    Telegram = pd.read_csv(models.telegram_chat_id_file)
    return Telegram


def set_telegram_chat(Telegram, chat_data):
    Telegram.loc[len(Telegram)] = chat_data
    Telegram.to_csv(models.telegram_chat_id_file, index=False)


def get_value(df, column):
    value = df[column].iloc[0]
    if value == 'nan':
        return None

    if column in ['open_time', 'update_time', 'time_to_set_stop', "time_to_cancel_order"]:
        return int(value)

    if column in models.int_columns:
        return Decimal(value).normalize()

    if column in models.decimal_columns:
        return Decimal(value).normalize()

    if column in models.str_columns:
        return str(value)

    return value
