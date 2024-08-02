import time
from decimal import Decimal
import threading

from src.services import utils
from src.services.database import db
from src.services.telegram import telegram_requests


def trailing_stop(position, last_price, lock):
    
    interval_stop_in_percent = db.get_value(position, 'interval_stop_in_percent')
    step_move_stop_in_percent = db.get_value(position, 'step_move_stop_in_percent')
    part_from_potential_profit = db.get_value(position, 'part_from_potential_profit')
    max_count_trail_take = db.get_value(position, 'max_count_trail_take')
    breakeven = Decimal('0.1')
    
    last_price = Decimal(last_price)
    open_price = db.get_value(position, 'open_price')
    take_price = db.get_value(position, 'take_price')
    stop_price = db.get_value(position, 'stop_price')
    count_trail_take = db.get_value(position, 'count_trail_take')
    position_side = db.get_value(position, 'position_side')

    potential_profit_in_percent, passed_profit_in_percent, passed_step_in_percent, step_price_in_percent = calculate_passed_step(open_price, last_price, take_price, position_side, interval_stop_in_percent)
   
 
    if passed_step_in_percent > step_move_stop_in_percent:
        
        if position_side == 'Sell':
            new_stop_price = open_price * (Decimal('1') - step_price_in_percent / Decimal('100'))
            
            if (stop_price / new_stop_price - Decimal('1')) * Decimal('100') > potential_profit_in_percent / part_from_potential_profit and (open_price / new_stop_price - Decimal('1')) * Decimal('100') > breakeven:
                
                change_stop_price(position, position_side, take_price, new_stop_price, stop_price, open_price, last_price, lock)
                stop_price = new_stop_price
 
 
        if position_side == 'Buy':
            new_stop_price = open_price * (Decimal('1') + step_price_in_percent / Decimal('100'))
            
            if (new_stop_price / stop_price - Decimal('1')) * Decimal('100') > potential_profit_in_percent / part_from_potential_profit and (new_stop_price / open_price - Decimal('1')) * Decimal('100') > breakeven:
                
                change_stop_price(position, position_side, take_price, new_stop_price, stop_price, open_price, last_price, lock)
                stop_price = Decimal(new_stop_price)
                
        potential_profit_in_percent, passed_profit_in_percent, passed_step_in_percent, step_price_in_percent = calculate_passed_step(stop_price, last_price, take_price, position_side, interval_stop_in_percent)
        
        if passed_step_in_percent > Decimal('70') and (count_trail_take < max_count_trail_take):
 
            if position_side == 'Sell':
          
                new_take_price = take_price * (Decimal('1') - step_price_in_percent / Decimal('100'))
                change_take_price(position, position_side, stop_price, new_take_price, take_price, open_price, last_price, count_trail_take, lock)
            
                
            if position_side == 'Buy':
               
                new_take_price = take_price * (Decimal('1') + step_price_in_percent / Decimal('100'))
                change_take_price(position, position_side, stop_price, new_take_price, take_price, open_price, last_price, count_trail_take, lock)
   

def change_stop_price(position, position_side, take_price, new_stop_price, old_stop_price, open_price, last_price, lock):
    print('Меняем стоп')
    try:
        account = db.get_account()
        client = utils.client_init()
        symbol = db.get_value(position, 'symbol')
        size = db.get_value(position, 'size')
        leverage = db.get_value(position, 'leverage')
        count_trail_stop = db.get_value(position, 'count_trail_stop')
        open_commission_in_dollars = db.get_value(position, 'open_commission_in_dollars')

        start_balance = db.get_value(account, 'start_balance')
        
        old_stop_price = utils.clear_price(client, symbol, old_stop_price)
        new_stop_price = utils.clear_price(client, symbol, new_stop_price)
        
        try:
            client.set_trading_stop(
            category = "linear",
            symbol = symbol,
            stopLoss = str(new_stop_price),
            positionIdx=0
            )
        except Exception as e:
            print('Set stop: ', e.message)
            return False
        
        take_in_percent, new_stop_in_percent = utils.calculate_take_and_stop_in_percent(open_price, take_price, new_stop_price, position_side)
        
        potential_profit_in_percent, potential_profit_in_dollars, potential_profit_in_percent_from_account = utils.calculate_profit(symbol, open_price, take_price, leverage, position_side, size, start_balance, open_commission_in_dollars)
    
        potential_loss_in_percent, potential_loss_in_dollars, potential_loss_in_percent_from_account = utils.calculate_profit(symbol, open_price, new_stop_price, leverage, position_side, size, start_balance, open_commission_in_dollars)
        
       
        position_data = {
            "stop_price": new_stop_price,
            "stop_in_percent": new_stop_in_percent,
            "count_trail_stop": count_trail_stop + Decimal('1'),
            "potential_profit_in_percent": potential_profit_in_percent,
            "potential_profit_in_dollars": potential_profit_in_dollars,
            "potential_profit_in_percent_from_account": potential_profit_in_percent_from_account,
            "potential_loss_in_percent": potential_loss_in_percent,
            "potential_loss_in_dollars": potential_loss_in_dollars,
            "potential_loss_in_percent_from_account": potential_loss_in_percent_from_account
        }
        lock.acquire()
        update_position = db.update_position(position, position_data, remote=True)
        lock.release()
        thread = threading.Thread(target=telegram_requests.trailing_stop_activated, args=(update_position, 'Stop', count_trail_stop + Decimal('1'), last_price, old_stop_price))
        thread.start()
        print('Изменили stop')
        time.sleep(1)
    except Exception as e:
        print('Stop: ', e.message)

