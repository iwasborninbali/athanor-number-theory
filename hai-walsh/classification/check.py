#!/usr/bin/env python3
"""Independent stdlib-only arithmetic/exhaustion checker.

This imports no search code or Sage/PARI. It verifies witnesses, congruence
exclusions, changes of MW basis, torsion by good reductions, and exhausts the
finite coefficient boxes and small-coordinate intervals supplied by Sage.
The rank upper bounds, saturation-index bounds and elliptic-logarithm bounds
remain trusted certified computations; this is not a formal verifier for them.
"""
from fractions import Fraction as F
from math import gcd, isqrt
from pathlib import Path
import argparse, hashlib, itertools, json, time

ROOT=Path(__file__).resolve().parent

class Curve:
    def __init__(self,a,b):self.a,self.b=a,b
    def on(self,p):
        return p is None or p[1]**2==p[0]**3+self.a*p[0]**2+self.b*p[0]
    def add(self,p,q):
        if p is None:return q
        if q is None:return p
        x,y=p;u,v=q
        if x==u:
            if y+v==0:return None
            lam=(3*x*x+2*self.a*x+self.b)/(2*y)
        else:lam=(v-y)/(u-x)
        w=lam*lam-self.a-x-u
        return w,lam*(x-w)-y
    def mul(self,n,p):
        if n<0:return self.mul(-n,None if p is None else (p[0],-p[1]))
        ans=None
        while n:
            if n&1:ans=self.add(ans,p)
            p=self.add(p,p);n//=2
        return ans
    def translate_torsion(self,p):
        if p is None:return F(0),F(0)
        x,y=p
        if not x:return None
        return self.b/x,-self.b*y/(x*x)

def point(coords):
    x,y,z=map(F,coords)
    if not z:
        assert x==0 and y!=0
        return None
    return x/z,y/z

def determinant(m):
    m=[list(map(F,r)) for r in m]
    ans=F(1)
    for i in range(len(m)):
        k=next((k for k in range(i,len(m)) if m[k][i]),None)
        if k is None:return 0
        if k!=i:m[i],m[k]=m[k],m[i];ans=-ans
        p=m[i][i];ans*=p
        for j in range(i+1,len(m)):
            c=m[j][i]/p
            for k in range(i+1,len(m)):m[j][k]-=c*m[i][k]
    return ans

def poly_sum(*polys):
    out=[0]*max(map(len,polys))
    for p in polys:
        for i,c in enumerate(p):out[i]+=c
    return out

def poly_product(p,q):
    out=[0]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):out[i+j]+=a*b
    return out

def primes(limit):
    for p in range(3,limit+1,2):
        if all(p%d for d in range(3,isqrt(p)+1,2)):yield p

def torsion_bound(curve):
    """Rational torsion injects into good reductions at odd primes."""
    disc=16*curve.b*curve.b*(curve.a*curve.a-4*curve.b)
    bound=0;used=[]
    for p in primes(300):
        if disc%p==0:continue
        squares={u*u%p for u in range(1,p)}
        count=1
        for x in range(p):
            f=(x*x*x+curve.a*x*x+curve.b*x)%p
            count+=1 if f==0 else (2 if f in squares else 0)
        bound=gcd(bound,count);used.append((p,count))
        if bound==2:return bound,used
    raise AssertionError(('could not certify torsion order 2',used))

def finite_points(curve,basis,bound,interval):
    """Exhaust the entire integer coefficient box using exact fractions."""
    found=set()
    def use(p):
        if p is not None and p[0].denominator==1:
            assert p[1].denominator==1
            found.add((int(p[0]),int(p[1])))
    # Include the independently exhaustive small-U interval.
    lo,hi=interval
    for u in range(lo,hi+1):
        v2=u*u*u+curve.a*u*u+curve.b*u
        if v2<0:continue
        v=isqrt(v2)
        if v*v==v2:found.update(((u,v),(u,-v)))
    multiples=[]
    for p in basis:
        pos=[None]
        for _ in range(bound):pos.append(curve.add(pos[-1],p))
        multiples.append([None if q is None else (q[0],-q[1]) for q in reversed(pos[1:])]+pos)
    visited=0
    def walk(i,p):
        nonlocal visited
        if i==len(multiples):
            use(p);use(curve.translate_torsion(p));visited+=1
            return
        for q in multiples[i]:walk(i+1,curve.add(p,q))
    walk(0,None)
    assert visited==(2*bound+1)**len(basis)
    return found,visited

