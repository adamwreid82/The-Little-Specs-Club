"""Create native SVG layouts from current Book 1 art and retained repair layers.

Illustrations remain embedded raster. Story text is real SVG text. SVG morphology
recovers background only beneath the old lettering, so deleting live text does
not expose a second baked copy. No character artwork is regenerated.
"""
from pathlib import Path
import base64, collections, csv, hashlib, io, json, re, subprocess, sys
from scipy.signal import correlate
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from lxml import etree as E
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

P=Path(__file__).resolve().parent
ROOT=P.parent
REPAIR=ROOT/'spread_repairs_2026_11_07'
OUT=P/'deliverables';OUT.mkdir(exist_ok=True)
NS='http://www.w3.org/2000/svg';INK='http://www.inkscape.org/namespaces/inkscape'
SOD='http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd'
XL='http://www.w3.org/1999/xlink'
def node(p,tag,**kw):
 return E.SubElement(p,'{'+NS+'}'+tag,{k.replace('_','-'):str(v) for k,v in kw.items()})
def layer(p,id,label,hidden=False):
 n=node(p,'g',id=id);n.set('{'+INK+'}groupmode','layer');n.set('{'+INK+'}label',label)
 if hidden:n.set('style','display:none')
 return n
def uri(data,mime='image/png'):
 if isinstance(data,Path):data=data.read_bytes()
 return 'data:'+mime+';base64,'+base64.b64encode(data).decode()
def png(im):
 b=io.BytesIO();im.save(b,format='PNG');return b.getvalue()
def pic(p,im,x,y,w,h,**kw):
 n=node(p,'image',x=x,y=y,width=w,height=h,preserveAspectRatio='none',**kw)
 n.set('{'+XL+'}href',uri(im));return n
def hashfile(p):return hashlib.sha256(p.read_bytes()).hexdigest()

if not (P/'Roboto-Bold.ttf').exists():
 instantiateVariableFont(TTFont(P/'Roboto.ttf'),{'wght':700,'wdth':100}).save(P/'Roboto-Bold.ttf')
fonts={400:ImageFont.truetype(str(P/'Roboto.ttf'),75),700:ImageFont.truetype(str(P/'Roboto-Bold.ttf'),75)}
groups=json.loads((P/'text_records_draft.json').read_text())
for g in groups:
 for q in g['lines']:
  s=q['text'].replace("'",'’').replace('“|','“I').replace('. | help','. I help').replace('“Im Ms.','“I’m Ms.').replace('"A fire','“A fire').replace('belongs,’','belongs,”').replace('now?’','now?”')
  q['text']=s
  q['weight']=700 if g['pages']=='32-33' and (s in ['Little Specs Construction Facts','Vinny’s Safety Corner','Next Time...','UP!','Next:','The Little Specs Club','The Fire Station','Book 2: The Fire Station Takes Shape'] or s.endswith('?')) else 400
groups.insert(0,{'pages':'02-03','side':'title','lines':[
 {'text':'Project One: The Fire Station','box':[770,1400,1730,1500],'weight':400},
 {'text':'Book 1','box':[1120,1550,1380,1650],'weight':400},
 {'text':'A Fire Station Begins','box':[890,1710,1610,1810],'weight':400},
 {'text':'This Book Belongs To:','box':[870,1970,1630,2075],'weight':400},
]})
inventory=json.loads((P/'inventory.json').read_text())
patches=json.loads((REPAIR/'records/patches.json').read_text())
logos=json.loads((REPAIR/'records/overlays.json').read_text())
old={r['pages']:r for r in json.loads((ROOT/'spread_review_2026_11_04/deliverables/Book1_People_Source_Review_2026-11-05.json').read_text())['spreads']}

