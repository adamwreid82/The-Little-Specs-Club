from pathlib import Path
import json,hashlib,copy,zipfile
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.utils import ImageReader
P=Path(__file__).resolve().parent; O=P/'deliverables';O.mkdir(exist_ok=True)
audit=json.loads((P.parent/'spread_review_2026_11_04/deliverables/Book1_People_Source_Review_2026-11-05.json').read_text())
qa=json.loads((P/'records/pixel_qa.json').read_text());patches=json.loads((P/'records/patches.json').read_text());overlays=json.loads((P/'records/overlays.json').read_text());drive={r['pages']:r for r in json.loads((P/'records/drive_candidates.json').read_text())}
changes={'08-09':'Rivera: added clear safety glasses.','12-13':'Rivera: added clear safety glasses.','14-15':'Natalie: exact Eastmark logo. Ben: dark shoe soles and tread.','16-17':'Steph: restored approved project-sticker scale and contour.','18-19':'Maya and Ben: restored sticker scale. Steph: removed extra earring.','20-21':'Rivera: clear safety glasses. Natalie: exact Eastmark logo.','22-23':'Leo: LS logo fully on the front shell; project sticker above the band.','24-25':'Jackson and Leo: restored sticker scale and spacing above the band.','26-27':'Rivera: added clear safety glasses.','28-29':'Brooks and Maya: restored sticker scale and shell placement.','30-31':'Steph, Ben and Leo: LS logos above the brim. Ben: corrected project sticker.'}
limits=['Hidden details and back-of-vest emblems remain UNVERIFIED because these scenes do not expose them.','Exact physical height is not measurable from scene perspective. The distant excavator operator on pages 24-25 remains unidentified.','Visual inspection and pixel preservation are not print proofing or a new author approval.']
manifest={'title':'Book 1 People Repairs','date':'2026-11-07','authorization':'Adam: fix these issues','scope':'20 findings in 11 active restarted spreads, actual page numbering 02-33.','status':'VERSION B - REVIEW REQUIRED','author_approval':None,'reference_approval_record_id':audit['reference_approval_record_id'],'current_reference_manifest_id':audit['current_reference_manifest_id'],'prior_audit_drive_id':'1hbjOKiUZby4VNmcl0ol81rSVRJaZC5vW','review_folder_id':'1xNu6j2qw5B0x70De9EuZg7BZKbt_IRHU','git_branch':'review/book1-people-repairs-2026-11-07','original_art_and_approvals_preserved':True,'limitations':limits,'source_registry_exceptions':audit['source_registry_exceptions'],'method':'Local imagegen restoration patches and direct projection of exact approved embedded logo/sticker PNG assets. No full-spread regeneration. All pixels outside documented repairs unchanged.','repaired_spreads':[],'unchanged_spreads':[],'native_graphics':[]}
for r in qa:
 old=next(s for s in audit['spreads'] if s['pages']==r['pages']);r=copy.deepcopy(r)
 assert r['source_sha256']==old['sha256']
 r.update(drive_id=drive[r['pages']]['id'],drive_url=drive[r['pages']]['url'],review_folder_id=drive[r['pages']]['parent_id'],status='VERSION B - REVIEW REQUIRED',author_approval=None,original_drive_id=old['id'],original_approval_state=old['prior_status'],changes=changes[r['pages']],visual_check='Identified repairs visually inspected against current approved eight-view and R8 sources; no additional visible mismatch identified in repair regions.',unverified=limits,source_bindings=copy.deepcopy(old['people']),findings=copy.deepcopy(old['findings']))
 r['pixel_sha256']=hashlib.sha256(Image.open(P/'candidates'/r['filename']).convert('RGB').tobytes()).hexdigest()
 for f in r['findings']:f['status']='CORRECTED_IN_REVIEW_CANDIDATE';f['repair_summary']=changes[r['pages']]
 for person in r['source_bindings']:
  person['previous_review_result']=person.pop('result');person['current_result']='VISIBLE_REPAIR_CHECK_COMPLETE' if person['finding_ids'] else 'UNCHANGED_FROM_PRIOR_VISUAL_REVIEW'
 r['repair_patches']=[x for x in patches if x['id']==r['pages']];r['graphic_placements']=[x for x in overlays if x['id']==r['pages']]
 manifest['repaired_spreads'].append(r)
