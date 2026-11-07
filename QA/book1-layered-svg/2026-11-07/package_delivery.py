from pathlib import Path
import base64,hashlib,html,io,json,zipfile
from PIL import Image
from lxml import etree as E,html as H

P=Path(__file__).resolve().parent;OUT=P/'deliverables'
records=json.loads((P/'build_records.json').read_text())
uploads={e['pages']:e for e in json.loads((P/'drive_uploads.json').read_text())}
assert len(records)==len(uploads)==16
verified=json.loads((P/'qa/drive_bytes_verification.json').read_text())
assert len(verified)==16 and all(e['saved_bytes_match'] for e in verified)
pixels=json.loads((P/'qa/pixel_check.json').read_text())
def fileurl(id):return f'https://drive.google.com/file/d/{id}/view'
def folderurl(id):return f'https://drive.google.com/drive/folders/{id}'
manifest={'project':'The Little Specs Club','book':1,'date':'2026-11-07','scope':'All 16 active restarted spreads, actual pages 02-33, including initial-approval spreads. Earlier revisions, cover and reserved pages 1/34 are not replaced.','status':'NEW SVG COMPANIONS REQUIRE AUTHOR REVIEW; ORIGINAL PNG APPROVALS UNCHANGED','fully_vector':False,'editability':{'live_text_lines':177,'retained_raster_repair_layers':14,'separate_raster_logo_sticker_objects':15,'other_artwork':'Embedded raster, including characters, clothing, scenery, title logo and branding not listed as separate objects. Individual vector paths are unavailable.','text_background':'SVG morphology reconstruction under original printed lettering, applied only through glyph masks. Keep recovery layer visible.','line_wrapping':'Independent live text lines; reflow manually when changing copy.'},'dimensions':{'viewBox':'0 0 5100 2550','physical_inches':[17,8.5]},'source_references':{'people_repairs_manifest':fileurl('17QpWtZ-D_3EoYL4tfC2WaxeqixmVEIzN'),'approved_8_view_folder':folderurl('1XGYEslC91ODbIkgWwS5gfjxASoZB17Z_'),'R8_editable_source_folder':folderurl('1v2EfX2WO-6zKStJnY8Z2fJuMHoxRdWxN')},'validation':{'all_16_svg_xml_valid':True,'all_images_embedded':True,'all_16_rendered_at':[5100,2550],'all_16_visually_reviewed':True,'text_hidden_checks':['06-07','12-13','32-33'],'illustration_comparison':pixels,'drive_byte_verification':verified},'spreads':[]}
for e in records:
 u=uploads[e['pages']];r=u['result']['structuredContent'];assert hashlib.sha256(Path(e['svg_path']).read_bytes()).hexdigest()==e['svg_sha256']
 manifest['spreads'].append({'pages':e['pages'],'source_revision':e['revision'],'source_png':e['filename'],'source_png_id':e['id'],'source_png_sha256':e['sha256'],'source_png_status':e['status'],'svg_filename':e['svg_filename'],'svg_id':r['id'],'svg_url':fileurl(r['id']),'svg_sha256':e['svg_sha256'],'svg_bytes':e['svg_bytes'],'svg_status':'REVIEW_REQUIRED','folder_id':u['folder_id'],'folder_url':folderurl(u['folder_id']),'live_text_lines':e['text_lines'],'repair_layers':e['repair_layers'],'separate_branding_objects':e['separate_branding_objects'],'text_layout':e['text_groups']})
mf=OUT/'Book1_Layered_SVG_Manifest_2026-11-07.json';mf.write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
guide='''THE LITTLE SPECS CLUB | BOOK 1 | SVG EDITING GUIDE
7 November 2026

16 current spreads: actual pages 02-33. Initial-approval spreads are included.

EDITABILITY LIMIT
These are layered layout SVGs, not fully vector illustrations. All 177 lines
of title, story and facts copy are live editable SVG text. The 14 existing
repair patches and 15 corrected logo/sticker placements remain separate
raster objects. Characters, clothing, backgrounds, the title logo, and other
branding remain embedded raster artwork. Converting the remaining painted
art into editable vector shapes would require a separate redraw.

The original PNGs and their approval records are unchanged. These new SVG
companions require author review. The REV number identifies the source PNG;
it does not indicate that an SVG has inherited approval. No source character
files were changed.

HOW TO EDIT
Open the SVG in Inkscape or another editor that supports SVG text, embedded
images and filters. The files contain all image assets; no image relinking
is needed. Roboto is embedded for compatible renderers and included in the
download bundle for desktop editors that need the font installed locally.

Layer 01: Original illustration as an embedded raster image.
Layer 02: Retained character and helmet cleanup patches, where available.
Layer 03: Separate corrected logo/sticker objects, where available.
Layer 04: Text background recovery. KEEP VISIBLE when editing or hiding text.
Layer 05: EDITABLE TEXT. Use the text tool to change individual lines. Longer
          wording requires manual line wrapping and positioning.
Layer 90: Hidden page/gutter guides. Keep hidden when exporting.

To reposition one of the 15 separate branding objects, select its named
sublayer in Layer 03. Other printed logos are still part of the illustration.
Changing a character or moving an entire person requires raster retouching
or new source artwork; the SVG does not expose individual face/clothing paths.

TEXT BACKGROUND RECOVERY
The supplied spreads had flattened lettering. Native SVG filters recover
the background beneath those letters through small glyph masks. The visible
copy is now separate live text. Do not hide Layer 04, because doing so exposes
the old flattened lettering. Minor background reconstruction is confined to
the original text area. Desktop apps may render SVG filters differently;
inspect an export after editing. Inkscape renders were checked at 5100x2550.

REVIEW AND VALIDATION
All 16 SVGs were parsed, rendered and visually reviewed. The three original
initial-approval illustrations (02-03, 04-05, 06-07) are pixel-identical outside
the text areas. Other spread art matches the current PNGs, allowing at most
2/255 channel levels of renderer rounding at composited patch edges. Exact
saved Drive bytes were checked against local SHA-256 hashes for all 16 SVGs.
Text was hidden for sky, canopy and dense facts-page checks with no duplicate
lettering left visible. Font and text antialiasing can differ from the PNG.

SOURCE SIZES
SVG canvas: 17 x 8.5 inches; viewBox 5100 x 2550.
This is an editable review companion, not a final press-ready PDF.

FONT
Roboto: Copyright 2011 The Roboto Project Authors
(https://github.com/googlefonts/roboto-classic).
Licensed under the SIL Open Font License, Version 1.1:
https://openfontlicense.org
The original font license and copyright metadata remain embedded in the font.

SPREAD INVENTORY
Pages | Source REV | Live text lines | Repair patches | Separate branding
'''
for e in records:guide+=f"{e['pages']} | {e['revision']} | {e['text_lines']} | {e['repair_layers']} | {e['separate_branding_objects']}\n"
gf=OUT/'Book1_SVG_Editing_Guide_2026-11-07.txt';gf.write_text(guide)

