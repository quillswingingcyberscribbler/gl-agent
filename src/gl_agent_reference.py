#!/usr/bin/env python3
"""Independent GL-Agent audit implementation, reconstructed 2026-10-22.

This is a new implementation of equations in the supplied v1.0 manuscript.
It is not the original supplement cited by that manuscript. Python >=3.10,
standard library only; optional --plots needs Matplotlib. Never edits Excel.
Copyright (c) 2026 Matthias Muhlert. SPDX-License-Identifier: MIT
"""
from __future__ import annotations
import argparse
import csv
import dataclasses
import json
import math
from pathlib import Path
import random
import sys
import xml.etree.ElementTree as ET
import zipfile


@dataclasses.dataclass(frozen=True)
class Parameters:
    lam: float = 40
    q0: float = .2
    loss: float = 50000
    gamma: float = .35
    cash: float = 20000
    tax: float = 30000
    hmax: float = .8
    kappa: float = .5
    load: float = 800
    capacity: float = 2000
    smooth: float = 600
    displacement: float = 8000
    benefit: float = 1500000

    @property
    def r0(self): return self.lam * self.q0 * self.loss
    @property
    def burden(self): return self.cash + self.tax

    def validate(self):
        values = dataclasses.asdict(self)
        if any(isinstance(v, bool) or not isinstance(v,(int,float)) or not math.isfinite(v) for v in values.values()):
            raise ValueError('All model inputs must be finite real numbers.')
        if any(v < 0 for v in values.values()): raise ValueError('Model inputs must be nonnegative.')
        if not 0 <= self.q0 <= 1 or not 0 <= self.hmax <= 1: raise ValueError('q0 and hmax must be in [0,1].')
        if self.smooth <= 0: raise ValueError('Fatigue smoothness must be positive.')
        if self.burden <= 0: raise ValueError('cash + tax must be positive.')


DEFAULT = Parameters()
PRESETS = {
    'Summarization': Parameters(25,.3,80000,.3,10000,25000,.6,.4,1500,2500,450,15000,600000),
    'MCP DevOps': Parameters(60,.25,400000,.45,25000,20000,.75,.6,400,1500,300,5000,2500000),
    'Finance': Parameters(15,.15,1200000,.5,40000,45000,.85,.7,200,1000,250,3000,3000000),
    'Drafting': Parameters(10,.35,5000,.3,8000,12000,.4,.3,600,800,150,20000,150000),
    'High-loss / smooth': dataclasses.replace(DEFAULT,loss=250000),
    'High-loss / steep': dataclasses.replace(DEFAULT,loss=250000,smooth=250),
}


def legacy(x: float,p: Parameters=DEFAULT) -> dict[str,float]:
    """Equations (19)-(21), with exactly the workbook's exponent clipping."""
    q = p.q0 * math.exp(-p.gamma*x)
    alerts = p.load*x
    detection = p.hmax * -math.expm1(-p.kappa*x)
    fatigue = 1/(1+math.exp(min(700,max(-700,(alerts-p.capacity)/p.smooth))))
    h = detection*fatigue
    attack = p.lam*q*p.loss*(1-h)
    d = p.displacement*x*x
    risk = attack+d
    cash = p.cash*x
    tax = p.tax*x
    delivered = p.benefit-tax
    h_prime = p.hmax*(p.kappa*math.exp(-p.kappa*x)*fatigue
                   -(-math.expm1(-p.kappa*x))*p.load/p.smooth*fatigue*(1-fatigue))
    r_prime = p.lam*q*p.loss*(-p.gamma*(1-h)-h_prime)+2*p.displacement*x
    return dict(x=x,q=q,alerts=alerts,detection=detection,fatigue=fatigue,h=h,
                attack=attack,displacement=d,risk=risk,cash=cash,tax=tax,
                delivered=delivered,welfare=delivered-risk-cash,burden=cash+tax,
                h_prime=h_prime,r_prime=r_prime,w_prime=-r_prime-p.burden)