for s in audit['spreads']:
 if s['pages'] not in changes:manifest['unchanged_spreads'].append({k:s[k] for k in ['pages','id','filename','sha256','review_status','prior_status']})
for name,svg,id,element in [('Eastmark_logo.png','Natalie_Chen_Hardhat_Source_R8.svg','1Jhvezhl4tFPlf0ytvCjtklKoiJy4rHgX','image2'),('LS_logo.png','Ben_Hardhat_Source_R8.svg','1QJdI271yiyhGr8OvCp8ojNzm_w4cmaKa','image2'),('Fire_Station_Sticker.png','Ben_Hardhat_Source_R8.svg','1QJdI271yiyhGr8OvCp8ojNzm_w4cmaKa','fire_asset')]:manifest['native_graphics'].append(dict(filename=name,sha256=hashlib.sha256((P/'inputs'/name).read_bytes()).hexdigest(),svg_source=svg,svg_drive_id=id,svg_sha256=hashlib.sha256((P/'inputs'/svg).read_bytes()).hexdigest(),embedded_element=element))
assert len(manifest['repaired_spreads'])==11 and sum(len(s['findings']) for s in manifest['repaired_spreads'])==20
(O/'Book1_People_Repairs_Manifest_2026-11-07.json').write_text(json.dumps(manifest,indent=2))
# Screen review PDF with full spreads and before/after details.
W,H=864,648; c=canvas.Canvas(str(O/'Book1_People_Repairs_REVIEW_2026-11-07.pdf'),pagesize=(W,H));c.setTitle('Book 1 People Repairs - Review 2026-11-07');c.setAuthor('The Little Specs Club')
NAVY=colors.HexColor('#173752');BLUE=colors.HexColor('#1261A0');LIGHT=colors.HexColor('#EAF2F7')
style=ParagraphStyle('body',fontName='Helvetica',fontSize=11,leading=15,textColor=NAVY)
page=0
def para(text,x,y,w,fontsize=11):
 s=ParagraphStyle('x',parent=style,fontSize=fontsize,leading=fontsize*1.35);p=Paragraph(text,s);_,h=p.wrap(w,H);p.drawOn(c,x,y-h);return y-h

def base(title,sub):
 global page
 page+=1;c.setFillColor(colors.white);c.rect(0,0,W,H,fill=1,stroke=0)
 c.setFillColor(NAVY);c.setFont('Helvetica-Bold',21);c.drawString(32,H-39,title)
 c.setFont('Helvetica',10);c.drawString(32,H-59,sub)
 c.setStrokeColor(colors.HexColor('#D6E2EA'));c.line(32,37,W-32,37)
 c.setFont('Helvetica',9);c.setFillColor(NAVY);c.drawString(32,22,'The Little Specs Club | Review candidate | 7 November 2026');c.drawRightString(W-32,22,str(page))

def photo(path,x,y,w,h):
 im=ImageReader(str(path));iw,ih=im.getSize();s=min(w/iw,h/ih);dw,dh=iw*s,ih*s;c.drawImage(im,x+(w-dw)/2,y+(h-dh)/2,width=dw,height=dh)
