import sys
import os
from dotenv import load_dotenv
load_dotenv()
root_path = os.getenv('ROOT_PATH')
sys.path.append(root_path)

import torch
from torch import nn
from torch.utils.data import DataLoader, random_split
from tqdm import tqdm

from src.programs.neural_network.models.transformer_encoder_V2.params import params
from src.services.telegram import telegram_requests

symbol = 'XMRUSDT'
num_workers = 8
train_size = 0.8

def train_fn(model, loss_fn, optimizer, train, test, num_epoch):
    if torch.cuda.is_available():
        model.to('cuda')
    accuracy_list = []
    loss_list = []
    for epoch in range(num_epoch):
        model.train()
        train_loop = tqdm(train)
        total = 0
        loss_sum = 0
        for batch_idx, (x, target) in enumerate(train_loop):
            if torch.cuda.is_available():
                x = x.to('cuda')
                target = target.to('cuda')
             
            prediction = model(x)
            loss = loss_fn(prediction, target)
            loss.backward()
            
            optimizer.zero_grad()
            optimizer.step()
            
            loss_sum += loss.item()
            total += 1
            
            train_loop.set_postfix(loss=loss.item())
        mean_loss = round(loss_sum / total, 2)
        loss_list.append(mean_loss)
        
        model.eval()
        test_loop = tqdm(test)
        with torch.no_grad():
            correct = 0
            total = 0
            for batch_idx, (x, target) in enumerate(test_loop):
                if torch.cuda.is_available():
                    x = x.to('cuda')
                    target = target.to('cuda')
                total += target.size(0)
                prediction = model(x)
                _, predicted = torch.max(prediction, 1)
                _, target = torch.max(target, 1)
                
                correct += (predicted == target).sum().item()
            accuracy = round(100 * correct / total, 2)
            accuracy_list.append(accuracy)
            
    if num_epoch == 1:
        return accuracy_list[0], loss_list[0]
    else:
        return accuracy_list, loss_list

            
def load_dataset(train_size, bs):
    dataset = TradeDatasetV1(symbol)
  
    train_size = int(len(dataset) * train_size)
    test_size = len(dataset) - train_size

    train, test = random_split(dataset, [train_size, test_size])
    
    train_loader = DataLoader(train, batch_size=bs, shuffle=True, num_workers=num_workers)
    test_loader = DataLoader(test, batch_size=bs, shuffle=True, num_workers=num_workers)
    
    return train_loader, test_loader
    
def main(n_heads, d_ff, n_layers, lr, optimizer, train, test, num_epoch, model, model_name, d_model, len_seq, bs, optimizer_name):
 
    d_model = count_prev_bars
    
    model = nn.DataParallel(model(d_model, n_heads, d_ff, n_layers, len_seq))
    optimizer = optimizer(model.parameters(), lr=lr)
                            
    loss_fn = nn.CrossEntropyLoss()
                            
    accuracy, loss = train_fn(model, loss_fn, optimizer, train, test, num_epoch)
    model_parameters_data = {
        'model': model_name,
        'accuracy': accuracy,
        'symbol': symbol,
        'loss': loss,
        'd_model': count_prev_bars,
        'len_seq': len_seq,
        'bs': bs,
        'lr': lr,
        'n_heads': n_heads,
        'n_layers': n_layers,
        'd_ff': d_ff,
        'optimizer': optimizer_name,
        'seed': seed 
    }
                                
    message = (
    f'Model: {model_parameters_data["model"]}\n'
    f'Symbol: {model_parameters_data["symbol"]}\n'
    f'Accuracy: {model_parameters_data["accuracy"]}\n'
    f'Loss: {model_parameters_data["loss"]}\n\n'
    f'D_Model: {model_parameters_data["count_prev_bars"]}\n'
    f'Len seq: {model_parameters_data["len_seq"]}\n'
    f'LR: {model_parameters_data["lr"]}\n'
    f'Batch Size: {model_parameters_data["bs"]}\n'
    f'N_Heads: {model_parameters_data["n_heads"]}\n'
    f'N_Layers: {model_parameters_data["n_layers"]}\n'
    f'Dim FF: {model_parameters_data["d_ff"]}\n'
    f'Optimizer: {model_parameters_data["optimizer"]}\n'
    f'Seed: {model_parameters_data["seed"]}\n'
       
    )
    telegram_requests.text_alert(message)
    
def grid():

    for len_seq in params['len_seq']:
        for d_model in params['d_model']:
            for bs in params['batch_size']:
                train, test = load_dataset(train_size, bs)
                telegram_requests.text_alert('Начался Grid Search')
                for d_ff in params['d_ff']:
                    for n_layers in params['n_layers']:
                        for n_heads in params['n_heads']:
                            for lr in params['lr']:
                                for optimizer_name, optimizer in params['optimizer'].items():
                                    for num_epoch in params['num_epoch']:
                                        for model_name, model in params['predictions'].items():
                                            main(n_heads, d_ff, n_layers, lr, optimizer, train, test, num_epoch, model, model_name, d_model, len_seq, bs, optimizer_name)
grid()


