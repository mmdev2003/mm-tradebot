import torch.optim as optim
from src.programs.neural_network.models.transformer_encoder_V2 import load_model

params = {
    "lr": [1e-3],
    "n_heads": [2, 5, 10],
    "n_layers": [3, 6, 12],
    "d_ff": [32, 64, 128, 256, 512, 1024, 2048],
    "batch_size": [8, 16, 32, 64],
    
    "d_model": [10],
    "len_seq": [2048, 1024, 512, 258, 128, 64, 32],

    "num_epoch": [1],
    "optimizer": {
        "Adam": optim.Adam
    },
    "predictions": {
        "TransformerEncoderV2_1": load_model.TransformerEncoderV2_1
    }
}

