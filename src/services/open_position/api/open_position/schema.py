from pydantic import BaseModel, Field


class RequestModel(BaseModel):
    password: str = Field(example="table.csv")
    symbol: str = Field(example="SOLUSDT")
    position_side: str = Field(example="BUY"),
    stop_in_percent: str = Field(example="0.65")
    take_in_percent: str = Field(example="1.49")
    size: str = Field(example="0.3")
    leverage: str = Field(example="4")
    time_frame: str = Field(example="1m")
    interval_stop_in_percent: str = Field(example="75")
    step_move_stop_in_percent: str = Field(example="90")
    part_from_potential_profit: str = Field(example="3")
    max_count_trail_take: str = Field(example="0")
    limit_depth: str = Field(example="0.4")
    time_to_set_stop: str = Field(example="120")
    time_to_cancel_order: str = Field(example="460")


class ResponseModel(BaseModel):
    message: str