def check_manifest():
    name=ROOT/'certificates/SHA256SUMS'
    if not name.exists():return 0
    n=0
    for line in name.read_text().splitlines():
        expected,path=line.split('  ',1)
        actual=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
        assert actual==expected,('SHA-256 mismatch',path)
        n+=1
    return n

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--quick',action='store_true',help='skip exact finite MW exhaustion; still check all witnesses and residue exclusions')
    ap.add_argument('--y',type=int,help='check one y only')
    args=ap.parse_args()
    start=time.monotonic()
    hashes=check_manifest()
    cert=json.loads((ROOT/'certificates/classification.json').read_text())
    assert cert['domain']==dict(y_min=1,y_max=100,x_min=2,z_min=1)
    assert len(cert['curves'])==200
    assert {(r['y'],r['sign']) for r in cert['curves']}==set(itertools.product(range(1,101),[-1,1]))
    solutions=[];methods={};open_cases=[];boxes=0;done=0
    for row in sorted(cert['curves'],key=lambda r:(r['y']!=4,r['y'],r['sign'])):
        y,s,d=row['y'],row['sign'],row['D']
        if args.y is not None and y!=args.y:continue
        assert d==y*y+1 and row['ainvs']==[0,2*s*d,0,d*(d+1),0]
        method=row['method'];methods[method]=methods.get(method,0)+1
        curve=Curve(2*s*d,d*(d+1))
        assert -64*d**3*(d+1)**2<0 # nonsingular, one real component
        if method=='open':
            open_cases.append((y,s));continue
        if method=='congruence_exclusion':
            assert s==1
            m=row['modulus'];assert m in [3,8]
            squares={x*x%m for x in range(m)}
            # Every integer z has exactly one of these residue classes.
            assert all((d*(z*z+s)**2+1)%m not in squares for z in range(m))
            assert row['solutions']==[]
            continue
        assert method=='elliptic_integral_points'
        rank=row['rank']
        assert row['rank_bounds']==[rank,rank] and row['field_certifications']==[1,1]
        assert row['saturation_success'] is True and row['unsaturated_primes']==[]
        assert row['saturation_index']>=1
        base=list(map(point,row['basis']));new=list(map(point,row['lll_basis']))
        assert len(base)==len(new)==rank and all(p is not None and curve.on(p) for p in base+new)
        change=row['basis_change']
        assert len(change)==rank and all(len(r)==rank for r in change)
        assert abs(determinant(change))==1
        for i in range(rank):
            p=None
            for j in range(rank):p=curve.add(p,curve.mul(change[j][i],base[j]))
            assert p==new[i],('basis change',y,s,i)
        torsion=list(map(point,row['torsion']))
        assert set(torsion)=={None,(F(0),F(0))}
        assert curve.add((F(0),F(0)),(F(0),F(0))) is None
        assert torsion_bound(curve)[0]==2
        pts=list(map(point,row['integral_points']))
        assert len(pts)==len(set(pts)) and None not in pts
        expected=set()
        for p in pts:
            assert curve.on(p) and all(c.denominator==1 for c in p)
            u,v=map(int,p);expected.add((u,v))
            assert u>=0
        assert all((u,-v) in expected for u,v in expected)
        if not args.quick:
            actual,n=finite_points(curve,new,row['coefficient_bound'],row['small_x_interval'])
            assert actual==expected,('finite point enumeration differs',y,s,actual^expected)
            boxes+=n
        # Independently apply the inverse map to every recorded integral point.
        recovered=[]
        for u,v in sorted(expected):
            if u<=0 or v<=0 or u%d:continue
            z=isqrt(u//d)
            if z==0 or z*z!=u//d or v%(d*z):continue
            x=v//(d*z)
            if x<=1:continue
            assert x*x-1==d*(z*z+s)**2
            assert u==d*z*z and v==d*x*z
            family=(x==2*y*y+1 and z*z+s==2*y)
            recovered.append(dict(x=x,y=y,z=z,sign=s,known_family=family))
        key=lambda p:(p['x'],p['z'])
        assert sorted(recovered,key=key)==sorted(row['solutions'],key=key)
        solutions.extend(recovered)
        done+=1
        if done%20==0:print(f'Checked {done} elliptic curves, {boxes} exact MW combinations, {time.monotonic()-start:.1f}s',flush=True)
    filtered=[r for r in cert['solutions'] if args.y is None or r['y']==args.y]
    key=lambda r:(r['y'],r['sign'],r['z'],r['x'])
    assert sorted(solutions,key=key)==sorted(filtered,key=key)
    assert json.loads((ROOT/'certificates/solutions.json').read_text())==cert['solutions']
    # Symbolic map identity, with z^2 denoted t, is exact coefficient equality:
    # F(Dt) = D^2*t*(D*t^2+2sD*t+D+1).
    for y in range(1,101):
        d=y*y+1
        for s in [-1,1]:
            u=[0,d]
            lhs=poly_sum(poly_product(u,poly_product(u,u)),
                         poly_product([2*s*d],poly_product(u,u)),
                         poly_product([d*(d+1)],u))
            rhs=poly_product([0,d*d],[d+1,2*s*d,d])
            assert lhs==rhs
        # Exceptional U=0 would have z=0, which is outside the domain;
        # even that quartic point would require a square y^2+2.
        assert y*y<y*y+2<(y+1)*(y+1)
    err=json.loads((ROOT/'certificates/source_errata.json').read_text())
    t=err['test_parameter']
    assert err['printed_triple']==[4*t**3-2*t,t,2*t]
    assert err['corrected_triple']==[4*t**3-3*t,t,2*t]
    x,y,z=err['printed_triple']
    assert all(x*x-1!=(y*y-1)*(z*z+s)**2 for s in [-1,1])
    x,y,z=err['corrected_triple']
    assert x*x-1==(y*y-1)*(z*z-1)**2
    # Verify the corrected family as a polynomial identity for every t.
    a=[0,-3,0,4]
    assert poly_sum(poly_product(a,a),[-1])==poly_product([-1,0,1],poly_product([-1,0,4],[-1,0,4]))
    print(json.dumps(dict(result='PASS',sha256_files=hashes,methods=methods,
          witnesses=len(solutions),open_cases=open_cases,exact_mw_combinations=boxes,
          finite_exhaustion=not args.quick,seconds=round(time.monotonic()-start,3))),flush=True)
    print('Unbounded completeness uses the stated PARI/eclib/Sage rank, saturation and height-bound dependencies.')

if __name__=='__main__':main()
