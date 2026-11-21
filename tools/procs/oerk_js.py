import json,sys;sys.path.insert(0,'/tmp/rkw')
from fx import F
d=json.load(open('ma.json'));X=d["X"]
def fx(n,role="",alt="",note=""):return {"n":n,"role":role,"alt":alt,"note":note}
def tf(a,b,crs=None,dst=None,fin=0,alt=None):
  g={"t":"tf","a":a,"b":b}
  if crs:g["crs"]=crs
  if dst:g["dst"]=dst
  if alt:g["alt"]=alt
  if fin:g["fin"]=1
  return g
def arc(a,b,ccw,R,alt):return {"t":"arc","a":a,"b":b,"ctr":"KSA","R":R,"ccw":ccw,"alt":alt,"lbl":"%.1f DME ARC KSA"%R}
def hold(f,inb,r,alt):return {"t":"hold","f":f,"inb":inb,"r":r,"len":4,"alt":alt,"ma":1}
def ma(*p):return {"t":"ma","pts":list(p)}
hMEP=hold("MEPTU",237,True,"5000");hPED4=hold("PEDIR",312,False,"4000");hPED7=hold("PEDIR",312,False,"7000")
hORL=hold("ORLUD",57,False,"6000");hORB=hold("ORBON",76,False,"4000");hSIS=hold("SISIR",217,False,"5000");hKIR=hold("KIRUL",126,False,"5500-7000")
MSA="MSA 25 NM KSA 5000";RNP="LNAV/VNAV · LNAV · "+MSA
LOC={"15L":"LOC 109.5 IELF","15R":"LOC 110.5 ITIH","33L":"LOC 110.1 IFAT","33R":"LOC 109.1 IKIA"}
maT={"15L":"Climb on 147° to RK703, turn left direct RK769 to 5000 FT, then RK762 and MEPTU and hold (right turns, inbound 237°).",
 "15R":"Climb on 147° to RK603, turn right direct RK612 to 4000 FT, then RK655 and PEDIR and hold (left turns, inbound 312°).",
 "33L":"Climb on 327° to RK503, turn left to RK526, then ORLUD at 6000 FT and hold (left turns, inbound 057°).",
 "33R":"Climb on 327° to RK533, turn right direct ORBON at 4000 FT and hold (left turns, inbound 076°)."}
def rnav(name,pg,rwy,ils=False):
  if rwy=="15L":
    fixes=[fx("RK721","IAF","6000"),fx("RK621","IAF","6000"),fx("LONUD","IF","6000"),fx("ITETU","FAF","4000"),fx("RW15L","MAP","2087"),fx("RK703"),fx("RK769","","5000"),fx("RK762"),fx("MEPTU","MAHF","5000")]
    legs=[tf("RK721","LONUD","147°","7.0"),tf("RK621","LONUD","135°","7.2"),tf("LONUD","ITETU","147°","7.7",1),tf("ITETU","RW15L","147°","6.0",1),ma("RW15L","RK703","RK769","RK762","MEPTU"),hMEP];fin=147;mt=maT["15L"]
  if rwy=="15R":
    fixes=[fx("RK621","IAF","5000"),fx("RK721","IAF","6000"),fx("ALPUR","IF","5000"),fx("TAVNU","FAF","5000"),fx("RW15R","MAP","2103"),fx("RK612","","4000"),fx("RK655"),fx("PEDIR","MAHF","4000")]
    if not ils:fixes.insert(5,fx("RK603"))
    legs=[tf("RK621","ALPUR","147°","7.1"),tf("RK721","ALPUR","159°","7.1"),tf("ALPUR","TAVNU","147°","4.2",1),tf("TAVNU","RW15R","147°","9.1",1),
          ma("RW15R",["ahead",3.5],"RK612","RK655","PEDIR") if ils else ma("RW15R","RK603","RK612","RK655","PEDIR"),hPED4];fin=147
    mt=maT["15R"].replace("Climb on 147° to RK603","Climb on 147° to 2500 FT") if ils else maT["15R"]
  if rwy=="33L":
    fixes=[fx("RK413","IAF","5000"),fx("RK517","IAF","7000"),fx("LOPAK","IF","5000"),fx("SODUT","FAF","3500"),fx("RW33L","MAP","2087"),fx("RK503"),fx("RK526"),fx("ORLUD","MAHF","6000")]
    legs=[tf("RK413","LOPAK","300°","3.3"),tf("RK517","LOPAK","327°","6.9"),tf("LOPAK","SODUT","327°","5.2",1),tf("SODUT","RW33L","327°","4.4",1),ma("RW33L","RK503","RK526","ORLUD"),hORL];fin=327;mt=maT["33L"]
  if rwy=="33R":
    fixes=[fx("RK413","IAF","4000"),fx("RK517","IAF","7000"),fx("ORMAT","IF","4000"),fx("KIRUP","FAF","3500"),fx("RW33R","MAP","2066"),fx("RK533"),fx("ORBON","MAHF","4000")]
    legs=[tf("RK413","ORMAT","327°","3.0"),tf("RK517","ORMAT","339°","7.1"),tf("ORMAT","KIRUP","327°","4.6",1),tf("KIRUP","RW33R","327°","4.5",1),ma("RW33R","RK533","ORBON"),hORB];fin=327;mt=maT["33R"]
  info=("GS 3.0° · "+LOC[rwy]+" · "+MSA) if ils else RNP
  return {"n":name,"rwy":rwy,"pg":str(pg),"fin":fin,"fixes":fixes,"legs":legs,"ma":mt,"info":info}
