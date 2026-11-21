import sys,json;sys.path.insert(0,'/tmp/rkw')
from fx import *
VAR=3
K=P(F["KSA"]);lat0=radians(K[0])
def xy(p):return ((p[1]-K[1])*60*cos(lat0),(p[0]-K[0])*60)
def ll(q):return [round(K[0]+q[1]/60,6),round(K[1]+q[0]/(60*cos(lat0)),6)]
def pol(b,d):return (d*sin(radians(b)),d*cos(radians(b)))
def add(a,b):return (a[0]+b[0],a[1]+b[1])
X={}
def turn(A,h0,h1,right,R=1.5,n=8):
  # returns points along a constant-radius turn starting at A heading h0 to h1
  s=1 if right else -1;c=add(A,pol(h0+90*s,R));pts=[];
  sw=((h1-h0)%360) if right else -((h0-h1)%360)
  for k in range(1,n+1):h=h0+sw*k/n;pts.append(add(c,pol(h-90*s,R)))
  return pts
def ray_circle(A,h,R):
  d=pol(h,1);b=2*(A[0]*d[0]+A[1]*d[1]);c=A[0]**2+A[1]**2-R*R;t=(-b+sqrt(b*b-4*c))/2;return add(A,(d[0]*t,d[1]*t))
def ray_radial(A,h,rb):
  d=pol(h,1);r=pol(rb,1);det=d[0]*(-r[1])+r[0]*d[1];t=(A[0]*r[1]-A[1]*r[0])/(-det) if False else None
  # solve A + t d = s r
  import numpy as np;M=np.array([[d[0],-r[0]],[d[1],-r[1]]]);t,s=np.linalg.solve(M,[-A[0],-A[1]]);return add(A,(d[0]*t,d[1]*t))
def arcpts(R,b0,b1,cw,n=None):
  sw=((b1-b0)%360) if cw else -((b0-b1)%360);n=n or max(6,int(abs(sw)/6));return [pol(b0+sw*k/n,R) for k in range(1,n)]
# 15L ILS Z: RWY HDG to 3.8 DME KSA, left HDG 107M to 7 DME arc, arc CCW to R037, then SISIR
A=ray_circle(xy(P(F["RW15L"])),150,3.8);T=turn(A,150,110,False);B=ray_circle(T[-1],110,7.0)
bB=(degrees(atan2(B[0],B[1]))+360)%360;C=pol(40,7.0)
m15L=[A]+T+[B]+arcpts(7.0,bB,40,False)+[C]
# 15R ILS Z / VOR 15R: 3.1 DME KSA, right turn to HDG 302M(305T), intercept R245(248T), out to 27.6, arc CW to PEDIR
A=pol(150,3.1);T=turn(A,150,305,True);B=ray_radial(T[-1],305,248);C=pol(248,27.6)
bP=(degrees(atan2(*xy(P(F["PEDIR"]))))+360)%360
m15R=[A]+T+[B,C]+arcpts(27.6,248,bP,True)
# 33R ILS Z: RWY HDG 330T until R082(085T), right turn, intercept R076(079T) to ORBON
A=ray_radial(xy(P(F["RW33R"])),330,85);T=turn(A,330,79,True,1.5,6)
m33R=[A]+T
def names(pfx,pts):
  r=[]
  for k,q in enumerate(pts):n="_%s%d"%(pfx,k);X[n]=ll(q);r.append(n)
  return r
M15L=names("a",m15L);M15R=names("b",m15R);M33R=names("c",m33R)
print(len(M15L),len(M15R),len(M33R),bB,bP)
json.dump({"X":X,"M15L":M15L,"M15R":M15R,"M33R":M33R},open('/tmp/rkw/ma.json','w'))
