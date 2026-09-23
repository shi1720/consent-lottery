"""Exact rational, one-use sampler for a fixed public contract lottery.

The broker is trusted. This process-local prototype controls one output, not
timing, network traffic, durable restarts, or the correctness of consent inputs.
"""
from fractions import Fraction
from functools import reduce
from math import gcd
import secrets
from threading import Lock


class OneShotBroker:
    def __init__(self, menu, weights, delta):
        self.menu = menu
        self.weights = tuple(Fraction(w) for w in weights)
        ds = tuple(Fraction(d) for d in delta)
        if len(self.weights) != len(menu.contracts) or len(ds) != menu.n:
            raise ValueError('dimension mismatch')
        if min(self.weights) < 0 or sum(self.weights) > 1 or min(ds) < 0 or max(ds) > 1:
            raise ValueError('invalid rational distribution or budget')
        for i in range(menu.n):
            load = sum(w for w,c in zip(self.weights,menu.contracts) if c & (1<<i))
            if load > ds[i]:
                raise ValueError('participation budget exceeded')
        self.denominator = reduce(lambda a,b:a*b//gcd(a,b),
                                  (w.denominator for w in self.weights),1)
        self.counts = tuple(int(w*self.denominator) for w in self.weights)
        self._used=False
        self._lock=Lock()

    def select(self, private_profile, *, randbelow=secrets.randbelow):
        """Return a zero-based public contract index or None; never retry vetoes."""
        if not isinstance(private_profile,int) or not 0 <= private_profile < 2**self.menu.n:
            raise ValueError('invalid profile')
        with self._lock:
            if self._used:
                raise RuntimeError('this one-output session has already been consumed')
            self._used=True
            draw=randbelow(self.denominator)
            if not isinstance(draw,int) or not 0 <= draw < self.denominator:
                raise ValueError('random source returned an invalid draw')
            for j,(count,contract) in enumerate(zip(self.counts,self.menu.contracts)):
                if draw < count:
                    return j if contract & private_profile == contract else None
                draw-=count
            return None
