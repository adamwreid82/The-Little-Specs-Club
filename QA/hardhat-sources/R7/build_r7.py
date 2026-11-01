from pathlib import Path
import concurrent.futures,copy,hashlib,json,re,subprocess
from lxml import etree as ET
from PIL import Image,ImageDraw,ImageFont
import fitz
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

ROOT=Path(__file__).resolve().parents[1];W=Path(__file__).resolve().parent
SOURCE=ROOT/'r5_source_review_2026_11_01'
OUT=W/'deliverables';SVG=OUT/'Editable_Sources_and_Placement_Records';PNG=OUT/'Individual_PNGs';TMP=W/'rendered_pages'
for p in [OUT,SVG,PNG,TMP,OUT/'Original_SVG_Snapshot']:p.mkdir(parents=True,exist_ok=True)
S='{http://www.w3.org/2000/svg}'
ORDER=['Ben','Leo','Vinny','Steph','Maya','Mrs_Harper','Elena_Rivera','Marcus_Jackson','Priya_Patel','Daniel_Brooks','Tony_Marino','Claire_Morgan','Omar_Haddad','Darius_Cole','Matthias_Becker','Luis_Mendoza','Andre_Lewis','Danny_Novak','Erik_Halvorsen','Sam_Carter','Hannah_Kowalski','Rebecca_Foster','Natalie_Chen','Rafael_Martinez','Marisol_Vega','Adrian_Park']
inventory=json.loads((W/'input_inventory.json').read_text());meta={x['name']:x for x in inventory if x['mime_type']=='image/svg+xml'}
assert len(meta)==len(ORDER)==26
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def geometry_tree(root):
 r=copy.deepcopy(root)
 for t in r.findall('.//'+S+'text'):t.getparent().remove(t)
 return ET.tostring(r,method='c14n')
def parse_svg(fn):
 r=ET.fromstring(fn.read_bytes());assert r.tag==S+'svg'
 ids={x.get('id') for x in r.iter() if x.get('id')};refs=[]
 for n in r.iter():
  for k,v in n.attrib.items():
   if k.endswith('href'):
    assert v.startswith(('data:','#')),f'External asset in {fn.name}'
    if v.startswith('#'):refs.append(v[1:])
   refs+=re.findall(r'url\(#([^\)]+)\)',v)
 assert set(refs)<=ids,f'Missing SVG references {set(refs)-ids}'
 return r
def build_one(key):
 name=key+'_Hardhat_Source_R5.svg';m=meta[name];src=SOURCE/name
 assert src.stat().st_size==m['size']
 root=parse_svg(src);before=geometry_tree(root)
 texts=root.findall('.//'+S+'text');assert len(texts)==2
 labels=['R7 REVIEW | Current edited SVG placement | Pending author approval','Front / back / left / right views | Left and right refer to the wearer']
 for node,label in zip(texts,labels):
  for child in list(node):node.remove(child)
  node.text=label
 assert geometry_tree(root)==before,'Artwork geometry changed'
 dest=SVG/(key+'_Hardhat_Source_R7.svg');dest.write_bytes(ET.tostring(root,xml_declaration=True,encoding='UTF-8'))
 snap=OUT/'Original_SVG_Snapshot'/name;snap.write_bytes(src.read_bytes())
 png=PNG/(key+'_Hardhat_Source_R7.png');pdf=TMP/(key+'.pdf')
 for fmt,path in [('png',png),('pdf',pdf)]:
  args=['inkscape',str(dest),'--export-area-page','--export-type='+fmt,'--export-filename='+str(path)]
  result=subprocess.run(args,capture_output=True,text=True,timeout=60)
  assert result.returncode==0 and path.exists(),result.stderr
 im=Image.open(png);im.verify();im=Image.open(png)
 record={'character':key.replace('_',' '),'revision':'R7','approval':'PENDING_AUTHOR_REVIEW','source':m,'source_sha256':sha(src),'derived_svg':{'filename':dest.name,'sha256':sha(dest),'bytes':dest.stat().st_size},'png':{'filename':png.name,'sha256':sha(png),'bytes':png.stat().st_size,'dimensions':list(im.size)},'canvas':{k:root.get(k) for k in ['width','height','viewBox']},'artwork_geometry_unchanged':True,'changes':'Only two review/footer text elements updated; all helmet, logo, sticker, shell and image data retained.','placement_record_type':'authored SVG element snapshot, not new 3D coordinates','elements':[]}
 for e in root.iter():
  if e.tag not in [S+'g',S+'use',S+'image',S+'clipPath']:continue
  attrs={k:v for k,v in e.attrib.items() if not k.endswith('href')}
  for k,v in e.attrib.items():
   if k.endswith('href'):attrs['embedded_asset_sha256' if v.startswith('data:') else 'reference']=hashlib.sha256(v.encode()).hexdigest() if v.startswith('data:') else v
  record['elements'].append({'tag':e.tag.split('}')[-1],'attributes':attrs,'ancestor_transforms':[{'id':a.get('id'),'transform':a.get('transform')} for a in reversed(list(e.iterancestors())) if a.get('transform')]})
 (SVG/(key+'_Placement_Record_R7.json')).write_text(json.dumps(record,indent=2))
 return record
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 records=list(pool.map(build_one,ORDER))

