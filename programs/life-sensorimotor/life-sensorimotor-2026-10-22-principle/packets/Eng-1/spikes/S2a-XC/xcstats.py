"""Clopper-Pearson bounds and divergence floor (numpy only, no scipy)."""
import math
import numpy as np


def _binom_cdf(k, n, p):
    """P(X <= k), X ~ Bin(n, p), exact sum in log space."""
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    if p <= 0.0:
        return 1.0
    if p >= 1.0:
        return 0.0
    j = np.arange(0, k + 1)
    lg = np.array([math.lgamma(x + 1.0) for x in (n, )])[0]
    lc = lg - np.array([math.lgamma(x + 1.0) for x in j]) - np.array(
        [math.lgamma(n - x + 1.0) for x in j])
    lp = lc + j * math.log(p) + (n - j) * math.log1p(-p)
    m = lp.max()
    return float(min(1.0, math.exp(m) * np.exp(lp - m).sum()))


def cp_upper(k, n, level):
    """One-sided upper bound: P(X<=k | p_U) = level."""
    if k >= n:
        return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if _binom_cdf(k, n, mid) > level:
            lo = mid
        else:
            hi = mid
    return hi


def cp_lower(k, n, level):
    """One-sided lower bound: P(X>=k | p_L) = level."""
    if k <= 0:
        return 0.0
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if 1.0 - _binom_cdf(k - 1, n, mid) < level:
            lo = mid
        else:
            hi = mid
    return lo


def dbits(a, b):
    """Binary KL d(a||b) in bits, 0<b<a<=1 assumed by caller; else 0."""
    if not (a > b):
        return 0.0
    t1 = a * math.log2(a / b)
    t2 = 0.0 if a >= 1.0 else (1 - a) * math.log2((1 - a) / (1 - b))
    return t1 + t2
