from pydantic import BaseModel


class OpenPositionBody(BaseModel):
    symbol: str
    size: str
    position_side: str
    leverage: str

    password: str

    take_in_percent: str
    stop_in_percent: str

    interval_stop_in_percent: str
    step_move_stop_in_percent: str
    part_from_potential_profit: str
    max_count_trail_take: str
    limit_depth: str
    wait_time_to_set_stop: str
    wait_time_to_cancel_order: str
