"""Read-only independent result checker; no package or solver imports."""
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def check_rows(P, contracts, n, multiplier, delta, rational):
    convert=(lambda v:F(float(v)).limit_denominator(10**8)) if rational else float
    P=[[convert(v) for v in row] for row in P]
    d=F(str(delta)) if rational else delta
    multiplier=F(round(multiplier)) if rational else multiplier
    tol=0 if rational else 1e-8
    worst=0
    for x,row in enumerate(P):
        assert abs(sum(row)-1)<=tol and min(row)>=-tol
        for j,c in enumerate(contracts):
            required=[i for i in range(n) if (c//2**i)%2]
            if not all((x//2**i)%2 for i in required): assert abs(row[j+1])<=tol
        for i in range(n):
            y=x+2**i if (x//2**i)%2==0 else x-2**i
            value=sum(max(0,p-multiplier*q) for p,q in zip(row,P[y]))
            assert value<=d+tol,(x,y,value,d)
            worst=max(worst,float(value-d))
    return worst


def main():
    summary={'suites':{},'sha256':{}}
    for suite,n in [('exhaustive',3),('cycle',5),('benchmark',6)]:
        path=ROOT/f'data/raw/{suite}.json'
        rows=json.loads(path.read_text());worst=0
        for r in rows:
            contracts=r.get('contracts',[3,6,12,24,17])
            delta=r.get('delta',.1)
            worst=max(worst,check_rows(r['P'],contracts,n,math.exp(r['epsilon']),delta,suite=='exhaustive'))
            if suite=='exhaustive':
                cert=r['certificate'];w=list(map(F,cert['weights']));y=list(map(F,cert['dual']))
                assert min(w+y)>=0 and sum(w)<=1
                for i in range(n):
                    assert sum(v for v,c in zip(w,contracts) if (c//2**i)%2)<=F(str(delta))
                for c in contracts:
                    assert sum(y[i] for i in range(n) if (c//2**i)%2)+y[-1]>=1
                assert sum(w)==F(str(delta))*sum(y[:-1])+y[-1]==F(cert['value'])
                assert abs(float(sum(w))-r['global'])<1e-8
            elif suite=='benchmark':
                q=r['q']
                expected=sum((q**bin(x).count('1'))*((1-q)**(n-bin(x).count('1')))*(1-r['P'][x][0]) for x in range(2**n))
                assert abs(expected-r['adaptive'])<1e-8
                assert r['uniform']<=r['static']+1e-8<=r['adaptive']+2e-8
                assert r['adaptive']<=r['pointwise_upper']+1e-8
        summary['suites'][suite]={'records':len(rows),'rational_dp_verified':suite=='exhaustive','max_privacy_excess':worst}
        summary['sha256'][suite]=hashlib.sha256(path.read_bytes()).hexdigest()
    (ROOT/'data/processed/verification.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
