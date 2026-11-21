import sys;sys.path.insert(0,'/tmp/gw')
from lib import *
F=dict(KSN="242836.1N 0463918.3E",RK551="242646.0N 0465244.0E",SN101="241518.0N 0464010.2E",SN707="243239.9N 0464901.6E",SN099="242034.4N 0462748.7E",SN096="241750.6N 0463413.1E",
SN094="242247.8N 0463644.2E",SN100="243629.5N 0465059.1E",SN023="243902.5N 0464501.2E",RW02R="242726.40N 0463906.02E",SN091="241806.7N 0463335.3E",SN090="242303.3N 0463606.1E",
SN006="243918.6N 0464423.3E",RW02L="242720.35N 0463816.90E",SN024="243439.3N 0464246.7E",RW20L="242909.50N 0463958.55E",SN005="243414.9N 0464148.2E",RW20R="242854.62N 0463904.92E",
RK558="243251.0N 0464854.0E",SN105="242755.2N 0465226.2E",SN106="241733.4N 0463404.4E",SN033="241749.6N 0463326.6E",SN034="242246.1N 0463557.4E",SN035="242436.0N 0463653.2E",
SN042="241826.3N 0463215.6E",SN041="242304.3N 0463528.2E",MAPT02L="242713.9N 0463821.3E",SN108="241706.0N 0463525.3E",SN109="242139.6N 0463657.6E",MAPT02R="242646.1N 0463841.1E",
SN114="242758.7N 0465120.5E",SN115="243356.4N 0464951.7E",SN116="243725.3N 0464633.3E",SN118="243320.0N 0464311.5E",MAPT20L="242914.4N 0463949.7E")
VAR=3
check(F,"KSN",VAR,[("RK551","SN101",225.1,16.2),("SN707","SN101",205,19.1),("SN101","SN096",295,6.0),("SN099","SN096",115,6.5),("SN096","SN094",25,5.4),("SN094","RW02R",25,5.1),("RW02R","SN023",25,12.8),("SN023","SN100",115.1,6.0),("SN100","SN707",205.1,4.2),
 ("SN101","SN091",295,6.6),("SN099","SN091",115,5.8),("SN091","SN090",25,5.4),("SN090","RW02L",25,4.7),("RW02L","SN006",25,13.2),("SN006","SN100",115.1,6.6),
 ("SN100","SN023",295,6.0),("SN101","SN100",25.1,23.3),("SN023","SN024",205,4.8),("SN024","RW20L",205,6.0),("RW20L","SN096",205,12.4),("SN096","SN101",115,6.0),
 ("SN100","SN006",295,6.6),("SN006","SN005",205,5.6),("SN005","RW20R",205,5.9),("RW20R","SN091",205,11.9),("SN091","SN101",111.9,6.6)],
 [("RK558",61,9.7),("SN105",90,12),("SN106",200,12),("SN033",203,12),("SN042",209,12),("SN041",209,6.5),("MAPT02L",209.3,1.6),("SN108",194,12),("SN109",194,7.2),("MAPT02R",194,1.9),("SN114",90,11),("SN115",58,11),("SN116",34,11),("SN118",34,5.9),("MAPT20L",34,0.8)])
G=Geo(F,"KSN");pol,add=G.pol,G.add
def maK(start,hdg_m,dist,right,pfx):
  h=hdg_m+VAR;S=G.xy(start);A=add(S,pol(h,dist));T=G.turn(A,h,(h+180)%360,right,1.5,10);return G.names(pfx,[A]+T)
hK=hold("KSN",62,True,"6000");hKa=hold("KSN",62,True,"6000",0)
MSA="MSA 25 NM KSN";RNP="LNAV/VNAV · LNAV · "+MSA;VOR="VORTAC 112.7 KSN · "+MSA
hS=hold("SN101",292,False,"6000")
def rnp(n,pg,rwy,fin,trans,final,mapn,mrest,alts,info=RNP):
  fixes=[];seen=set()
  def af(nm,role="",alt=""):
    if nm not in seen:seen.add(nm);fixes.append(fx(nm,role,alt))
  for t in trans:
    for k,nm in enumerate(t[0]):af(nm,"IAF" if k==0 else "",alts.get(nm,""))
  IF,FAF=final;af(IF,"IF",alts.get(IF,""));af(FAF,"FAF",alts.get(FAF,""));af(mapn,"MAP",alts.get(mapn,""))
  for nm in mrest:af(nm,"MAHF" if nm=="SN101" else "",alts.get(nm,""))
  legs=[]
  for pts,crs in trans:
    for k in range(1,len(pts)):legs.append(tf(pts[k-1],pts[k],crs[k-1]))
  tc="%03d°"%fin;legs+= [tf(IF,FAF,tc,None,1),tf(FAF,mapn,tc,None,1),ma(*([mapn]+mrest)),hS]
  return {"n":n,"rwy":rwy,"pg":pg,"fin":fin,"fixes":fixes,"legs":legs,"ma":"Climb on %s via %s and hold at SN101 at 6000 FT (inbound 292°, left turns)."%(tc," – ".join(mrest)),"info":info}