def fit_line(arr,q):
 s=q['text'];f=fonts[q['weight']];l,t,r,b=f.getbbox(s,anchor='ls')
 glyph=Image.new('L',(r-l+8,b-t+8));ImageDraw.Draw(glyph).text((4-l,4-t),s,font=f,fill=255,anchor='ls')
 template=(np.asarray(glyph)>127).astype('uint8')*255
 x0,y0,x1,y1=q['box'];x0=max(0,x0-40);y0=max(0,y0-45);x1=min(5100,max(x1+40,x0+glyph.width+80));y1=min(2550,max(y1+45,y0+glyph.height+80))
 crop=arr[y0:y1,x0:x1]
 # All production body copy is dark blue on a light background.
 binary=((crop[:,:,0]<110)&(crop[:,:,1]<130)&(crop[:,:,2]<165)).astype('uint8')*255
 binary=binary.astype('float32')/255;template=template.astype('float32')/255
 centered=template-template.mean();num=correlate(binary,centered,mode='valid',method='fft')
 kernel=np.ones(template.shape,dtype='float32');total=correlate(binary,kernel,mode='valid',method='fft')
 denom=np.sqrt(np.maximum(total-total**2/template.size,1e-6)*np.sum(centered**2))
 match=num/denom;iy,ix=np.unravel_index(np.argmax(match),match.shape);score=float(match[iy,ix]);pt=(int(ix),int(iy))
 x=x0+pt[0]+4-l;y=y0+pt[1]+4-t
 q.update(x=x,baseline=y,font_size=75,match_score=round(score,5),ink_box=[x+l,y+t,x+r,y+b])
 # Recover the exact source color from the most common dark pixel.
 A=arr[max(0,y+t):y+b,max(0,x+l):x+r];px=A[(A[:,:,0]<110)&(A[:,:,1]<130)&(A[:,:,2]<165)]
 col,cnt=np.unique(px,axis=0,return_counts=True);q['fill']='#'+''.join(f'{v:02x}' for v in col[np.argmax(cnt)])
 return q

