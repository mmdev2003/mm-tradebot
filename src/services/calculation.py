from decimal import Decimal, ROUND_HALF_EVEN


def calculate_stop_price(client, symbol, open_price, stop_in_percent, position_side, size, open_commission_in_dollars):
    tick_size = get_tick_size(client, symbol)

    if position_side == 'Buy':
        stop_price = (open_price * size + open_commission_in_dollars) / size * (
                Decimal('1') - (stop_in_percent / Decimal('100'))) * (
                             Decimal('1') + (config.taker / Decimal('100')))

    if position_side == 'Sell':
        stop_price = (open_price * size - open_commission_in_dollars) / size * (
                Decimal('1') + (stop_in_percent / Decimal('100'))) * (
                             Decimal('1') - (config.taker / Decimal('100')))

    return stop_price.quantize(tick_size, rounding=ROUND_HALF_EVEN)


def calculate_take_price(client, symbol, open_price, take_in_percent, position_side, size, open_commission_in_dollars):
    tick_size = get_tick_size(client, symbol)
    if position_side == 'Buy':
        take_price = (open_price * size + open_commission_in_dollars) / size * (
                Decimal('1') + (take_in_percent / Decimal('100'))) * (
                             Decimal('1') + (config.taker / Decimal('100')))

    if position_side == 'Sell':
        take_price = (open_price * size - open_commission_in_dollars) / size * (
                Decimal('1') - (take_in_percent / Decimal('100'))) * (
                             Decimal('1') - (config.taker / Decimal('100')))
    return take_price.quantize(tick_size, rounding=ROUND_HALF_EVEN)


def calculate_limit_price(client, symbol, last_price, position_side, limit_depth):
    tick_size = get_tick_size(client, symbol)
    if position_side == 'Sell':
        limit_price = last_price * (Decimal('1') + limit_depth / Decimal('100'))

    if position_side == 'Buy':
        limit_price = last_price * (Decimal('1') - limit_depth / Decimal('100'))
    return limit_price.quantize(Decimal(tick_size), rounding=ROUND_HALF_EVEN).normalize()


def calculate_purchased_price(client, symbol, prev_size, current_size, prev_price, current_price):
    tick_size = get_tick_size(client, symbol)
    qty_step = get_qty_step(client, symbol)
    purchased_size = current_size - prev_size
    purchased_price = ((current_price * current_size) - (prev_price * prev_size)) / purchased_size

    return purchased_price.quantize(tick_size, rounding=ROUND_HALF_EVEN), purchased_size.quantize(qty_step,
                                                                                                  rounding=ROUND_HALF_EVEN)


def get_time_to_cancel(time_frame, open_time, wait_time):
    open_time = datetime.fromtimestamp(open_time)
    time_to_cancel = open_time + timedelta(seconds=wait_time)
    return time_to_cancel.timestamp()


def get_time_to_set_stop(update_time, time_to_set_stop):
    update_time = datetime.fromtimestamp(update_time)
    time_to_set_stop = update_time + timedelta(seconds=time_to_set_stop)
    return time_to_set_stop.timestamp()


def calculate_take_and_stop_in_percent(open_price, take_price, stop_price, position_side):
    if position_side == 'Buy':
        take_in_percent = (take_price - open_price) / open_price * Decimal('100')
        stop_in_percent = (stop_price - open_price) / open_price * Decimal('100')
    if position_side == 'Sell':
        take_in_percent = (open_price - take_price) / open_price * Decimal('100')
        stop_in_percent = (open_price - stop_price) / open_price * Decimal('100')

    return take_in_percent.quantize(Decimal('0.001'), rounding=ROUND_HALF_EVEN), stop_in_percent.quantize(
        Decimal('0.001'), rounding=ROUND_HALF_EVEN)


def calculate_unrealized_pnl(open_price, last_price, position_side, leverage, size):
    if position_side == 'Sell':
        unrealized_profit_in_percent = (open_price / last_price - Decimal('1')) * Decimal('100') * leverage
        unrealized_profit_in_dollars = (open_price - last_price) * size

    if position_side == 'Buy':
        unrealized_profit_in_percent = (last_price / open_price - Decimal('1')) * Decimal('100') * leverage
        unrealized_profit_in_dollars = (last_price - open_price) * size
    return unrealized_profit_in_percent.quantize(Decimal('0.001'),
                                                 rounding=ROUND_HALF_EVEN), unrealized_profit_in_dollars.quantize(
        Decimal('0.001'), rounding=ROUND_HALF_EVEN)


def calculate_commission(commission_in_percent, price, size):
    commission_in_dollars = price * size * (commission_in_percent / Decimal('100'))
    return commission_in_dollars


def get_tick_size(client, symbol):
    symbol_info = client.get_instruments_info(category='linear', symbol=symbol)
    tick_size = symbol_info['result']['list'][0]['priceFilter']['tickSize']
    return Decimal(tick_size)

def clear_price(client, symbol, price):
    tick_size = get_tick_size(client, symbol)
    return price.quantize(tick_size, rounding=ROUND_HALF_EVEN).normalize()


def get_qty_step(client, symbol):
    symbol_info = client.get_instruments_info(category='linear', symbol=symbol)
    qty_step = symbol_info['result']['list'][0]['lotSizeFilter']['qtyStep']
    return Decimal(qty_step)


def clear_price(price, tick_size):
    return price.quantize(tick_size, rounding=ROUND_HALF_EVEN).normalize()


