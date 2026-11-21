import sys,json;sys.path.insert(0,'/tmp/maw')
from fx import *
import numpy as np
VAR=4;K=P(F["PMA"]);lat0=radians(K[0])
def xy(p):return ((p[1]-K[1])*60*cos(lat0),(p[0]-K[0])*60)
def ll(q):return [round(K[0]+q[1]/60,6),round(K[1]+q[0]/(60*cos(lat0)),6)]
def pol(b,d):return (d*sin(radians(b)),d*cos(radians(b)))
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def brgK(q):return (degrees(atan2(q[0],q[1]))+360)%360
def turn(A,h0,h1,right,R=1.5,n=8):
  s=1 if right else -1;c=add(A,pol(h0+90*s,R));sw=((h1-h0)%360) if right else -((h0-h1)%360)
  return [add(c,pol(h0+sw*k/n-90*s,R)) for k in range(1,n+1)]
def ray_radial(A,h,rb):
  d=pol(h,1);r=pol(rb,1);t,s=np.linalg.solve(np.array([[d[0],-r[0]],[d[1],-r[1]]]),[-A[0],-A[1]]);return add(A,(d[0]*t,d[1]*t))
def arcpts(R,b0,b1,cw):
  sw=((b1-b0)%360) if cw else -((b0-b1)%360);n=max(6,int(abs(sw)/6));return [pol(b0+sw*k/n,R) for k in range(1,n)]
X={}
def names(pfx,pts):
  r=[]
  for k,q in enumerate(pts):n="_%s%d"%(pfx,k);X[n]=ll(q);r.append(n)
  return r
G=brgK(xy(P(F["GERIR"])))
# 17/18: climb ahead (~3 NM), left turn to R148 (152T) outbound to 16 DME, arc CCW to GERIR
def ma17(start,crs):
  S=xy(P(F[start]));A=add(S,pol(crs,3.0));T=turn(A,crs,152,False);B=ray_radial(T[-1],152,152) if False else None
  # join R148: from end of turn fly 152T parallel then intercept: approximate by projecting onto radial
  E=T[-1];r=pol(152,1);proj=max(E[0]*r[0]+E[1]*r[1],4.0);J=pol(152,proj+1.5)
  return [A]+T+[J,pol(152,16)]+arcpts(16,152,G,False)
# 35/36: climb ahead to 5 DME PMA (or 3000 ft), right turn to R060 (064T) out to 16 DME, arc CW to GERIR
def ma35(start,crs,dme=5.0):
  S=xy(P(F[start]));A=pol(crs,dme) if dme else add(S,pol(crs,2.5));T=turn(A,crs,64+40,True);E=T[-1]
  r=pol(64,1);proj=max(E[0]*r[0]+E[1]*r[1],5);J=pol(64,proj+1.0)
  return [A]+T+[J,pol(64,16)]+arcpts(16,64,G,True)
M={"I17":names("p",ma17("RW17",169)),"V17":names("q",ma17("MAPT17V",174)),"V18":names("r",ma17("MAPT18V",179)),
   "I35":names("s",ma35("RW35",349)),"V35":names("t",ma35("MAPT35V",340,0)),"V36":names("u",ma35("MAPT36V",9,0))}
def fx(n,role="",alt="",note=""):return {"n":n,"role":role,"alt":alt,"note":note}
def tf(a,b,crs=None,dst=None,fin=0,alt=None):
  g={"t":"tf","a":a,"b":b}
  for k,v in (("crs",crs),("dst",dst),("alt",alt)):
    if v:g[k]=v
  if fin:g["fin"]=1
  return g
