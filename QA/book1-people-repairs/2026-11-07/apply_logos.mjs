import fs from 'node:fs';
import path from 'node:path';
import {execFileSync as run} from 'node:child_process';
const dir=path.resolve('spread_repairs_2026_11_07');
const rows=JSON.parse(fs.readFileSync(path.join(dir,'records/overlays.json'),'utf8'));
for(const r of rows){
 if(process.argv[2] && r.id!==process.argv[2])continue;
 const asset=path.join(dir,'inputs',r.asset);
 const [w,h]=run('magick',['identify','-format','%w %h',asset],{encoding:'utf8'}).trim().split(' ').map(Number);
 const q=r.quad.map(([x,y])=>[x+r.origin[0],y+r.origin[1]]);
 const x=Math.floor(Math.min(...q.map(p=>p[0])))-3,y=Math.floor(Math.min(...q.map(p=>p[1])))-3;
 const bw=Math.ceil(Math.max(...q.map(p=>p[0])))-x+4,bh=Math.ceil(Math.max(...q.map(p=>p[1])))-y+4;
 const src=[[0,0],[w-1,0],[w-1,h-1],[0,h-1]];
 const coords=src.map((s,i)=>`${s[0]},${s[1]} ${q[i][0]-x},${q[i][1]-y}`).join(' ');
 const layer=path.join(dir,'generated',`${r.id}_${r.key}_logo.png`);
 run('magick',[asset,'-alpha','on','-virtual-pixel','transparent','-define',`distort:viewport=${bw}x${bh}+0+0`,'-distort','Perspective',coords,layer]);
 const file=path.join(dir,'candidates',`Book1_Pages${r.id}_REV${r.revision}_PEOPLE_REPAIRS_REVIEW.png`);
 run('magick',[file,layer,'-geometry',`+${x}+${y}`,'-compose','Over','-composite',file]);
 r.full_quad=q;r.layer_box=[x,y,bw,bh];
}
fs.writeFileSync(path.join(dir,'records/overlays.json'),JSON.stringify(rows,null,2));
for(const id of new Set(rows.map(r=>r.id))){const r=rows.find(r=>r.id===id);run('magick',[path.join(dir,'candidates',`Book1_Pages${id}_REV${r.revision}_PEOPLE_REPAIRS_REVIEW.png`),'-resize','2400x1200',path.join(dir,'candidates',id+'_preview.jpg')]);}
console.log('Applied',rows.length,'exact source graphics');
