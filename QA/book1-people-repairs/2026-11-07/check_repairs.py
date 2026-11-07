import json,hashlib,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
p=Path(__file__).resolve().parent
prior=p.parent/'spread_review_2026_11_04'
patches=json.loads((p/'records/patches.json').read_text())
overlays=json.loads((p/'records/overlays.json').read_text())
results=[]
(p/'qa').mkdir(exist_ok=True)
for id in sorted(set(r['id'] for r in patches)):
 rs=[r for r in patches if r['id']==id];r=rs[0]
 source=prior/'spreads'/r['original'];candidate=p/'candidates'/f'Book1_Pages{id}_REV{r["revision"]}_PEOPLE_REPAIRS_REVIEW.png'
 a=np.array(Image.open(source).convert('RGB'));b=np.array(Image.open(candidate).convert('RGB'))
 assert a.shape==b.shape==(2550,5100,3)
 allowed=np.zeros(a.shape[:2],dtype=bool)
 for row in rs:
  x,y,w,h=row['crop'];key=id+'_'+row.get('key','Rivera')
  mask=np.array(Image.open(p/'generated'/f'{key}_mask.png').convert('L'))>0
  allowed[y:y+h,x:x+w]|=mask
  for kind,im in [('before',source),('after',candidate)]:
   target=p/'qa'/f'{key}_{kind}.jpg'
   subprocess.run(['magick',str(im),'-crop',f'{w}x{h}+{x}+{y}','+repage','-resize','1200x900>','-quality','93',str(target)],check=True)
 for row in [o for o in overlays if o['id']==id]:
  x,y,w,h=row['layer_box'];mask=np.array(Image.open(p/'generated'/f'{id}_{row["key"]}_logo.png').convert('RGBA'))[:,:,3]>0
  allowed[y:y+h,x:x+w]|=mask
 changed=np.any(a!=b,axis=2)
 outside=int(np.count_nonzero(changed&~allowed));assert outside==0,(id,outside)
 results.append(dict(pages=id,revision=r['revision'],filename=candidate.name,sha256=hashlib.sha256(candidate.read_bytes()).hexdigest(),bytes=candidate.stat().st_size,dimensions=[5100,2550],source_filename=source.name,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),changed_pixels=int(changed.sum()),changed_percent=round(100*changed.mean(),4),changed_outside_repair_masks=outside,preservation='PASS - all RGB pixels outside documented repairs identical'))
 print(id,results[-1]['changed_percent'],'percent changed; outside masks:',outside,flush=True)
(p/'records/pixel_qa.json').write_text(json.dumps(results,indent=2))
