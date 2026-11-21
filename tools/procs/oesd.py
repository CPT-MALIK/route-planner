import sys;sys.path.insert(0,'/tmp/gw')
from lib import *
F=dict(KSB="275250.1N 0453320.5E",RANLA="275010.5N 0453653.2E",UKSUK="273726.2N 0455534.7E",ITIXI="275030.9N 0470434.9E",DEBOL="272116.1N 0461843.4E",KATOX="274308.8N 0454616.9E",
METSI="275755.3N 0452629.6E",RW31="275324.95N 0453232.63E",TASVA="280710.7N 0452130.2E",VUSIR="280111.2N 0452206.2E",SERLO="275213.6N 0460132.7E",RW13="275441.32N 0453050.14E",D14R307="280151.0N 0452113.4E")
VAR=3
check(F,"KSB",VAR,[("TASVA","VUSIR",175,6.0),("VUSIR","METSI",130,5.0),("ITIXI","SERLO",272,55.9),("DEBOL","UKSUK",308,26.1),("SERLO","VUSIR",285,36.1),("UKSUK","VUSIR",308,38.0),("KATOX","RANLA",310,10.9)],
 [("RANLA",127,4.1),("UKSUK",125,25),("KATOX",127,15),("METSI",307,7.9),("D14R307",307,14)])
G=Geo(F,"KSB");pol,add=G.pol,G.add
def ptk(name,rad_m,R):F[name]=G.ll(pol(rad_m+VAR,R))
ptk("D15R089",89,15);ptk("D14R089",89,14);ptk("D14R043",43,14);ptk("D15R043",43,15)
def maK(start,hdg_m,dist,right,pfx):
  h=hdg_m+VAR;A=add(G.xy(start),pol(h,dist));T=G.turn(A,h,(h+180)%360,right,1.5,10);return G.names(pfx,[A]+T)
def pt(rad_m,dist,pt_m,right,pfx):
  o=rad_m+VAR;A=pol(o,dist);B=add(A,pol(pt_m+VAR,3.0));T=G.turn(B,pt_m+VAR,(pt_m+180)%360+VAR,right,1.5,10);E=T[-1]
  h=(pt_m+180+VAR)%360;d=pol(h,1);r=pol(o,1);t,s2=np.linalg.solve(np.array([[d[0],-r[0]],[d[1],-r[1]]]),[-E[0],-E[1]]);I=add(E,(d[0]*t,d[1]*t))
  return G.names(pfx,[A,B]+T+[I])
MSA="MSA 25 NM KSB 4000";VOR="VORTAC 115.9 KSB · "+MSA;GNSS="RNAV (GNSS) · LNAV · MSA 25 NM 4000"
hKSB=hold("KSB",127,False,"4000");hKAT=hold("KATOX",307,True,"5000");hKAT0=hold("KATOX",307,True,"5000",0)
north=[tf("ITIXI","D15R089","269°"),arc("D15R089","KATOX",False,15,"KSB","4000"),tf("DEBOL","UKSUK","305°","26.1"),tf("UKSUK","KATOX","300°"),hKAT0]
L=[]
for nm,pg,info in (("ILS-DME RWY 31","11","GS 3.0° · LOC 108.7 IKSB · "+MSA),("VOR-DME or TACAN RWY 31","13",VOR)):
  L.append({"n":nm,"rwy":"31","pg":pg,"fin":307,"fixes":[fx("ITIXI","","8000","R118/59.5 HFR"),fx("DEBOL","","8000","R167/60.9 HFR"),fx("D15R089","IAF","4000","R089/15 KSB"),fx("UKSUK","IAF","4000","R125/25 KSB"),fx("KATOX","","4000","R127/15 KSB"),fx("RANLA","IAF/FAF","","4.1 DME KSB"),fx("RW31","MAP",""),fx("KSB","MAHF","4000")],
   "legs":north+[tf("KATOX","RANLA","307°","10.9",1),tf("RANLA","RW31",fin=1),ma(*(["RW31"]+maK("RW31",307,2.5,False,"a"+pg)+["KSB"])),hKSB],
   "ma":"Climb to 4000 FT, then turn left to KSB and hold (inbound 127°, left turns).","info":info})
L.append({"n":"RNAV (GNSS) RWY 31","rwy":"31","pg":"19","fin":307,"fixes":[fx("UKSUK","IAF","4000"),fx("SERLO","IAF","4000"),fx("RANLA","FAF",""),fx("RW31","MAP",""),fx("KATOX","MAHF","5000")],
 "legs":[tf("ITIXI","SERLO","269°","55.9"),tf("DEBOL","UKSUK","305°","26.1"),tf("SERLO","RANLA"),tf("UKSUK","RANLA"),tf("RANLA","RW31","307°",None,1),ma("RW31",["ahead",2.5],"KATOX"),hKAT],
 "ma":"Climb straight ahead, then direct KATOX at 5000 FT and hold.","info":GNSS})
L.append({"n":"RNAV (GNSS) RWY 13","rwy":"13","pg":"21","fin":127,"fixes":[fx("TASVA","IAF","4000"),fx("VUSIR","IAF","4000"),fx("SERLO","","4000"),fx("UKSUK",""),fx("METSI","FAF",""),fx("RW13","MAP",""),fx("KATOX","MAHF","5000")],
 "legs":[tf("TASVA","VUSIR","172°","6.0"),tf("ITIXI","SERLO","269°","55.9"),tf("SERLO","VUSIR","282°","36.1"),tf("DEBOL","UKSUK","305°","26.1"),tf("UKSUK","VUSIR","305°","38.0"),tf("VUSIR","METSI","127°","5.0",1),tf("METSI","RW13","127°",None,1),ma("RW13","KATOX"),hKAT],
 "ma":"Climb to 5000 FT direct KATOX and hold.","info":GNSS})
L.append({"n":"VOR RWY 31","rwy":"31","pg":"17","fin":307,"fixes":[fx("ITIXI","","8000","R118/59.5 HFR"),fx("DEBOL","","8000","R167/60.9 HFR"),fx("KSB","IAF/MAP/MAHF","4000","KSB VORTAC")],
 "legs":[tf("ITIXI","KSB","269°","80.9"),tf("DEBOL","KSB","305°","51.5"),{"t":"path","pts":["KSB"]+pt(127,8,82,False,"b")+["KSB"],"lbl":"082° / 262°"},ma(*(["KSB"]+maK("KSB",307,3,False,"c")+["KSB"])),hKSB],
 "ma":"Climb to 4000 FT, then turn left to KSB and hold.","info":VOR})
L.append({"n":"VOR-DME or TACAN RWY 13","rwy":"13","pg":"15","fin":127,"fixes":[fx("D14R043","IAF","4000","R043/14 KSB"),fx("D14R089","IAF","4000","R089/14 KSB"),fx("D14R307","IF","4000","R307/14 KSB"),fx("METSI","FAF","3000","7.9 DME KSB"),fx("RW13","MAP",""),fx("KATOX","MAHF","5000","R127/15 KSB")],
 "legs":[tf("ITIXI","D14R089","269°"),arc("D14R089","D14R307",True,14,"KSB","4000"),arc("D14R043","D14R307",True,14,"KSB","4000"),tf("D14R307","METSI","127°","6.1",1),tf("METSI","RW13",fin=1),ma("RW13","KSB","KATOX"),hKAT],
 "ma":"Climb to 5000 FT via R127 KSB direct KATOX (15 DME) and hold.","info":VOR})
emit("OESD","Saudi eAIP AD 2 OESD (AIRAC AMDT 11/26)",F,G.X,VAR,L,'/tmp/gw/oesd.js')
