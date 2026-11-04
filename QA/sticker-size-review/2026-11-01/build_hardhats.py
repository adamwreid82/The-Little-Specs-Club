from pathlib import Path
from lxml import etree as E
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,re,subprocess,copy,concurrent.futures
W=Path(__file__).resolve().parent;SRC=W.parent/'hardhat_r7_2026_11_01/deliverables/Editable_Sources_and_Placement_Records';OUT=W/'deliverables';SVG=OUT/'Editable_Sources_and_Placement_Records';PNG=OUT/'Hardhat_R8_PNGs';TMP=W/'hardhat_pages'
for p in [SVG,PNG,TMP]:p.mkdir(parents=True,exist_ok=True)
ACTUAL=json.loads((W/'actual_sticker_bounds.json').read_text())
S='{http://www.w3.org/2000/svg}';CAL=json.loads((W/'controls/calibration.json').read_text())
ORDER=['Ben','Leo','Vinny','Steph','Maya','Mrs_Harper','Elena_Rivera','Marcus_Jackson','Priya_Patel','Daniel_Brooks','Tony_Marino','Claire_Morgan','Omar_Haddad','Darius_Cole','Matthias_Becker','Luis_Mendoza','Andre_Lewis','Danny_Novak','Erik_Halvorsen','Sam_Carter','Hannah_Kowalski','Rebecca_Foster','Natalie_Chen','Rafael_Martinez','Marisol_Vega','Adrian_Park']
def bbox(g):
 pts=[tuple(map(float,x.split(','))) for p in g.findall('.//'+S+'polygon') for x in p.get('points').split()];xs=[p[0] for p in pts];ys=[p[1] for p in pts];return min(xs),min(ys),max(xs),max(ys)
def geometry(root):
 r=copy.deepcopy(root)
 for t in r.findall('.//'+S+'text'):t.getparent().remove(t)
 return E.tostring(r,method='c14n')
def build(key):
 src=SRC/f'{key}_Hardhat_Source_R7.svg';root=E.fromstring(src.read_bytes());before=geometry(root);groups=[g for g in root.findall('.//'+S+'g') if (g.get('id') or '').startswith('fire_station_')];changes=[]
 if groups:
  side=next(g for g in groups if 'wearer_' in g.get('id'));b=bbox(side);view=side.get('id').replace('fire_station_','');cal=next(c for c in CAL[key]['views'] if c['view']==view);target=.19*cal['bbox'][2];ab=ACTUAL[key][view];scale=target/(ab[3]-ab[1])
  for g in groups:
   x1,y1,x2,y2=bbox(g);cx=(x1+x2)/2;cy=(y1+y2)/2
   n=E.Element(S+'g',id='r8_size_'+g.get('id'),transform=f'translate({cx:.8f},{cy:.8f}) scale({scale:.10f}) translate({-cx:.8f},{-cy:.8f})')
   for child in list(g):g.remove(child);n.append(child)
   g.append(n);changes.append({'view':g.get('id'),'scale':scale,'local_center':[cx,cy],'old_clip_bbox':[x1,y1,x2,y2],'new_clip_bbox':[cx+(x1-cx)*scale,cy+(y1-cy)*scale,cx+(x2-cx)*scale,cy+(y2-cy)*scale],'existing_view_transform':g.get('transform')})
  reference={'original_visible_profile_bounds':ab,'profile_width':cal['bbox'][2],'target_profile_sticker_height':target,'scale':scale}
 else:reference={'exception':'Rebecca Foster has no project stickers'}
 for t,label in zip(root.findall('.//'+S+'text'),['R8 REVIEW | Jobsite sticker size: approved Ben / Leo eight-view reference | Pending approval','Front / back / left / right views | Left and right refer to the wearer']):
  for child in list(t):t.remove(child)
  t.text=label
 test=copy.deepcopy(root)
 for g in list(test.findall('.//'+S+'g')):
  if (g.get('id') or '').startswith('r8_size_'):
   parent=g.getparent();idx=parent.index(g)
   for child in list(g):g.remove(child);parent.insert(idx,child);idx+=1
   parent.remove(g)
 assert geometry(test)==before,'Non-sticker artwork changed: '+key
 dest=SVG/f'{key}_Hardhat_Source_R8.svg';dest.write_bytes(E.tostring(root,xml_declaration=True,encoding='UTF-8'))
 png=PNG/f'{key}_Hardhat_Source_R8.png';pdf=TMP/f'{key}.pdf'
 for fmt,path in [('png',png),('pdf',pdf)]:
  r=subprocess.run(['inkscape',str(dest),'--export-area-page','--export-type='+fmt,'--export-filename='+str(path)],capture_output=True,text=True,timeout=90);assert r.returncode==0,r.stderr
 rec={'character':key,'revision':'R8','status':'PENDING_AUTHOR_REVIEW','source_revision':'R7_APPROVED','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'svg_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'png_sha256':hashlib.sha256(png.read_bytes()).hexdigest(),'reference':reference,'changes':changes,'all_original_svg_nodes_and_transforms_preserved':True,'new_scaling_wrappers_only':True}
 (SVG/f'{key}_Placement_Record_R8.json').write_text(json.dumps(rec,indent=2));return rec
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(build,ORDER))
(OUT/'Hardhat_Source_Register_R8.json').write_text(json.dumps({'revision':'R8','status':'PENDING_AUTHOR_REVIEW','reference_ratio':.19,'reference':'Ben approved eight-view PPE R10 and Leo approved eight-view PPE R8. Not R7 helmet-only approval.','characters':records},indent=2))
for off in range(0,len(ORDER),6):
 o=Image.new('RGB',(1500,1120),'#e6e9ef');d=ImageDraw.Draw(o)
 for j,key in enumerate(ORDER[off:off+6]):
  im=Image.open(PNG/f'{key}_Hardhat_Source_R8.png').convert('RGB');im.thumbnail((490,510));x=j%3*500+(500-im.width)//2;y=j//3*560+30;o.paste(im,(x,y));d.text((j%3*500+5,j//3*560+5),key,fill='black')
 o.save(W/f'hardhat_contact_{off//6+1}.jpg',quality=95)
print('26 hardhat R8 sheets exported; all old SVG geometry retained under size wrappers.')
