import sys;sys.path.insert(0,'/tmp/gw')
from lib import *
F=dict(SHA="172812.9N 0470802.2E",DATPI="174200.3N 0465926.8E",D16R286="173317.2N 0465209.0E",IF08="172634.5N 0465123.2E",FAF08="172720.0N 0465956.8E",MAPT08="172755.2N 0470615.2E",
ALMIM="173530.5N 0472146.2E",RW08="172755.18N 0470615.23E",IF08V="172550.8N 0465129.0E",FAF08V="172712.4N 0470057.8E",MAPT08V="172757.6N 0470614.9E",FAF26="172800.7N 0471413.4E",MAPT26="172812.4N 0470818.6E")
VAR=2
check(F,"SHA",VAR,[],[("DATPI",327,16),("D16R286",286,16),("IF08",None,16),("FAF08",None,7.8),("MAPT08",None,1.7),("ALMIM",59,15),("IF08V",259,16),("FAF08V",259,6.84),("MAPT08V",259,1.73),("FAF26",90,5.92),("MAPT26",90,0.3)])
G=Geo(F,"SHA");pol,add=G.pol,G.add
def ptk(name,rad_m,R):F[name]=G.ll(pol(rad_m+VAR,R))
ptk("D10R090",90,10)
def maL(start,pass_d,right,to_rad,pfx):
  h=90+VAR;A=add(G.xy(start),pol(h,pass_d));T=G.turn(A,h,to_rad+VAR,right,1.5,8);return G.names(pfx,[A]+T)
MSA="MSA 25 NM SHA";VOR="VORTAC 114.3 SHA · "+MSA;ILS="GS 3.0° · LOC 109.7 ISHA · "+MSA
hAL=hold("ALMIM",239,False,"5000");hS=hold("SHA",240,True,"5000")
maY="Climb to 5000 FT outbound on SHA R090 until passing 3500 FT, then turn left to SHA R059 to ALMIM (15 DME) and hold."
maZ="Climb to 5000 FT outbound on SHA R090 until passing 4000 FT, then turn left to SHA and hold."
def r08(nm,pg,IF,FAF,MAPT,info,y,notes):
  mp=(maL(MAPT,4,False,59,"a"+pg)+["ALMIM"]) if y else (G.names("b"+pg,[add(G.xy(MAPT),pol(92,4))]+G.turn(add(G.xy(MAPT),pol(92,4)),92,272,False,1.5,10))+["SHA"])
  return {"n":nm,"rwy":"08","pg":pg,"fin":82 if "ILS" in nm else 79,"fixes":[fx("DATPI","IAF","5000","R327/16 SHA"),fx("D16R286","IAF","5000","R286/16 SHA"),fx(IF,"IF","5000",notes[0]),fx(FAF,"FAF","",notes[1]),fx(MAPT,"MAP","",notes[2]),fx("ALMIM" if y else "SHA","MAHF","5000")],
   "legs":[arc("DATPI",IF,True,16,"SHA","5000"),tf(IF,FAF,"%03d°"%(82 if "ILS" in nm else 79),None,1),tf(FAF,MAPT,fin=1),ma(*([MAPT]+mp)),hAL if y else hS],"ma":maY if y else maZ,"info":info}
L=[r08("ILS (Y) or LOC (Y) RWY 08","9","IF08","FAF08","MAPT08",ILS,True,("14.4 DME ISHA","6.23 DME ISHA","0.18 DME ISHA")),
   r08("ILS (Z) or LOC (Z) RWY 08","11","IF08","FAF08","MAPT08",ILS,False,("14.4 DME ISHA","6.23 DME ISHA","0.18 DME ISHA")),
   r08("VOR (Y) RWY 08","13","IF08V","FAF08V","MAPT08V",VOR,True,("079°/16 DME SHA","079°/6.84 DME SHA","079°/1.73 DME SHA")),
   r08("VOR (Z) RWY 08","15","IF08V","FAF08V","MAPT08V",VOR,False,("079°/16 DME SHA","079°/6.84 DME SHA","079°/1.73 DME SHA"))]
o=90+VAR;A=pol(o,10);B=add(A,pol(45+VAR,3.0));T=G.turn(B,45+VAR,225+VAR,True,1.5,10);E=T[-1]
d=pol(225+VAR,1);r=pol(o,1);t,s2=np.linalg.solve(np.array([[d[0],-r[0]],[d[1],-r[1]]]),[-E[0],-E[1]]);I=add(E,(d[0]*t,d[1]*t))
P26=G.names("c",[A,B]+T+[I])
M26=G.names("d",[pol(270+VAR,3)]+G.turn(pol(270+VAR,3),272,92,True,1.5,10))
L.append({"n":"VOR RWY 26","rwy":"26","pg":"17","fin":270,"fixes":[fx("SHA","IAF/MAHF","5000","SHA VORTAC"),fx("FAF26","FAF","","270°/5.92 DME SHA"),fx("MAPT26","MAP","","270°/0.3 DME SHA")],
 "legs":[{"t":"path","pts":["SHA"]+P26,"lbl":"045° / 225°"},tf(P26[-1],"FAF26","270°",None,1),tf("FAF26","MAPT26",fin=1),ma(*(["MAPT26"]+M26+["SHA"])),hold("SHA",90,True,"5000")],
 "ma":"Climb to 5000 FT via SHA R270, then turn right direct SHA and hold.","info":VOR})
emit("OESH","Saudi eAIP AD 2 OESH (AIRAC AMDT 11/26)",F,G.X,VAR,L,'/tmp/gw/oesh.js')
