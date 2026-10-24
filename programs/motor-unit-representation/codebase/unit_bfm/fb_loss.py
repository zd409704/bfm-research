"""Reference FB density loss; no environment reward enters these functions."""
import torch


def fb_loss(forwards, backward, target_density, discount=.99):
    """forwards [2,N,D], backward [N,D], stopped target_density [N,N]."""
    n = backward.shape[0]
    if n < 2:
        raise ValueError('FB independent-pair estimator requires N >= 2')
    mask = 1 - torch.eye(n, device=backward.device, dtype=backward.dtype)
    density = forwards @ backward.T
    diff = density - discount * target_density.detach()
    offdiag = .5 * (diff * mask).square().sum() / mask.sum()
    positive = -diff.diagonal(dim1=-2, dim2=-1).mean() * forwards.shape[0]
    gram = backward @ backward.T
    orth = .5 * (gram * mask).square().sum() / mask.sum() - gram.diag().mean()
    return offdiag + positive + orth, offdiag, positive, orth


def actor_loss(forwards, z):
    return -(forwards * z).sum(-1).min(dim=0).values.mean()


def sample_action(mean, std=.2, clip=.3):
    # Straight-through bound matches the reference truncated normal sampler.
    noise = torch.randn_like(mean) * std
    if clip is not None:
        noise = noise.clamp(-clip, clip)
    value = mean + noise
    bounded = value.clamp(-1 + 1e-6, 1 - 1e-6)
    return value - value.detach() + bounded.detach()
