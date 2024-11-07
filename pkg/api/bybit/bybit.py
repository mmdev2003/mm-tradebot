import pandas as pd
from decimal import Decimal
from datetime import datetime
from pybit.unified_trading import HTTP

from internal import model


class BybitClient(model.IMarketClient):
    def __init__(self, api_key: str, api_secret_key: str):
        self.client = HTTP(api_key=api_key, api_secret=api_secret_key)

    def wallet_by_symbol(self, symbol: str) -> model.BybitWallet:
        response = self.client.get_wallet_balance(accountType='CONTRACT', coin=symbol)
        return model.WalletResponse(**response).result.list[0]

    def get_position(self, symbol: str) -> model.BybitPosition:
        response = self.client.get_positions(category='linear', symbol=symbol)
        return model.PositionResponse(**response).result.list[0]

    def get_price(self, symbol: str) -> Decimal:
        last_price = self.client.get_tickers(
            category='linear',
            symbol=symbol
        )['result']['list'][0]['lastPrice']
        return Decimal(last_price).normalize()

    def get_open_orders(self, symbol: str):
        open_orders = self.client.get_open_orders(
            category='linear',
            symbol=symbol)['result']['list']
        return open_orders

    def get_unrealized_pnl(self, symbol: str) -> Decimal:
        position = self.get_position(symbol)
        return Decimal(position['unrealisedPnl'])

    def get_open_limit_order(self, symbol: str):
        open_orders = self.get_open_orders(symbol)
        open_limit_order = list(filter(lambda order: order['orderType'] == 'Limit', open_orders))
        return open_limit_order

    def get_position_size(self, symbol: str) -> Decimal:
        position = self.get_position(symbol)
        size = position['size']
        return Decimal(size)

    def get_tick_size(self, symbol: str):
        symbol_info = self.client.get_instruments_info(category='linear', symbol=symbol)
        tick_size = symbol_info['result']['list'][0]['priceFilter']['tickSize']
        return Decimal(tick_size)

    def get_qty_step(self, symbol: str) -> Decimal:
        symbol_info = self.client.get_instruments_info(category='linear', symbol=symbol)
        qty_step = symbol_info['result']['list'][0]['lotSizeFilter']['qtyStep']
        return Decimal(qty_step)

    def cancel_all_orders(self, symbol: str) -> Decimal:
        return self.client.cancel_all_orders(category='linear', symbol=symbol)

    def set_leverage(self, symbol: str, leverage: int):
        current_leverage = self.get_position(symbol)['leverage']
        if Decimal(current_leverage) != leverage:
            return self.client.set_leverage(
                category='linear',
                symbol=symbol,
                buyLeverage=str(leverage),
                sellLeverage=str(leverage)
            )

    def open_features_limit_order(
            self,
            order_id: int,
            symbol: str,
            size: Decimal,
            open_price: Decimal,
            position_side: str,
            leverage: int,

    ):
        self.set_leverage(symbol, leverage)

        order = self.client.place_order(
            category='linear',
            symbol=symbol,
            side=position_side,
            orderType='Limit',
            price=str(open_price),
            qty=str(size),
            orderLinkId=str(order_id)
        )

        return order

    def get_order_history(self, symbol: str, limit: int = None):
        if limit:
            history = self.client.get_order_history(
                category='linear',
                symbol=symbol,
                limit=limit
            )
        else:
            history = self.client.get_order_history(
                category='linear',
                symbol=symbol
            )
        return history['result']['list']

    def get_klines(
            self,
            symbol: str,
            time_frame: str,
            start_time: str,
            end_time: str
    ):
        end_tmstmp = int(end_time.timestamp()) * 1000
        start_tmstmp = int(start_time.timestamp()) * 1000

        klines = self.client.get_kline(
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
