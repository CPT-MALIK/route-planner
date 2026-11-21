import sys;sys.path.insert(0,'/tmp/gw')
from lib import *
F=dict(WEJ="261045.6N 0362917.2E",ORBUD="261405.8N 0370250.5E",PUTMU="254745.2N 0364709.9E",IMKEM="263047.6N 0363023.6E",WJ401="260937.9N 0365230.9E",GOKVI="260155.7N 0363448.1E",
FAF33="260741.7N 0363112.2E",RW33="261111.62N 0362900.98E",RW15="261238.24N 0362806.81E",D12R079="261205.7N 0364232.7E",IF33Z="260016.5N 0363549.9E",MAPT33Z="261044.0N 0362918.3E",
D17R359="262747.3N 0363013.6E",TP12R359="262246.8N 0362957.0E",IF15Z="262114.5N 0362243.6E",FAF15Z="261609.7N 0362554.5E",MAPT15Z="261238.2N 0362806.8E",IF33V="260016.0N 0363549.0E",FAF33V="260740.1N 0363112.8E")
VAR=4.2
check(F,"WEJ",VAR,[("ORBUD","WJ401",244.4,10.3),("WJ401","GOKVI",244.4,17.7),("PUTMU","GOKVI",321.8,18.0),("IMKEM","GOKVI",172.1,29.1),("GOKVI","FAF33",330.6,6.6),("FAF33","RW33",330.6,4.0)],
 [("D12R079",79,12),("D17R359",359,17),("TP12R359",359,12),("IF15Z",326,12),("FAF15Z",326,6.2),("MAPT15Z",326,2.1),("IF33V",147,12),("FAF33V",147,3.5)])
G=Geo(F,"WEJ");pol,add=G.pol,G.add
def pt(rad_m,out_min,pt_m,right,pfx,spd=3.0):
  o=rad_m+VAR;A=pol(o,out_min*spd+0.5);B=add(A,pol(pt_m+VAR,3.0));T=G.turn(B,pt_m+VAR,(pt_m+180)%360+VAR,right,1.5,10);E=T[-1]
  h=(pt_m+180+VAR)%360;d=pol(h,1);r=pol(o,1);t,s2=np.linalg.solve(np.array([[d[0],-r[0]],[d[1],-r[1]]]),[-E[0],-E[1]]);I=add(E,(d[0]*t,d[1]*t))
  return G.names(pfx,[A,B]+T+[I])
def maK(start,hdg_m,dist,right,pfx):
  h=hdg_m+VAR;A=add(G.xy(start),pol(h,dist));T=G.turn(A,h,(h+180)%360,right,1.5,10);return G.names(pfx,[A]+T)
MSA="MSA 25 NM WEJ 3000";VOR="VORTAC 113.9 WEJ · "+MSA
hW15=hold("WEJ",326,False,"3000");hW33=hold("WEJ",146,True,"3000");hG=hold("GOKVI",326,False,"3000")
L=[{"n":"ILS Y RWY 33","rwy":"33","pg":"13","fin":326,"fixes":[fx("ORBUD","IAF",""),fx("PUTMU","IAF",""),fx("IMKEM","IAF",""),fx("WJ401","","11000"),fx("GOKVI","IF/MAHF","3000","10.8 DME IWEJ"),fx("FAF33","FAF","1400","4.2 DME IWEJ"),fx("RW33","MAP","")],
 "legs":[tf("ORBUD","WJ401","240°","10.3"),tf("WJ401","GOKVI","240°","17.7"),tf("PUTMU","GOKVI","318°","18.0"),tf("IMKEM","GOKVI","168°","29.1"),tf("GOKVI","FAF33","326°","6.6",1),tf("FAF33","RW33","326°","4.0",1),ma("RW33",["ahead",2.5],"GOKVI"),hG],
 "ma":"Climb on 326° to 2000 FT, turn left direct GOKVI at 3000 FT and hold (inbound 326°, left turns).","info":"GS 3.0° · LOC 110.7 IWEJ · "+MSA}]
