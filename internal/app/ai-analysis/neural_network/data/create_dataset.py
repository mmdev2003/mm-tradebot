import sys
import os
from dotenv import load_dotenv
load_dotenv()
root_path = os.getenv('ROOT_PATH')
sys.path.append(root_path)

import torch
import pandas as pd
from tqdm import tqdm
import torch.nn.functional as F

from src.services import utils, config


def create_dataset(symbol, version):
    data = pd.read_csv(f'{config.data_path}/data_{symbol}.csv')
    
    close = data['close']
    high = data['high']
    low = data['low']
    open_ = data['open_position']
    time = data['time']
    volume = data['volume']
    
    count_prev_bars = 2048
    count_next_bars = 20
    threshold = 0.15
    shift = 60
  
    features_df = utils.calculate_indicators(open_, high, low, close, volume, shift)
    
    data = data[shift:]
    dataset = pd.DataFrame(columns=[str(i) for i in range(shift + count_prev_bars, len(data) - count_next_bars - 1)])
    
    target_list = list()
    target_time_list = list()
    target_dict = dict()
 
    loop = tqdm(range(shift + count_prev_bars, len(data) - count_next_bars - 1))
    for id in loop:
        current_bar = close.iloc[id]
        
        long_profit_bar_count = 0
        long_loss_bar_count = 0
        
        short_profit_bar_count = 0
        short_loss_bar_count = 0
        
        for bar in range(1, count_next_bars + 1):
            bar_low = low.iloc[id + bar]
            bar_high = high.iloc[id + bar]
            
            if (bar_high - current_bar) / current_bar * 100 > threshold:
                long_profit_bar_count += 1
            if (bar_low - current_bar) / current_bar * 100 > -threshold:
                long_loss_bar_count += 1
                
            if (bar_low - current_bar) / current_bar * 100 < -threshold:
                short_profit_bar_count += 1
            if (bar_high - current_bar) / current_bar * 100 < threshold:
                short_loss_bar_count += 1
               
        target = 0
        if long_profit_bar_count > 0 and long_loss_bar_count == count_next_bars:
            target = 2
            
        if short_profit_bar_count > 0 and short_loss_bar_count == count_next_bars:
            target = 1
        
        if version == 'V1':
            x = features_df.iloc[id + 1 - count_prev_bars:id + 1, :].values.T
        if version == 'V2':
            x = features_df.iloc[id + 1 - count_prev_bars:id + 1, :].values
        dataset.loc[0, str(id)] = x
        
        target_list.append(target)
        target_time_list.append(time.iloc[id])
    
    target_dict['target'] = F.one_hot(torch.tensor(target_list), num_classes=3).tolist()
    target_dict['target_time'] = target_time_list
    target = pd.DataFrame(target_dict)
    
    print(x.shape)
    print(len(dataset.columns))
    print(len(dataset))
    print(target)
  
    target.to_csv(f'{config.data_path}/target_{version}_{symbol}.csv', index=False)
    dataset.to_csv(f'{config.data_path}/dataset_{version}_{symbol}.csv', index=False)

create_dataset('XMRUSDT', 'V2')