# Add companion links to current rows only. Historical review remains intact.
doc=H.fromstring((P/'previous_review_index.html').read_text())
rows=doc.xpath('//table')[0].xpath('.//tbody/tr')
assert len(rows)==16
for row,e in zip(rows,manifest['spreads']):
 assert row.xpath('./td')[0].text_content()==e['pages'];td=row.xpath('./td')[-1]
 E.SubElement(td,'br');a=E.SubElement(td,'a',href=e['svg_url']);a.text='Layered SVG (review)'
 E.SubElement(td,'br');a=E.SubElement(td,'a',href=e['folder_url']);a.text='Page folder'
notice=H.fromstring('''<section class="notice" id="svg-companions"><h2>Editable SVG companions: 7 November 2026</h2><p><strong>All 16 current spreads now have a layered SVG in their page folder, including initial-approval spreads.</strong> The SVGs contain 177 editable text lines, 14 retained repair layers and 15 separate corrected logo/sticker objects.</p><p>These are <strong>not fully vector illustrations</strong>: characters, clothing, scenery and other branding remain raster. The new SVGs require review; the original PNGs and their approval records remain unchanged. Every saved SVG was checked against its local SHA-256 hash.</p></section>''')
body=doc.find('body');body.insert(1,notice)
index=OUT/'Book1_Review_Index.html';index.write_text('<!doctype html>\n'+H.tostring(doc,encoding='unicode'))

# Standalone visual index; uses small embedded review thumbnails.
cards=[]
for e in manifest['spreads']:
 im=Image.open(P/'renders'/f"{e['pages']}.png").convert('RGB');im.thumbnail((1020,510));b=io.BytesIO();im.save(b,'JPEG',quality=87)
 cards.append(f'''<article><h2>Pages {e['pages']} <small>Source REV{e['source_revision']}</small></h2><a href="{e['svg_url']}"><img alt="Pages {e['pages']} SVG render" src="data:image/jpeg;base64,{base64.b64encode(b.getvalue()).decode()}"></a><p><a href="{e['svg_url']}">Open SVG</a> · <a href="{e['folder_url']}">Page folder</a> · <a href="{fileurl(e['source_png_id'])}">Source PNG</a></p><p>{e['live_text_lines']} editable text lines · {e['repair_layers']} repair patches · {e['separate_branding_objects']} separate branding objects</p></article>''')
gallery=OUT/'Book1_SVG_Visual_Index_2026-11-07.html';gallery.write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Book 1 SVG companions</title><style>body{font:16px system-ui;margin:32px auto;max-width:1280px;padding:16px;background:#fffaf0;color:#173752;line-height:1.5}h1{font-size:32px}h2{font-size:20px}small{font-size:14px;font-weight:400}article{background:white;padding:18px;border:1px solid #d3d9dc;border-radius:8px;margin:20px 0}img{width:100%;height:auto}a{color:#1768aa}aside{background:#fff2cf;border-left:4px solid #e5a833;padding:15px}</style><h1>Book 1 · Editable SVG companions</h1><p>All 16 current spreads, including initial-approval spreads. 7 November 2026.</p><aside><strong>Layered layouts, not fully vector artwork.</strong> Story text and retained repair/logo layers are separate. Painted characters, backgrounds and other branding remain raster. New SVGs require review. Original PNG approval records are unchanged.</aside>'''+''.join(cards)+'</html>')

bundle=OUT/'Book1_All_16_Layered_SVG_Spreads_2026-11-07.zip'
with zipfile.ZipFile(bundle,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for e in records:z.write(e['svg_path'],f"Pages_{e['pages']}/{e['svg_filename']}")
 for f in [mf,gf,gallery]:z.write(f,f.name)
 z.write(P/'Roboto.ttf','Fonts/Roboto.ttf')
 z.write(P/'OFL.txt','Fonts/OFL.txt')
with zipfile.ZipFile(bundle) as z:assert z.testzip() is None
print(json.dumps({'files':[f.name for f in [mf,gf,index,gallery,bundle]],'bundle_mb':round(bundle.stat().st_size/1e6,1)},indent=2))
