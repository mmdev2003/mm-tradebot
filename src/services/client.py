import config
from pybit.unified_trading import HTTP
from decimal import Decimal

import calculation


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class BybitClient(metaclass=SingletonMeta):
    def __init__(self):
        api_key = config.get('API_KEY')
        api_secret_key = config.get('API_SECRET_KEY')
        self.client = HTTP(api_key=api_key, api_secret=api_secret_key)


def get_client():
    return BybitClient().client


def get_account():
    return BybitClient().client.get_wallet_balance(accountType='CONTRACT', coin='USDT')


def set_leverage(symbol, leverage):
    client = BybitClient().client

    current_leverage = get_position(client, symbol)['leverage']
    if Decimal(current_leverage) != leverage:
        return client.set_leverage(
            category='linear',
            symbol=symbol,
            buyLeverage=str(leverage),
            sellLeverage=str(leverage)
        )


def open_features_order(symbol, size, open_price, position_side, leverage, order_type, order_id=None):
    client = BybitClient().client
    set_leverage(client, symbol, leverage)

    if order_type == 'Limit':
        order = client.place_order(
            category='linear',
            symbol=symbol,
            side=position_side,
            orderType='Limit',
            price=str(open_price),
            qty=str(size),
            orderLinkId=str(order_id)
        )

    if order_type == 'Market':
        order = client.place_order(
            symbol=symbol,
            category='linear',
            side=position_side,
            orderType='Market',
            qty=str(size)
        )
    return order


def get_position(symbol=None, settle_coin=None):
    client = BybitClient().client
    position = None
    if symbol:
        position = client.get_positions(category='linear', symbol=symbol)['result']['list'][0]
    if settle_coin:
        position = client.get_positions(category='linear', settleCoin=settle_coin)['result']['list']
    return position


def get_price(symbol):
    client = BybitClient().client
    last_price = client.get_tickers(
        category='linear',
        symbol=symbol
    )['result']['list'][0]['lastPrice']
    return Decimal(last_price).normalize()


def get_open_price(symbol, position_side, limit_depth):
    client = BybitClient().client
    last_price = get_price(client, symbol)
    open_price = calculation.calculate_limit_price(client, symbol, last_price, position_side, limit_depth)
    return Decimal(open_price)


def cancel_all_orders(symbol):
    client = BybitClient().client
    return client.cancel_all_orders(category='linear', symbol=symbol)


def get_unrealized_pnl(symbol):
    client = BybitClient().client
    position = get_position(client, symbol)
    return Decimal(position['unrealisedPnl'])


def get_order_history(symbol, limit=None):
    client = BybitClient().client
    if limit:
        history = client.get_order_history(
            category='linear',
            symbol=symbol,
            limit=limit
        )
    else:
        history = client.get_order_history(
            category='linear',
            symbol=symbol
        )
    return history['result']['list']


def get_open_orders(symbol):
    client = BybitClient().client
    open_orders = client.get_open_orders(
        category='linear',
        symbol=symbol)['result']['list']
    return open_orders


def get_open_limit_order(symbol):
    client = BybitClient().client
    open_orders = get_open_orders(client, symbol)
    open_limit_order = list(filter(lambda order: order['orderType'] == 'Limit', open_orders))
    return open_limit_order


def get_position_size(symbol):
    client = BybitClient().client
    position = get_position(client, symbol)
    size = position['size']
    return Decimal(size)


def get_size_for_open(balance, symbol):
    client = BybitClient().client
    qty_step = get_qty_step(client, symbol)
    price = get_price(client, symbol)
    size = round((balance / 4) / price, qty_step)
    return size


def get_tick_size(symbol):
    client = BybitClient().client
    symbol_info = client.get_instruments_info(category='linear', symbol=symbol)
    tick_size = symbol_info['result']['list'][0]['priceFilter']['tickSize']
    return Decimal(tick_size)


def get_qty_step(symbol):
    client = BybitClient().client
    symbol_info = client.get_instruments_info(category='linear', symbol=symbol)
    qty_step = symbol_info['result']['list'][0]['lotSizeFilter']['qtyStep']
    return Decimal(qty_step)


def get_klines(symbol, time_frame, start_time, end_time):
    client = BybitClient().client
    end_tmstmp = int(end_time.timestamp()) * 1000
    start_tmstmp = int(start_time.timestamp()) * 1000

    klines = client.get_kline(
        category='linear',
        interval=time_frame,
        start=start_tmstmp,
        end=end_tmstmp,
        symbol=symbol,
        limit=1000
    )
    klines_columns = ['time', 'open_position', 'high', 'low', 'close', 'volume', 'turnover']
    klines_df = pd.DataFrame(klines['result']['list'], columns=klines_columns)
    klines_df['time'] = klines_df['time'].apply(lambda tmstmp: datetime.fromtimestamp(int(tmstmp) / 1000))
    klines_df['open_position'] = klines_df['open_position'].astype('float64')
    klines_df['high'] = klines_df['high'].astype('float64')
    klines_df['low'] = klines_df['low'].astype('float64')
    klines_df['close'] = klines_df['close'].astype('float64')
    klines_df['volume'] = klines_df['volume'].astype('float64')

    return klines_df[::-1]
