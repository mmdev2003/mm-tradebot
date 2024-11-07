import config

ROOT_PATH = config.get("ROOT_PATH")

account_file = f'{ROOT_PATH}/database/account.csv'
positions_file = f'{ROOT_PATH}/database/position.csv'
telegram_chat_id_file = f'{ROOT_PATH}/database/telegram_chat_id.csv'

telegram_columns = ['chat_id']

position_columns = ['symbol', 'position_side', 'open_price', 'purchased_price', 'order_status', 'close_price', 'size',
                    'limit_order_size', 'order_id', 'take_price', 'take_in_percent', 'stop_price', 'stop_in_percent',
                    'profit_in_dollars', 'profit_in_percent', 'profit_in_percent_from_account', 'leverage', 'open_time',
                    'update_time', 'close_time', 'time_frame', 'count_trail_stop', 'count_trail_take', 'time_to_cancel',
                    'prev_balance', 'current_balance', 'potential_profit_in_percent', 'potential_profit_in_dollars',
                    'potential_profit_in_percent_from_account', 'potential_loss_in_percent',
                    'potential_loss_in_dollars', 'potential_loss_in_percent_from_account', 'start_balance',
                    'open_commission_in_percent', 'open_commission_in_dollars', 'clear_take_in_percent',
                    'clear_stop_in_percent', 'interval_stop_in_percent', 'step_move_stop_in_percent',
                    'part_from_potential_profit', 'max_count_trail_take', 'cum_profit_in_dollars', 'position_sum',
                    "time_to_set_stop", 'time_to_cancel_order'
                    ]

decimal_columns = ['open_price', 'purchased_price', 'close_price', 'size', 'limit_order_size', 'take_price',
                   'take_in_percent', 'stop_price', 'stop_in_percent', 'profit_in_dollars', 'profit_in_percent',
                   'profit_in_percent_from_account', 'leverage', 'prev_balance', 'current_balance',
                   'potential_profit_in_percent', 'potential_profit_in_dollars',
                   'potential_profit_in_percent_from_account', 'potential_loss_in_percent', 'potential_loss_in_dollars',
                   'potential_loss_in_percent_from_account', 'start_balance', 'open_commission_in_percent',
                   'open_commission_in_dollars', 'clear_take_in_percent', 'clear_stop_in_percent', 'balance',
                   'total_profit_in_percent', 'total_profit_in_dollars', 'leverage', 'interval_stop_in_percent',
                   'step_move_stop_in_percent', 'part_from_potential_profit', 'cum_profit_in_dollars', 'position_sum'
                   ]

int_columns = ['count_trail_stop', 'count_trail_take', 'chat_id', 'count_profit_positions', 'count_loss_positions',
               'count_active_positions', 'count_closed_positions', 'open_time', 'close_time', 'max_count_trail_take',
               'update_time', "time_to_set_stop", "time_to_cancel_order"]

str_columns = ['symbol', 'position_side', 'order_id', 'time_frame']

account_columns = ['balance', 'total_profit_in_percent', 'total_profit_in_dollars', 'count_profit_positions',
                   'count_loss_positions', 'count_active_positions', 'count_closed_positions', 'start_balance']

model_parameters_column = ['model', 'accuracy', 'symbol', 'loss', 'bs', 'lr', 'n_heads', 'n_layers', 'd_ff',
                           'optimizer', 'len_seq', 'd_model']

db_lock = f'{ROOT_PATH}/database/db.lock'
