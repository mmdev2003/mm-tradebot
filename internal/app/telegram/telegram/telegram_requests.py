import os
from dotenv import load_dotenv
load_dotenv()

import requests

from src.services.database import db

main_server = os.getenv('MAIN_SERVER')
base_url = f'{main_server}/telegram'

def trailing_stop_activated(position, order_type, count_trail, last_price, old_price):
    
    position_data = {
        "symbol": db.get_value(position, 'symbol'),
        "open_price": str(db.get_value(position, 'open_price')),
        "position_side": str(db.get_value(position, 'position_side')),
        "count_trail": str(count_trail),
        "last_price": str(last_price),
        
        "take_in_percent": str(db.get_value(position, 'take_in_percent')),
        "stop_in_percent": str(db.get_value(position, 'stop_in_percent')),
        "take_price": str(db.get_value(position, 'take_price')),
        "stop_price": str(db.get_value(position, 'stop_price')),
        "old_price": str(old_price),
        "size": str(db.get_value(position, 'size')),
        "leverage": str(db.get_value(position, 'leverage')),
        "order_type": order_type,
        "potential_profit_in_percent": str(db.get_value(position, 'potential_profit_in_percent')),
        "potential_profit_in_dollars": str(db.get_value(position, 'potential_profit_in_dollars')),
        "potential_profit_in_percent_from_account": str(
            db.get_value(position, 'potential_profit_in_percent_from_account')),
        "potential_loss_in_percent": str(db.get_value(position, 'potential_loss_in_percent')),
        "potential_loss_in_dollars": str(db.get_value(position, 'potential_loss_in_dollars')),
        "potential_loss_in_percent_from_account": str(db.get_value(position, 'potential_loss_in_percent_from_account'))
    }
    
    response = requests.post(
            f'{base_url}/trailing_stop_activated',
            json=position_data
            )
    
    

def position_closed(position):
    
    position_data = {
        "symbol": db.get_value(position, 'symbol'),
        "position_side": db.get_value(position, 'position_side'),
        "open_price": str(db.get_value(position, 'open_price')),
        "size": str(db.get_value(position, 'size')),
        "leverage": str(db.get_value(position, 'leverage')),
        "close_price": str(db.get_value(position, 'close_price')),
        "profit_in_dollars": str(db.get_value(position, 'profit_in_dollars')),
        "profit_in_percent_from_account": str(db.get_value(position, 'profit_in_percent_from_account')),
        "profit_in_percent": str(db.get_value(position, 'profit_in_percent')),
        "prev_balance": str(db.get_value(position, 'prev_balance')),
        "current_balance": str(db.get_value(position, 'current_balance'))
    }
    
    response = requests.post(
        f'{base_url}/position_closed',
        json=position_data
        )

def set_stop(position):
    
    position_data = {
        "symbol": db.get_value(position, 'symbol'),
        "position_side": db.get_value(position, 'position_side'),
        "open_price": str(db.get_value(position, 'open_price')),
        "size": str(db.get_value(position, 'size')),
        "leverage": str(db.get_value(position, 'leverage')),
        
        "take_in_percent": str(db.get_value(position, 'take_in_percent')),
        "stop_in_percent": str(db.get_value(position, 'stop_in_percent')),
        
        "stop_price": str(db.get_value(position, 'stop_price')),
        "take_price": str(db.get_value(position, 'take_price')),
        "potential_profit_in_percent": str(db.get_value(position, 'potential_profit_in_percent')),
        "potential_profit_in_dollars": str(db.get_value(position, 'potential_profit_in_dollars')),
        "potential_profit_in_percent_from_account": str(
            db.get_value(position, 'potential_profit_in_percent_from_account')),
        "potential_loss_in_percent": str(db.get_value(position, 'potential_loss_in_percent')),
        "potential_loss_in_dollars": str(db.get_value(position, 'potential_loss_in_dollars')),
        "potential_loss_in_percent_from_account": str(db.get_value(position, 'potential_loss_in_percent_from_account')),
        "prev_balance": str(db.get_value(position, 'prev_balance')),
        "current_balance": str(db.get_value(position, 'current_balance'))
    }
    
    response = requests.post(
        f'{base_url}/set_stop',
        json=position_data
        )

def purchased_position(position):
    position_data = {
        "symbol": db.get_value(position, 'symbol'),
        "position_side": db.get_value(position, 'position_side'),
        "open_price": str(db.get_value(position, 'open_price')),
        "size": str(db.get_value(position, 'size')),
        "leverage": str(db.get_value(position, 'leverage')),
        
        "take_in_percent": str(db.get_value(position, 'take_in_percent')),
        "stop_in_percent": str(db.get_value(position, 'stop_in_percent')),
        
        "stop_price": str(db.get_value(position, 'stop_price')),
        "take_price": str(db.get_value(position, 'take_price')),
        "potential_profit_in_percent": str(db.get_value(position, 'potential_profit_in_percent')),
        "potential_profit_in_dollars": str(db.get_value(position, 'potential_profit_in_dollars')),
        "potential_profit_in_percent_from_account": str(
            db.get_value(position, 'potential_profit_in_percent_from_account')),
        "potential_loss_in_percent": str(db.get_value(position, 'potential_loss_in_percent')),
        "potential_loss_in_dollars": str(db.get_value(position, 'potential_loss_in_dollars')),
        "potential_loss_in_percent_from_account": str(db.get_value(position, 'potential_loss_in_percent_from_account')),
        "prev_balance": str(db.get_value(position, 'prev_balance')),
        "current_balance": str(db.get_value(position, 'current_balance'))
    }
    
    response = requests.post(
        f'{base_url}/position_purchased',
        json=position_data
        )
        
def position_opened(position):
    
    position_data = {
        "symbol": db.get_value(position, 'symbol'),
        "position_side": db.get_value(position, 'position_side'),
        "open_price": str(db.get_value(position, 'open_price')),
        "size": str(db.get_value(position, 'size')),
        "leverage": str(db.get_value(position, 'leverage')),
        
        "take_in_percent": str(db.get_value(position, 'take_in_percent')),
        "stop_in_percent": str(db.get_value(position, 'stop_in_percent')),
        
        "stop_price": str(db.get_value(position, 'stop_price')),
        "take_price": str(db.get_value(position, 'take_price')),
        "potential_profit_in_percent": str(db.get_value(position, 'potential_profit_in_percent')),
        "potential_profit_in_dollars": str(db.get_value(position, 'potential_profit_in_dollars')),
        "potential_profit_in_percent_from_account": str(
            db.get_value(position, 'potential_profit_in_percent_from_account')),
        "potential_loss_in_percent": str(db.get_value(position, 'potential_loss_in_percent')),
        "potential_loss_in_dollars": str(db.get_value(position, 'potential_loss_in_dollars')),
        "potential_loss_in_percent_from_account": str(db.get_value(position, 'potential_loss_in_percent_from_account')),
        "prev_balance": str(db.get_value(position, 'prev_balance')),
        "current_balance": str(db.get_value(position, 'current_balance'))
    }
    
    response = requests.post(
        f'{base_url}/position_opened',
        json=position_data
        )
        
def text_alert(text):
    
    text_data = {
        'text': text
    }
    
    response = requests.post(
        f'{base_url}/text_alert',
        json=text_data
        )