def arc(a,b,ccw,alt):return {"t":"arc","a":a,"b":b,"ctr":"PMA","R":16.0,"ccw":ccw,"alt":alt,"lbl":"16.0 DME ARC PMA"}
def hold(f,inb,r,alt,ma=1):return {"t":"hold","f":f,"inb":inb,"r":r,"len":4,"alt":alt,"ma":ma}
def ma(*p):return {"t":"ma","pts":list(p)}
hG=hold("GERIR",273,True,"6700");hG6=hold("GERIR",273,True,"6000");hO=hold("ORLIG",258,True,"7000")
hE=hold("EGMEM",166,True,"7200",0);hOB=hold("OBTOX",344,True,"6000",0)
MSA="MSA 25 NM PMA 6700";RNP="LNAV/VNAV · LNAV · "+MSA
northIAF=[fx("D16R268","IAF","7500","R268/16 PMA"),fx("D16R296","IAF","7500","R296/16 PMA"),fx("D16R006","IAF","6700","R006/16 PMA"),fx("D16R060","IAF","6700","R060/16 PMA"),fx("D16R078","IAF","6700","R078/16 PMA"),fx("D16R114","IAF","6700","R114/16 PMA")]
southIAF=[fx("D16R060","IAF","6000","R060/16 PMA"),fx("D16R078","IAF","6000","R078/16 PMA"),fx("D16R114","IAF","6000","R114/16 PMA")]
maN="Climb to 6700 FT, passing 4000 FT turn left to R148 PMA, then turn left onto the 16.0 DME arc PMA to GERIR and hold (inbound 273°, right turns)."
maS="Climb to 6000 FT, passing 5.0 DME PMA turn right to R060 PMA, then turn right onto the 16.0 DME arc PMA to GERIR and hold (inbound 273°, right turns)."
def rnp(n,pg,rwy,fin,pts,alts,mapn,mapalt,mrows):
  a,b,c=pts;tc=str(fin).zfill(3)+"°"
  return {"n":n,"rwy":rwy,"pg":str(pg),"fin":fin,"fixes":[fx(a,"IF",alts[0]),fx(b,"",alts[1]),fx(c,"FAF",alts[2]),fx(mapn,"MAP",mapalt),fx(mrows,""),fx("ORLIG","MAHF","7000")],
    "legs":[tf(a,b,tc,None,1),tf(b,c,tc,None,1),tf(c,mapn,tc,None,1),ma(mapn,mrows,"ORLIG"),hO],
    "ma":"Climb on %s to %s, turn %s direct ORLIG at 7000 FT and hold (inbound 258°, right turns)."%(tc,mrows,"left" if rwy in("17","18") else "right"),"info":RNP}
L=[rnp("RNP RWY 17",97,"17",165,("MA407","EGMEM","MA455"),("6700","6700","4500"),"RW17","2184","MA454"),
   rnp("RNP RWY 18",101,"18",180,("MA465","MA415","MA417"),("6400","6400","5000"),"RW18","2174","MA419"),
   rnp("RNP RWY 35",99,"35",345,("MA443","OBTOX","MA703"),("6300","6000","4400"),"RW35","2113","MA702"),
   rnp("RNP RWY 36",103,"36",360,("MA428","MUVDA","MA510"),("6300","6000","3800"),"RW36","2109","MA508")]
L.append({"n":"ILS or LOC RWY 17","rwy":"17","pg":"85","fin":165,
 "fixes":northIAF+[fx("EGMEM","IAF/IF","6700","R346/16 PMA"),fx("FAF17I","FAF","5300","10.0 DME INAH"),fx("RW17","MAP","","0.2 DME INAH"),fx("GERIR","MAHF","6700","R093/16 PMA")],
 "legs":[arc("D16R268","EGMEM",False,"7500"),arc("D16R114","EGMEM",True,"6700"),hE,tf("EGMEM","FAF17I","165°",None,1),tf("FAF17I","RW17",fin=1),ma(*(["RW17"]+M["I17"]+["GERIR"])),hG],
 "ma":maN,"info":"GS 3.0° · LOC 111.7 INAH · "+MSA})
L.append({"n":"ILS or LOC RWY 35","rwy":"35","pg":"87","fin":345,
 "fixes":southIAF+[fx("D27R179","IAF","6000","R179/27 PMA"),fx("TP22R179","","6000","R179/22 PMA"),fx("OBTOX","IAF/IF","6000","R164/16 PMA"),fx("FAF35I","FAF","","7.6 DME IDIN"),fx("RW35","MAP","","0.2 DME IDIN"),fx("GERIR","MAHF","6000","R093/16 PMA")],
 "legs":[arc("D16R060","OBTOX",False,"6000"),tf("D27R179","TP22R179","359°","5.0"),tf("TP22R179","OBTOX","031°","7.7"),hOB,tf("OBTOX","FAF35I","345°",None,1),tf("FAF35I","RW35",fin=1),ma(*(["RW35"]+M["I35"]+["GERIR"])),hG6],
 "ma":maS,"info":"GS 3.0° · LOC 111.3 IDIN · "+MSA})
