from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Account:
    balance: Decimal
    start_balance: Decimal
    total_profit_in_percent: Decimal
    total_profit_in_dollars: Decimal
    count_profit_positions: Decimal
    count_loss_positions: Decimal
    count_active_positions: Decimal
    count_closed_positions: Decimal


@dataclass
class Position:
    order_id: Decimal

    # for trade
    symbol: str
    position_side: str
    position_status: str
    open_price: Decimal
    purchased_price: Decimal
    close_price: Decimal
    size: Decimal
    limit_order_size: Decimal
    open_commission_in_percent: Decimal
    open_commission_in_dollars: Decimal
    leverage: Decimal

    # RM
    time_to_set_stop: Decimal
    time_to_cancel_order: Decimal
    take_price: Decimal
    take_in_percent: Decimal
    stop_price: Decimal
    stop_in_percent: Decimal
    clear_take_in_percent: Decimal
    clear_stop_in_percent: Decimal

    # trailing
    count_trail_stop: Decimal
    count_trail_take: Decimal
    max_count_trail_take: Decimal
    interval_stop_in_percent: Decimal
    step_move_stop_in_percent: Decimal

    # Что-то на потенциальном
    potential_profit_in_percent: Decimal
    potential_profit_in_dollars: Decimal
    potential_profit_in_percent_from_account: Decimal
    potential_loss_in_percent: Decimal
    potential_loss_in_dollars: Decimal
    potential_loss_in_percent_from_account: Decimal

    # Что-то про деньги
    profit_in_dollars: Decimal
    profit_in_percent: Decimal
    profit_in_percent_from_account: Decimal
    part_from_potential_profit: Decimal
    cum_profit_in_dollars: Decimal
    position_sum: Decimal
    prev_balance: Decimal
    current_balance: Decimal
    start_balance: Decimal

    # Что-то про время
    time_frame: Decimal
    time_to_cancel: Decimal
    open_time: Decimal
    update_time: Decimal
    close_time: Decimal

