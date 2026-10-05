import json,base64,io,struct,hashlib,shutil
from pathlib import Path
import numpy as np
from PIL import Image,ImageFont,ImageDraw,ImageOps
p=Path(__file__).resolve().parents[1];d=json.loads((p/'src/segregation-data.json').read_text(encoding='utf-8'));source=p/'references/esoteric-fonts'
def cmap(path):
 b=path.read_bytes();tables={b[12+i*16:16+i*16]:struct.unpack_from('>II',b,20+i*16) for i in range(struct.unpack_from('>H',b,4)[0])};off=tables[b'cmap'][0];result={}
 for i in range(struct.unpack_from('>H',b,off+2)[0]):
  sub=off+struct.unpack_from('>I',b,off+8+i*8)[0];fmt=struct.unpack_from('>H',b,sub)[0]
  if fmt!=4:continue
  n=struct.unpack_from('>H',b,sub+6)[0]//2;ends=struct.unpack_from('>'+str(n)+'H',b,sub+14);starts=struct.unpack_from('>'+str(n)+'H',b,sub+16+2*n);delta=struct.unpack_from('>'+str(n)+'h',b,sub+16+4*n);rpos=sub+16+6*n;offsets=struct.unpack_from('>'+str(n)+'H',b,rpos)
  for j in range(n):
   for cp in range(starts[j],min(ends[j],65534)+1):
    if offsets[j]:
     idx=rpos+2*j+offsets[j]+2*(cp-starts[j]);gid=struct.unpack_from('>H',b,idx)[0];gid=(gid+delta[j])%65536 if gid else 0
    else:gid=(cp+delta[j])%65536
    if gid:result[cp]=gid
 return result

def uri(im):
 o=io.BytesIO();im.save(o,format='PNG');return 'data:image/png;base64,'+base64.b64encode(o.getvalue()).decode()
def decode(url):return Image.open(io.BytesIO(base64.b64decode(url.split(',',1)[1]))).convert('RGB')
def mask(im):
 a=np.array(im.convert('L'));m=a<min(180,float(np.percentile(a,25))+25);ys,xs=np.where(m)
 if not len(xs):return np.zeros((32,24),bool)
 return np.array(Image.fromarray(m[ys.min():ys.max()+1,xs.min():xs.max()+1].astype('uint8')*255).resize((24,32),Image.Resampling.NEAREST))>0

def dilate(m):
 a=np.pad(m,1);return np.logical_or.reduce([a[y:y+32,x:x+24] for y in range(3) for x in range(3)])
def score(a,b):
 return float(((a&dilate(b)).sum()/max(1,a.sum())+(b&dilate(a)).sum()/max(1,b.sum()))/2)
files={'Theban':'Theban_TGEA.ttf','Alphabet of the Magi':'Magi.ttf','Celestial font':'celestial_TGEA.ttf','Malachim font':'Malachim_TGEA.ttf','Passing the River font':'Transitus_Fluvii_TGEA.ttf','Chaldean':'Chaldaen Theseus Ambrosius.ttf','Enochian':'Enochian-3188.ttf'}
refs=[];manifest=[]
for family,file in files.items():
 path=source/file;font=ImageFont.truetype(str(path),72);mapping=cmap(path);seen=set();count=0
 for cp in list(range(65,91))+list(range(97,123))+list(range(0x5d0,0x5eb)):
  gid=mapping.get(cp)
  if not gid or gid in seen:continue
  seen.add(gid);char=chr(cp);box=font.getbbox(char);im=Image.new('RGB',(max(1,box[2]-box[0]+8),max(1,box[3]-box[1]+8)),'white');ImageDraw.Draw(im).text((4-box[0],4-box[1]),char,font=font,fill='black');m=mask(im)
  if not m.any():continue
  refs.append({'family':family,'fontKey':char,'glyphId':gid,'image':uri(im),'mask':m});count+=1
 manifest.append({'family':family,'file':file,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'forms':count})