A02R={"RK551":"7000","SN101":"6000","SN707":"6000","SN099":"6000","SN096":"5000","SN094":"4000","RW02R":"2460"}
A02L={"RK551":"7000","SN101":"6000","SN707":"6000","SN099":"6000","SN091":"4100","SN090":"4000","RW02L":"2499"}
A20L={"RK551":"7000","SN101":"6000","SN100":"6000","SN023":"4300","SN024":"4300","RW20L":"2375"}
A20R={"RK551":"7000","SN101":"6000","SN100":"6000","SN006":"4300","SN005":"4300","RW20R":"2430"}
T02R=[(["RK551","SN101"],["222°"]),(["SN707","SN101","SN096"],["202°","292°"]),(["SN099","SN096"],["112°"])]
L=[rnp("RNP RWY 02R","23","02R",22,T02R,("SN096","SN094"),"RW02R",["SN023","SN100","SN707","SN101"],A02R),
   rnp("ILS Y RWY 02R","29","02R",22,T02R,("SN096","SN094"),"RW02R",["SN023","SN100","SN707","SN101"],A02R,"GS 3.0° · LOC 111.95 ISND · "+MSA),
   rnp("RNP RWY 02L","21","02L",22,[(["RK551","SN101"],["222°"]),(["SN707","SN101","SN091"],["202°","292°"]),(["SN099","SN091"],["112°"])],("SN091","SN090"),"RW02L",["SN006","SN100","SN707","SN101"],A02L),
   rnp("RNP RWY 20L","25","20L",202,[(["RK551","SN101","SN100","SN023"],["222°","022°","292°"])],("SN023","SN024"),"RW20L",["SN096","SN101"],A20L),
   rnp("RNP RWY 20R","27","20R",202,[(["RK551","SN101","SN100","SN006"],["222°","022°","292°"])],("SN006","SN005"),"RW20R",["SN091","SN101"],A20R)]
ent=[tf("RK558","KSN","241°","9.7"),hKa,tf("KSN","SN105","090°","12.0")]
entF=[fx("RK558","IAF","7000","R061/9.7 KSN"),fx("SN105","","6000","R090/12 KSN")]
maILS="Climb on RWY HDG 022° at or above 3500 FT, then turn right direct KSN at 6000 FT and hold (inbound 062°, right turns)."
def conv(n,pg,rwy,fin,IF,FAF,MAPT,ifn,fafn,mapn,alts,info,mpts,mtext,extra=[]):
  return {"n":n,"rwy":rwy,"pg":pg,"fin":fin,"fixes":entF+[fx(IF,"IF",alts[0],ifn),fx(FAF,"FAF",alts[1],fafn)]+extra+[fx(MAPT,"MAP","",mapn),fx("KSN","IAF/MAHF","6000","KSN VORTAC")],
   "legs":ent+[arc("SN105",IF,False,12,"KSN","6000"),tf(IF,FAF,"%03d°"%fin,None,1),tf(FAF,MAPT,fin=1),ma(*([MAPT]+mpts+["KSN"])),hK],"ma":mtext,"info":info}
L.append(conv("ILS Z or LOC RWY 02R","31","02R",22,"SN106","SN094","RW02R","11.0 DME ISND","5.3 DME ISND","0.2 DME ISND",("5000","4000"),"GS 3.0° · LOC 111.95 ISND · "+MSA,maK("RW02R",22,3,True,"a"),maILS))
L.append(conv("ILS or LOC RWY 02L","33","02L",22,"SN033","SN034","RW02L","10.6 DME KSND","5.2 DME KSND","0.2 DME KSND",("5000","4100"),"GS 3.0° · LOC 111.1 KSND · "+MSA,maK("RW02L",22,3,True,"b"),maILS,[fx("SN035","SDF","","3.2 DME KSND")]))
L.append(conv("VOR RWY 02L","35","02L",29,"SN042","SN041","MAPT02L","R209/12 KSN","R209/6.5 KSN","R209/1.6 KSN",("4400","4100"),VOR,maK("KSN",29,6,True,"c"),"Climb on R029 KSN to 6.0 DME KSN, then turn right direct KSN at 6000 FT and hold (inbound 062°, right turns)."))
L.append(conv("VOR RWY 02R","37","02R",14,"SN108","SN109","MAPT02R","R194/12 KSN","R194/7.2 KSN","R194/1.9 KSN",("4400","4400"),VOR,maK("KSN",14,6,True,"d"),"Climb on R014 KSN to 6.0 DME KSN, then turn right direct KSN at 6000 FT and hold (inbound 062°, right turns)."))
L.append({"n":"VOR RWY 20L","rwy":"20L","pg":"39","fin":214,"fixes":[fx("RK558","IAF","7000","R061/9.7 KSN"),fx("SN114","","6000","R090/11 KSN"),fx("SN115","","6000","R058/11 KSN"),fx("SN116","IF","4000","R034/11 KSN"),fx("SN118","FAF","4000","R034/5.9 KSN"),fx("MAPT20L","MAP","","R034/0.8 KSN"),fx("KSN","IAF/MAHF","6000","KSN VORTAC")],
 "legs":[tf("RK558","KSN","241°","9.7"),hKa,tf("KSN","SN114","090°","11.0"),arc("SN114","SN116",True,11,"KSN","6000"),tf("SN116","SN118","214°","5.1",1),tf("SN118","MAPT20L",fin=1),ma(*(["MAPT20L"]+maK("KSN",214,6,False,"e")+["KSN"])),hK],
 "ma":"Climb on R214 KSN to 6.0 DME KSN, then turn left direct KSN at 6000 FT and hold (inbound 062°, right turns).","info":VOR})
emit("OESN","Saudi eAIP AD 2 OESN (AIRAC AMDT 11/26)",F,G.X,VAR,L,'/tmp/gw/oesn.js')
