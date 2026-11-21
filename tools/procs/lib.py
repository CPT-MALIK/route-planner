from math import *
import numpy as np,json
def P(s):
  a,b=s.split();f=lambda v,n:int(v[:n])+int(v[n:n+2])/60+float(v[n+2:-1])/3600;return f(a,2),f(b,3)
def PP(v):return tuple(v) if isinstance(v,(list,tuple)) else P(v)
def inv(a,b):
  la1,lo1=map(radians,a);la2,lo2=map(radians,b);dl=lo2-lo1
  y=sin(dl)*cos(la2);x=cos(la1)*sin(la2)-sin(la1)*cos(la2)*cos(dl)
  d=2*asin(sqrt(sin((la2-la1)/2)**2+cos(la1)*cos(la2)*sin(dl/2)**2))*3440.065
  return (degrees(atan2(y,x))+360)%360,d
class Geo:
  def __init__(s,F,ctr):s.F=F;s.K=PP(F[ctr]);s.c=cos(radians(s.K[0]));s.X={}
  def xy(s,n):p=PP(s.F[n]) if isinstance(n,str) else n;return ((p[1]-s.K[1])*60*s.c,(p[0]-s.K[0])*60)
  def ll(s,q):return [round(s.K[0]+q[1]/60,6),round(s.K[1]+q[0]/(60*s.c),6)]
  @staticmethod
  def pol(b,d):return (d*sin(radians(b)),d*cos(radians(b)))
  @staticmethod
  def add(a,b):return (a[0]+b[0],a[1]+b[1])
  def brg(s,q):return (degrees(atan2(q[0],q[1]))+360)%360
  def turn(s,A,h0,h1,right,R=1.5,n=8):
    sg=1 if right else -1;c=s.add(A,s.pol(h0+90*sg,R));sw=((h1-h0)%360) if right else -((h0-h1)%360)
    return [s.add(c,s.pol(h0+sw*k/n-90*sg,R)) for k in range(1,n+1)]
  def arcpts(s,R,b0,b1,cw):
    sw=((b1-b0)%360) if cw else -((b0-b1)%360);n=max(6,int(abs(sw)/6));return [s.pol(b0+sw*k/n,R) for k in range(1,n)]
  def names(s,pfx,pts):
    r=[]
    for k,q in enumerate(pts):n="_%s%d"%(pfx,k);s.X[n]=s.ll(q);r.append(n)
    return r
def check(F,ctr,var,legs,radials):
  bad=0
  for a,b,c,d in legs:
    t,dd=inv(PP(F[a]),PP(F[b]));flag=abs(((t-c+180)%360)-180)>1.5 or (d and abs(dd-d)>0.3);bad+=bool(flag)
    if flag:print(f"!! {a}->{b} {t:.1f}({c}) {dd:.2f}({d})")
  for n,r,dm in radials:
    t,dd=inv(PP(F[ctr]),PP(F[n]));m=(t-var)%360;flag=(r is not None and abs(((m-r+180)%360)-180)>1.5) or (dm and abs(dd-dm)>0.3);bad+=bool(flag)
    if flag:print(f"!! {ctr}->{n} R{m:.1f}({r}) {dd:.2f}({dm})")
  print("checks",len(legs)+len(radials),"bad",bad)
def fx(n,role="",alt="",note=""):return {"n":n,"role":role,"alt":alt,"note":note}
def tf(a,b,crs=None,dst=None,fin=0,alt=None):
  g={"t":"tf","a":a,"b":b}
  for k,v in (("crs",crs),("dst",dst),("alt",alt)):
    if v:g[k]=v
  if fin:g["fin"]=1
  return g
