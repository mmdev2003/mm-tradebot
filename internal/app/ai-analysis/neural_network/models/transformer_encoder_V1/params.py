import torch.optim as optim
from src.programs.neural_network.models.transformer_encoder_V1 import load_model

params = {
    "lr": [1e-3],
    "n_heads": [128, 256, 512],
    "n_layers": [3, 6, 12],
    "d_ff": [2048],
    "batch_size": [32, 16],
    
    "count_prev_bars": [2048, 512],
    "len_seq": [10],

    "num_epoch": [1, 2],
    "optimizer": {
        "Adam": optim.Adam
    },
    "predictions": {
        "TransformerEncoderV1_1": load_model.TransformerEncoderV1_1
    }
}