L=[]
for rwy,pg in (("15L",119),("15R",121),("33L",123),("33R",125)):L.append(rnav("RNP RWY "+rwy,pg,rwy))
for rwy,pg in (("15L",127),("15R",129),("33L",131),("33R",133)):L.append(rnav("ILS Y RWY "+rwy,pg,rwy,True))
M15L,M15R,M33R=d["M15L"],d["M15R"],d["M33R"]
L.append({"n":"ILS Z or LOC RWY 15L","rwy":"15L","pg":"135","fin":147,
 "fixes":[fx("KITAM","IAF","6000","R292/17.0 KSA"),fx("PEBAK","IAF","6000","R018/17.0 KSA"),fx("PUXIB","","6000","R332/17.0 KSA"),fx("LONUD","IF","6000","13.9 IELF"),fx("ITETU","FAF","4000","6.2 IELF"),fx("RW15L","MAP","","0.2 IELF"),fx("SISIR","MAHF","5000","R037/16.5 KSA")],
 "legs":[arc("KITAM","PUXIB",False,17.0,"6000"),arc("PEBAK","PUXIB",True,17.0,"6000"),tf("PUXIB","LONUD"),tf("LONUD","ITETU","147°","7.7",1),tf("ITETU","RW15L",fin=1),ma(*(["RW15L"]+M15L+["SISIR"])),hSIS],
 "ma":"Climb on RWY HDG to 3.8 DME KSA, turn left HDG 107° to join 7.0 DME arc KSA, turn right to intercept R037 KSA to SISIR at 5000 FT and hold.","info":"GS 3.0° · "+LOC["15L"]+" · "+MSA})
L.append({"n":"ILS Z or LOC RWY 15R","rwy":"15R","pg":"137","fin":147,
 "fixes":[fx("KITAM","IAF","6000","R292/17.0 KSA"),fx("PEBAK","IAF","6000","R018/17.0 KSA"),fx("ORDEG","","5000","R327/17.0 KSA"),fx("ALPUR","IF","5000","13.5 ITIH"),fx("TAVNU","FAF","","9.3 ITIH"),fx("RW15R","MAP","","0.2 ITIH"),fx("PEDIR","MAHF","7000","R312/27.6 KSA")],
 "legs":[arc("KITAM","ORDEG",False,17.0,"5000"),arc("PEBAK","ORDEG",True,17.0,"5000"),tf("ORDEG","ALPUR"),tf("ALPUR","TAVNU","147°","4.2",1),tf("TAVNU","RW15R",fin=1),ma(*(["RW15R"]+M15R+["PEDIR"])),hPED7],
 "ma":"Climb on RWY HDG to 3.1 DME KSA, turn right HDG 302° to intercept R245 KSA, then turn right to join the 27.6 DME arc KSA to PEDIR and hold.","info":"GS 3.0° · "+LOC["15R"]+" · "+MSA})
