import sys;sys.path.insert(0,'/tmp/gw')
from lib import *
F=dict(RSI="253652.6N 0370603.6E",KULKI="254814.0N 0371445.0E",RS115="255017.6N 0370440.8E",RS195="255852.4N 0365856.2E",DEMBI="255545.1N 0365314.7E",RS012="255127.9N 0365607.2E",
RS011="254710.6N 0365859.5E",LUDUR="254252.5N 0370152.1E",RW15L="253832.97N 0370445.44E",RS880="253141.1N 0370920.0E",RS515="252849.0N 0372016.1E",OBSEG="253914.6N 0372929.5E",
ORGIM="252344.8N 0370539.8E",TUGRU="254252.9N 0365055.8E",SDF15="254109.6N 0370300.9E",
ATBOR="252417.8N 0371414.8E",RS133="253050.4N 0371738.5E",RAGNO="251617.0N 0371123.0E",RS101="252743.9N 0371157.8E",MEPLA="253201.5N 0370906.4E",RW33R="253650.09N 0370554.07E",
RS200="254414.5N 0371000.9E",RS700="254350.4N 0372025.5E",SITEV="253626.0N 0372738.0E",RS316="252245.9N 0372417.2E",SDF33="253415.6N 0370737.1E",
MAPT15Z="253849.8N 0370434.2E",MAPT33Z="253639.8N 0370600.9E",RS601="254653.9N 0365837.1E",RS602="254317.7N 0370117.8E",RS603="254102.3N 0370258.3E",MAPT15V="253912.2N 0370420.0E",
RS850="252651.1N 0371049.0E",RS851="253144.2N 0370830.0E")
VAR=4
check(F,"RSI",VAR,[("KULKI","RS115",282.7,9.3),("RS115","RS195",328.8,10),("RS195","DEMBI",238.8,6),("DEMBI","RS012",148.8,5),("RS012","RS011",148.8,5),("ORGIM","TUGRU",325.1,23.3),("TUGRU","RS011",59.6,8.4),
 ("RS011","LUDUR",148.8,5),("LUDUR","SDF15",148.8,2),("SDF15","RW15L",148.8,3),("RW15L","RS880",148.9,8),("RS880","RS515",106.2,10.3),("RS515","OBSEG",38.8,13.3),
 ("ATBOR","RS101",328.9,4),("KULKI","RS200",227,5.8),("RS200","RS133",152.7,15),("RS133","RS101",238.9,6),("RAGNO","ATBOR",18,8.4),("RS101","MEPLA",328.9,5),("MEPLA","SDF33",328.9,2.6),("SDF33","RW33R",328.9,3),
 ("RS200","RS700",92.5,9.4),("RS700","SITEV",138.6,9.8),("SITEV","RS316",192.5,14),("RS316","ATBOR",279.5,9.2)],
 [("RAGNO",163,21.1),("RS601",322,12),("RS602",322,7.7),("RS603",322,5),("MAPT15V",322,2.8),("RS850",153,10.9),("RS851",153,5.6),("RS011",None,12.1),("RS101",None,10.6)])
G=Geo(F,"RSI");pol,add=G.pol,G.add
def loop(rad_m,dme,inb_m,right,pfx):
  o=rad_m+VAR;A=pol(o,dme);T=G.turn(A,o,inb_m+VAR,right,2.0,12);return G.names(pfx,[A]+T)
def maK(start,hdg_m,dist,right,pfx):
  h=hdg_m+VAR;A=add(G.xy(start),pol(h,dist));T=G.turn(A,h,(h+180)%360,right,1.5,10);return G.names(pfx,[A]+T)
MSA="MSA 25 NM RSI";RNP="LNAV/VNAV · LNAV · "+MSA;VOR="VOR/DME 112.6 RSI · "+MSA
hOB=hold("OBSEG",286,True,"5000");hDE=hold("DEMBI",145,False,"4000",0);hSI=hold("SITEV",134,False,"4000");hAT=hold("ATBOR",325,False,"4000",0)
hR15=hold("RSI",352,True,"4500",0);hR15m=hold("RSI",352,True,"4500");hR33=hold("RSI",145,False,"4500",0);hR33m=hold("RSI",145,False,"4500")
L=[]
for nm,pg,info in (("RNP RWY 15L","25",RNP),("ILS Y RWY 15L","29","GS 3.0° · LOC 109.1 IERS · "+MSA)):
  L.append({"n":nm,"rwy":"15L","pg":pg,"fin":145,"fixes":[fx("DEMBI","IAF","4000"),fx("ORGIM","IAF","7500"),fx("KULKI","IAF","13000"),fx("RS115","","10000"),fx("RS195","","6000"),fx("TUGRU","","5000"),fx("RS012","","3000"),fx("RS011","IF","1800"),fx("LUDUR","FAF","1800"),fx("RW15L","MAP",""),fx("RS880"),fx("RS515"),fx("OBSEG","MAHF","5000")],
   "legs":[tf("KULKI","RS115","279°","9.3"),tf("RS115","RS195","325°","10.0"),tf("RS195","DEMBI","235°","6.0"),hDE,tf("DEMBI","RS012","145°","5.0"),tf("RS012","RS011","145°","5.0"),tf("ORGIM","TUGRU","321°","23.3"),tf("TUGRU","RS011","055°","8.4"),
     tf("RS011","LUDUR","145°","5.0",1),tf("LUDUR","RW15L","145°","5.0",1),ma("RW15L","RS880","RS515","OBSEG"),hOB],
   "ma":"Climb on 145° to RS880, turn left to RS515, then OBSEG at 5000 FT and hold (inbound 286°, right turns).","info":info})