L.append({"n":"ILS Z or LOC RWY 33","rwy":"33","pg":"15","fin":326,"fixes":[fx("D12R079","IAF","2000","R079/12 WEJ"),fx("WEJ","IAF/MAHF","3000","WEJ VORTAC"),fx("IF33Z","IF","2000","12.7 DME IWEJ"),fx("FAF33","FAF","1400","4.2 DME IWEJ"),fx("MAPT33Z","MAP","","0.7 DME IWEJ")],
 "legs":[arc("D12R079","IF33Z",False,12,"WEJ","2000"),{"t":"path","pts":["WEJ"]+pt(146,1.5,191,False,"a")[:-1]+["IF33Z"],"lbl":"191° / 011°"},tf("IF33Z","FAF33","326°","8.5",1),tf("FAF33","MAPT33Z",fin=1),ma(*(["MAPT33Z"]+maK("MAPT33Z",326,3,False,"b")+["WEJ"])),hW33],
 "ma":"Climb to 3000 FT on RWY heading until passing 2000 FT, then turn left direct WEJ and hold.","info":"GS 3.0° · LOC 110.7 IWEJ · "+MSA})
L.append({"n":"VOR Z RWY 15","rwy":"15","pg":"27","fin":146,"fixes":[fx("D17R359","IAF","","R359/17 WEJ"),fx("TP12R359","","2000","R359/12 WEJ"),fx("IF15Z","IF","2000","R326/12 WEJ"),fx("FAF15Z","FAF","1400","R326/6.2 WEJ"),fx("MAPT15Z","MAP","","R326/2.1 WEJ"),fx("WEJ","IAF/MAHF","3000","WEJ VORTAC")],
 "legs":[tf("D17R359","TP12R359","179°","5.0"),arc("TP12R359","IF15Z",True,12,"WEJ","2000"),{"t":"path","pts":["WEJ"]+pt(326,1.5,281,True,"c")[:-1]+["IF15Z"],"lbl":"281° / 101°"},tf("IF15Z","FAF15Z","146°","5.8",1),tf("FAF15Z","MAPT15Z",fin=1),ma(*(["MAPT15Z"]+maK("WEJ",146,3,True,"d")+["WEJ"])),hW15],
 "ma":"Climb to 3000 FT on R146 WEJ until passing 2000 FT, then turn right direct WEJ and hold.","info":VOR})
L.append({"n":"VOR Z RWY 33","rwy":"33","pg":"21","fin":327,"fixes":[fx("D12R079","IAF","2000","R079/12 WEJ"),fx("WEJ","IAF/MAP","3000","WEJ VORTAC"),fx("IF33V","IF","2000","R147/12 WEJ"),fx("FAF33V","FAF","","R147/3.5 WEJ")],
 "legs":[arc("D12R079","IF33V",False,12,"WEJ","2000"),tf("IF33V","FAF33V","327°","8.5",1),tf("FAF33V","WEJ",fin=1),ma(*(["WEJ"]+maK("WEJ",326,3,False,"e")+["WEJ"])),hW33],
 "ma":"Climb to 3000 FT on R326 WEJ until passing 2000 FT, then turn left direct WEJ and hold.","info":VOR})
for nm,pg,rad,ptm,right,mins,fin,h,mrad,mright in (("VOR X RWY 15","23",326,281,True,1,146,hW15,146,True),("VOR Y RWY 15","25",326,281,True,2,146,hW15,146,True),
                                                   ("VOR X RWY 33","17",146,191,False,1,326,hW33,326,False),("VOR Y RWY 33","19",146,191,False,2,326,hW33,326,False)):
  T=pt(rad,mins,ptm,right,"p"+nm[4]+str(fin))
  L.append({"n":nm,"rwy":nm[-2:],"pg":pg,"fin":fin,"fixes":[fx("WEJ","IAF/MAP/MAHF","3000","WEJ VORTAC")],
   "legs":[{"t":"path","pts":["WEJ"]+T+["WEJ"],"lbl":"%03d° / %03d°"%(ptm,(ptm+180)%360)},ma(*(["WEJ"]+maK("WEJ",mrad,3,mright,"m"+nm[4]+str(fin))+["WEJ"])),h],
   "ma":"Climb to 3000 FT on R%03d WEJ until passing 2000 FT, then turn %s direct WEJ and hold."%(mrad,"right" if mright else "left"),"info":VOR+(" · outbound %d min"%mins)})
emit("OEWJ","Saudi eAIP AD 2 OEWJ (AIRAC AMDT 11/26)",F,G.X,VAR,L,'/tmp/gw/oewj.js')
