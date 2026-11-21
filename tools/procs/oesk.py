import sys;sys.path.insert(0,'/tmp/gw')
from lib import *
F=dict(AJF="294722.3N 0400418.1E",D15R035="295858.6N 0401516.7E",D15R188="293239.7N 0400043.6E",IF28="294446.9N 0402116.8E",FAF28="294555.1N 0401350.4E",RW28="294656.26N 0400707.25E",
IF10="295009.2N 0394721.4E",FAF10="294819.8N 0395829.3E",MAPT10="294716.3N 0400452.9E",IF28V="294444.5N 0402116.4E",FAF28V="294553.5N 0401353.3E")
VAR=4
check(F,"AJF",VAR,[],[("D15R035",35,15),("D15R188",188,15),("IF28",96,15),("FAF28",96,6.1+2.4),("RW28",96,2.5),("IF10",276,15),("FAF10",276,5.2),("MAPT10",276,0.5),("IF28V",96,15),("FAF28V",96,8.47)])
G=Geo(F,"AJF");pol,add=G.pol,G.add
def maR(start,crs_m,dist,pfx):
  h=crs_m+VAR;A=add(G.xy(start),pol(h,dist));T=G.turn(A,h,(h+180)%360,True,1.5,10);return G.names(pfx,[A]+T)
MSA="MSA 25 NM AJF";VOR="DVORTAC 117.8 AJF · "+MSA
h=hold("AJF",96,False,"5000")
L=[]
for nm,pg,IF,FAF,info,n in (("ILS or LOC RWY 28","13","IF28","FAF28","GS 3.0° · LOC 109.9 IAJF · "+MSA,("12.7 DME IAJF","6.1 DME IAJF")),("VOR RWY 28","17","IF28V","FAF28V",VOR,("276°/15 DME AJF","276°/8.47 DME AJF"))):
  L.append({"n":nm,"rwy":"28","pg":pg,"fin":276,"fixes":[fx("D15R035","IAF","5000","R035/15 AJF"),fx("D15R188","IAF","5000","R188/15 AJF"),fx(IF,"IF","5000",n[0]),fx(FAF,"FAF","",n[1]),fx("RW28","MAP","","2.5 DME AJF"),fx("AJF","IAF/MAHF","5000")],
   "legs":[arc("D15R035",IF,False,15,"AJF","5000"),arc("D15R188",IF,True,15,"AJF","5000"),tf(IF,FAF,"276°",None,1),tf(FAF,"RW28",fin=1),ma(*(["RW28"]+maR("RW28",276,3,"a"+pg)+["AJF"])),h],
   "ma":"Climb on R276 AJF to 5000 FT, passing 4000 FT turn right direct AJF and hold.","info":info})
L.append({"n":"VOR RWY 10","rwy":"10","pg":"15","fin":96,"fixes":[fx("D15R035","IAF","5000","R035/15 AJF"),fx("D15R188","IAF","5000","R188/15 AJF"),fx("IF10","IF","5000","R276/15 AJF"),fx("FAF10","FAF","","R276/5.2 AJF"),fx("MAPT10","MAP","","R276/0.5 AJF"),fx("AJF","IAF/MAHF","5000")],
 "legs":[arc("D15R035","IF10",True,15,"AJF","5000"),arc("D15R188","IF10",False,15,"AJF","5000"),tf("IF10","FAF10","096°",None,1),tf("FAF10","MAPT10",fin=1),ma(*(["MAPT10"]+maR("AJF",96,3,"b")+["AJF"])),hold("AJF",276,False,"5000")],
 "ma":"Climb on R096 AJF to 5000 FT, passing 4000 FT turn right direct AJF and hold.","info":VOR})
emit("OESK","Saudi eAIP AD 2 OESK (AIRAC AMDT 11/26)",F,G.X,VAR,L,'/tmp/gw/oesk.js')
