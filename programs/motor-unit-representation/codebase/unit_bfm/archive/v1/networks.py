"""Exact UFO-simple layer contract; independent Actor, F1, F2 and B."""
import torch
from torch import nn


def embedding(n):
    return nn.Sequential(nn.Linear(n, 256), nn.LayerNorm(256), nn.Tanh(),
                         nn.Linear(256, 128), nn.ReLU())


class Actor(nn.Module):
    def __init__(self):
        super().__init__()
        self.embed_s = embedding(336)
        self.embed_z = embedding(352)
        self.head = nn.Sequential(nn.Linear(256, 256), nn.ReLU(), nn.Linear(256, 1), nn.Tanh())

    def context(self, x):
        return self.embed_s(x)

    def forward(self, x, z):
        return self.head(torch.cat((self.embed_s(x), self.embed_z(torch.cat((x, z), -1))), -1))


class ForwardMap(nn.Module):
    def __init__(self):
        super().__init__()
        self.embed_sa = embedding(337)
        self.embed_z = embedding(352)
        self.head = nn.Sequential(nn.Linear(256, 256), nn.ReLU(), nn.Linear(256, 16))

    def forward(self, x, u, z):
        return self.head(torch.cat((self.embed_sa(torch.cat((x, u), -1)),
                                    self.embed_z(torch.cat((x, z), -1))), -1))


class BackwardMap(nn.Sequential):
    def __init__(self):
        super().__init__(nn.Linear(25, 256), nn.LayerNorm(256), nn.Tanh(),
                         nn.Linear(256, 256), nn.ReLU(), nn.Linear(256, 16))


class Networks(nn.Module):
    def __init__(self):
        super().__init__()
        self.actor = Actor()
        self.f1, self.f2 = ForwardMap(), ForwardMap()
        self.b = BackwardMap()

    def counts(self):
        counts = {k: sum(p.numel() for p in v.parameters()) for k, v in self.named_children()}
        counts['online'] = sum(counts.values())
        counts['execution'] = counts['actor'] + counts['b']
        return counts
