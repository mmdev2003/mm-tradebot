from fastapi import APIRouter
from fastapi.responses import JSONResponse
from decimal import Decimal

import client

import service
import repository
from schema import ResponseModel, RequestModel

router = APIRouter()


@router.post("/position/open", response_model=ResponseModel)
def open_position(
        request_data: RequestModel
):
    order_data = request_data.model_dump()

    symbol = order_data['symbol']
    size = Decimal(order_data['size'])
    position_side = order_data['position_side']
    time_frame = order_data['time_frame']
    leverage = Decimal(order_data['leverage'])

    stop_in_percent = Decimal(order_data['stop_in_percent'])
    take_in_percent = Decimal(order_data['take_in_percent'])

    # Трейлинг стоп
    interval_stop_in_percent = Decimal(order_data['interval_stop_in_percent'])
    step_move_stop_in_percent = Decimal(order_data['step_move_stop_in_percent'])
    part_from_potential_profit = Decimal(order_data['part_from_potential_profit'])
    max_count_trail_take = Decimal(order_data['max_count_trail_take'])

    # Глубина заброса лимитки?
    limit_depth = Decimal(order_data['limit_depth'])

    # Закрытие лимитки, которая долго не исполняется
    time_to_cancel_order = Decimal(order_data['time_to_cancel_order'])

    # Отложенный стоп лосс
    time_to_set_stop = Decimal(order_data['time_to_set_stop'])

    client.get_client()

    # Попытка решить race condition
    lock = repository.get_lock()

    with lock:
        position_info = service.open_position(
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
        )

    res = ResponseModel(
        message=position_info,
    )

    return JSONResponse(res.model_dump(), status_code=200)
