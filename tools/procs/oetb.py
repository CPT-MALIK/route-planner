import sys;sys.path.insert(0,'/tmp/gw')
from lib import *
F=dict(TBK="282152.9N 0363636.9E",SOBOX="282517.2N 0364453.3E",MUPVA="282826.7N 0365155.2E",IF24="282813.3N 0365202.4E",RW24="282253.91N 0363904.95E",
IF31="281136.9N 0364901.8E",ITNOG="281818.2N 0364116.3E",RW31="282142.69N 0363703.14E",IF31V="281249.1N 0365010.5E",KUMDI="281839.8N 0364135.5E",
IF31W="281626.8N 0364445.3E",MEMTO="281946.9N 0363951.8E",IF06="281545.0N 0362105.8E",RIKOL="281959.8N 0363202.8E",RW06="282207.96N 0363713.44E")
VAR=4
check(F,"TBK",VAR,[("IF24","SOBOX",246,None),("IF31","ITNOG",313,None)],[("SOBOX",62,8.0),("MUPVA",61,15),("IF24",None,15),("IF31",None,15),("IF31V",None,15),("KUMDI",None,5.4),("IF31W",None,9),("MEMTO",None,3.6),("IF06",242,15),("RIKOL",242,4.4),("ITNOG",None,None)])
G=Geo(F,"TBK");pol,add=G.pol,G.add
def ptk(name,rad_m,R):F[name]=G.ll(pol(rad_m+VAR,R))
ptk("D15R179",179,15);ptk("D15R043",43,15);ptk("D9R179",179,9);ptk("D9R043",43,9);ptk("D20R061",61,20)
def maT(start,hdg_m,pfx):
  h=hdg_m+VAR;A=add(G.xy(start),pol(h,2.0));T=G.turn(A,h,61+VAR,True,1.5,8);return G.names(pfx,[A]+T)
MSA="MSA 25 NM TBK";VOR="VORTAC 115.7 TBK · "+MSA
hM=hold("MUPVA",241,False,"6000")
mtxt="Climb to 3500 FT, then climbing right turn to 6000 FT via R061 TBK to MUPVA (15 DME) and hold. Stay within 5 DME TBK in the turn."
L=[]
L.append({"n":"ILS-DME RWY 24","rwy":"24","pg":"19","fin":242,"fixes":[fx("D15R179","IAF","5500","R179/15 TBK"),fx("D20R061","IAF","5000","R061/20 TBK"),fx("IF24","IF","4400","15 DME TBK"),fx("SOBOX","IAF/FAF","4100","5.8 DME ITBK"),fx("RW24","MAP",""),fx("MUPVA","MAHF","6000","R061/15 TBK")],
 "legs":[arc("D15R179","IF24",True,15,"TBK","5500"),tf("D20R061","IF24","242°"),tf("IF24","SOBOX","242°",None,1),tf("SOBOX","RW24",fin=1),ma(*(["RW24","TBK"]+maT("TBK",242,"a")+["MUPVA"])),hM],
 "ma":"Climb to 3500 FT direct TBK, then climbing right turn to 6000 FT via R061 TBK to MUPVA and hold.","info":"GS 3.0° · LOC 109.5 ITBK · "+MSA})
def r31(nm,pg,IF,FAF,R,fafn,info,iafs):
  return {"n":nm,"rwy":"31","pg":pg,"fin":309,"fixes":[fx(i,"IAF","5000","R%s/%d TBK"%(i[-3:],R)) for i in iafs]+[fx(IF,"IF","","%d DME TBK"%R),fx(FAF,"FAF","",fafn),fx("RW31","MAP",""),fx("MUPVA","MAHF","6000","R061/15 TBK")],
   "legs":[arc(iafs[0],IF,True,R,"TBK","5000"),arc(iafs[1],IF,False,R,"TBK","5000"),tf(IF,FAF,"309°",None,1),tf(FAF,"RW31",fin=1),ma(*(["RW31"]+maT("RW31",309,"b"+pg)+["MUPVA"])),hM],
   "ma":mtxt,"info":info}
L.append(r31("ILS-DME RWY 31","21","IF31","ITNOG",15,"5.2 DME IPKS","GS 3.0° · LOC 111.9 IPKS · "+MSA,["D15R179","D15R043"]))
L.append(r31("VOR-DME or TACAN 1 RWY 31","29","IF31V","KUMDI",15,"5.4 DME TBK",VOR,["D15R179","D15R043"]))
L.append(r31("VOR-DME or TACAN 2 RWY 31","31","IF31W","MEMTO",9,"3.6 DME TBK",VOR,["D9R179","D9R043"]))
L.append({"n":"VOR-DME or TACAN RWY 06","rwy":"06","pg":"23","fin":62,"fixes":[fx("D15R179","IAF","5200","R179/15 TBK"),fx("IF06","IF","","R242/15 TBK"),fx("RIKOL","IAF/FAF","4200","R242/4.4 TBK"),fx("TBK","MAP",""),fx("MUPVA","MAHF","6000","R061/15 TBK")],
 "legs":[arc("D15R179","IF06",False,15,"TBK","5200"),tf("IF06","RIKOL","062°","10.6",1),tf("RIKOL","TBK",fin=1),ma("TBK","MUPVA"),hM],
 "ma":"Climb to 6000 FT via R061 TBK to MUPVA (15 DME) and hold.","info":VOR})
L.append({"n":"VOR-DME or TACAN RWY 24","rwy":"24","pg":"27","fin":242,"fixes":[fx("D15R179","IAF","5500","R179/15 TBK"),fx("IF24","IF","","15 DME TBK"),fx("SOBOX","IAF/FAF","","8.0 DME TBK"),fx("RW24","MAP",""),fx("MUPVA","MAHF","6000")],
 "legs":[arc("D15R179","IF24",True,15,"TBK","5500"),tf("IF24","SOBOX","242°",None,1),tf("SOBOX","RW24",fin=1),ma(*(["RW24","TBK"]+maT("TBK",242,"c")+["MUPVA"])),hM],
 "ma":"Climb to 3500 FT direct TBK, then climbing right turn to 6000 FT via R061 TBK to MUPVA and hold.","info":VOR})
emit("OETB","Saudi eAIP AD 2 OETB (AIRAC AMDT 11/26)",F,G.X,VAR,L,'/tmp/gw/oetb.js')
