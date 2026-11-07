import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
const root=process.cwd();
const dir=path.join(root,'spread_repairs_2026_11_07');
const records=JSON.parse(fs.readFileSync(path.join(dir,'records/patches.json'),'utf8'));
const started=new Set();
for(const r of records){
 if(process.argv[2] && r.id!==process.argv[2])continue;
 const [x,y,w,h]=r.crop;
 const original=path.join(root,'spread_review_2026_11_04/spreads',r.original);
 const key=r.id+'_'+(r.key||'Rivera');
 const resized=path.join(dir,'generated',key+'_aligned.png');
 const mask=path.join(dir,'generated',key+'_mask.png');
 const patch=path.join(dir,'generated',key+'_patch.png');
 const output=path.join(dir,'candidates',`Book1_Pages${r.id}_REV${r.revision}_PEOPLE_REPAIRS_REVIEW.png`);
 execFileSync('magick',[path.join(root,'generated_images',r.generated),'-resize',`${w}x${h}!`,resized]);
 const draw=(r.polygons||[r.polygon]).map(p=>'polygon '+p).join(' ');
 execFileSync('magick',['-size',`${w}x${h}`,'xc:black','-fill','white','-draw',draw,'-blur',`0x${r.feather}`,mask]);
 execFileSync('magick',[resized,mask,'-alpha','off','-compose','CopyOpacity','-composite',patch]);
 if(!started.has(r.id)){fs.copyFileSync(original,output);started.add(r.id);}
 execFileSync('magick',[output,patch,'-geometry',`+${x}+${y}`,'-compose','Over','-composite',output]);
 execFileSync('magick',[output,'-resize','2400x1200',path.join(dir,'candidates',r.id+'_preview.jpg')]);
 console.log(output);
}
