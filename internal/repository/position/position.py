import orjson

from internal import model


class PositionRepository(model.IPositionRepository):
    def __init__(
            self,
            in_memory_kv_db: model.IInMemoryKvDB,
    ):
        self.in_memory_kv_db = in_memory_kv_db

    def set_position(
            self,
            order_id: int,
            symbol: str,
            open_price: str,
            size: str,
            position_side: str,
            leverage: int,
            take_in_percent: str,
            stop_in_percent: str,
            interval_stop_in_percent: str,
            step_move_stop_in_percent: str,
            part_from_potential_profit: str,
            max_count_trail_take: str,
            wait_time_to_set_stop: str,
            wait_time_to_cancel_order: str,
            limit_order_size: str,
            open_time: int,
            update_time: int
    ):
        position_data = {
            'order_id': order_id,
            'symbol': symbol,
            'open_price': open_price,
            'size': size,
            'position_side': position_side,
            'leverage': leverage,
            'take_in_percent': take_in_percent,
            'stop_in_percent': stop_in_percent,
            'interval_stop_in_percent': interval_stop_in_percent,
            'step_move_stop_in_percent': step_move_stop_in_percent,
            'part_from_potential_profit': part_from_potential_profit,
            'max_count_trail_take': max_count_trail_take,
            'wait_time_to_set_stop': wait_time_to_set_stop,
            'wait_time_to_cancel_order': wait_time_to_cancel_order,
            'limit_order_size': limit_order_size,
            'open_time': open_time,
            'update_time': update_time
        }
        position = orjson.dumps(position_data).decode('utf-8')

        self.in_memory_kv_db.set(symbol, position)

    def get_position(
            self,
            symbol: str,
    ) -> model.Position:
        position = self.in_memory_kv_db.get(symbol)
        position = orjson.loads(position)
        return model.Position(**position)

    def delete_position(self, symbol: str):
        self.in_memory_kv_db.delete(symbol)

    def get_all_position(self) -> list[model.Position]:
        positions = []

        keys = self.in_memory_kv_db.all_keys()
        for key in keys:
            position = self.in_memory_kv_db.get(key)
            position = orjson.loads(position)
            positions.append(model.Position(**position))

        return positions
