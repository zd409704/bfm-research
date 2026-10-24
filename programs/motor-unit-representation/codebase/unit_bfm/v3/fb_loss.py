"""Unmodified FB estimator with explicit transition-row discounts."""
import torch


def fb_loss(forwards,backward,target_density,discount,pair_mask=None):
    n = backward.shape[0]
    if n < 2 or forwards.shape != (2,n,backward.shape[-1]) or backward.ndim != 2:
        raise ValueError('Expected forwards [2,N,D], backward [N,D], N>=2')
    if target_density.shape != (n,n) or discount.shape != (n,1):
        raise ValueError('Expected target [N,N] and row discount [N,1]; [N] is ambiguous')
    if not torch.isfinite(discount).all() or torch.any((discount<0)|(discount>1)):
        raise ValueError('Discount outside [0,1]')
    mask = 1-torch.eye(n,device=backward.device,dtype=backward.dtype)
    if pair_mask is not None:
        # B03 configuration-matched pairs. Cross-config entries are not a reference.
        if pair_mask.shape != (n,n):
            raise ValueError('pair_mask must be [N,N]')
        mask = mask * pair_mask.to(dtype=mask.dtype, device=mask.device)
        if float(mask.sum()) <= 0:
            raise ValueError('INSUFFICIENT_SUPPORT: no matched off-diagonal pairs')
    density = forwards @ backward.T
    diff = density-discount.detach().reshape(1,n,1)*target_density.detach()
    offdiag = .5*(diff*mask).square().sum()/mask.sum()
    positive = -diff.diagonal(dim1=-2,dim2=-1).mean()*2
    gram = backward @ backward.T
    orth = .5*(gram*mask).square().sum()/mask.sum()-gram.diag().mean()
    return offdiag+positive+orth,offdiag,positive,orth


def actor_loss(forwards,z):
    return -(forwards*z).sum(-1).min(dim=0).values.mean()


def sample_action(mean,std=.2,clip=.3,generator=None):
    noise = torch.randn(mean.shape,dtype=mean.dtype,device=mean.device,generator=generator)*std
    if clip is not None:
        noise = noise.clamp(-clip,clip)
    value = mean+noise
    bounded = value.clamp(-1+1e-6,1-1e-6)
    return value-value.detach()+bounded.detach()