base('Book 1 people repairs','11 revised spreads | 20 findings addressed | Awaiting Adam\'s approval')
y=para('The approved character sources remain the authority. This set corrects the findings from the 5 November review and retains the original text, composition and all artwork outside the repair areas.',32,560,800,12)
rows=[['Pages','Revision','Corrections']]+[[r['pages'],str(r['revision']),Paragraph(changes[r['pages']],ParagraphStyle('table',parent=style,fontSize=10,leading=13))] for r in qa]
t=Table(rows,colWidths=[65,60,675]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(-1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),10),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('ROWBACKGROUNDS',(0,1),(-1,-1),[LIGHT,colors.white])]))
_,th=t.wrap(800,500);t.drawOn(c,32,y-18-th);y-=th+35
para('All 11 files retain 5100 x 2550 pixels. Pixel comparisons found zero changes outside the documented repairs. Hidden rear vest logos and unmeasurable features remain UNVERIFIED. Earlier files and approvals are preserved.',32,y,800,10)
c.linkURL('https://drive.google.com/drive/folders/1xNu6j2qw5B0x70De9EuZg7BZKbt_IRHU',(32,50,450,73));c.setFillColor(BLUE);c.setFont('Helvetica-Bold',11);c.drawString(32,57,'Open the full-resolution review folder');c.showPage()
labels={'Rivera':'Rivera safety glasses','Natalie':'Natalie helmet logo','Shoes':'Ben shoe soles','StephSticker':'Steph project sticker','MayaBenStickers':'Maya and Ben project stickers','StephEar':'Steph earring','Leo':'Leo helmet graphics','JacksonLeo':'Jackson and Leo project stickers','MayaBrooks':'Maya and Brooks project stickers','ThreeLogos':'Steph, Ben and Leo helmet graphics'}
for r in qa:
 id=r['pages'];base(f'Pages {id} - Revision {r["revision"]}',changes[id])
 photo(P/'candidates'/f'{id}_preview.jpg',32,148,800,400)
 para('Status: VERSION B - REVIEW REQUIRED. The existing text and all pixels outside the listed repair areas are unchanged.',32,125,800,11)
 c.setFillColor(BLUE);c.setFont('Helvetica-Bold',11);c.drawString(32,72,'Open full-resolution PNG');c.linkURL(drive[id]['url'],(32,67,240,84))
 c.setFont('Helvetica',9);c.setFillColor(NAVY);c.drawRightString(W-32,72,f'{r["changed_percent"]:.3f}% of pixels changed within repair regions');c.showPage()
 for q in [p for p in patches if p['id']==id]:
  key=q.get('key','Rivera');stem=id+'_'+key;base(f'Pages {id} - {labels[key]}','Before and after | The right image is the new review candidate')
  c.setFont('Helvetica-Bold',12);c.setFillColor(NAVY);c.drawString(32,550,'BEFORE');c.drawString(448,550,'AFTER')
  photo(P/'qa'/f'{stem}_before.jpg',32,105,384,425);photo(P/'qa'/f'{stem}_after.jpg',448,105,384,425)
  para(changes[id],32,88,800,11);c.showPage()
c.save();print('Created PDF:',page,'pages')
# Retain compact, mechanically compositable repair layers.
rebuild='''import json,hashlib,subprocess,sys\nfrom pathlib import Path\nfrom PIL import Image\np=Path(__file__).resolve().parent;src=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(exist_ok=True)\nm=json.loads((p/'manifest.json').read_text())\nfor r in m['repaired_spreads']:\n original=src/r['source_filename'];assert hashlib.sha256(original.read_bytes()).hexdigest()==r['source_sha256']\n target=out/r['filename'];target.write_bytes(original.read_bytes())\n for q in r['repair_patches']:\n  x,y,w,h=q['crop'];key=q['id']+'_'+q.get('key','Rivera')\n  subprocess.run(['magick',str(target),str(p/'layers'/f'{key}_patch.png'),'-geometry',f'+{x}+{y}','-compose','Over','-composite',str(target)],check=True)\n for q in r['graphic_placements']:\n  x,y,w,h=q['layer_box']\n  subprocess.run(['magick',str(target),str(p/'layers'/f'{q["id"]}_{q["key"]}_logo.png'),'-geometry',f'+{x}+{y}','-compose','Over','-composite',str(target)],check=True)\n assert hashlib.sha256(Image.open(target).convert('RGB').tobytes()).hexdigest()==r['pixel_sha256']\n print(r['pages']+': exact RGB pixels reproduced')\n'''
with zipfile.ZipFile(O/'Book1_People_Repair_Layers_2026-11-07.zip','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('manifest.json',json.dumps(manifest,indent=2));z.writestr('rebuild.py',rebuild);z.writestr('README.txt','Review-only repairs. Original approved sources remain unchanged.\nDownload the exact original spread files identified in manifest.json to a folder.\nRequires ImageMagick, Python and Pillow.\nRun: python rebuild.py ORIGINAL_FOLDER OUTPUT_FOLDER\nEach output is verified against its recorded decoded RGB hash. PNG container bytes may vary by encoder metadata.\n')
 for r in patches:
  name=r['id']+'_'+r.get('key','Rivera')+'_patch.png';z.write(P/'generated'/name,'layers/'+name)
 for r in overlays:
  name=r['id']+'_'+r['key']+'_logo.png';z.write(P/'generated'/name,'layers/'+name)
 for r in manifest['native_graphics']:z.write(P/'inputs'/r['filename'],'source_assets/'+r['filename'])
print('Manifest and repair layers saved')
