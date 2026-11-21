import sys,glob,os,subprocess
from PIL import Image
ap=sys.argv[1];out='/tmp/w/'+ap;os.makedirs(out,exist_ok=True)
src=('/tmp/t3/src/' if __import__('os').path.isdir('/tmp/t3/src/'+ap) else '/tmp/t2/src/')+ap
fs=[f for f in sorted(os.listdir(src)) if 'abulation' in f.lower() and not f.startswith(('SID','STAR','ATC','Radar'))]
D=[]
for f in fs:
  b=os.path.join(out,'r_'+str(len(D)))
  subprocess.run(['pdftoppm','-r','170','-png','-singlefile',os.path.join(src,f),b])
  im=Image.open(b+'.png').convert('L');W,H=im.size;px=im.load()
  ys=[y for y in range(int(H*.12),H-int(H*.08)) if sum(1 for x in range(int(W*.13),int(W*.9),3) if px[x,y]<120)>2]
  # cluster into runs, drop runs separated by >250 px gap at the end
  last=ys[0]
  for y in ys:
    if y-last>260:break
    last=y
  D.append((f,im.crop((int(W*.10),ys[0]-5,int(W*.94),last+8))))
  print(len(D)-1,f,D[-1][1].size)
k=0;i=0
while i<len(D):
  grp=[];h=0
  while i<len(D) and (h+D[i][1].height<1500 or not grp):grp.append(D[i][1]);h+=D[i][1].height+14;i+=1
  Wd=max(g.width for g in grp);o=Image.new('L',(Wd,h),255);y=0
  for g in grp:o.paste(g,(0,y));y+=g.height+14
  o.save(out+'/S%d.png'%k);print('S%d'%k,o.size);k+=1
