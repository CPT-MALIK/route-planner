import sys,json
from PIL import Image
ap=sys.argv[1];names=sys.argv[2:]
s=open('/home/claude/route-planner/index.html').read();k=s.find('CHARTS=');o,_=json.JSONDecoder().raw_decode(s[k+7:])
C={c['t']:c['pg'] for c in o.get(ap,[]) if c['k']=='APP'}
if not names:print(C);sys.exit()
ims=[]
for n in names:
  pg=C[n];im=Image.open('/home/claude/route-planner/charts/%s/AD2-%s-%s.webp'%(ap,ap,pg)).convert('L');W,H=im.size
  a=im.crop((int(W*.1),int(H*.16),int(W*.92),int(H*.62)));b=im.crop((int(W*.06),int(H*.62),int(W*.5),int(H*.74)))
  a=a.resize((640,int(a.height*640/a.width)));b=b.resize((640,int(b.height*640/b.width)))
  t=Image.new('L',(640,a.height+b.height+4),255);t.paste(a,(0,0));t.paste(b,(0,a.height+4));ims.append(t)
for k in range(0,len(ims),2):
  g=ims[k:k+2];o2=Image.new('L',(1290,max(i.height for i in g)),255)
  for j,i in enumerate(g):o2.paste(i,(j*650,0))
  o2.save('/tmp/w/%s/C%d.png'%(ap,k//2));print('C%d'%(k//2),[names[k+j] for j in range(len(g))])
