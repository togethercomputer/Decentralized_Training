import torch
import cupy
import numpy as np

from .utils import *


def topr(x, ratio):
    x_flat = x.view(-1)
    numel = x.numel()
    k = max(int(numel * ratio), 1)
    _, indexes = torch.topk(torch.abs(x_flat.data), k=k, sorted=False)
    masks = torch.zeros_like(x_flat, dtype=torch.bool)
    masks[indexes] = 1
    masks = masks.view(x.shape)
    values = x.data[masks]
    return values, masks

def topk(x, k, return_values=True):
    x_flat = x.view(-1)
    _, indexes = torch.topk(torch.abs(x_flat.data), k=k, sorted=False)
    masks = torch.zeros_like(x_flat, dtype=torch.bool)
    masks[indexes] = 1
    masks = masks.view(x.shape)
    if return_values:
        values = x.data[masks]
        return values, masks
    else:
        return masks

def compress_topk(x, k):
    values, masks = topk(x, k)
    masks = cupy_to_tensor(
        cupy.packbits(tensor_to_cupy(masks))
    )
    return values, masks

def decompress_topk(values, masks, original_shape):
    masks = cupy_to_tensor(
        cupy.unpackbits(tensor_to_cupy(masks))
    )
    x = torch.zeros(masks.shape, dtype=values.dtype, device=values.device)
    x[masks] = values
    x = x.view(original_shape)
    return x