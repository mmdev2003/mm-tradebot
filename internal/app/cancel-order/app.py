import time
from datetime import datetime


from internal import model


def New(
        position_service: model.IPositionService,
        lock
):
    while True:
        with lock:
            positions = position_service.get_all_position()

            if not positions:
                for position in positions:
                    time_to_cancel = position_service.calculate_time_to_cancel(
                        open_time=position.open_time,
                        wait_time=position.wait_time_to_set_stop
                    )
                    time_now = datetime.now().timestamp()

                    if time_to_cancel - time_now < 0:
                        position_service.cancel_order(position.symbol)
        time.sleep(20)
