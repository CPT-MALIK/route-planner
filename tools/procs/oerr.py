import sys;sys.path.insert(0,'/tmp/gw')
from lib import *
F=dict(AAR="305428.9N 0410831.8E",RR501="305619.3N 0412708.0E",RR502="304441.9N 0412333.2E",ELUPI="305030.6N 0412520.5E",ALTUT="305247.3N 0411522.4E",RW28="305411.22N 0410913.27E",
RR503="310358.7N 0405322.8E",RR504="305220.3N 0404951.8E",KULNO="305809.5N 0405137.2E",RR505="305549.8N 0410157.8E",RW10="305436.42N 0410722.14E",
IMDEM="302441.8N 0411317.7E",ITGIR="303427.6N 0413430.2E",D15R168="303935.4N 0411055.1E",D15R127="304428.9N 0412132.4E",
BOVUL="303124.2N 0404613.3E",OBTOM="304351.4N 0403556.3E",SESRO="310523.8N 0403600.4E",D15R215="304257.0N 0405721.2E",D15R245="304911.2N 0405213.2E",D15R287="305957.4N 0405217.0E",
IF10V="305710.4N 0405122.3E",DANEL="305531.8N 0410153.0E",MAPT10V="305439.8N 0410722.9E",IF28V="304923.3N 0412455.7E",GESAV="305230.5N 0411454.0E",MAPT28V="305415.5N 0410915.1E")
VAR=4.5
check(F,"AAR",VAR,[("RR501","ELUPI",194.9,6.0),("RR502","ELUPI",14.9,6.0),("ELUPI","ALTUT",284.7,8.9),("ALTUT","RW28",284.7,5.5),("RR503","KULNO",194.9,6.0),("RR504","KULNO",14.9,6.0),("KULNO","RR505",104.6,9.2),("RR505","RW10",104.7,4.8)],
 [("IMDEM",168,30),("ITGIR",127,30),("D15R168",168,15),("D15R127",127,15),("BOVUL",215,30),("OBTOM",245,30),("SESRO",287,30),("D15R215",215,15),("D15R245",245,15),("D15R287",287,15),("IF10V",276,15),("DANEL",276,5.8),("MAPT10V",276,1.0),("IF28V",105,15),("GESAV",105,5.8),("MAPT28V",105,0.7)])
G=Geo(F,"AAR");pol,add=G.pol,G.add
# teardrops: RWY 10 (outbound 321M, left turn to 096M inbound to AAR); RWY 28 (outbound 060M from R105, right turn, inbound 285M)
def ptturn(rad_m,out_min,pt_m,right180):
  # outbound on radial rad_m for out_min, 45-deg turn to pt_m for 1 min, 180 turn, intercept the radial back to AAR
  o=rad_m+VAR;A=pol(o,out_min*3.3);B=add(A,pol(pt_m+VAR,3.3));T=G.turn(B,pt_m+VAR,(pt_m+180)%360+VAR,right180,1.5,10);E=T[-1]
  h=(pt_m+180+VAR)%360;d=pol(h,1);r=pol(o,1);t,s2=np.linalg.solve(np.array([[d[0],-r[0]],[d[1],-r[1]]]),[-E[0],-E[1]]);I=add(E,(d[0]*t,d[1]*t))
  return [A,B]+T+[I]
