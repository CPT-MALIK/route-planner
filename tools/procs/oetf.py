import sys;sys.path.insert(0,'/tmp/gw')
from lib import *
F=dict(TIF="212911.3N 0403250.1E",OTERI="213819.0N 0404437.1E",KUSBU="212642.1N 0404801.0E",TF620="213230.5N 0404619.1E",TF625="213035.7N 0403851.5E",RW25="212910.34N 0403319.73E",LAKNO="211007.6N 0405014.8E",
TUDID="211524.8N 0402811.2E",OTOPI="211614.4N 0403432.9E",TF610="212225.5N 0403338.1E",MENDA="215414.6N 0403125.7E",RW35="212834.90N 0403243.40E",
D13R009="214154.8N 0403554.8E",D13R136="211916.8N 0404153.9E",D13R291="213440.3N 0402010.9E",D13R308="213744.5N 0402218.3E",MAPT25Z="212918.9N 0403352.8E",MAPT35Z="212809.5N 0403247.2E",
IF07="212458.9N 0401938.6E",FAF07="212656.9N 0402548.3E",MAPT07="212826.0N 0403027.7E",IF17="214153.2N 0402938.1E",FAF17="213554.2N 0403108.6E",MAPT17="213107.9N 0403220.8E",
IF25="213110.9N 0404636.8E",FAF25="213005.1N 0403900.8E",MAPT25="212922.4N 0403406.6E",IF35="211608.5N 0403249.9E",FAF35="212259.3N 0403250.0E",MAPT35="212749.8N 0403250.1E")
VAR=3.6
check(F,"TIF",VAR,[("OTERI","TF620",164.7,6),("KUSBU","TF620",344.7,6),("TF620","TF625",254.6,7.2),("TF625","RW25",254.6,5.3),("TUDID","OTOPI",82.1,6),("LAKNO","OTOPI",292.6,15.9),("OTOPI","TF610",352.1,6.2),("TF610","RW35",352.1,6.2)],
 [("D13R009",9,13),("D13R136",136,13),("D13R291",291,13),("D13R308",308,13),("LAKNO",136,25),("MENDA",354,25),("IF07",248,13),("FAF07",248,6.9),("MAPT07",248,2.3),("IF17",343,13),("FAF17",343,6.9),("MAPT17",343,2.0),
  ("IF25",78,13),("FAF25",78,5.8),("MAPT25",78,1.2),("IF35",177,13),("FAF35",177,6.2),("MAPT35",177,1.4)])
G=Geo(F,"TIF")
MSA="MSA 25 NM TIF";VOR="VORTAC 113.4 TIF · "+MSA
hL=hold("LAKNO",316,False,"9300");hM=hold("MENDA",174,True,"8000");hO=hold("OTOPI",289,True,"8000",0)
def b(n):return G.brg(G.xy(n))
def arcdir(a,b_):
  d=(b(b_)-b(a))%360;return d>180   # ccw if shorter way is decreasing
L=[]
L.append({"n":"ILS Y RWY 25","rwy":"25","pg":"43","fin":251,"fixes":[fx("OTERI","IAF","8000"),fx("KUSBU","IAF","8000"),fx("TF620","IF","7500"),fx("TF625","FAF","6500"),fx("RW25","MAP",""),fx("LAKNO","MAHF","9300")],
 "legs":[tf("OTERI","TF620","161°","6.0"),tf("KUSBU","TF620","341°","6.0"),tf("TF620","TF625","251°","7.2",1),tf("TF625","RW25","251°","5.3",1),ma("RW25",["ahead",3],"LAKNO"),hL],
 "ma":"Climb on 251° to 5600 FT, turn left direct LAKNO at 9300 FT and hold (inbound 316°, left turns).","info":"GS 3.0° · LOC ITIF · "+MSA})
