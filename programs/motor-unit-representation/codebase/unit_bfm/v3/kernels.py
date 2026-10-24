"""Device transport helpers for the audited batched solve pipeline.

Control/loading remains host evaluated in this reference batch backend. These
helpers copy complete arrays in place, avoiding stale CUDA graph pointers.
"""
import numpy as np


def assign_batch(device_array, values):
    import warp as wp
    host=np.ascontiguousarray(values,dtype=np.float32)
    if tuple(device_array.shape)!=tuple(host.shape[:device_array.ndim]):
        raise ValueError(f'batch shape mismatch: {device_array.shape}, {host.shape}')
    device_array.assign(wp.array(host,dtype=device_array.dtype,device=device_array.device))


def check_capacity(data,contact_capacity):
    n=int(data.nacon.numpy()[0])
    if n>int(data.naconmax): raise OverflowError('Warp global contact overflow: expand and recollect')
    if np.any(data.nefc.numpy()>data.njmax): raise OverflowError('Warp constraint overflow: expand and recollect')
    worlds=data.contact.worldid.numpy()[:n]
    if n and np.max(np.bincount(worlds.astype(int)))>contact_capacity:
        raise OverflowError('per-world privileged contact capacity exceeded')
    return n