manifest=[]
for entry in inventory:
 pg=entry['pages']
 if len(sys.argv)>1 and pg not in sys.argv[1:]:continue
 latest=Path(entry['path']);im=Image.open(latest).convert('RGB');arr=np.asarray(im)
 gs=[g for g in groups if g['pages']==pg]
 for g in gs:
  for q in g['lines']:
   fit_line(arr,q)
   if g['side']!='title':
    shift=(2920 if pg=='04-05' else (180 if g['side']=='left' else 2820))-q['x']
    q['x']+=shift;q['ink_box'][0]+=shift;q['ink_box'][2]+=shift
 root=E.Element('{'+NS+'}svg',nsmap={None:NS,'xlink':XL,'inkscape':INK,'sodipodi':SOD},width='17in',height='8.5in',viewBox='0 0 5100 2550',version='1.1')
 node(root,'title').text=f'The Little Specs Club, Book 1, pages {pg}, source REV{entry["revision"]}, layered SVG companion'
 node(root,'desc').text='Editable story text and retained repair/branding layers. Character and background illustrations are embedded raster, not individually editable vector paths. Original PNG and approval remain separate. This new SVG requires review.'
 md={'pages':pg,'source_png':entry['filename'],'source_drive_id':entry['id'],'source_sha256':entry['sha256'],'source_status':entry['status'],'svg_status':'REVIEW_REQUIRED','illustrations':'embedded raster','text':'live editable SVG text','background_recovery':'native SVG morphology only under source lettering','fully_vector':False}
 node(root,'metadata',id='production-record').text=json.dumps(md)
 defs=node(root,'defs')
 node(defs,'style',type='text/css').text="@font-face{font-family:'Roboto';src:url("+uri(P/'Roboto.ttf','font/ttf')+") format('truetype');font-weight:100 900;} text{font-family:Roboto,sans-serif;font-size:75px;}"
 fil=node(defs,'filter',id='text-background-recovery',x='-10%',y='-30%',width='120%',height='160%',color_interpolation_filters='sRGB')
 radius=16 if pg=='32-33' else 8
 node(fil,'feMorphology',operator='dilate',radius=radius,result='expanded')
 node(fil,'feMorphology',operator='erode',radius=radius,result='closed')
 node(fil,'feGaussianBlur',stdDeviation='0.65')
 base=layer(root,'illustration','01 Illustration | embedded raster')
 related=[r for r in patches if r['id']==pg]
 basepath=latest if not related else ROOT/'spread_review_2026_11_04/spreads'/related[0]['original']
 pic(base,basepath,0,0,5100,2550,id='source-illustration')
 repairs=layer(root,'repair-layers','02 Retained character and helmet cleanup layers')
 for r in related:
  key=pg+'_'+r.get('key','Rivera');x,y,w,h=r['crop'];n=layer(repairs,key,key.replace('_',' ')+' | raster patch')
  pic(n,REPAIR/'generated'/f'{key}_patch.png',x,y,w,h)
 branding=layer(root,'branding','03 Separately placed source logos and stickers')
 relatedlogos=[r for r in logos if r['id']==pg]
 for r in relatedlogos:
  key=pg+'_'+r['key'];x,y,w,h=r['layer_box'];n=layer(branding,key+'-branding',r['key']+' | '+r['asset'].replace('_',' '))
  pic(n,REPAIR/'generated'/f'{key}_logo.png',x,y,w,h,id=key+'-image')
 cleanup=layer(root,'text-background','04 Text background recovery | keep visible')
 textlayer=layer(root,'editable-text','05 EDITABLE TEXT | Roboto 75 px')
 for gi,g in enumerate(gs):
  lines=g['lines'];x0=max(0,min(q['ink_box'][0] for q in lines)-25);y0=max(0,min(q['ink_box'][1] for q in lines)-25);x1=min(5100,max(q['ink_box'][2] for q in lines)+25);y1=min(2550,max(q['ink_box'][3] for q in lines)+25)
  crop=im.crop((x0,y0,x1,y1));a=np.asarray(crop);mask=np.zeros((y1-y0,x1-x0),dtype=np.uint8)
  for q in lines:
   l,t,r,b=q['ink_box'];ol,ot,orr,ob=q['box']
   l=min(l,ol);t=min(t,ot);r=max(r,orr);b=max(b,ob)
   l=max(x0,l-4)-x0;t=max(y0,t-4)-y0;r=min(x1,r+4)-x0;b=min(y1,b+4)-y0
   aa=a[t:b,l:r];dark=(aa[:,:,0]<150)&(aa[:,:,1]<165)&(aa[:,:,2]<205)
   mask[t:b,l:r]=dark.astype('uint8')*255
  mask=Image.fromarray(mask).filter(ImageFilter.MaxFilter(7))
  mask.save(P/'qa'/f'{pg}_{g["side"]}_glyph_mask.png')
  m=node(defs,'mask',id=f'textmask-{gi}',maskUnits='userSpaceOnUse',x=x0,y=y0,width=x1-x0,height=y1-y0)
  pic(m,png(mask.convert('RGB')),x0,y0,x1-x0,y1-y0)
  cg=node(cleanup,'g',mask=f'url(#textmask-{gi})')
  pic(cg,png(crop),x0,y0,x1-x0,y1-y0,filter='url(#text-background-recovery)')
  tg=layer(textlayer,'text-'+g['side'],g['side'].capitalize()+' page text')
  for j,q in enumerate(lines):
   tx=node(tg,'text',id=f'{g["side"]}-line-{j+1:02}',x=q['x'],y=q['baseline'],fill=q['fill'],font_weight=q['weight'])
   tx.set('{http://www.w3.org/XML/1998/namespace}space','preserve');tx.text=q['text']
 guides=layer(root,'guides','90 Nonprinting page and gutter guides',True)
 node(guides,'path',d='M2550 0 V2550',stroke='#ff00ff',stroke_width=2,fill='none')
 node(guides,'rect',x=2437,y=0,width=226,height=2550,fill='#ff00ff',opacity='.1')
 name=f'Book1_Pages{pg}_REV{entry["revision"]}_LAYERED_EDITABLE_TEXT_REVIEW.svg'
 target=OUT/name;E.ElementTree(root).write(str(target),encoding='UTF-8',xml_declaration=True,pretty_print=True)
 record={**entry,'svg_filename':name,'svg_path':str(target),'svg_sha256':hashfile(target),'svg_bytes':target.stat().st_size,'text_lines':sum(len(g['lines']) for g in gs),'repair_layers':len(related),'separate_branding_objects':len(relatedlogos),'fully_vector':False,'text_groups':gs}
 manifest.append(record)
 print(pg,'text',record['text_lines'],'branding',len(relatedlogos),'min_fit',min(q['match_score'] for g in gs for q in g['lines']),flush=True)
if len(sys.argv)>1 and (P/'build_records.json').exists():
 previous={e['pages']:e for e in json.loads((P/'build_records.json').read_text())}
 previous.update({e['pages']:e for e in manifest});manifest=[previous[k] for k in sorted(previous)]
(P/'build_records.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