def vorN(n,pg,rwy,fin,IF,FAF,MAPT):
  return {"n":n,"rwy":rwy,"pg":str(pg),"fin":fin,
   "fixes":northIAF+[fx("EGMEM","","6700","R346/16 PMA"),fx(IF,"IF","6700","R%03d/16 PMA"%((fin+180)%360)),fx(FAF,"FAF","","%03d°/%s DME PMA"%(fin,{"FAF17V":"9.4","FAF18V":"8.3"}[FAF])),fx(MAPT,"MAP","",""),fx("GERIR","MAHF","6700","R093/16 PMA")],
   "legs":[arc("D16R268",IF,False,"7500"),arc("D16R114",IF,True,"6700"),hE,tf(IF,FAF,"%03d°"%fin,None,1),tf(FAF,MAPT,fin=1),ma(*([MAPT]+M["V"+rwy]+["GERIR"])),hG],"ma":maN,"info":"VOR/DME 114.1 PMA · "+MSA}
L.append(vorN("VOR RWY 17",89,"17",170,"IF17V","FAF17V","MAPT17V"))
L.append(vorN("VOR RWY 18",93,"18",175,"IF18V","FAF18V","MAPT18V"))
L.append({"n":"VOR RWY 35","rwy":"35","pg":"91","fin":336,
 "fixes":southIAF+[fx("D16R179","IAF","6000","R179/16 PMA"),fx("OBTOX","","6000","R164/16 PMA"),fx("IF35V","IF","6000","336°/16 DME PMA"),fx("FAF35V","FAF","","336°/8.2 DME PMA"),fx("MAPT35V","MAP","","336°/0.7 DME PMA"),fx("GERIR","MAHF","6000","R093/16 PMA")],
 "legs":[arc("D16R060","IF35V",False,"6000"),tf("D16R179","OBTOX",alt="6000"),tf("OBTOX","IF35V"),hOB,tf("IF35V","FAF35V","336°",None,1),tf("FAF35V","MAPT35V",fin=1),ma(*(["MAPT35V"]+M["V35"]+["GERIR"])),hG6],
 "ma":"At MAPT turn right climbing to 6000 FT to R060 PMA, then turn right onto the 16.0 DME arc PMA to GERIR and hold (inbound 273°, right turns).","info":"VOR/DME 114.1 PMA · "+MSA})
L.append({"n":"VOR RWY 36","rwy":"36","pg":"95","fin":5,
 "fixes":southIAF+[fx("D26R179","IAF","6000","R179/26 PMA"),fx("OBTOX","","6000","R164/16 PMA"),fx("IF36V","IF","6000","005°/16 DME PMA"),fx("FAF36V","FAF","","005°/6.0 DME PMA"),fx("MAPT36V","MAP","","005°/0.7 DME PMA"),fx("GERIR","MAHF","6000","R093/16 PMA")],
 "legs":[arc("D16R060","IF36V",False,"6000"),tf("D26R179","IF36V","359°",None,0,"6000"),hOB,tf("IF36V","FAF36V","005°",None,1),tf("FAF36V","MAPT36V",fin=1),ma(*(["MAPT36V"]+M["V36"]+["GERIR"])),hG6],
 "ma":"Climb to 6000 FT, passing 3000 FT turn right to R060 PMA, then turn right onto the 16.0 DME arc PMA to GERIR and hold (inbound 273°, right turns).","info":"VOR/DME 114.1 PMA · "+MSA})
FF=dict(F);FF.update(X)
o={"src":"Saudi eAIP AD 2 OEMA (AIRAC AMDT 11/26)","F":FF,"VAR":VAR,"list":L}
open('/tmp/maw/oema.js','w').write("PROCS.OEMA="+json.dumps(o,separators=(',',':'),ensure_ascii=False)+";\n");print(len(L))