for nm,pg,info in (("RNP RWY 33R","27",RNP),("ILS Y RWY 33R","31","GS 3.0° · LOC 109.3 IRSI · "+MSA)):
  L.append({"n":nm,"rwy":"33R","pg":pg,"fin":325,"fixes":[fx("ATBOR","IAF","4000"),fx("KULKI","IAF","13000"),fx("RAGNO","IAF","7500"),fx("RS200","","10500"),fx("RS133","","5000"),fx("RS101","IF","3000"),fx("MEPLA","FAF","2000"),fx("RW33R","MAP",""),fx("RS700"),fx("SITEV","MAHF","4000")],
   "legs":[tf("KULKI","RS200","223°","5.8"),tf("RS200","RS133","149°","15.0"),tf("RS133","RS101","235°","6.0"),tf("RAGNO","ATBOR","014°","8.4"),hAT,tf("ATBOR","RS101","325°","4.0"),
     tf("RS101","MEPLA","325°","5.0",1),tf("MEPLA","RW33R","325°","5.6",1),ma("RW33R",["ahead",2],"RS200","RS700","SITEV"),hSI],
   "ma":"Climb on 325° to 900 FT, turn right direct RS200, then RS700 and SITEV at 4000 FT and hold (inbound 134°, left turns).","info":info})
ent=[tf("RAGNO","RSI","343°","21.1")]
L.append({"n":"ILS Z or LOC RWY 15L","rwy":"15L","pg":"33","fin":145,"fixes":[fx("RAGNO","IAF","7500","R163/21.1 RSI"),fx("RSI","IAF/MAHF","4500","RSI DVOR/DME"),fx("RS011","IF","1800","10.2 DME IERS"),fx("LUDUR","FAF","1800","5.2 DME IERS"),fx("MAPT15Z","MAP","","0.5 DME IERS")],
 "legs":ent+[hR15,{"t":"path","pts":["RSI"]+loop(344,11,145,False,"a")+["RS011"],"lbl":"R344 / 145°"},tf("RS011","LUDUR","145°","5.0",1),tf("LUDUR","MAPT15Z",fin=1),ma(*(["MAPT15Z"]+maK("MAPT15Z",145,4,False,"b")+["RSI"])),hR15m],
 "ma":"Climb to 2000 FT on heading 145°, then turn left direct RSI at 4500 FT and hold.","info":"GS 3.0° · LOC 109.1 IERS · "+MSA})
L.append({"n":"VOR RWY 15L","rwy":"15L","pg":"37","fin":142,"fixes":[fx("RAGNO","IAF","7500","R163/21.1 RSI"),fx("RSI","IAF/MAHF","4500","RSI DVOR/DME"),fx("RS601","IF","2000","R322/12 RSI"),fx("RS602","FAF","2000","R322/7.7 RSI"),fx("RS603","SDF","","R322/5.0 RSI"),fx("MAPT15V","MAP","","R322/2.8 RSI")],
 "legs":ent+[hR15,{"t":"path","pts":["RSI"]+loop(342,11,142,False,"c")+["RS601"],"lbl":"R342 / 142°"},tf("RS601","RS602","142°","4.3",1),tf("RS602","MAPT15V",fin=1),ma(*(["MAPT15V"]+maK("RSI",142,4,False,"d")+["RSI"])),hR15m],
 "ma":"Climb to 2000 FT on R142 RSI, then turn left direct RSI at 4500 FT and hold.","info":VOR})
L.append({"n":"ILS Z or LOC RWY 33R","rwy":"33R","pg":"35","fin":325,"fixes":[fx("RAGNO","IAF","7500","R163/21.1 RSI"),fx("RSI","IAF/MAHF","4500","RSI DVOR/DME"),fx("RS101","IF","2000","10.8 DME IRSI"),fx("MEPLA","FAF","2000","5.8 DME IRSI"),fx("MAPT33Z","MAP","","0.4 DME IRSI")],
 "legs":ent+[hR33,{"t":"path","pts":["RSI"]+loop(128,11,325,True,"e")+["RS101"],"lbl":"R128 / 325°"},tf("RS101","MEPLA","325°","5.0",1),tf("MEPLA","MAPT33Z",fin=1),ma(*(["MAPT33Z"]+maK("MAPT33Z",325,4,True,"f")+["RSI"])),hR33m],
 "ma":"Climb to 2000 FT on heading 325°, then turn right direct RSI at 4500 FT and hold.","info":"GS 3.0° · LOC 109.3 IRSI · "+MSA})
L.append({"n":"VOR RWY 33R","rwy":"33R","pg":"39","fin":333,"fixes":[fx("RAGNO","IAF","7500","R163/21.1 RSI"),fx("RSI","IAF/MAP/MAHF","4500","RSI DVOR/DME"),fx("RS850","IF","2000","R153/10.9 RSI"),fx("RS851","FAF","2000","R153/5.6 RSI")],
 "legs":ent+[hR33,{"t":"path","pts":["RSI"]+loop(134,11,333,True,"g")+["RS850"],"lbl":"R134 / 333°"},tf("RS850","RS851","333°","5.3",1),tf("RS851","RSI",fin=1),ma(*(["RSI"]+maK("RSI",325,4,True,"h")+["RSI"])),hR33m],
 "ma":"Climb to 2000 FT on R325 RSI, then turn right direct RSI at 4500 FT and hold.","info":VOR})
emit("OERS","Saudi eAIP AD 2 OERS (AIRAC AMDT 11/26)",F,G.X,VAR,L,'/tmp/gw/oers.js')