def arc(a,b,ccw,R,ctr,alt=""):return {"t":"arc","a":a,"b":b,"ctr":ctr,"R":R,"ccw":ccw,"alt":alt,"lbl":"%.1f DME ARC %s"%(R,ctr)}
def hold(f,inb,r,alt,ma=1,ln=4):return {"t":"hold","f":f,"inb":inb,"r":r,"len":ln,"alt":alt,"ma":ma}
def ma(*p):return {"t":"ma","pts":list(p)}
def emit(ap,src,F,X,var,L,path):
  FF=dict(F);FF.update(X)
  o={"src":src,"F":FF,"VAR":var,"list":L}
  open(path,'w').write("PROCS.%s="%ap+json.dumps(o,separators=(',',':'),ensure_ascii=False)+";\n");print(ap,len(L),"procs")
def insert(path):
  s=open('/home/claude/route-planner/index.html').read();js=open(path).read();ap=js[6:js.find('=')]
  assert 'PROCS.%s='%ap not in s
  i=s.find('const procP=n=>');s=s[:i]+js+s[i:];open('/home/claude/route-planner/index.html','w').write(s);print('inserted',ap)

def _autoarc(F,L):
  for pr in L:
    for g in pr["legs"]:
      if g["t"]=="arc" and g.get("ccw") is None:
        c=PP(F[g["ctr"]]);a=PP(F[g["a"]]) if not isinstance(F[g["a"]],list) else tuple(F[g["a"]]);b=PP(F[g["b"]]) if not isinstance(F[g["b"]],list) else tuple(F[g["b"]])
        b0=inv(c,a)[0];b1=inv(c,b)[0];g["ccw"]=((b1-b0)%360)>180
_emit0=emit
def emit(ap,src,F,X,var,L,path):
  FF=dict(F);FF.update(X);_autoarc(FF,L);return _emit0(ap,src,F,X,var,L,path)
def A(a,b,R,ctr,alt=""):return arc(a,b,None,R,ctr,alt)
class Apt:
  def __init__(s,F,ctr,var):s.F=F;s.var=var;s.G=Geo(F,ctr);s.ctr=ctr;s.n=0
  def rd(s,name,rad_m,R):s.F[name]=s.G.ll(s.G.pol(rad_m+s.var,R));return name
  def back(s,start,crs_m,dist,right,to=None):
    G=s.G;h=crs_m+s.var;A_=G.add(G.xy(start),G.pol(h,dist));T=G.turn(A_,h,(h+180)%360 if to is None else to+s.var,right,1.5,10);s.n+=1;return G.names("z%d_"%s.n,[A_]+T)
  def pt(s,rad_m,dist,pt_m,right):
    G=s.G;o=rad_m+s.var;A_=G.pol(o,dist);B=G.add(A_,G.pol(pt_m+s.var,3.0));T=G.turn(B,pt_m+s.var,(pt_m+180)%360+s.var,right,1.5,10);E=T[-1]
    h=(pt_m+180+s.var)%360;d=G.pol(h,1);r=G.pol(o,1);t,_=np.linalg.solve(np.array([[d[0],-r[0]],[d[1],-r[1]]]),[-E[0],-E[1]]);I=G.add(E,(d[0]*t,d[1]*t));s.n+=1
    return G.names("y%d_"%s.n,[A_,B]+T+[I])

