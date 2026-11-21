import sys;sys.path.insert(0,'/tmp/gw')
from lib import *
F=dict(YEN="240858.3N 0380219.0E",ATBEB="242324.4N 0375740.6E",DARAG="241251.2N 0381809.9E",ALNIS="235504.6N 0380836.6E",YN400="240531.8N 0381816.7E",SEPMA="240704.8N 0381105.4E",
MAPT28="240827.1N 0380444.1E",RW28="240827.11N 0380444.13E",YN500="241221.4N 0374620.0E",LAGRI="241012.8N 0375625.2E",RW10="240850.97N 0380253.39E",
LADSI="234107.3N 0381454.5E",RANBU="240432.0N 0374422.5E",VEDAX="241426.0N 0382444.0E",NADKO="242010.7N 0374817.7E",PASUS="243708.9N 0375314.6E",ORSAS="235743.0N 0381616.6E",GEROG="241321.3N 0382017.2E")
VAR=4
check(F,"YEN",VAR,[("LADSI","RANBU",309.9,36.4),("RANBU","YN500",12.9,8),("VEDAX","NADKO",279.9,33.8),("NADKO","YN500",193,8),("PASUS","NADKO",195,17.5),("YN500","LAGRI",103,9.5),("LAGRI","RW10",103,6.1),
 ("LADSI","ORSAS",4.3,16.6),("ORSAS","YN400",13.2,8),("VEDAX","GEROG",255.2,4.2),("GEROG","YN400",193.3,8),("PASUS","GEROG",133.8,34.2),("YN400","SEPMA",283.3,6.7),("SEPMA","RW28",283.3,6.0)],
 [("ATBEB",340,15),("DARAG",71,15),("ALNIS",153,15),("YN400",99,15),("SEPMA",99,8.2),("MAPT28",99,2.3),("YN500",279,15),("LAGRI",279,5.5)])
G=Geo(F,"YEN");pol,add=G.pol,G.add
def maY(start,crs_m,dist,right,pfx):
  h=crs_m+VAR;A=add(G.xy(start),pol(h,dist));T=G.turn(A,h,(h+180)%360,right,1.5,10);return G.names(pfx,[A]+T)
MSA="MSA 25 NM YEN 4000";RNP="LNAV/VNAV · LNAV · "+MSA;VOR="VOR/DME 112.9 YEN · "+MSA
hY28=hold("YEN",99,False,"3000");hY10=hold("YEN",279,False,"3000")
L=[]
L.append({"n":"RNP RWY 10","rwy":"10","pg":"19","fin":99,"fixes":[fx("LADSI","IAF","5000"),fx("VEDAX","IAF","5000"),fx("PASUS","IAF","9000"),fx("RANBU","","5000"),fx("NADKO","","5000"),fx("YN500","IF","2500"),fx("LAGRI","FAF","2000"),fx("RW10","MAP",""),fx("RANBU","MAHF","5000")],
 "legs":[tf("LADSI","RANBU","306°","36.4"),tf("RANBU","YN500","009°","8.0"),tf("VEDAX","NADKO","276°","33.8"),tf("PASUS","NADKO","191°","17.5"),tf("NADKO","YN500","189°","8.0"),hold("NADKO",189,True,"5000",0),
  tf("YN500","LAGRI","099°","9.5",1),tf("LAGRI","RW10","099°","6.1",1),ma("RW10",["ahead",2.5],"RANBU"),hold("RANBU",9,False,"5000")],
 "ma":"Climb on 099° to 3000 FT, turn right direct RANBU at 5000 FT and hold (inbound 009°, left turns).","info":RNP})
L.append({"n":"RNP RWY 28","rwy":"28","pg":"21","fin":279,"fixes":[fx("LADSI","IAF","5000"),fx("VEDAX","IAF","5000"),fx("PASUS","IAF","9000"),fx("ORSAS","","5000"),fx("GEROG","","5000"),fx("YN400","IF","3000"),fx("SEPMA","FAF","2000"),fx("RW28","MAP",""),fx("ORSAS","MAHF","5000")],
 "legs":[tf("LADSI","ORSAS","360°","16.6"),tf("ORSAS","YN400","009°","8.0"),tf("VEDAX","GEROG","251°","4.2"),tf("PASUS","GEROG","130°","34.2"),tf("GEROG","YN400","189°","8.0"),hold("GEROG",251,False,"5000",0),
  tf("YN400","SEPMA","279°","6.7",1),tf("SEPMA","RW28","279°","6.0",1),ma("RW28",["ahead",2.5],"ORSAS"),hold("ORSAS",0,True,"5000")],
 "ma":"Climb on 279° to 3000 FT, turn left direct ORSAS at 5000 FT and hold (inbound 360°, right turns).","info":RNP})
for nm,pg,info in (("ILS or LOC RWY 28","13","GS 3.0° · LOC 111.5 IYEN · "+MSA),("VOR RWY 28","17",VOR)):
  L.append({"n":nm,"rwy":"28","pg":pg,"fin":279,"fixes":[fx("ATBEB","IAF","6200","R340/15 YEN"),fx("DARAG","IAF","5100","R071/15 YEN"),fx("ALNIS","IAF","5000","R153/15 YEN"),fx("YN400","IF","3000","279°/15 DME YEN"),fx("SEPMA","FAF","","279°/8.2 DME YEN"),fx("MAPT28","MAP","","279°/2.3 DME YEN"),fx("YEN","MAHF","3000")],
   "legs":[arc("ATBEB","YN400",False,15,"YEN","6000"),arc("ALNIS","YN400",True,15,"YEN","3000"),tf("DARAG","YN400"),hold("ATBEB",160,True,"6200",0),hold("DARAG",251,True,"5100",0),hold("ALNIS",333,True,"5000",0),
    tf("YN400","SEPMA","279°","6.8",1),tf("SEPMA","MAPT28",fin=1),ma(*(["MAPT28"]+maY("MAPT28",279,4,False,"a"+pg)+["YEN"])),hY28],
   "ma":"Climb on R279 YEN to 1000 FT, then turn left direct YEN climbing to 3000 FT and hold.","info":info})
L.append({"n":"VOR RWY 10","rwy":"10","pg":"15","fin":99,"fixes":[fx("ATBEB","IAF","6200","R340/15 YEN"),fx("ALNIS","IAF","5000","R153/15 YEN"),fx("YN500","IF","2500","099°/15 DME YEN"),fx("LAGRI","FAF","","099°/5.5 DME YEN"),fx("YEN","MAP/MAHF","3000")],
 "legs":[arc("ATBEB","YN500",True,15,"YEN","2500"),arc("ALNIS","YN500",False,15,"YEN","2500"),hold("ATBEB",160,True,"6200",0),hold("ALNIS",333,True,"5000",0),
  tf("YN500","LAGRI","099°","9.5",1),tf("LAGRI","YEN",fin=1),ma(*(["YEN"]+maY("YEN",99,4,False,"b")+["YEN"])),hY10],
 "ma":"Climb on R099 YEN to 1000 FT, then turn left direct YEN climbing to 3000 FT and hold.","info":VOR})
emit("OEYN","Saudi eAIP AD 2 OEYN (AIRAC AMDT 11/26)",F,G.X,VAR,L,'/tmp/gw/oeyn.js')
