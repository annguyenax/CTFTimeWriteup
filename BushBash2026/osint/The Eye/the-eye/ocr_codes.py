import cv2, numpy as np
from scipy.spatial import cKDTree

im=cv2.imread('dots.png'); b,g,r=cv2.split(im)
mask=((r>90)&(r>g*1.35)&(r>b*1.35)).astype('uint8')
d=cv2.dilate(mask*255,cv2.getStructuringElement(cv2.MORPH_RECT,(5,2)))
n,lab,st,cen=cv2.connectedComponentsWithStats(d)
words=[]
for x,y,w,h,a in st[1:]:
    if 12<=w<=42 and 6<=h<=18 and a>=25: words.append((x+w/2,y+h/2,x,y,w,h))
tree=cKDTree(np.array([(z[0],z[1]) for z in words]))

known=[
((2080.5,928.5),'200F'),((2234,965.5),'B9A3'),((2169.5,772.5),'A82F'),((2189,1154.5),'299B'),((1335,606.5),'18C6'),((1704,1184.5),'28F0'),((2062,1279.5),'B82C'),((1267.5,684.5),'F05A'),
((632,310.5),'DB92'),((557.5,173.5),'916A'),((482,328.5),'F92D'),((690.5,94.5),'BFCC'),((888,941.5),'9F52'),((1011,356.5),'290A'),((830,85.5),'1009'),((962,929.5),'EBBE'),
((393.5,418.5),'C901'),((246.5,385.5),'E290'),((240,537.5),'E29D'),((342,194.5),'10BB'),((976,966.5),'F901'),((803.5,327.5),'D957'),((494.5,119.5),'A6EE'),((1023.5,929.5),'49A0'),
((1730.5,489.5),'2778'),((1858.5,365.5),'FAED'),((1667.5,319),'B82C'),((1976.5,489.5),'72AB'),((1093.5,949.5),'0F27'),((1783,899.5),'571A'),((2048.5,665.5),'CB2D'),((1142.5,1025.5),'28F0'),
((722.5,373.5),'F0B1'),((820.5,249.5),'1057'),((865,409.5),'AA9B'),((701,169.5),'10F6'),((442,936.5),'02E3'),((388,911.5),'B000'),
((2220,142.5),'A81F'),((2212.5,183),'8DF7'),((2197.5,223.5),'F78A'),((2311,159.5),'C718'),((2345.5,258.5),'0003'),((2116.5,162.5),'8FFF'),((2272.5,247.5),'295F')]

def glyphs(cx,cy):
    x0=max(0,int(round(cx))-27);x1=min(mask.shape[1],int(round(cx))+28)
    y0=max(0,int(round(cy))-7);y1=min(mask.shape[0],int(round(cy))+7)
    roi=mask[y0:y1,x0:x1]
    nn,ll,ss,cc=cv2.connectedComponentsWithStats(roi)
    out=[]
    for i,(x,y,w,h,a) in enumerate(ss[1:],1):
        if a>=8 and h>=7 and w<=11:
            z=(ll[y:y+h,x:x+w]==i).astype('uint8')
            canvas=np.zeros((14,12),dtype='uint8')
            # preserve the characteristic glyph width; centre horizontally and
            # align its baseline at row 11.
            xx=(12-w)//2; yy=11-h+1
            canvas[yy:yy+h,xx:xx+w]=z
            out.append((x,canvas,w,h,a))
    out.sort(key=lambda q:q[0])
    return out

samples=[]
for pos,text in known:
    dist,wi=tree.query(pos)
    gs=glyphs(words[wi][0],words[wi][1])
    if len(gs)!=4:
        print('bad training segmentation',pos,text,len(gs));continue
    for (_,arr,w,h,a),ch in zip(gs,text):samples.append((arr,w,h,ch,text,pos))

def gd(a,b):
    # tolerate a one-pixel vertical rasterization shift.
    return min(np.count_nonzero(a!=np.roll(b,s,axis=0)) for s in (-1,0,1))

def classify(arr,w,h):
    scores=[]
    for ta,tw,th,ch,*_ in samples:
        scores.append((gd(arr,ta)+2*abs(w-tw)+abs(h-th),ch))
    scores.sort()
    # vote among the nearest renderings; repeated training examples damp errors.
    top=scores[:5]
    by={}
    for score,ch in top:by[ch]=by.get(ch,0)+1/(1+score)
    return max(by,key=by.get),scores[0][0]

ok=tot=0
for pos,text in known:
    _,wi=tree.query(pos);gs=glyphs(words[wi][0],words[wi][1])
    if len(gs)==4:
        got=''.join(classify(a,w,h)[0] for _,a,w,h,_ in gs);ok+=got==text;tot+=1
        if got!=text:print('training mismatch',pos,text,got)
print('training words',ok,'/',tot,'samples',len(samples))

codes=[]
for z in words:
    gs=glyphs(z[0],z[1])
    if len(gs)==4:
        code=''.join(classify(a,w,h)[0] for _,a,w,h,_ in gs)
        confidence=sum(classify(a,w,h)[1] for _,a,w,h,_ in gs)
    else: code=None;confidence=999
    codes.append(code)
manual_missing={
2:'A09B',16:'1009',22:'AA40',28:'A89C',31:'EC84',33:'AB8D',51:'AAC2',56:'AA8A',63:'A890',70:'8AA7',71:'EAEA',72:'F38A',73:'B009',78:'8266',82:'92A8',87:'EAFE',88:'290A',90:'10A3',91:'EAED',92:'F82D',101:'E290',105:'0025',107:'AA98',119:'5AB0',124:'0980',136:'A890',137:'1850',138:'7A90',139:'FABB',155:'B02A',156:'B893',159:'E72A',160:'FB88',163:'D1A9',164:'8AD7',176:'3040',178:'F05A',192:'8A9F',196:'A82F',200:'A900',201:'400A',205:'002E',213:'77A8',216:'3589',221:'09A2',231:'D4F9',233:'B000',250:'20AF',255:'F901',280:'8AFE',287:'99E2',289:'30AC',295:'1194',298:'E92A',300:'CE06',302:'B7A8',312:'A2F1',315:'000B',320:'AAA5',324:'AA0A',331:'0B00',338:'8930',340:'D190',347:'9A40',348:'205F',349:'0A2F',353:'B824',357:'A295',372:'20AF',392:'002F',400:'A201',404:'150B',405:'590A',409:'C345',418:'FAFD',432:'FAAA'}
for i,c in manual_missing.items(): codes[i]=c
for i,(z,c) in enumerate(zip(words,codes)):
    print(i,round(z[0],1),round(z[1],1),c)