def conv(ap,name,rwy,pg,fin,IF,FAF,MAPT,MAHF,info,iafs=(),pre=(),notes={},alts={},R=None,mright=True,hold_inb=None,hold_r=True,extra_fix=()):
  """generic: IAFs (on the IF's DME ring -> arc; else straight) to IF, IF->FAF->MAPT, missed straight ahead then back to MAHF and hold"""
  F=ap.F;c=PP(F[ap.ctr]);fixes=[];legs=list(pre)
  G=ap.G;P_=lambda n:PP(F[n]) if not isinstance(F[n],list) else tuple(F[n])
  join=IF
  if IF and R and abs(inv(c,P_(IF))[1]-R)>0.4:
    q=G.xy(IF);d=G.pol((fin+ap.var+180)%360,1);b=2*(q[0]*d[0]+q[1]*d[1]);cc=q[0]**2+q[1]**2-R*R;disc=b*b-4*cc
    if disc>=0:
      t=(-b+(disc**.5))/2;jn="J_%s_%d"%(IF,int(fin));G.X[jn]=G.ll((q[0]+d[0]*t,q[1]+d[1]*t));F[jn]=G.X[jn];join=jn
  joined=False
  for i in iafs:
    fixes.append(fx(i,"IAF",alts.get(i,""),notes.get(i,"")))
    if not IF:continue
    di=inv(c,P_(i))[1]
    if R and abs(di-R)<0.4:legs.append(A(i,join,R,ap.ctr,alts.get(i,"")));joined=True
    elif R and di>R+0.4:
      rb=inv(c,P_(i))[0];jn="K_%s"%i;G.X[jn]=G.ll(G.pol(rb,R));F[jn]=G.X[jn]
      legs.append(tf(i,jn));legs.append(A(jn,join,R,ap.ctr,alts.get(i,"")));joined=True
    else:legs.append(tf(i,IF))
  if join!=IF and joined:legs.append(tf(join,IF))
  for e in extra_fix:fixes.append(fx(e,"",alts.get(e,""),notes.get(e,"")))
  if IF:fixes.append(fx(IF,"IF",alts.get(IF,""),notes.get(IF,"")))
  if FAF:fixes.append(fx(FAF,"FAF",alts.get(FAF,""),notes.get(FAF,"")))
  fixes.append(fx(MAPT,"MAP","",notes.get(MAPT,"")))
  if MAHF!=MAPT:fixes.append(fx(MAHF,"MAHF",alts.get(MAHF,""),notes.get(MAHF,"")))
  tc="%03d°"%fin
  if IF and FAF:legs.append(tf(IF,FAF,tc,None,1))
  if FAF:legs.append(tf(FAF,MAPT,fin=1))
  mp=ap.back(MAPT,fin,3,mright)
  legs.append(ma(*([MAPT]+mp+[MAHF])))
  legs.append(hold(MAHF,fin if hold_inb is None else hold_inb,hold_r,alts.get(MAHF,"")))
  return {"n":name,"rwy":rwy,"pg":str(pg),"fin":fin,"fixes":fixes,"legs":legs,"ma":"Missed approach drawn simplified: climb ahead, then to %s and hold. Follow the chart text."%MAHF,"info":info}
def rnp(name,rwy,pg,fin,trans,final,mapn,mrest,alts,info,hold_at=None,hold_inb=None,hold_r=True):
  """trans: list of (pts list, courses list); final: (IF,FAF); mrest: missed fixes after MAP"""
  fixes=[];seen=set()
  def af(n,role=""):
    if n not in seen:seen.add(n);fixes.append(fx(n,role,alts.get(n,"")))
  legs=[]
  for pts,crs in trans:
    for k,n in enumerate(pts):af(n,"IAF" if k==0 else "")
    for k in range(1,len(pts)):legs.append(tf(pts[k-1],pts[k],crs[k-1] if crs else None))
  IF,FAF=final;af(IF,"IF");af(FAF,"FAF");af(mapn,"MAP")
  hf=hold_at or mrest[-1]
  for n in mrest:af(n,"MAHF" if n==hf else "")
  tc="%03d°"%fin;legs+=[tf(IF,FAF,tc,None,1),tf(FAF,mapn,tc,None,1),ma(*([mapn,["ahead",2]]+list(mrest))),hold(hf,fin if hold_inb is None else hold_inb,hold_r,alts.get(hf,""))]
  return {"n":name,"rwy":rwy,"pg":str(pg),"fin":fin,"fixes":fixes,"legs":legs,"ma":"Climb on %s, then via %s and hold at %s."%(tc," – ".join(mrest),hf),"info":info}
def ins(path):
  s=open('/home/claude/route-planner/index.html').read();js=open(path).read();ap=js[6:js.find('=')]
  i=s.find('PROCS.%s='%ap)
  if i>=0:j=s.find(';\n',i)+2;s=s[:i]+js+s[j:]
  else:k=s.find('const procP=n=>');s=s[:k]+js+s[k:]
  open('/home/claude/route-planner/index.html','w').write(s);print('ins',ap)