L.append({"n":"ILS Z or LOC RWY 33L","rwy":"33L","pg":"139","fin":327,
 "fixes":[fx("MOGUB","IAF","6000","R212/12.5 KSA"),fx("TUGNA","IAF","6000","R079/12.5 KSA"),fx("LOPAK","IF","5000","9.7 IFAT"),fx("SODUT","FAF","3500","4.6 IFAT"),fx("RW33L","MAP","","0.2 IFAT"),fx("KIRUL","MAHF","5500-7000","R306/16.7 KSA")],
 "legs":[arc("MOGUB","LOPAK",True,12.5,"6000"),arc("TUGNA","LOPAK",False,12.5,"5000"),tf("LOPAK","SODUT","327°","5.2",1),tf("SODUT","RW33L",fin=1),ma("RW33L","KSA","KIRUL"),hKIR],
 "ma":"Climb straight ahead to KSA, turn left to intercept and follow R306 KSA to KIRUL between 5500 and 7000 FT and hold.","info":"GS 3.0° · "+LOC["33L"]+" · "+MSA})
L.append({"n":"ILS Z or LOC RWY 33R","rwy":"33R","pg":"141","fin":327,
 "fixes":[fx("MOGUB","IAF","6000","R212/12.5 KSA"),fx("TUGNA","IAF","6000","R079/12.5 KSA"),fx("ORMAT","IF","4000","9.2 IKIA"),fx("KIRUP","FAF","3500","4.7 IKIA"),fx("RW33R","MAP","","0.2 IKIA"),fx("ORBON","MAHF","4000","R076/16.4 KSA")],
 "legs":[arc("MOGUB","ORMAT",True,12.5,"6000"),arc("TUGNA","ORMAT",False,12.5,"4000"),tf("ORMAT","KIRUP","327°","4.6",1),tf("KIRUP","RW33R",fin=1),ma(*(["RW33R"]+M33R+["ORBON"])),hORB],
 "ma":"Climb on RWY HDG until crossing R082 KSA, turn right to intercept R076 KSA to ORBON at 4000 FT and hold.","info":"GS 3.0° · "+LOC["33R"]+" · "+MSA})
L.append({"n":"VOR RWY 15R","rwy":"15R","pg":"143","fin":147,
 "fixes":[fx("KITAM","IAF","6000","R292/17.0 KSA"),fx("PEBAK","IAF","6000","R018/17.0 KSA"),fx("ORDEG","","5000","R327/17.0 KSA"),fx("LOVAT","IF","5000","R327/13.4 KSA"),fx("TAVNU","FAF","","R327/8.4 KSA"),fx("KSA","MAP","","KSA DVOR/DME"),fx("PEDIR","MAHF","7000","R312/27.6 KSA")],
 "legs":[arc("KITAM","ORDEG",False,17.0,"5000"),arc("PEBAK","ORDEG",True,17.0,"5000"),tf("ORDEG","LOVAT"),tf("LOVAT","TAVNU","147°","5.0",1),tf("TAVNU","KSA","147°",fin=1),ma(*(["KSA"]+M15R+["PEDIR"])),hPED7],
 "ma":"Climb on RWY HDG to 3.1 DME KSA, turn right HDG 302° to intercept R245 KSA, then turn right to join the 27.6 DME arc KSA to PEDIR and hold.","info":"VOR/DME 115.0 KSA · "+MSA})
L.append({"n":"VOR RWY 33L","rwy":"33L","pg":"145","fin":327,
 "fixes":[fx("MOGUB","IAF","6000","R212/12.5 KSA"),fx("TUGNA","IAF","6000","R079/12.5 KSA"),fx("LOPAK","IF","4600","R147/12.5 KSA"),fx("KEDOL","FAF","","R147/7.4 KSA"),fx("MAPT33L","MAP","","R147/2.9 KSA"),fx("KIRUL","MAHF","5500-7000","R306/16.7 KSA")],
 "legs":[arc("MOGUB","LOPAK",True,12.5,"6000"),arc("TUGNA","LOPAK",False,12.5,"4600"),tf("LOPAK","KEDOL","327°","5.1",1),tf("KEDOL","MAPT33L",fin=1),ma("MAPT33L","KSA","KIRUL"),hKIR],
 "ma":"Climb on R147 KSA to KSA, turn left to intercept and follow R306 KSA to KIRUL between 5500 and 7000 FT and hold.","info":"VOR/DME 115.0 KSA · "+MSA})
FF=dict(F);FF.update(X)
o={"src":"Saudi eAIP AD 2 OERK (AIRAC AMDT 11/26)","F":FF,"VAR":3,"list":L}
open('/tmp/rkw/oerk.js','w').write("PROCS.OERK="+json.dumps(o,separators=(',',':'),ensure_ascii=False)+";\n")
print(len(L),len(open('/tmp/rkw/oerk.js').read()))