L.append({"n":"ILS Y RWY 35","rwy":"35","pg":"45","fin":349,"fixes":[fx("TUDID","IAF","8600"),fx("LAKNO","IAF","9000"),fx("OTOPI","IF","8000"),fx("TF610","FAF","6800"),fx("RW35","MAP",""),fx("MENDA","MAHF","8000")],
 "legs":[tf("TUDID","OTOPI","079°","6.0"),tf("LAKNO","OTOPI","289°","15.9"),hO,tf("OTOPI","TF610","349°","6.2",1),tf("TF610","RW35","349°","6.2",1),ma("RW35",["ahead",3],"MENDA"),hM],
 "ma":"Climb on 349° to 5600 FT, turn right direct MENDA at 8000 FT and hold (inbound 174°, right turns).","info":"GS 3.0° · LOC ITAI · "+MSA})
pol,add=G.pol,G.add
def mpath(start,h_m,dist,rad_m,right,pfx):
  h=h_m+VAR;A=add(G.xy(start),pol(h,dist));r=rad_m+VAR;tgt=pol(r,8);T=G.turn(A,h,r,right,1.8,10);return G.names(pfx,[A]+T+[tgt])
MA={(251,"LAKNO"):mpath("MAPT25Z",251,4.5,136,False,"a"),(349,"MENDA"):mpath("MAPT35Z",349,2.5,354,True,"b"),(68,"MENDA"):mpath("MAPT07",68,2.5,354,False,"c"),
 (163,"LAKNO"):mpath("MAPT17",163,2.5,136,False,"d"),(258,"LAKNO"):mpath("MAPT25",258,3.5,136,False,"e"),(357,"MENDA"):mpath("MAPT35",357,2.5,354,True,"f")}
def conv(n,pg,rwy,fin,iafs,IF,FAF,MAPT,mahf,info,notes):
  fixes=[fx(i,"IAF","","R%s/13 TIF"%i[-3:]) for i in iafs]+[fx(IF,"IF","",notes[0]),fx(FAF,"FAF","",notes[1]),fx(MAPT,"MAP","",notes[2]),fx(mahf,"MAHF","9300" if mahf=="LAKNO" else "8000")]
  legs=[arc(i,IF,arcdir(i,IF),13,"TIF") for i in iafs]+[tf(IF,FAF,"%03d°"%fin,None,1),tf(FAF,MAPT,fin=1),ma(*([MAPT]+MA[(fin,mahf)]+[mahf])),hL if mahf=="LAKNO" else hM]
  return {"n":n,"rwy":rwy,"pg":pg,"fin":fin,"fixes":fixes,"legs":legs,"ma":"Climb on the final course, then turn to join R%s TIF to %s and hold."%("136" if mahf=="LAKNO" else "354",mahf),"info":info}
L.append(conv("ILS Z or LOC RWY 25","47","25",251,["D13R009","D13R136"],"TF620","TF625","MAPT25Z","LAKNO","GS 3.0° · LOC ITIF · "+MSA,("251°/12.7 DME ITIF","251°/5.5 DME ITIF","251°/0.7 DME ITIF")))
L.append(conv("ILS Z or LOC RWY 35","49","35",349,["D13R291","D13R136"],"OTOPI","TF610","MAPT35Z","MENDA","GS 3.0° · LOC ITAI · "+MSA,("349°/12.6 DME ITAI","349°/6.4 DME ITAI","349°/0.6 DME ITAI")))
L.append(conv("VOR RWY 07","51","07",68,["D13R009","D13R291"],"IF07","FAF07","MAPT07","MENDA",VOR,("068°/13 DME TIF","068°/6.9 DME TIF","068°/2.3 DME TIF")))
L.append(conv("VOR RWY 17","53","17",163,["D13R009","D13R308"],"IF17","FAF17","MAPT17","LAKNO",VOR,("163°/13 DME TIF","163°/6.9 DME TIF","163°/2.0 DME TIF")))
L.append(conv("VOR RWY 25","55","25",258,["D13R009","D13R136"],"IF25","FAF25","MAPT25","LAKNO",VOR,("078° R/13 DME TIF","5.8 DME TIF","1.2 DME TIF")))
L.append(conv("VOR RWY 35","57","35",357,["D13R291","D13R136"],"IF35","FAF35","MAPT35","MENDA",VOR,("R177/13 DME TIF","R177/6.2 DME TIF","R177/1.4 DME TIF")))
emit("OETF","Saudi eAIP AD 2 OETF (AIRAC AMDT 11/26)",F,G.X,VAR,L,'/tmp/gw/oetf.js')
