from datetime import datetime
from decimal import Decimal

from internal import model


class PositionService(model.IPositionService):
    def __init__(
            self,
            position_repo: model.IPositionRepository,
            market_client: model.IMarketClient,
            trade_calculator: model.ITradeCalculator,
    ):
        self.position_repo = position_repo
        self.market_client = market_client
        self.trade_calculator = trade_calculator

    def get_position(self, symbol: str) -> model.Position:
        position = self.position_repo.get_position(symbol)
        return position

    def calculate_limit_order_price(self, symbol: str, position_side: str, limit_depth: Decimal) -> Decimal:
        price = self.market_client.get_price(symbol=symbol)
        limit_price = self.trade_calculator.calculate_limit_order_price(
            price=price,
            position_side=position_side,
            limit_depth=limit_depth
        )
        return limit_price

    def open_futures_limit_order(
            self,
            symbol: str,
            open_price: Decimal,
            size: Decimal,
            position_side: str,
            leverage: str,
            take_in_percent: str,
            stop_in_percent: str,
            interval_stop_in_percent: str,
            step_move_stop_in_percent: str,
            part_from_potential_profit: str,
            max_count_trail_take: str,
            time_to_set_stop: str,
            time_to_cancel_order: str,
    ):
        open_time = int(datetime.now().timestamp())
        self.market_client.open_features_limit_order(
            order_id=open_time,
            symbol=symbol,
            size=size,
            open_price=open_price,
            position_side=position_side,
            leverage=int(leverage)
        )
        self.position_repo.set_position(
            order_id=open_time,
            symbol=symbol,
            size=size,
            open_price=open_price,
            position_side=position_side,
            leverage=leverage,
            take_in_percent=take_in_percent,
            stop_in_percent=stop_in_percent,
            interval_stop_in_percent=interval_stop_in_percent,
            step_move_stop_in_percent=step_move_stop_in_percent,
            part_from_potential_profit=part_from_potential_profit,
            max_count_trail_take=max_count_trail_take,
            time_to_set_stop=time_to_set_stop,
            time_to_cancel_order=time_to_cancel_order,
            limit_order_size=size,
            open_time=open_time,
            update_time=open_time,
        )