T10X=G.names("x",ptturn(276,2,321,False));T10Y=G.names("y",ptturn(276,4,321,False))
T28X=G.names("v",ptturn(105,2,60,True));T28Y=G.names("w",ptturn(105,4,60,True))
# missed approaches: 28: climb ahead (RWY HDG 285M) ~3 NM, turn right direct AAR ; 10: climb on R096 (100.5T) ~3 NM, turn left direct AAR
def maPts(start,hdg_m,right):h=hdg_m+VAR;A=add(G.xy(start),pol(h,3.0));T=G.turn(A,h,(h+180)%360,right,1.5,10);return [A]+T
M28=G.names("m",maPts("RW28",285,True));M28V=G.names("n",maPts("MAPT28V",285,True));M10=G.names("o",maPts("RW10",96,False));M10V=G.names("p",maPts("MAPT10V",96,False));MA_AAR=G.names("q",maPts("AAR",285,True));MA_AAR10=G.names("r",maPts("AAR",96,False))
hA28=hold("AAR",105,False,"5000");hA10=hold("AAR",276,False,"5000")
MSA="MSA 25 NM AAR 5000";RNP="LNAV/VNAV · LNAV · "+MSA;VOR="VOR/DME 113.3 AAR · "+MSA
ma28="Climb to 5000 FT on RWY heading (R285 AAR) until passing 3400 FT, then turn right direct AAR and hold (inbound 105°, left turns)."
ma10="Climb to 5000 FT on R096 AAR until passing 3400 FT, then turn left direct AAR and hold (inbound 276°, left turns)."
L=[]
L.append({"n":"RNP RWY 10","rwy":"10","pg":"9","fin":100,"fixes":[fx("RR503","IAF","5000"),fx("RR504","IAF","5000"),fx("KULNO","IF/MAHF","5000"),fx("RR505","FAF","3400"),fx("RW10","MAP","1869")],
 "legs":[tf("RR503","KULNO","190°","6.0"),tf("RR504","KULNO","010°","6.0"),tf("KULNO","RR505","100°","9.2",1),tf("RR505","RW10","100°","4.8",1),ma("RW10",["ahead",3],"KULNO"),hold("KULNO",100,False,"5000")],
 "ma":"Climb on 100° to 3400 FT, then turn left direct KULNO at 5000 FT and hold (inbound 100°, left turns).","info":RNP})
for nm,pg in (("RNP RWY 28","11"),("ILS Y RWY 28","13")):
  L.append({"n":nm,"rwy":"28","pg":pg,"fin":280,"fixes":[fx("RR501","IAF","5000"),fx("RR502","IAF","5000"),fx("ELUPI","IF/MAHF","5000"),fx("ALTUT","FAF","3600"),fx("RW28","MAP","1855")],
   "legs":[tf("RR501","ELUPI","190°","6.0"),tf("RR502","ELUPI","010°","6.0"),tf("ELUPI","ALTUT","280°","8.9",1),tf("ALTUT","RW28","280°","5.5",1),ma("RW28",["ahead",3],"ELUPI"),hold("ELUPI",280,True,"5000")],
   "ma":"Climb on 280° to 3400 FT, then turn right direct ELUPI at 5000 FT and hold (inbound 280°, right turns).","info":RNP if nm.startswith("RNP") else "GS 3.0° · LOC 111.1 IAAR · "+MSA})
L.append({"n":"ILS Z or LOC RWY 28","rwy":"28","pg":"15","fin":280,"fixes":[fx("IMDEM","IAF","5000","R168/30 AAR"),fx("ITGIR","IAF","5000","R127/30 AAR"),fx("D15R168","","5000","R168/15 AAR"),fx("D15R127","","5000","R127/15 AAR"),fx("ELUPI","IF","5000","14.5 DME IAAR"),fx("ALTUT","FAF","3600","5.6 DME IAAR"),fx("RW28","MAP","","0.2 DME IAAR"),fx("AAR","MAHF","5000")],
 "legs":[tf("IMDEM","D15R168","348°","15.0"),tf("ITGIR","D15R127","307°","15.0"),arc("D15R168","ELUPI",True,15,"AAR","5000"),arc("D15R127","ELUPI",True,15,"AAR","5000"),tf("ELUPI","ALTUT","280°","8.9",1),tf("ALTUT","RW28",fin=1),ma(*(["RW28"]+M28+["AAR"])),hA28],
 "ma":ma28,"info":"GS 3.0° · LOC 111.1 IAAR · "+MSA})