# Cover is separate from the unscaled SVG page exports.
cover=TMP/'cover.pdf';c=canvas.Canvas(str(cover),pagesize=(864,576))
c.setTitle('Hardhat Sources R7 - All Characters - Review')
c.setFillColor(HexColor('#113F93'));c.setFont('Helvetica-Bold',30);c.drawString(42,522,'HARDHAT SOURCES R7')
c.setFillColor(HexColor('#222222'));c.setFont('Helvetica',15);c.drawString(42,492,'All 26 characters | Edited SVG review | November 1, 2026')
c.setStrokeColor(HexColor('#F6BA32'));c.setLineWidth(3);c.line(42,477,822,477)
c.setFont('Helvetica',11)
for y,line in [(451,'Direct exports from the current SVGs in the R5 Editable Sources and Placement Records folder.'),(434,'Helmet shapes, logos and sticker placements are preserved. Only review/footer labels say R7.'),(417,'Review each character before approval. Earlier R5 and R6 files remain preserved.')]:c.drawString(42,y,line)
c.setFont('Helvetica-Bold',12);c.drawString(42,381,'CHARACTER');c.drawRightString(393,381,'PAGE');c.drawString(459,381,'CHARACTER');c.drawRightString(810,381,'PAGE')
for i,r in enumerate(records):
 col=i//13;row=i%13;x=42+417*col;y=358-row*21
 c.setFillColor(HexColor('#1F2937'));c.setFont('Helvetica',12);c.drawString(x,y,r['character']);c.drawRightString(x+351,y,str(i+2))
c.setFillColor(HexColor('#113F93'));c.setFont('Helvetica-Bold',12);c.drawString(42,54,'PENDING AUTHOR APPROVAL')
c.setFillColor(HexColor('#555555'));c.setFont('Helvetica',9);c.drawString(42,36,'This package shows the edited SVGs. It does not certify the existing illustrated shells as measured 3D models.')
c.showPage();c.save()
pdf=OUT/'Hardhat_Source_Review_R7_All_Characters.pdf';doc=fitz.open();doc.insert_pdf(fitz.open(cover));toc=[[1,'R7 review index',1]]
for i,key in enumerate(ORDER):
 child=fitz.open(TMP/(key+'.pdf'));assert len(child)==1
 doc.insert_pdf(child);toc.append([1,key.replace('_',' '),i+2])
doc.set_toc(toc);doc.set_metadata({'title':'Hardhat Sources R7 - All Characters - Review','author':'The Little Specs Club','subject':'Current edited SVGs, pending author approval'})
doc.save(pdf,garbage=4,deflate=True);doc.close()