def q_only(p: Parameters=DEFAULT) -> tuple[float,float,float]:
    p.validate()
    x = math.log(p.gamma*p.r0/p.burden)/p.gamma if p.gamma*p.r0>p.burden else 0.
    return x,p.r0*math.exp(-p.gamma*x),(p.burden*x/p.r0 if p.r0 else 0.)


def bisect(fn,left,right,tol=1e-12):
    fl,fr=fn(left),fn(right)
    if fl==0:return left
    if fr==0:return right
    if fl*fr>0:raise ValueError('Root is not bracketed.')
    for _ in range(150):
        mid=(left+right)/2;fm=fn(mid)
        if right-left<tol or fm==0:return mid
        if fl*fm<=0:right=mid
        else:left=mid;fl=fm
    return (left+right)/2


def roots(fn,left=0.,right=10.,step=.001):
    """Scan sign changes, then bisect; tangential roots are not guaranteed."""
    result=[];n=math.ceil((right-left)/step);a=left;fa=fn(a)
    for i in range(1,n+1):
        b=min(right,left+i*step);fb=fn(b)
        if fa==0:result.append(a)
        elif fa*fb<0:result.append(bisect(fn,a,b))
        a,fa=b,fb
    if fa==0:result.append(right)
    return sorted(set(result))


def extrema(p:Parameters):
    p.validate()
    wr=roots(lambda x:legacy(x,p)['w_prime'])
    rr=roots(lambda x:legacy(x,p)['r_prime'])
    wx=max([0.,10.]+wr,key=lambda x:legacy(x,p)['welfare'])
    rx=min([0.,10.]+rr,key=lambda x:legacy(x,p)['risk'])
    return {'welfare_x':wx,'risk_x':rx,'welfare':legacy(wx,p)['welfare'],
            'risk_at_welfare':legacy(wx,p)['risk'],'minimum_risk':legacy(rx,p)['risk'],
            'welfare_stationary':wr,'risk_stationary':rr,
            'search_interval':[0,10],'root_scan_step':.001}


def bounded(x,r0=400000.,substitute=800000.,gamma=.5,rho=.1,k=20000.,benefit=1500000.):
    share=math.exp(-rho*x);governed=r0*math.exp(-gamma*x)
    risk=share*governed+(1-share)*substitute
    derivative=rho*substitute*share-(gamma+rho)*r0*math.exp(-(gamma+rho)*x)
    return dict(x=x,share=share,governed=governed,risk=risk,welfare=benefit-risk-k*x,r_prime=derivative,burden=k*x)


def bounded_risk_minimum(r0,substitute,gamma,rho):
    if min(r0,substitute,gamma,rho)<=0:raise ValueError('Closed form needs positive r0, substitute, gamma and rho.')
    return max(0.,math.log((gamma+rho)*r0/(rho*substitute))/gamma)


def avoided_loss(t,efficacy,decay,rate,r0=400000.):
    if min(t,efficacy,decay,rate,r0)<0 or efficacy>1:raise ValueError('Invalid durability domain.')
    total=decay+rate
    return r0*efficacy*(-math.expm1(-total*t)/total if total else t)


def joint_failure(n,q,beta):
    if isinstance(n,bool) or not isinstance(n,int) or n<1 or not 0<=q<=1 or not 0<=beta<=1:
        raise ValueError('Require integer n >= 1, q and beta in [0,1].')
    return (1-beta)*q**n+beta*q


def refresh_value(chi,interval=.5,rate=.1,kappa=.5,effort=4.,r0=400000.,efficacy=.95,initial=20000.,cost=5000.):
    """Appendix C discounted infinite series, truncated at <1e-13 weight."""
    if not 0<=chi<=1 or interval<=0 or rate<=0:raise ValueError('Invalid refresh domain.')
    delta=kappa*effort;cycle=(1-math.exp(-(rate+delta)*interval))/(rate+delta)
    carried=0.;series=0.;n=0
    while True:
        term=math.exp(-rate*n*interval-kappa*carried)
        series+=term
        if math.exp(-rate*n*interval)<1e-13:break
        carried=chi*(carried+effort*interval);n+=1
    gross=r0*efficacy*cycle*series
    refresh_cost=cost*math.exp(-rate*interval)/(1-math.exp(-rate*interval))
    return gross,gross-initial-refresh_cost


