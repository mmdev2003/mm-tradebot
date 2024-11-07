from decimal import Decimal
from fastapi import status
from fastapi.responses import JSONResponse

from internal import model
from .model import *


def open_position_handler(
        account_service: model.IAccountService,
        position_service: model.IPositionService,
        max_loss: str,
        lock,
):
    async def open_position(request_data: OpenPositionBody):
        order_data = request_data.model_dump()

        password: str = order_data['password']

        symbol: str = order_data['symbol']
        size = Decimal(order_data['size'])
        position_side: str = order_data['position_side']
        leverage = order_data["leverage"]

        stop_in_percent = order_data['stop_in_percent']
        take_in_percent = order_data['take_in_percent']

        # Трейлинг стоп
        interval_stop_in_percent = order_data['interval_stop_in_percent']
        step_move_stop_in_percent = order_data['step_move_stop_in_percent']
        part_from_potential_profit = order_data['part_from_potential_profit']
        max_count_trail_take = order_data['max_count_trail_take']

        # Глубина заброса лимитки
        limit_depth = Decimal(order_data['limit_depth'])

        # Закрытие лимитки, которая долго не исполняется
        wait_time_to_cancel_order = order_data['wait_time_to_cancel_order']

        # Отложенный стоп лосс
        wait_time_to_set_stop = order_data['wait_time_to_set_stop']

        with lock:
            account = account_service.get_account()

            if account.total_profit_in_percent < max_loss:
                return JSONResponse(
                    content={"message": "Максимальная просадка, давай думать"},
                    status_code=status.HTTP_200_OK
                )

            position_db = position_service.get_position(symbol=symbol)

            if position_db:
                return JSONResponse(
                    content={"message": "Позиция уже открыта, ну его нафиг что-то делать с этим"},
                    status_code=status.HTTP_200_OK
                )
            else:
                limit_price = position_service.calculate_limit_order_price(
                    symbol=symbol,
                    position_side=position_side,
                    limit_depth=limit_depth,
                )
                position_service.open_futures_limit_order(
                    symbol=symbol,
                    open_price=limit_price,
                    size=size,
                    position_side=position_side,
                    leverage=leverage,
                    stop_in_percent=stop_in_percent,
                    take_in_percent=take_in_percent,
                    interval_stop_in_percent=interval_stop_in_percent,
                    step_move_stop_in_percent=step_move_stop_in_percent,
                    part_from_potential_profit=part_from_potential_profit,
                    max_count_trail_take=max_count_trail_take,
                    wait_time_to_cancel_order=wait_time_to_cancel_order,
                    wait_time_to_set_stop=wait_time_to_set_stop,
                )
