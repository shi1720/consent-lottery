"""Standalone rational checker of the analytic C5 frontier.

Deliberately imports neither NumPy, scipy nor the implementation package.
Enumerates every output event; verifies probabilities and sharp witnesses.
"""
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path

CONTRACTS = (3, 6, 12, 24, 17)


def mechanism(delta, kind):
    rows=[]
    for profile in range(32):
        feasible=[j for j,c in enumerate(CONTRACTS) if c & profile == c]
        weights=[F(0)]*5
        if kind=='full':
            for j in feasible: weights[j]=delta/2
        else:
            if len(feasible)==1: weights[feasible[0]]=delta
            elif len(feasible)==2:
                for j in feasible: weights[j]=delta/2
            elif len(feasible)==3:
                for j in feasible:
                    neighbors=sum(bool(CONTRACTS[j]&CONTRACTS[l]) for l in feasible if l!=j)
                    weights[j]=delta*((0 if neighbors==2 else 1) if kind=='relaxed'
                                      else (F(1,4) if neighbors==2 else F(3,4)))
            elif len(feasible)==5:
                weights=[delta*(F(1,3) if kind=='relaxed' else F(5,12))]*5
        rows.append([1-sum(weights)]+weights)
    return rows


def verify(P,delta,multiplier=1):
    checked=0;worst=F(0)
    for x in range(32):
        assert sum(P[x])==1 and min(P[x])>=0
        for j,c in enumerate(CONTRACTS):
            if c&x != c: assert P[x][j+1]==0
        for i in range(5):
            y=x^(1<<i)
            for event in range(64):
                diff=sum(P[x][j]-multiplier*P[y][j] for j in range(6) if event&(1<<j))
                assert diff<=delta
                worst=max(worst,diff);checked+=1
    return checked,worst


def run():
    rows=[]
    for delta in (F(1,100),F(1,10),F(2,5)):
        A=mechanism(delta,'full');B=mechanism(delta,'withdrawal')
        for t in (F(i,20) for i in range(21)):
            P=[[t*a+(1-t)*b for a,b in zip(ar,br)] for ar,br in zip(A,B)]
            count,worst=verify(P,delta)
            h=1-P[31][0]
            w=sum(1-P[31^(1<<i)][0] for i in range(5))/5
            assert h==t*5*delta/2+(1-t)*25*delta/12
            assert w==t*3*delta/2+(1-t)*7*delta/4
            assert w==3*delta-3*h/5
            rows.append({'delta':str(delta),'mixture':str(t),'full':str(h),'withdrawal':str(w),
                         'events_checked':count,'max_divergence':str(worst)})
    relaxed=[]
    for delta in (F(1,100),F(1,10),F(2,5)):
        P=mechanism(delta,'relaxed');count,worst=verify(P,delta,2)
        h=1-P[31][0];w=sum(1-P[31^(1<<i)][0] for i in range(5))/5
        assert h==5*delta/3 and w==2*delta
        relaxed.append({'delta':str(delta),'full':str(h),'withdrawal':str(w),
                        'events_checked':count,'max_divergence':str(worst)})
    dest=Path(__file__).resolve().parents[1]/'data/processed/exact-cycle.json'
    dest.write_text(json.dumps({'mechanisms':len(rows),'event_inequalities':sum(r['events_checked'] for r in rows),
                               'rows':rows,'relaxed_mechanisms':relaxed},indent=2))
    print(len(rows),'rational mechanisms;',sum(r['events_checked'] for r in rows),'event inequalities')

if __name__=='__main__':run()