manifest={'revision':'R7','created_on':'2026-11-01','status':'PENDING_AUTHOR_REVIEW','source_folder_id':'1a_M9FhDZNTlgbJxcUw2CRvp7Sai41_ov','source_parent_folder_id':'1K_eAuaSVVqKkBeb8fSBUQ80pmPpmD2mL','source_folder':'Hardhat Sources R5 - Logo and Placement Corrections - REVIEW 2026-10-21/Editable Sources and Placement Records','existing_r6_folder_id':'1qUS-LlAMDgpSOXA_IkA9GITKlPD-MjiW','scope':'Export all current source SVGs as a new R7 review set; preserve author edits exactly outside the two review/footer text elements.','source_count':len(records),'pdf':{'filename':pdf.name,'sha256':sha(pdf),'bytes':pdf.stat().st_size,'pages':27},'characters':records,'limitations':['Author approval pending.','No new measured 3D model or physical cross-view validation.','Old R5 JSON coordinates were not used to reposition any SVG content.','R7 placement records store actual authored SVG transforms, including independent per-view edits.','Existing character-sheet approvals and artwork are unchanged.']}
(OUT/'Hardhat_Source_Register_R7.json').write_text(json.dumps(manifest,indent=2))
(OUT/'README_R7.txt').write_text('THE LITTLE SPECS CLUB - HARDHAT SOURCES R7\nNovember 1, 2026. PENDING AUTHOR APPROVAL.\n\nOpen Hardhat_Source_Review_R7_All_Characters.pdf for the 27-page review: one index page and 26 character sheets. Individual PNG exports are in Individual_PNGs. Editable R7 SVG copies and per-character placement snapshots are in Editable_Sources_and_Placement_Records. Original_SVG_Snapshot preserves the exact input bytes.\n\nSOURCE: Hardhat Sources R5 - Logo and Placement Corrections - REVIEW 2026-10-21 / Editable Sources and Placement Records. All 26 SVGs were included. The existing 3D R6 set was inspected only to avoid revision conflict; it was not used to replace the selected artwork.\n\nOnly the two review/footer text elements were updated for R7. Helmet shapes, colors, front logos, job stickers, embedded images, clipping paths and transforms were preserved. No AI image generation, retouching, logo placement correction or 3D fitting was applied.\n\nThe old R5 JSON placement records were not used to rebuild the artwork because they do not incorporate all current SVG edits. The R7 records snapshot actual SVG elements, nested transforms and asset references. They are not a mathematical reconstruction of a single 3D helmet.\n\nAll 26 SVGs parsed with internal references resolved, and exported to PNG/PDF. Geometry outside text labels was verified unchanged. Visual export review is separate from canon or author approval. Earlier R5/R6 files, approved character sheets and their approval records remain untouched.\n')

# Review every final PDF page through a raster image, in groups of six.
pdfdoc=fitz.open(pdf);previews=[]
for i,page in enumerate(pdfdoc):
 pix=page.get_pixmap(matrix=fitz.Matrix(1.1,1.1),alpha=False);p=TMP/f'final_page_{i+1:02d}.png';pix.save(p);previews.append(p)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
for start in range(0,len(previews),6):
 contact=Image.new('RGB',(1500,1120),'#e6e9ef');draw=ImageDraw.Draw(contact)
 for j,p in enumerate(previews[start:start+6]):
  im=Image.open(p).convert('RGB');im.thumbnail((490,510));x=(j%3)*500+(500-im.width)//2;y=(j//3)*560+30
  contact.paste(im,(x,y));draw.text(((j%3)*500+14,(j//3)*560+6),f'PDF page {start+j+1}',font=font,fill='#113f93')
 contact.save(TMP/f'contact_{start//6+1}.jpg',quality=92)
print(json.dumps({'characters':len(records),'pages':len(pdfdoc),'pdf_bytes':pdf.stat().st_size,'geometry_preserved':all(x['artwork_geometry_unchanged'] for x in records),'pdf':str(pdf)},indent=2))