def change_take_price(position, position_side, stop_price, new_take_price, old_take_price, open_price, last_price, count_trail_take, lock):
    print('Меняем тейк')
    try:
        account = db.get_account()
        client = utils.client_init()
        
        symbol = db.get_value(position, 'symbol')
        size = db.get_value(position, 'size')
        leverage = db.get_value(position, 'leverage')
        open_commission_in_dollars = db.get_value(position, 'open_commission_in_dollars')
        
        start_balance = db.get_value(account, 'start_balance')
        
        old_take_price = utils.clear_price(client, symbol, old_take_price)
        new_take_price = utils.clear_price(client, symbol, new_take_price)
        
        
        try:
            client.set_trading_stop(
            category = "linear",
            symbol = symbol,
            takeProfit = str(new_take_price),
            positionIdx=0
        )
            
        except Exception as e:
            print('Set take: ', e.message)
            return False
        
        new_take_in_percent, stop_in_percent = utils.calculate_take_and_stop_in_percent(open_price, new_take_price, stop_price, position_side)
        
        potential_profit_in_percent, potential_profit_in_dollars, potential_profit_in_percent_from_account = utils.calculate_profit(symbol, open_price, new_take_price, leverage, position_side, size, start_balance, open_commission_in_dollars)
    
        potential_loss_in_percent, potential_loss_in_dollars, potential_loss_in_percent_from_account = utils.calculate_profit(symbol, open_price, stop_price, leverage, position_side, size, start_balance, open_commission_in_dollars)
        
        position_data = {
            "take_price": new_take_price,
            "take_in_percent": new_take_in_percent,
            "count_trail_take": count_trail_take + Decimal('1'),
            "potential_profit_in_percent": potential_profit_in_percent,
            "potential_profit_in_dollars": potential_profit_in_dollars,
            "potential_profit_in_percent_from_account": potential_profit_in_percent_from_account,
            "potential_loss_in_percent": potential_loss_in_percent,
            "potential_loss_in_dollars": potential_loss_in_dollars,
            "potential_loss_in_percent_from_account": potential_loss_in_percent_from_account
        }
        lock.acquire()
        update_position = db.update_position(position, position_data, remote=True)
        lock.release()
        thread = threading.Thread(target=telegram_requests.trailing_stop_activated, args=(update_position, 'Take', count_trail_take + Decimal('1'), last_price, old_take_price))
        thread.start()
        print('Изменили take')
        time.sleep(1)
    except Exception as e:
        print('Take: ', e.message)

def calculate_passed_step(open_price, last_price, take_price, position_side, interval_stop_in_percent):
    
     
    if position_side == 'Sell':
        potential_profit_in_percent = ((open_price - take_price) / open_price) * Decimal('100')           
        passed_profit_in_percent = ((open_price - last_price) / open_price) * Decimal('100')
                
    if position_side == 'Buy':
        potential_profit_in_percent = (( take_price - open_price ) / open_price) * Decimal('100')           
        passed_profit_in_percent = ((last_price - open_price) / open_price) * Decimal('100')    
                
    
    passed_step_in_percent = (passed_profit_in_percent / potential_profit_in_percent) * Decimal('100')  
    step_price_in_percent = (passed_profit_in_percent / Decimal('100')) * interval_stop_in_percent
    
    return potential_profit_in_percent, passed_profit_in_percent, passed_step_in_percent, step_price_in_percent
    