orientations={'original':lambda im:im,'rotate90':lambda im:im.transpose(Image.Transpose.ROTATE_90),'rotate180':lambda im:im.transpose(Image.Transpose.ROTATE_180),'rotate270':lambda im:im.transpose(Image.Transpose.ROTATE_270),'mirror':ImageOps.mirror,'mirror90':lambda im:ImageOps.mirror(im).transpose(Image.Transpose.ROTATE_90),'mirror180':lambda im:ImageOps.mirror(im).transpose(Image.Transpose.ROTATE_180),'mirror270':lambda im:ImageOps.mirror(im).transpose(Image.Transpose.ROTATE_270)}
rows=[]
for item in d['items']:
 if 'sample' not in item:continue
 im=decode(item['image'])
 for orientation,transform in orientations.items():
  m=mask(transform(im))
  ranked=sorted([(score(m,r['mask']),r) for r in refs],key=lambda pair:pair[0],reverse=True)
  top=ranked[:3];lead=top[0][0]-top[1][0];rows.append({'id':item['id'],'region':item['region'],'orientation':orientation,'top':[{'family':r['family'],'fontKey':r['fontKey'],'score':round(s*100,2),'image':r['image']} for s,r in top],'lead':round(lead*100,2),'passesShapeScreen':top[0][0]>=.9 and lead>=.1})
unknown=[r for r in rows if r['id']=='G099'];counts={region:sum(r['passesShapeScreen'] for r in rows if r['region']==region and r['orientation']=='original') for region in set(r['region'] for r in rows)}
readings=[{'region':'Upper left three lines','text':'я:надеюсь:что:сюда / будут:присылать / много:биткоинов','meaning':'I hope that many bitcoins will be sent here.','status':'Existing community plaintext; reproduced with crib derived image templates.'},{'region':'Lower left','text':'сумма:двух:чисел','meaning':'Sum of two numbers.','status':'Existing community plaintext; held out same artwork recognition previously 92.9 percent.'},{'region':'Right border','text':'здесь:зашифрованы:биткоины:на:черный:день:номер:□','meaning':'Here bitcoins are encoded for a rainy day, number [unknown].','status':'Existing community plaintext; terminal glyph remains unknown. The idiom черный день means a rainy day or hard times.'},{'region':'Above Trump','text':'TUESDAY','meaning':'Tuesday.','status':'Existing English cipher reading. Independent chart only recognition previously 71.4 percent.'}]
result={'readings':readings,'fonts':manifest,'referenceForms':len(refs),'comparisons':len(rows),'rows':rows,'unknownCandidates':unknown,'originalShapeScreenCounts':counts,'license':'Reference fonts by Joseph H. Peterson, CC BY 4.0, https://esotericarchives.com/fonts/ . Font glyphs rendered and normalized for analysis. Changes: size normalization and bitmap reference crops. https://creativecommons.org/licenses/by/4.0/','method':'106 glyphs against seven font families under eight fixed rotations and reflections. Glyph cmap entries must exist; duplicate glyph IDs excluded. Score is bidirectional one pixel tolerant ink overlap after 24 by 32 normalization. Shape screen uses score >=90 and lead >=10 percentage points. Font keys are encoding labels, not independently verified transliterations. Passing this screen is not acceptance of a letter or family.','conclusion':'No new plaintext or terminal glyph value is accepted. No interpretation is established by a single nearest shape. Existing messages are separated from author verified keys and unresolved positions are retained.'}
(p/'src/decipher-data.json').write_text(json.dumps(result,ensure_ascii=False),encoding='utf-8');(p/'reports/decipherment-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');(p/'licenses/Esoteric-Fonts-ATTRIBUTION.txt').write_text(result['license'],encoding='utf-8')
print(json.dumps({'referenceForms':len(refs),'comparisons':len(rows),'fontCounts':[(f['family'],f['forms']) for f in manifest],'originalShapeScreenCounts':counts,'unknownTop':[(r['orientation'],r['top'][0]['family'],r['top'][0]['fontKey'],r['top'][0]['score'],r['lead']) for r in unknown]},ensure_ascii=False))
