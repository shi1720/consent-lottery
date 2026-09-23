"""Declared experiments; exact expectations, deterministic synthetic fixtures."""
import argparse
from fractions import Fraction
import hashlib
import json
import platform
from pathlib import Path
import time

import numpy as np
import scipy
from consent_lottery import Menu, packing, lottery, profile_prior, uniform_lottery, optimal_mechanism, audit

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw'
RAW.mkdir(exist_ok=True, parents=True)


def save(name, rows):
    path = RAW / (name + '.json')
    path.write_text(json.dumps(rows, indent=2))
    print(name, len(rows), 'records', flush=True)


def checked(menu, P, epsilon, delta, events=False):
    result = audit(menu, P, epsilon, delta, events)
    for key in ('max_privacy_excess', 'max_infeasible_mass', 'max_normalization_error', 'negative_mass', 'event_enumeration_disagreement'):
        if result[key] > 1e-7:
            raise AssertionError((key, result))
    return result


def rational_certificate(menu, delta, packed):
    """Exact weak-duality certificate after rational reconstruction.

    No reliance on a solver status: equality of feasible rational primal and
    dual proves the packing optimum for this finite instance.
    """
    F = lambda x: Fraction(float(x)).limit_denominator(1000000)
    w = list(map(F, packed['weights']))
    y = list(map(F, packed['dual']))
    d = F(delta)
    assert min(w + y) >= 0 and sum(w) <= 1
    for i in range(menu.n):
        assert sum(w[j] for j,c in enumerate(menu.contracts) if c & (1<<i)) <= d
    for j,c in enumerate(menu.contracts):
        assert sum(y[i] for i in range(menu.n) if c & (1<<i)) + y[-1] >= 1
    assert sum(w) == d*sum(y[:-1]) + y[-1]
    return {'weights': list(map(str,w)), 'dual': list(map(str,y)), 'value': str(sum(w))}


def exhaustive():
    rows = []
    for mask in range(1, 128):
        menu = Menu(3, tuple(c for c in range(1,8) if mask & (1<<(c-1))))
        prior = np.zeros(8); prior[-1] = 1
        for delta in (.01,.1,.4):
            packed = packing(menu, delta)
            certificate = rational_certificate(menu, delta, packed)
            fixed = lottery(menu, packed['weights'], delta)
            fixed_audit = checked(menu, fixed, 0, delta, True)
            for epsilon in (0., float(np.log(2))):
                result = optimal_mechanism(menu, epsilon, delta, prior)
                if abs(result['value'] - packed['value']) > 1e-7:
                    raise AssertionError('frontier mismatch')
                rows.append({'menu_mask':mask, 'contracts':list(menu.contracts),
                    'delta':delta,'epsilon':epsilon,'packing':packed['value'],
                    'global':result['value'],'certificate':certificate,
                    'P':result['P'].tolist(),'audit':checked(menu,result['P'],epsilon,delta,True),
                    'fixed_audit':fixed_audit})
        if mask % 32 == 0: print('exhaustive menu',mask,flush=True)
    save('exhaustive',rows)


def cycle():
    menu = Menu(5,(3,6,12,24,17))
    rows=[]
    for epsilon in (0.,float(np.log(2)),float(np.log(10))):
        for mix in np.linspace(0,1,21):
            prior=np.zeros(32);prior[-1]=mix
            for i in range(5): prior[31^(1<<i)]=(1-mix)/5
            result=optimal_mechanism(menu,epsilon,.1,prior)
            P=result['P']; h=1-P[31,0]
            w=np.mean([1-P[31^(1<<i),0] for i in range(5)])
            assert w <= .2-np.exp(-epsilon)*max(0,3*h/5-.1)+1e-7
            rows.append({'epsilon':epsilon,'mix':float(mix),'full_success':float(h),
                         'withdrawal_success':float(w),'objective':result['value'],
                         'P':P.tolist(),'audit':checked(menu,P,epsilon,.1)})
    save('cycle',rows)


def menus():
    candidates=[c for c in range(1,64) if bin(c).count('1') in (2,3)]
    for seed in range(24):
        rng=np.random.default_rng(27000+seed)
        yield seed,Menu(6,tuple(sorted(int(c) for c in rng.choice(candidates,size=8,replace=False))))


def benchmark():
    rows=[]
    for seed,menu in menus():
        feasible=np.array([menu.feasible(x) for x in range(64)])
        for delta in (.02,.1,.25):
            pointwise=np.array([packing(menu,delta,profile=x)['value'] for x in range(64)])
            for q in (.5,.8):
                prior=profile_prior(6,q)
                coeff=prior@feasible
                static=packing(menu,delta,values=coeff)
                U=lottery(menu,uniform_lottery(menu,delta),delta)
                L=lottery(menu,static['weights'],delta)
                checked(menu,U,0,delta);checked(menu,L,0,delta)
                for epsilon in (0.,float(np.log(2))):
                    start=time.perf_counter()
                    result=optimal_mechanism(menu,epsilon,delta,prior)
                    elapsed=time.perf_counter()-start
                    value=result['value']
                    ub=float(prior@pointwise)
                    assert value >= static['value']-1e-7 and value <= ub+1e-7
                    rows.append({'seed':seed,'contracts':list(menu.contracts),
                        'delta':delta,'epsilon':epsilon,'q':q,
                        'uniform':float(prior@(1-U[:,0])), 'static':static['value'],
                        'adaptive':value,'pointwise_upper':ub,'solve_seconds':elapsed,
                        'static_weights':static['weights'].tolist(), 'P':result['P'].tolist(),
                        'audit':checked(menu,result['P'],epsilon,delta)})
        print('benchmark menu',seed,flush=True)
    save('benchmark',rows)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('suite',choices=['exhaustive','cycle','benchmark','all']);args=parser.parse_args()
    start=time.time()
    manifest={'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
              'platform':platform.platform(),'suite':args.suite,'started_unix':start,
              'protocol_sha256':hashlib.sha256((ROOT/'notes/PROTOCOL.md').read_bytes()).hexdigest()}
    for suite,fn in [('exhaustive',exhaustive),('cycle',cycle),('benchmark',benchmark)]:
        if args.suite in ('all',suite):fn()
    manifest['wall_seconds']=time.time()-start
    (RAW/('manifest-'+args.suite+'.json')).write_text(json.dumps(manifest,indent=2))
