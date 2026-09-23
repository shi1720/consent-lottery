"""Deterministic vector figures and manuscript tables from saved results."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT=Path(__file__).resolve().parents[1]
FIG=ROOT/'paper/figures';FIG.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.labelsize':9,
    'axes.titlesize':10,'legend.fontsize':8,'xtick.labelsize':8,'ytick.labelsize':8,
    'pdf.fonttype':42,'ps.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,
    'savefig.facecolor':'white'})
NAVY='#17324d';TEAL='#087e8b';ORANGE='#cc6f21';RED='#b1455d';GRAY='#84929e';PURPLE='#7755a3'


def save(fig,name):
    fig.savefig(FIG/(name+'.pdf'),bbox_inches='tight',pad_inches=.05)
    fig.savefig(FIG/(name+'.png'),dpi=220,bbox_inches='tight',pad_inches=.05)
    plt.close(fig)


def pipeline():
    fig,ax=plt.subplots(figsize=(7,2.65));ax.set(xlim=(0,10),ylim=(0,4));ax.axis('off')
    boxes=[(.1,2.1,2.5,1.45,'Public menu',r'$e_j\subseteq N,\quad v_j\geq0$',NAVY),
           (3.1,2.1,3,1.45,'Public lottery',r'$Aw\leq\delta,\quad\mathbf{1}^{T}w\leq1$',TEAL),
           (6.7,2.1,3.1,1.45,'One draw + veto',r'Execute $j$ only if $e_j\in\mathcal{F}(x)$',NAVY)]
    for x,y,w,h,title,detail,color in boxes:
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.04,rounding_size=.08',lw=1,ec=color,fc='#f4f7fa'))
        ax.text(x+w/2,y+h*.7,title,ha='center',va='center',weight='bold',color=color)
        ax.text(x+w/2,y+h*.31,detail,ha='center',va='center',fontsize=10)
    for x1,x2 in [(2.65,3.03),(6.15,6.63)]:
        ax.add_patch(FancyArrowPatch((x1,2.8),(x2,2.8),arrowstyle='-|>',mutation_scale=12,color=GRAY))
    ax.text(1.35,1.35,'Public design stage',ha='center',color=GRAY)
    ax.text(4.6,1.35,'No current private bits',ha='center',color=GRAY)
    ax.annotate('Contract ID or abstention',xy=(8.25,2.02),xytext=(8.25,1.3),ha='center',
                arrowprops={'arrowstyle':'<-','color':GRAY},color=NAVY)
    ax.text(5,.25,'One agent changing its bit can affect at most its incident lottery mass.',ha='center',fontsize=10,color=NAVY)
    save(fig,'01-lottery')


def cycle_graph(ax,weights,withdraw=False):
    angles=np.pi/2+np.arange(5)*2*np.pi/5
    pts=np.c_[np.cos(angles),np.sin(angles)]
    edges=[(0,1),(1,2),(2,3),(3,4),(4,0)]
    event={0,2,4}
    for j,(i,k) in enumerate(edges):
        p,q=pts[i],pts[k]
        color=RED if j in event else TEAL
        ax.plot([p[0],q[0]],[p[1],q[1]],color=color,lw=2.8,ls='--' if weights[j]==0 else '-')
        mid=(p+q)*.54
        ax.text(mid[0],mid[1],weights[j],ha='center',va='center',fontsize=10,
                bbox={'facecolor':'white','edgecolor':'none','pad':1.2},color=color)
    for i,p in enumerate(pts):
        ax.scatter([p[0]],[p[1]],s=300,c=['#eceff2' if withdraw and i==0 else '#ffffff'],edgecolors=NAVY,zorder=5)
        ax.text(p[0],p[1],str(i+1),ha='center',va='center',zorder=6,color=NAVY)
    ax.set(xlim=(-1.28,1.28),ylim=(-1.12,1.3),aspect='equal');ax.axis('off')


def obstruction():
    fig,axs=plt.subplots(1,2,figsize=(7,3.15))
    cycle_graph(axs[0],['1/2']*5)
    cycle_graph(axs[1],[0,'1',0,'1',0],True)
    axs[0].set_title('Full profile: pointwise optimum',color=NAVY)
    axs[1].set_title('Agent 1 unavailable: pointwise optimum',color=NAVY)
    axs[0].text(0,-1.22,r'Red event: $3\delta/2$',ha='center',color=RED,fontsize=10)
    axs[1].text(0,-1.22,'Red event: 0',ha='center',color=RED,fontsize=10)
    fig.text(.5,.01,r'Edge labels show probability / $\delta$.  The two optimal rows violate every finite-$\epsilon$ guarantee.',ha='center',fontsize=8)
    save(fig,'02-obstruction')


def frontier():
    rows=json.loads((ROOT/'data/raw/cycle.json').read_text())
    fig,ax=plt.subplots(figsize=(3.45,2.95))
    hs=np.array([25/12,2.5]);ws=np.array([1.75,1.5])
    ax.plot(hs,ws,lw=2.3,color=NAVY,label=r'Exact frontier, $\epsilon=0$')
    ax.scatter(hs,ws,c=NAVY,s=35,zorder=4)
    for e,color,label in [(np.log(2),TEAL,r'LP, $\epsilon=\log 2$'),(np.log(10),ORANGE,r'LP, $\epsilon=\log 10$')]:
        points=sorted(set((round(r['full_success']/.1,8),round(r['withdrawal_success']/.1,8)) for r in rows if abs(r['epsilon']-e)<1e-8))
        points=[p for p in points if not any(q[0]>=p[0]-1e-7 and q[1]>=p[1]-1e-7 and (q[0]>p[0]+1e-7 or q[1]>p[1]+1e-7) for q in points)]
        ax.plot(*np.array(points).T,'o--',ms=4,color=color,lw=1.3,label=label)
    ax.scatter([2.5],[2],marker='x',s=55,lw=1.7,c=RED,zorder=5)
    ax.annotate('Separate row optima',xy=(2.5,2),xytext=(1.66,2.085),fontsize=8,color=RED,
                arrowprops={'arrowstyle':'-','color':RED,'lw':.8})
    ax.set(xlabel=r'Full-profile success $h/\delta$',ylabel=r'Mean withdrawal success $w/\delta$',
           xlim=(1.6,2.56),ylim=(1.44,2.14))
    ax.grid(alpha=.15);ax.legend(loc='lower left',frameon=False,fontsize=7.2)
    save(fig,'03-frontier')


def benchmark():
    rows=json.loads((ROOT/'data/raw/benchmark.json').read_text())
    fig,axs=plt.subplots(1,2,figsize=(7,2.65),sharey=True)
    for ax,q in zip(axs,[.5,.8]):
        z=[r for r in rows if r['q']==q and r['delta']==.1 and r['epsilon']==0]
        for i,(key,color,label) in enumerate([('uniform',GRAY,'Uniform'),('static',TEAL,'Fixed LP'),('adaptive',NAVY,'Adaptive LP'),('pointwise_upper',ORANGE,'Row bound')]):
            values=np.array([r[key]*100 for r in z]);jitter=np.linspace(-.15,.15,len(values))
            ax.scatter(i+jitter,values,s=11,alpha=.45,c=color,linewidths=0)
            ax.plot([i-.2,i+.2],[values.mean()]*2,color=color,lw=3)
        ax.set_xticks(range(4),['Uniform','Fixed LP','Adaptive LP','Row bound'])
        ax.set_title(r'Availability prior $q='+str(q)+r'$',color=NAVY)
        ax.grid(axis='y',alpha=.16)
    axs[0].set_ylabel('Expected agreement probability (%)')
    fig.tight_layout(w_pad=1.2)
    save(fig,'04-benchmark')
    table=[r'\begin{tabular}{ccrrrr}',r'\toprule',r'$q$ & $\epsilon$ & Uniform & Fixed LP & Adaptive LP & Row bound \\',r'\midrule']
    stats=[]
    for q in (.5,.8):
        for epsilon in (0.,float(np.log(2))):
            z=[r for r in rows if r['q']==q and r['delta']==.1 and r['epsilon']==epsilon]
            means={k:float(np.mean([r[k] for r in z])) for k in ('uniform','static','adaptive','pointwise_upper')}
            e='0' if epsilon==0 else r'\log 2'
            table.append(f'{q:.1f} & ${e}$ & '+' & '.join(f'{100*means[k]:.2f}' for k in means)+r' \\')
            differences=[r['adaptive']-r['static'] for r in z]
            stats.append({'q':q,'epsilon':epsilon,'means':means,'adaptive_minus_fixed_mean':float(np.mean(differences)),
                          'difference_min':min(differences),'difference_max':max(differences),
                          'strictly_better':sum(x>1e-8 for x in differences)})
    table.extend([r'\bottomrule',r'\end{tabular}'])
    (ROOT/'paper/benchmark-table.tex').write_text('\n'.join(table)+'\n')
    (ROOT/'data/processed/summary.json').write_text(json.dumps(stats,indent=2))


if __name__=='__main__':
    pipeline();obstruction();frontier();benchmark()
    print('Generated four vector figures and a result table.')