def calculate_profit(symbol, open_price, close_price, leverage, position_side, size, balance,
                     open_commission_in_dollars):
    close_commission_in_percent = config.taker

    close_commission_in_dollars = calculate_commission(close_commission_in_percent, close_price, size)

    commission_in_dollars = open_commission_in_dollars + close_commission_in_dollars

    if position_side == 'Sell':
        profit_in_dollars = (open_price - close_price) * size - commission_in_dollars

    if position_side == 'Buy':
        profit_in_dollars = (close_price - open_price) * size - commission_in_dollars

    profit_in_percent = profit_in_dollars / (open_price * size / leverage) * Decimal('100')
    profit_in_percent_from_account = profit_in_dollars / balance * Decimal('100')

    return profit_in_percent, profit_in_dollars, profit_in_percent_from_account


def cancel_order(client, symbol, order_id):
    return client.cancel_order(
        symbol=symbol,
        category='linear',
        orderLinkId=order_id
    )

def get_unlock_time(time_frame):
    if time_frame == '5m':
        lock_time = 100
    if time_frame == '15m':
        lock_time = 300
    if time_frame == '30m':
        lock_time = 600
    if time_frame == '1h':
        lock_time = 1200
    if time_frame == '2h':
        lock_time = 2400
    if time_frame == '4h':
        lock_time = 4800

    unlock_time = datetime.now() + timedelta(minutes=lock_time)
    return unlock_time.timestamp()


def crossing_threshold(data, threshold):
    cross_up_indices = []
    cross_down_indices = []
    for i in range(1, len(data)):
        if data[i - 1] < threshold <= data[i]:
            cross_up_indices.append(i)
        elif data[i - 1] > threshold >= data[i]:
            cross_down_indices.append(i)
    return cross_up_indices, cross_down_indices

def calculate_indicators(open_, high, low, close, volume, shift):
    features_df = pd.DataFrame(columns=config.features)

    features_df['high_change'] = high.pct_change(periods=5)
    features_df['low_change'] = low.pct_change(periods=5)
    features_df['close_change'] = close.pct_change(periods=5)

    # Momentum [-1;1]
    features_df['apo'] = ta.apo(close)
    features_df['ao'] = ta.ao(high, low)
    features_df['bop'] = ta.bop(open_, high, low, close)
    features_df['cci'] = ta.cci(high, low, close)
    features_df['cfo'] = ta.cfo(close)
    features_df['cmo'] = ta.cmo(close)
    features_df['coppock'] = ta.coppock(close)
    features_df['kst'] = ta.kst(close).iloc[:, 0]
    features_df['kst_signal'] = ta.kst(close).iloc[:, 1]
    features_df['pgo'] = ta.pgo(high, low, close)
    features_df['pvo'] = ta.pvo(volume).iloc[:, 0]
    features_df['pvo_hist'] = ta.pvo(volume).iloc[:, 1]
    features_df['pvo_signal'] = ta.pvo(volume).iloc[:, 2]
    features_df['rvgi'] = ta.rvgi(open_, high, low, close).iloc[:, 0]
    features_df['rvgi_signal'] = ta.rvgi(open_, high, low, close).iloc[:, 1]
    features_df['smi'] = ta.smi(close).iloc[:, 0]
    features_df['smi_signal'] = ta.smi(close).iloc[:, 1]
    features_df['smi_osc'] = ta.smi(close).iloc[:, 2]
    features_df['stoch_k'] = ta.stoch(high, low, close).iloc[:, 0]
    features_df['stoch_d'] = ta.stoch(high, low, close).iloc[:, 1]
    features_df['tsi'] = ta.tsi(close).iloc[:, 0]
    features_df['tsi_signal'] = ta.tsi(close).iloc[:, 1]

    # Trend [-1;1]

    features_df['qstick'] = ta.qstick(open_, close)

    # Volume [-1;1]
    features_df['cmf'] = ta.cmf(high, low, close, volume)

    # Momentum [0;1]
    features_df['rsi'] = ta.rsi(close)
    features_df['inertia'] = ta.inertia(close=close, high=high, low=low)
    features_df['stoch_rsi_k'] = ta.stochrsi(close).iloc[:, 0]
    features_df['stoch_rsi_d'] = ta.stochrsi(close).iloc[:, 1]
    features_df['willr'] = ta.willr(high, low, close)

    # Trend [0;1]
    features_df['adx'] = ta.adx(high, low, close).iloc[:, 0]
    features_df['dmp'] = ta.adx(high, low, close).iloc[:, 1]
    features_df['dmn'] = ta.adx(high, low, close).iloc[:, 2]
    features_df['chop'] = ta.chop(high, low, close)
    features_df['vip'] = ta.vortex(high, low, close).iloc[:, 0]
    features_df['vim'] = ta.vortex(high, low, close).iloc[:, 1]

    # Volatility [0;1]
    features_df['atr'] = ta.atr(high, low, close)
    features_df['massi'] = ta.massi(high, low)
    features_df['rvi'] = ta.rvi(close)
    features_df['ui'] = ta.ui(close)

    features_df = features_df[shift:]

    print(features_df.isna().sum())
    for feature in config.features_1_1:
        scaler = MinMaxScaler()
        features_df[feature] = scaler.fit_transform(features_df[feature].values.reshape(-1, 1)).flatten().round(5)

    for feature in config.features_0_1:
        scaler = MinMaxScaler()
        features_df[feature] = scaler.fit_transform(features_df[feature].values.reshape(-1, 1)).flatten().round(5)

    return features_df

