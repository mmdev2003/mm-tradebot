from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_EVEN


class Calculator:
    def __init__(self, taker: Decimal, maker: Decimal):
        self.taker = taker
        self.maker = maker

    def calculate_stop_price(
            self,
            position_side: str,
            open_price: Decimal,
            size: Decimal,
            open_commission_in_dollars: Decimal,
            stop_in_percent: Decimal,
            tick_size: int,
    ):
        if position_side == 'Buy':
            stop_price = (open_price * size + open_commission_in_dollars) / size * (
                    Decimal('1') - (stop_in_percent / Decimal('100'))) * (
                                 Decimal('1') + (self.taker / Decimal('100')))
        else:
            stop_price = (open_price * size - open_commission_in_dollars) / size * (
                    Decimal('1') + (stop_in_percent / Decimal('100'))) * (
                                 Decimal('1') - (self.taker / Decimal('100')))
        return stop_price.quantize(tick_size, rounding=ROUND_HALF_EVEN)

    def calculate_take_price(
            self,
            position_side: str,
            open_price: Decimal,
            size: Decimal,
            open_commission_in_dollars: Decimal,
            take_in_percent: Decimal,
            tick_size: int,
    ):
        if position_side == 'Buy':
            take_price = (open_price * size + open_commission_in_dollars) / size * (Decimal('1') + (take_in_percent / Decimal('100'))) * (Decimal('1') + (self.taker / Decimal('100')))

        else:
            take_price = (open_price * size - open_commission_in_dollars) / size * (
                    Decimal('1') - (take_in_percent / Decimal('100'))) * (
                                 Decimal('1') - (self.taker / Decimal('100')))
        return take_price.quantize(tick_size, rounding=ROUND_HALF_EVEN)

    def calculate_limit_order_price(self, price: Decimal, position_side: str, limit_depth: Decimal) -> Decimal:
        if position_side == 'Sell':
            limit_price = price * (Decimal('1') + limit_depth / Decimal('100'))
        else:
            limit_price = price * (Decimal('1') - limit_depth / Decimal('100'))
        return limit_price

    def calculate_purchased_price(
            self,
            prev_size: Decimal,
            current_size: Decimal,
            prev_price: Decimal,
            current_price: Decimal,
            tick_size: int,
            qty_step: int
    ):
        purchased_size = current_size - prev_size
        purchased_price = ((current_price * current_size) - (prev_price * prev_size)) / purchased_size

        return purchased_price.quantize(tick_size, rounding=ROUND_HALF_EVEN), purchased_size.quantize(qty_step,
                                                                                                      rounding=ROUND_HALF_EVEN)



    def get_time_to_set_stop(self, update_time, time_to_set_stop):
        update_time = datetime.fromtimestamp(update_time)
        time_to_set_stop = update_time + timedelta(seconds=time_to_set_stop)
        return time_to_set_stop.timestamp()

    def calculate_take_and_stop_in_percent(self, open_price, take_price, stop_price, position_side):
        if position_side == 'Buy':
            take_in_percent = (take_price - open_price) / open_price * Decimal('100')
            stop_in_percent = (stop_price - open_price) / open_price * Decimal('100')
        else:
            take_in_percent = (open_price - take_price) / open_price * Decimal('100')
            stop_in_percent = (open_price - stop_price) / open_price * Decimal('100')

        return take_in_percent.quantize(Decimal('0.001'), rounding=ROUND_HALF_EVEN), stop_in_percent.quantize(
            Decimal('0.001'), rounding=ROUND_HALF_EVEN)

    def calculate_unrealized_pnl(self, open_price, last_price, position_side, leverage, size):
        if position_side == 'Sell':
            unrealized_profit_in_percent = (open_price / last_price - Decimal('1')) * Decimal('100') * leverage
            unrealized_profit_in_dollars = (open_price - last_price) * size

        else:
            unrealized_profit_in_percent = (last_price / open_price - Decimal('1')) * Decimal('100') * leverage
            unrealized_profit_in_dollars = (last_price - open_price) * size
        return unrealized_profit_in_percent.quantize(Decimal('0.001'),
                                                     rounding=ROUND_HALF_EVEN), unrealized_profit_in_dollars.quantize(
            Decimal('0.001'), rounding=ROUND_HALF_EVEN)

    def calculate_commission(self, commission_in_percent, price, size):
        commission_in_dollars = price * size * (commission_in_percent / Decimal('100'))
        return commission_in_dollars

    def calculate_profit(self, symbol, open_price, close_price, leverage, position_side, size, balance,
                         open_commission_in_dollars):
        close_commission_in_percent = self.taker

        close_commission_in_dollars = self.calculate_commission(close_commission_in_percent, close_price, size)

        commission_in_dollars = open_commission_in_dollars + close_commission_in_dollars

        if position_side == 'Sell':
            profit_in_dollars = (open_price - close_price) * size - commission_in_dollars

        else:
            profit_in_dollars = (close_price - open_price) * size - commission_in_dollars

        profit_in_percent = profit_in_dollars / (open_price * size / leverage) * Decimal('100')
        profit_in_percent_from_account = profit_in_dollars / balance * Decimal('100')

        return profit_in_percent, profit_in_dollars, profit_in_percent_from_account
