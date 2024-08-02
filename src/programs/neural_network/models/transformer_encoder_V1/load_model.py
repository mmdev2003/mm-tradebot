import torch.nn as nn

class TransformerEncoderV1_1(nn.Module):
    def __init__(self, d_model, n_heads, d_ff, n_layers, len_seq):
        super().__init__()
        
        self.encoder = nn.TransformerEncoder(
                nn.TransformerEncoderLayer(d_model=d_model, nhead=n_heads, dim_feedforward=d_ff, batch_first=True),
                num_layers=n_layers
            )
        self.classifier = nn.Linear(len_seq * d_model, 3)
    def forward(self, features):
        z = self.encoder(features)
        z = z.reshape(z.size(0), -1)
        predict = self.classifier(z)
        return predict
        
class TransformerEncoderV1_2(nn.Module):
    def __init__(self, d_model, n_heads, d_ff, n_layers, len_seq):
        super().__init__()
        
        self.encoder = nn.TransformerEncoder(
                nn.TransformerEncoderLayer(d_model=d_model, nhead=n_heads, dim_feedforward=d_ff, batch_first=True),
                num_layers=n_layers
            )
       
        self.fc1 = nn.Linear(len_seq * d_model, 2048)
        self.fc2 = nn.Linear(2048, 512)
        self.fc3 = nn.Linear(512, 1024)
        self.fc4 = nn.Linear(1024, 2048)
        self.relu = nn.ReLU()
        self.classifier = nn.Linear(2048, 3)

    def forward(self, features):
        z = self.encoder(features)
        z = z.reshape(z.size(0), -1)
        
        fc = self.relu(self.fc1(z))
        fc2 = self.relu(self.fc2(fc))
        fc3 = self.relu(self.fc3(fc2))
        fc4 = self.relu(self.fc4(fc3))
        predict = self.classifier(fc4)
        return predict