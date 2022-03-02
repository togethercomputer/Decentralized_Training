import torch
import math
from torch import nn
from torch.nn import functional
from torch.utils.checkpoint import checkpoint
from transformers.modeling_outputs import (
    BaseModelOutputWithPastAndCrossAttentions,
    CausalLMOutputWithCrossAttentions,
)
from transformers.models.gpt2.modeling_gpt2 import GPT2Attention as _GPT2Attention
from transformers.models.gpt2.modeling_gpt2 import GPT2MLP as _GPT2MLP
from transformers.models.gpt2.modeling_gpt2 import GPT2Block as _GPT2Block
from transformers.models.gpt2.modeling_gpt2 import GPT2Model as _GPT2Model
from transformers.models.gpt2.modeling_gpt2 import GPT2LMHeadModel as _GPT2LMHeadModel
from transformers.models.gpt2.configuration_gpt2 import GPT2Config as GPTConfig

# @torch.jit.script
def gpt_loss_func(input, target):
    lm_logits, labels = input, target
    shift_logits = lm_logits[..., :-1, :].contiguous()
    shift_labels = labels[..., 1:].contiguous()
    loss = functional.cross_entropy(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1))
    return loss

class GPTEmbeddings(nn.Module):
    def __init__(self, config):
        super().__init__()
        
        self.config = config
        self.embed_dim = config.hidden_size
        self.wte = nn.Embedding(config.vocab_size, self.embed_dim)
        self.wpe = nn.Embedding(config.max_position_embeddings, self.embed_dim)
        self.drop = nn.Dropout(config.embd_pdrop)
        
    def forward(self, input_ids):
        
        device = input_ids.device
        
        # input ids
        input_shape = input_ids.size()
        input_ids = input_ids.view(-1, input_shape[-1])
        batch_size = input_ids.shape[0]
        
        # position ids
        position_ids = torch.arange(0, input_shape[-1], dtype=torch.long, device=device)
        position_ids = position_ids.unsqueeze(0).view(-1, input_shape[-1])
            
        inputs_embeds = self.wte(input_ids)
        position_embeds = self.wpe(position_ids)
        hidden_states = inputs_embeds + position_embeds

        hidden_states = self.drop(hidden_states)
        
        return hidden_states
    

class GPTBlock(_GPT2Block):
    def __init__(self, *args, use_checkpoint=True, **kargs):
        super().__init__(*args, **kargs)
        self.use_checkpoint = use_checkpoint
        
        def attn_res(x: torch.Tensor) -> torch.Tensor:
            res = x
            x = self.ln_1(x)
            x = self.attn(x)[0]
            return x + res
        self.attn_res = attn_res
        
        def mlp_res(x: torch.Tensor) -> torch.Tensor:
            res = x
            x = self.ln_2(x)
            x = self.mlp(x)[0]
            return x + res
        self.mlp_res = mlp_res

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if self.use_checkpoint:
            x.requires_grad_(True)
            x = checkpoint(self.attn_res, x)
        else:
            x = self.attn_res(x)
        if self.use_checkpoint:
            x.requires_grad_(True)
            x = checkpoint(self.mlp_res, x)
        else:
            x = self.mlp_res(x)
        return x
    
    
class GPTModel(_GPT2Model):
    def __init__(self, config):
        super(_GPT2Model, self).__init__(config)

        self.embed_dim = config.hidden_size
        
        emb_layer = GPTEmbeddings(config)
        self.wte = emb_layer.wte
        self.wpe = emb_layer.wpe
        self.emb_layer = emb_layer

        self.drop = nn.Dropout(config.embd_pdrop)
        self.h = nn.ModuleList([GPTBlock(config, layer_idx=i, use_checkpoint=True) for i in range(config.num_hidden_layers)])
        self.ln_f = nn.LayerNorm(self.embed_dim, eps=config.layer_norm_epsilon)

        # Model parallel
        self.model_parallel = False
        self.device_map = None
        self.gradient_checkpointing = False

        # Initialize weights and apply final processing
        self.post_init()
        
    def forward(self, input_ids, attention_mask=None, **kargs):
        
        hidden_states = self.emb_layer(input_ids)
        for layer in self.h:
            hidden_states = layer(hidden_states)
        hidden_states = self.ln_f(hidden_states)
        
        return BaseModelOutputWithPastAndCrossAttentions(
            last_hidden_state=hidden_states,
            past_key_values=None,
            hidden_states=None,
            attentions=None,
            cross_attentions=None,
        )
    
class GPTLMHead(nn.Sequential):
    def __init__(self, config):
        super().__init__()
        self.ln_f = nn.LayerNorm(config.n_embd, eps=config.layer_norm_epsilon)
        self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)
    
class GPTLMHeadModel(_GPT2LMHeadModel):

    def __init__(self, config):
        super(_GPT2LMHeadModel, self).__init__(config)
        self.transformer = GPTModel(config)
        self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)
        # ln_f will be calculated in self.transformer

        self.init_weights()

        # Model parallel
        self.model_parallel = False
        self.device_map = None