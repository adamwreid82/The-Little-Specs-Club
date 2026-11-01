from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,re,shutil
from scipy.ndimage import map_coordinates
W=Path(__file__).resolve().parent;OUT=W/'deliverables';P=OUT/'Eight_View_PNGs';P.mkdir(parents=True,exist_ok=True)
plan=json.loads((W/'edit_plan.json').read_text());D=plan['characters'];F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
cleanfiles=['exec-c8c6e77b-9ef9-4079-be50-638f6247fcff.png','exec-355c8c98-c9df-4983-b475-eb60de2de734.png']
for i,f in enumerate(cleanfiles):shutil.copyfile(W.parent/'generated_images'/f,W/f'cleanup_result_{i+1}.png')
clean=[Image.open(W/f'cleanup_result_{i+1}.png').convert('RGB').resize((1536,1536),Image.Resampling.LANCZOS) for i in range(2)]
records=[];tiles=[]
for r in D:
 src=W/'inputs'/r['filename'];orig=Image.open(src).convert('RGB');out=orig.copy();allowed=np.zeros((orig.height,orig.width),bool)
 for m in r['marks']:
  cx,cy=m['center'];a=m['atlas'];x0,y0=a['origin'];j=a['cell'];tx=j%6*256;ty=j//6*256
  before=np.array(orig.crop((x0,y0,x0+128,y0+128))).astype(float)
  bg=np.array(clean[a['file']-1].crop((tx,ty,tx+256,ty+256)).resize((128,128),Image.Resampling.LANCZOS)).astype(float)
  yy,xx=np.mgrid[0:128,0:128];dx=xx-(cx-x0);dy=yy-(cy-y0);w,h,angle=m['old_ellipse'];th=np.deg2rad(angle)
  u=dx*np.cos(th)-dy*np.sin(th);v=dx*np.sin(th)+dy*np.cos(th)
  # Narrow antialiased mask includes the existing decal edge and preserves its rendered perspective.
  radius=np.sqrt((u/(w/2+1.5))**2+(v/(h/2+1.5))**2)
  alpha=np.clip((1-radius)*min(w,h)/2+0.5,0,1)
  radius_clean=np.sqrt((u/(w/2+5))**2+(v/(h/2+5))**2)
  mask=np.clip((1-radius_clean)*min(w,h)/2,0,1)
  # Match generated shell color to the unedited surrounding shell before bounded compositing.
  ring=(radius_clean>1.02)&(radius_clean<1.18)
  A=np.stack([np.ones_like(dx),dx/64,dy/64],axis=-1)
  for k in range(3):
   coef=np.linalg.lstsq(A[ring],(before-bg)[ring,k],rcond=None)[0];bg[:,:,k]+=A@coef
  repaired=before*(1-mask[:,:,None])+np.clip(bg,0,255)*mask[:,:,None]
  s=m['scale'];sx=dx/s+cx-x0;sy=dy/s+cy-y0
  aa=map_coordinates(alpha,[sy,sx],order=1,mode='constant',cval=0)
  # Sample the original flattened sticker pixels; no replacement or regeneration of the decal artwork.
  sampled=np.stack([map_coordinates(before[:,:,k],[sy,sx],order=3,mode='nearest') for k in range(3)],axis=2)
  final=np.clip(np.rint(repaired*(1-aa[:,:,None])+sampled*aa[:,:,None]),0,255).astype('uint8')
  out.paste(Image.fromarray(final),(x0,y0));allowed[y0:y0+128,x0:x0+128]|=(mask>0)|(aa>0)
  tiles.append((r['character'],m['view'],Image.fromarray(final).resize((256,256),Image.Resampling.LANCZOS)))
  m['new_ellipse']=[w*s,h*s,angle]
 # Footer is a new review label in the existing footer strip.
 old_rev=int(re.search(r'_R(\d+)\.png$',r['filename']).group(1));new_rev=old_rev+1
 draw=ImageDraw.Draw(out);draw.rectangle((0,1994,3071,2047),fill='white');draw.text((36,2009),f'{r["character"].replace("_"," ")} | PPE R{new_rev} | JOBSITE STICKER SIZE REVIEW | Ben R10 / Leo R8 eight-view reference | PENDING AUTHOR APPROVAL',font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20),fill='#173d70');allowed[1994:]=True
 fn=f'{r["character"]}_PPE_8_Angles_REVIEW_R{new_rev}.png';dest=P/fn;out.save(dest)
 delta=np.any(np.array(out)!=np.array(orig),axis=2);assert not (delta&~allowed).any()
 records.append({**r,'new_revision':new_rev,'new_filename':fn,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'changed_pixels':int(delta.sum()),'changed_pixels_outside_stickers_and_footer':int((delta&~allowed).sum()),'approval':'PENDING_AUTHOR_REVIEW'})
# Untouched standards and established no-sticker exception are included in the review package.
for fname,key,revision in [('ben_approved.png','Ben','APPROVED_R10'),('leo_approved.png','Leo','APPROVED_R8'),('Rebecca_Foster_PPE_8_Angles_REVIEW_R3.png','Rebecca_Foster','REVIEW_R3')]:
 src=W/'inputs'/fname;fn=f'{key}_PPE_8_Angles_{revision}_UNCHANGED.png';shutil.copyfile(src,P/fn)
 records.append({'character':key,'source_filename':fname,'new_filename':fn,'unchanged':True,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'reason':'Approved eight-view size reference' if key!='Rebecca_Foster' else 'Canon no-jobsite-sticker exception'})
(OUT/'Eight_View_Sticker_Size_Record.json').write_text(json.dumps({'status':'PENDING_AUTHOR_REVIEW','reference_ratio':.19,'reference_measurements':plan['reference_measurements'],'characters':records},indent=2))
for off in range(0,len(tiles),36):
 o=Image.new('RGB',(1536,1728),'#e2e6ed');d=ImageDraw.Draw(o)
 for k,(name,view,im) in enumerate(tiles[off:off+36]):
  x=k%6*256;y=k//6*288;o.paste(im,(x,y+30));d.text((x+4,y+4),f'{name} | view {view}',font=F,fill='black')
 o.save(W/f'edited_stickers_{off//36+1}.jpg',quality=95)
print('Saved',len(records),'sheets; all protected pixels unchanged.')