def read_cached(path):
    """Read cached cell values directly from OOXML, never import/save workbook."""
    ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
    with zipfile.ZipFile(path) as z:
        shared=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            shared=[''.join(s.itertext()) for s in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        rel={r.attrib['Id']:r.attrib['Target'] for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        wb=ET.fromstring(z.read('xl/workbook.xml'));out={}
        for sh in wb.findall('s:sheets/s:sheet',ns):
            target=rel[sh.attrib['{'+ns['r']+'}id']]
            target=target.lstrip('/') if target.startswith('/') else 'xl/'+target
            cells={}
            for c in ET.fromstring(z.read(target)).findall('.//s:sheetData/s:row/s:c',ns):
                v=c.find('s:v',ns);value=v.text if v is not None else None;t=c.attrib.get('t','n')
                if t=='s' and value is not None:value=shared[int(value)]
                elif t=='inlineStr':value=''.join(c.find('s:is',ns).itertext())
                elif t=='n' and value is not None:value=float(value)
                cells[c.attrib['r']]=value
            out[sh.attrib['name']]=cells
        return out


def check_workbook(path):
    data=read_cached(path);comparisons=[];failures=[];max_scaled=0.;worst=None
    def check(sheet,cell,expected):
        nonlocal max_scaled,worst
        actual=data.get(sheet,{}).get(cell)
        if isinstance(expected,(int,float)):
            passed=isinstance(actual,(int,float)) and math.isclose(actual,expected,rel_tol=1e-10,abs_tol=1e-7)
            scaled=abs(actual-expected)/max(1.,abs(expected)) if isinstance(actual,(int,float)) else math.inf
            if scaled>max_scaled:max_scaled=scaled;worst=f'{sheet}!{cell}'
        else:passed=actual==expected
        comparisons.append((sheet,cell,actual,expected,passed))
        if not passed:failures.append({'sheet':sheet,'cell':cell,'actual':actual,'expected':expected})
    # Freeze the publication parameters independently of the workbook inputs.
    # A modified workbook is not expected to pass these publication regressions.
    for r,v in zip(range(9,22),dataclasses.astuple(DEFAULT)):check('Dashboard',f'C{r}',v)
    grid=[legacy(i/100) for i in range(1001)]
    keys=['x','q','alerts','detection','fatigue','h','attack','displacement','risk','cash','tax','delivered','welfare','burden','h_prime','r_prime','w_prime']
    for i,row in enumerate(grid,2):
        for col,key in zip('ABCDEFGHIJKLMNOPQ',keys):check('Curves',f'{col}{i}',row[key])
    wx=max(grid,key=lambda r:r['welfare']);rx=min(grid,key=lambda r:r['risk']);qx,qr,qs=q_only()
    dash={'C27':DEFAULT.r0,'C28':DEFAULT.burden,'C30':qx,'C31':qr,'C32':wx['x'],'C33':rx['x'],'C34':wx['attack'],'C35':wx['displacement'],'C36':qs,'C38':wx['burden']/DEFAULT.r0,'C39':wx['welfare'],'C40':0.,'C42':legacy(2)['welfare'],'C43':legacy(2)['risk'],'I9':legacy(2)['fatigue'],'I10':legacy(2)['detection'],'I11':legacy(2)['h'],'I12':legacy(2)['h_prime'],'I13':legacy(2)['r_prime'],'I14':legacy(2)['w_prime']}
    for cell,value in dash.items():check('Dashboard',cell,value)
    check('Dashboard','I15','VALID')
    for j,(name,p) in enumerate(PRESETS.items()):
        col=chr(ord('C')+j)
        for r,v in zip(range(6,19),dataclasses.astuple(p)):check('Examples',f'{col}{r}',v)
        rows=[legacy(i/100,p) for i in range(1001)]
        bestw=max(rows,key=lambda r:r['welfare']);bestr=min(rows,key=lambda r:r['risk']);qx,qr,qs=q_only(p)
        for r,v in [(20,p.r0),(21,p.burden),(23,qx),(24,qs),(25,bestw['x']),(26,bestr['x'])]:check('Examples',f'{col}{r}',v)
        for i,row in enumerate(rows,2):
            if j==0:check('ScenarioCurves',f'A{i}',row['x'])
            check('ScenarioCurves',f'{chr(ord("B")+2*j)}{i}',row['welfare'])
            check('ScenarioCurves',f'{chr(ord("C")+2*j)}{i}',row['risk'])
    for i in range(501):
        t=i/100;a=avoided_loss(t,.95,2,.1);b=avoided_loss(t,.6,.3,.1)
        for col,v in [('B',t),('C',a),('D',b),('E',int(t>0 and b>a))]:check('Durability',f'{col}{i+20}',v)
    for cell,v in [('C12',.62),('C13',400000*.95/2.1),('C14',600000)]:check('Durability',cell,v)
    for n in range(1,11):
        risk=joint_failure(n,.1,.1);prev=joint_failure(n-1,.1,.1) if n>1 else risk
        for col,v in [('C',risk),('D',.1/risk),('E',10),('F',prev/risk)]:check('Stacking',f'{col}{n+10}',v)
    check('Stacking','C8',10)
    bg=[bounded(i/100) for i in range(1001)]
    for i,row in enumerate(bg,25):
        for col,key in zip('BCDEFGH',['x','share','governed','risk','welfare','r_prime','burden']):check('BoundedMigration',f'{col}{i}',row[key])
    br=bounded_risk_minimum(400000,800000,.5,.1)
    for cell,v in [('C15',br),('C16',min(bg,key=lambda r:r['risk'])['x']),('C17',max(bg,key=lambda r:r['welfare'])['x']),('C18',160000),('C19',1100000),('C20',800000)]:check('BoundedMigration',cell,v)
    for r in range(6,18):check('Verification',f'F{r}','PASS')
    return {'comparison_count':len(comparisons),'failed_count':len(failures),'max_scaled_difference':max_scaled,'worst_cell':worst,'failures':failures,'scope':'Publication input/default caches, main curves and presets, durability, stacking, bounded migration. This is not Excel-engine recalculation.'}


def verification():
    tests=[]
    def add(name,ok,detail=''):tests.append({'test':name,'passed':bool(ok),'detail':detail})
    ex=extrema(DEFAULT);hi=extrema(PRESETS['High-loss / smooth']);steep=extrema(PRESETS['High-loss / steep'])
    add('Default continuous welfare optimum',abs(ex['welfare_x']-1.446034)<1e-6,ex['welfare_x'])
    add('Default continuous risk minimum',abs(ex['risk_x']-2.057115)<1e-6,ex['risk_x'])
    add('High-loss smooth extrema',abs(hi['welfare_x']-2.588029)<1e-6 and abs(hi['risk_x']-5.685050)<1e-6,hi)
    add('High-loss steep three stationary welfare points',len(steep['welfare_stationary'])==3 and abs(steep['welfare_x']-2.023920)<1e-6,steep)
    wr=steep['welfare_stationary'];p=PRESETS['High-loss / steep']
    add('Early steep welfare maximum dominates later maximum',legacy(wr[0],p)['welfare']>legacy(wr[-1],p)['welfare'])
    xs=[.05,.5,1.8,3.5,7.4];der_errors=[]
    for p in [DEFAULT,*PRESETS.values()]:
        for x in xs:
            h=1e-5;numeric=(legacy(x+h,p)['risk']-legacy(x-h,p)['risk'])/(2*h);analytic=legacy(x,p)['r_prime']
            der_errors.append(abs(numeric-analytic)/max(1.,abs(analytic)))
    add('Risk derivative finite-difference agreement',max(der_errors)<1e-6,max(der_errors))
    add('Welfare accounting identity',all(abs(legacy(x)['welfare']+legacy(x)['risk']+DEFAULT.burden*x-DEFAULT.benefit)<1e-8 for x in xs))
    add('Zero-risk q-only corner',q_only(dataclasses.replace(DEFAULT,lam=0))==(0.,0.,0.))
    add('Zero-productivity q-only corner',q_only(dataclasses.replace(DEFAULT,gamma=0))==(0.,400000.,0.))
    add('Exact q-only entry threshold',q_only(dataclasses.replace(DEFAULT,gamma=.125))[0]==0)
    corner=dataclasses.replace(DEFAULT,hmax=0,displacement=0)
    add('Full family nests q-only family',abs(extrema(corner)['welfare_x']-q_only(corner)[0])<1e-8)
    br=bounded_risk_minimum(400000,800000,.5,.1);bw=bisect(lambda x:bounded(x)['r_prime']+20000,0,br)
    add('Bounded migration analytic minimum',abs(br-2*math.log(3))<1e-12,br)
    add('Bounded welfare precedes risk minimum',0<bw<br and abs(bw-1.679110)<1e-6,bw)
    add('Bounded initial threshold corner',bounded_risk_minimum(400000,3000000,.5,.1)==0)
    add('Bounded migration accounting identity',all(abs(bounded(x)['risk']-(bounded(x)['share']*bounded(x)['governed']+(1-bounded(x)['share'])*800000))<1e-8 for x in xs))
    cap=dataclasses.replace(DEFAULT,gamma=2,displacement=0)
    add('Capacity crossing does not force risk reversal',all(legacy(i/100,cap)['r_prime']<0 for i in range(1001)))
    cross=bisect(lambda t:avoided_loss(t,.95,2,.1)-avoided_loss(t,.6,.3,.1),.01,2)
    add('Durability crossover',.618<cross<.620,cross)
    add('Zero-discount and zero-decay finite-horizon limit',avoided_loss(3,.5,0,0)==600000)
    add('Zero-efficacy durability value',avoided_loss(3,0,0,0)==0)
    add('Independent layer limit',all(math.isclose(joint_failure(n,.1,0),.1**n) for n in range(1,11)))
    add('Fully common layer limit',all(joint_failure(n,.1,1)==.1 for n in range(1,11)))
    add('Stacking zero/one risk boundaries',joint_failure(5,0,.1)==0 and joint_failure(5,1,.1)==1)
    add('Perfect refresh reset formula',math.isclose(refresh_value(0)[0],400000*.95*(1-math.exp(-2.1*.5))/(2.1*(1-math.exp(-.1*.5))),rel_tol=1e-12))
    add('Complete carry-over refresh limit',math.isclose(refresh_value(1)[0],400000*.95/2.1,rel_tol=1e-12))
    add('Refresh partial carry-over bounded by endpoints',refresh_value(1)[0]<refresh_value(.5)[0]<refresh_value(0)[0])
    rng=random.Random(20261022);exp_ratios=[];hyp_ratios=[]
    for _ in range(500):
        r=[10**rng.uniform(2,6) for _ in range(rng.randint(1,6))];g=[10**rng.uniform(-2,1) for _ in r];k=10**rng.uniform(2,6)
        for family,ratios in [('exp',exp_ratios),('hyperbolic',hyp_ratios)]:
            productivity=lambda x:sum(ri*gi*(math.exp(-gi*x) if family=='exp' else 1/(1+gi*x)**2) for ri,gi in zip(r,g))-k
            if productivity(0)<=0:x=0
            else:
                upper=1.
                while productivity(upper)>0:upper*=2
                x=bisect(productivity,0,upper)
            ratios.append(k*x/sum(r))
    add('500 heterogeneous exponential all-in bounds',max(exp_ratios)<=1/math.e+1e-9,max(exp_ratios))
    add('500 heterogeneous hyperbolic all-in bounds',max(hyp_ratios)<=.25+1e-9,max(hyp_ratios))
    # Risk reversal can never be inferred from mean review effectiveness alone.
    sign_ok=True
    for _ in range(500):
        r0=10**rng.uniform(2,6);u=10**rng.uniform(2,6);g=10**rng.uniform(-2,1);rho=10**rng.uniform(-2,1)
        x=bounded_risk_minimum(r0,u,g,rho)
        if x>0:
            # Factor out exp(-rho*x)>0: extreme draws otherwise underflow
            # both true derivatives to zero despite opposite analytic signs.
            bracket=lambda at:rho*u-(g+rho)*r0*math.exp(-g*at)
            sign_ok &= bracket(x*.9)<0 and bracket(x*1.1)>0
        else:sign_ok &= bounded(0,r0,u,g,rho)['r_prime']>=-1e-8
    add('500 bounded migration sign cases',sign_ok)
    invalid=0
    for change in [{'smooth':0},{'q0':1.1},{'lam':-1},{'cash':0,'tax':0},{'lam':None},{'lam':float('nan')}]:
        try:dataclasses.replace(DEFAULT,**change).validate()
        except (ValueError,TypeError):invalid+=1
    add('Invalid input rejection',invalid==6)
    add('Robust two-control complementarity example',100-100-30<0 and 100-0-60==40)
    return tests


def write_csv(path,rows):
    if not rows:return
    with path.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=Path('results'))
    parser.add_argument('--check-workbook',type=Path)
    parser.add_argument('--plots',action='store_true',help='Requires Matplotlib, otherwise all operations use standard library.')
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    tests=verification();summaries=[];curves=[]
    for name,p in {'Retained default':DEFAULT,**PRESETS}.items():
        result=extrema(p);summaries.append({'scenario':name,**result})
        curves.extend({'scenario':name,**legacy(i/100,p)} for i in range(1001))
    bounded_rows=[bounded(i/100) for i in range(1001)]
    write_csv(args.out/'numerical_results.csv',summaries)
    write_csv(args.out/'curve_results.csv',curves)
    write_csv(args.out/'bounded_results.csv',bounded_rows)
    write_csv(args.out/'verification_results.csv',tests)
    params={'provenance':'Independent reconstruction from supplied GL-Agent paper and simulator on 2026-10-22. All presets synthetic; not recovered original supplement.','default':dataclasses.asdict(DEFAULT),'presets':{name:dataclasses.asdict(p) for name,p in PRESETS.items()}}
    (args.out/'parameters.json').write_text(json.dumps(params,indent=2)+'\n')
    result={'implementation':'independent-audit-2026-10-22','tests':len(tests),'failed':sum(not t['passed'] for t in tests),'numerical_results':summaries}
    if args.check_workbook:result['workbook']=check_workbook(args.check_workbook)
    (args.out/'verification_summary.json').write_text(json.dumps(result,indent=2)+'\n')
    if args.plots:
        try:import matplotlib.pyplot as plt
        except ImportError:parser.error('--plots requires Matplotlib; rerun without it for standard-library outputs.')
        fig,ax=plt.subplots(figsize=(9,5));ax.plot([r['x'] for r in bounded_rows],[r['risk'] for r in bounded_rows]);ax.set(xlabel='Control intensity',ylabel='Annual realized risk',title='Bounded migration (synthetic)');fig.tight_layout();fig.savefig(args.out/'bounded-migration.png',dpi=180);plt.close(fig)
        fig,ax=plt.subplots(figsize=(9,5))
        for name in ['High-loss / smooth','High-loss / steep']:
            rows=[r for r in curves if r['scenario']==name];ax.plot([r['x'] for r in rows],[r['welfare'] for r in rows],label=name)
        ax.set(xlabel='Control intensity',ylabel='Annual welfare',title='Alternative welfare shapes (synthetic)');ax.legend();fig.tight_layout();fig.savefig(args.out/'welfare.png',dpi=180);plt.close(fig)
        fig,ax=plt.subplots(figsize=(9,5));horizons=[i/100 for i in range(501)]
        ax.plot(horizons,[avoided_loss(t,.95,2,.1) for t in horizons],label='Initial efficacy 0.95; decay 2/year');ax.plot(horizons,[avoided_loss(t,.6,.3,.1) for t in horizons],label='Initial efficacy 0.60; decay 0.3/year');ax.set(xlabel='Years',ylabel='Gross discounted avoided loss',title='Durability (synthetic, control costs excluded)');ax.legend();fig.tight_layout();fig.savefig(args.out/'durability.png',dpi=180);plt.close(fig)
    print(json.dumps({k:v for k,v in result.items() if k!='numerical_results'},indent=2))
    return int(result['failed']>0 or result.get('workbook',{}).get('failed_count',0)>0)


if __name__=='__main__':sys.exit(main())
