import sys
from playwright.sync_api import sync_playwright
from PIL import Image
pairs=[a.split(':') for a in sys.argv[1:]]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome");c=b.new_context(viewport={"width":980,"height":980});c.add_init_script("if(!sessionStorage.x){sessionStorage.x=1;localStorage.setItem('routeplanner.v2',JSON.stringify({clean1:true,wps:[],theme:'light'}))}");pg=c.new_page()
    e=[];pg.on("pageerror",lambda x:e.append(str(x)))
    pg.goto("http://localhost:8765/");pg.wait_for_timeout(2500)
    ims=[]
    for ap,i in pairs:
        pg.evaluate("([a,i])=>window.__procSet(a,i,true)",[ap,int(i)]);pg.wait_for_timeout(1300)
        pg.screenshot(path='/tmp/p.png');ims.append(Image.open('/tmp/p.png').crop((120,60,980,920)).resize((420,420)))
    o=Image.new('RGB',(1260,420*((len(ims)+2)//3)),'white')
    for k,im in enumerate(ims):o.paste(im,((k%3)*420,(k//3)*420))
    o.save('/tmp/pg.png');print('errors',e)
    b.close()
