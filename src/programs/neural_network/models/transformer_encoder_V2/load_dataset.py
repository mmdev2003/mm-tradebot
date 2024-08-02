import sys
import os
from dotenv import load_dotenv
load_dotenv()
root_path = os.getenv('ROOT_PATH')
sys.path.append(root_path)

import torch
from torch.utils.data import Dataset
import pandas as pd
import numpy as np
import ast

from src.services import config


class TradeDatasetV2(Dataset):
    
    def __init__(self, symbol, d_model, len_seq, seed):
        self.dataset = pd.read_csv(f'{config.data_path}/dataset_V2_{symbol}.csv')
        self.target = pd.read_csv(f'{config.data_path}/target_V2_{symbol}.csv')
        
    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        x = ast.literal_eval(dataset.iloc[0, idx])
        target = ast.literal_eval(self.target['target'].iloc[idx])
        
        x = torch.tensor(np.array(x), dtype=torch.float)
        target = torch.tensor(np.array(target), dtype=torch.float)
        return x, target 