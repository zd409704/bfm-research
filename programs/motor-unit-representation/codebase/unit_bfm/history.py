"""One causal assembler for live control and raw 100 Hz Replay.

raw is [..., 22, 24], ending at current control boundary n. Negative
episode indices are padding. No resampling phase is inferred from chunk start.
"""
import torch


def assemble(raw, n, m):
    n = torch.as_tensor(n, device=raw.device, dtype=torch.long)
    batch = raw.shape[0]
    rows = torch.arange(batch, device=raw.device)[:, None]
    k = n - n.remainder(2)
    endpoints = k[:, None] + torch.arange(-18, 1, 2, device=raw.device)
    idx = 21 + endpoints - n[:, None]
    end = raw[rows, idx]
    prev = raw[rows, idx - 1]
    slow = end.clone()
    slow[..., 12:14] = (end[..., 12:14] + prev[..., 12:14]) * .5
    slow[..., 14:16] = torch.maximum(end[..., 14:16], prev[..., 14:16])
    slow[..., 18:24] = (end[..., 18:24] + prev[..., 18:24]) * .5
    valid = endpoints >= 2
    slow = slow * valid[..., None]
    age = ((n[:, None] - endpoints) * .05) * valid
    slow = torch.cat((slow, (~valid)[..., None], age[..., None]), -1)
    fast_idx = torch.arange(14, 22, device=raw.device)
    fast_valid = n[:, None] + torch.arange(-7, 1, device=raw.device) >= 1
    fast = raw[:, fast_idx][..., [13, 12]] * fast_valid[..., None]
    fast = torch.cat((fast, (~fast_valid)[..., None]), -1)
    return torch.cat((raw[:, -1], m, slow.flatten(1), fast.flatten(1)), -1)


class History:
    def __init__(self, nworld, device):
        self.raw = torch.zeros(nworld, 22, 24, device=device)
        self.n = torch.zeros(nworld, dtype=torch.long, device=device)

    def reset(self, o, ids=None):
        if ids is None:
            self.raw.zero_(); self.n.zero_(); self.raw[:, -1] = o
        else:
            self.raw[ids] = 0; self.n[ids] = 0; self.raw[ids, -1] = o

    def append(self, o):
        self.raw[:, :-1] = self.raw[:, 1:].clone()
        self.raw[:, -1] = o
        self.n += 1

    def input(self, m):
        return assemble(self.raw, self.n, m)
