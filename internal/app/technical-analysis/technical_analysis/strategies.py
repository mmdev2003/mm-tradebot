from src.services.telegram import telegram_requests
from db import db
from datetime import datetime
from src.services import utils


def divergence(divergence, symbol):
    
    divergence_signal = []
    
    for time_frame in divergence:
        for indicator in divergence[time_frame]:
            if divergence[time_frame][indicator] == 'Buy' or divergence[time_frame][indicator] == 'Sell':
                
                divergence_signal.append(
                    {
                        "indicator": indicator,
                        "position_side": divergence[time_frame][indicator],
                        "time_frame": time_frame
                    }
                )
    Lock_signal = db.get_lock_signal(symbol)
    print(divergence_signal)
    for signal in divergence_signal:
        time_frame = signal['time_frame']
        indicator = signal['indicator']
        position_side = signal['position_side']
        lock = check_lock_signal(Lock_signal, indicator, time_frame, symbol, position_side)
        if lock:
            continue
        unlock_time = utils.get_unlock_time(time_frame)
        lock_signal_data = {
            "symbol": symbol,
            "indicator": indicator,
            "time_frame": time_frame,
            "unlock_time": unlock_time
        }
        db.set_lock_signal(Lock_signal, lock_signal_data, symbol)
 
        telegram_requests.text_alert(f'Обнаружили дивергенцию {symbol} {position_side} {indicator} на {time_frame}')
        # request.open_position(symbol, position_side, time_frame)
        
    return divergence_signal
    

def check_lock_signal(Lock_signal, indicator, time_frame, symbol, position_side):
    lock = False
    if not Lock_signal.empty:
        lock_signal = Lock_signal[(Lock_signal['time_frame'] == time_frame) & (Lock_signal['indicator'] == indicator)]
        if not lock_signal.empty:
            unlock_time = db.get_value(lock_signal, 'unlock_time')
            time_now = datetime.now().timestamp()
           
            if unlock_time - time_now < 0:
                telegram_requests.text_alert(f'Сигнал {symbol} {position_side} {indicator} на {time_frame} разблокировался')
                lock = False
                db.del_lock_signal(Lock_signal, symbol, indicator, time_frame)
            else:
                lock = True 
    return lock