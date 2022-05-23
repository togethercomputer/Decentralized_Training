import torch


class SeqClassification(torch.nn.Module):
    def __init__(self, model_dim, num_classes):
        super(SeqClassification, self).__init__()
        self.model_dim = model_dim
        self.num_classes = num_classes
        self.pooler_layer = torch.nn.Linear(model_dim, model_dim)
        self.fc_layer = torch.nn.Linear(model_dim, num_classes)

    def forward(self, hidden_states, pooler_index=0):
        pooled = hidden_states[:, pooler_index, :]
        pooled = self.pooler_layer(pooled)
        pooled = torch.tanh(pooled)
        return self.fc_layer(pooled)


class Seq2SeqClassification(torch.nn.Module):
    def __init__(self, vocab_size, model_dim, layer_norm_eps=1e-5, ):
        super(Seq2SeqClassification, self).__init__()
        self.ln_f = torch.nn.LayerNorm(model_dim, eps=layer_norm_eps)
        self.lm_head = torch.nn.Linear(model_dim, vocab_size, bias=False)

    def forward(self, x, input_ids=None):
        x = self.ln_f(x)
        x = self.lm_head(x)
        return x