L.append({"n":"VOR Z RWY 28","rwy":"28","pg":"27","fin":285,"fixes":[fx("IMDEM","IAF","5000","R168/30 AAR"),fx("ITGIR","IAF","5000","R127/30 AAR"),fx("D15R168","","5000","R168/15 AAR"),fx("D15R127","","5000","R127/15 AAR"),fx("IF28V","IF","5000","R105/15 AAR"),fx("GESAV","FAF","3500","R105/5.8 AAR"),fx("MAPT28V","MAP","","R105/0.7 AAR"),fx("AAR","MAHF","5000")],
 "legs":[tf("IMDEM","D15R168","348°","15.0"),tf("ITGIR","D15R127","307°","15.0"),arc("D15R168","IF28V",True,15,"AAR","5000"),arc("D15R127","IF28V",True,15,"AAR","5000"),tf("IF28V","GESAV","285°","9.2",1),tf("GESAV","MAPT28V",fin=1),ma(*(["MAPT28V"]+M28V+["AAR"])),hA28],
 "ma":ma28.replace("RWY heading (R285 AAR)","R285 AAR"),"info":VOR})
L.append({"n":"VOR Z RWY 10","rwy":"10","pg":"25","fin":96,"fixes":[fx("SESRO","IAF","5500","R287/30 AAR"),fx("OBTOM","IAF","5500","R245/30 AAR"),fx("BOVUL","IAF","6100","R215/30 AAR"),fx("IMDEM","IAF","5000","R168/30 AAR"),fx("D15R287","","5000","R287/15 AAR"),fx("D15R245","","5000","R245/15 AAR"),fx("D15R215","","5000","R215/15 AAR"),fx("D15R168","","5000","R168/15 AAR"),fx("IF10V","IF","5000","R276/15 AAR"),fx("DANEL","FAF","3400","R276/5.8 AAR"),fx("MAPT10V","MAP","","R276/1.0 AAR"),fx("AAR","MAHF","5000")],
 "legs":[tf("SESRO","D15R287","107°","15.0"),tf("OBTOM","D15R245","065°","15.0"),tf("BOVUL","D15R215","035°","15.0"),tf("IMDEM","D15R168","348°","15.0"),arc("D15R287","IF10V",True,15,"AAR","5000"),arc("D15R168","IF10V",False,15,"AAR","5000"),tf("IF10V","DANEL","096°","9.2",1),tf("DANEL","MAPT10V",fin=1),ma(*(["MAPT10V"]+M10V+["AAR"])),hA10],
 "ma":ma10,"info":VOR})
for nm,pg,T in (("VOR X RWY 10","17",T10X),("VOR Y RWY 10","21",T10Y)):
  L.append({"n":nm,"rwy":"10","pg":pg,"fin":96,"fixes":[fx("AAR","IAF/MAP/MAHF","5000","AAR VOR/DME")],
   "legs":[{"t":"path","pts":["AAR"]+T+["AAR"],"lbl":"321° / 141°"},ma(*(["AAR"]+MA_AAR10+["AAR"])),hA10],
   "ma":ma10,"info":VOR+(" · CAT C-D, outbound 2 min" if "X" in nm else " · outbound 4 min")})
for nm,pg,T in (("VOR X RWY 28","19",T28X),("VOR Y RWY 28","23",T28Y)):
  L.append({"n":nm,"rwy":"28","pg":pg,"fin":285,"fixes":[fx("AAR","IAF/MAP/MAHF","5000","AAR VOR/DME")],
   "legs":[{"t":"path","pts":["AAR"]+T+["AAR"],"lbl":"060° / 240°"},ma(*(["AAR"]+MA_AAR+["AAR"])),hA28],
   "ma":ma28.replace("RWY heading (R285 AAR)","R285 AAR"),"info":VOR+(" · CAT C-D, outbound 2 min" if "X" in nm else " · outbound 4 min")})
emit("OERR","Saudi eAIP AD 2 OERR (AIRAC AMDT 11/26)",F,G.X,VAR,L,'/tmp/gw/oerr.js')
