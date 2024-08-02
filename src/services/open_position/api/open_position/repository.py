from db import interface as db


def get_lock():
    return db.get_lock()


def get_value(df, column_name):
    return db.get_value(df, column_name)


def get_positions(symbol, state):
    return db.get_positions(symbol=symbol, state=state)


def get_account():
    return db.get_account()


def update_position(position, position_data):
    return db.update_position(position, position_data)


def set_position(position_data, symbol):
    return db.set_position(position_data, symbol)
