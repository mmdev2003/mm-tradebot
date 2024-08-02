import torch.nn as nn

class TransformerEncoderV2_1(nn.Module):
    def __init__(self, d_model, n_heads, d_ff, n_layers, len_seq):
        super().__init__()
        
        self.encoder = nn.TransformerEncoder(
                nn.TransformerEncoderLayer(d_model=d_model, nhead=n_heads, dim_feedforward=d_ff, batch_first=True),
                num_layers=n_layers
            )
        self.positional_encoding = PositionalEncoding(d_model, len_seq)

        self.classifier = nn.Linear(d_model * len_seq, 3)

    def forward(self, features):
        pe_features = self.positional_encoding(features )
        z = self.encoder(pe_features)
        z = z.reshape(z.size(0), -1)
        z = self.fc(z)
        predict = self.classifier(z)
        return predict
        
        
class PositionalEncoding(nn.Module):

    def __init__(self, d_model: int, dropout: float = 0.1, max_len: int = 5000):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(max_len, 1, d_model)
        pe[:, 0, 0::2] = torch.sin(position * div_term)
        pe[:, 0, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x: Tensor) -> Tensor:
        """
        Arguments:
            x: Tensor, shape ``[seq_len, batch_size, embedding_dim]``
        """
        x_permute = x.permute(1, 0, 2)
        x = x_permute + self.pe[:x_permute.size(0)]
        output = x.permute(1, 0, 2)
        print(output.shape)
        return self.dropout(output)