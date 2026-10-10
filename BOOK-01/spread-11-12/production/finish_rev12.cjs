const fs=require('fs'),s=require('sharp'),c=require('crypto');const hash=p=>c.createHash('sha256').update(fs.readFileSync(p)).digest('hex');const clamp=n=>Math.max(0,Math.min(1,n));
(async()=>{
 const base='work/Pages_11-12_REV9_PERSPECTIVE_CORRECTIONS_PENDING_REVIEW.png',crop='work/REV10_CORRECTED_CHILDREN_DETAIL.png',k=5100/1774,W=1121,H=1366,L=2774,T=1121;
 let p=await s(crop).ensureAlpha().raw().toBuffer();
 // Bring forward only the corrected iris pixels from REV11.
 const iris=await s('work/Pages_11-12_REV11_CANON_CORRECTIONS_PENDING_REVIEW.png').extract({left:L+190,top:T+238,width:150,height:100}).ensureAlpha().raw().toBuffer();
 for(let y=0;y<100;y++)for(let x=0;x<150;x++)for(let a=0;a<3;a++)p[((y+238)*W+x+190)*4+a]=iris[(y*150+x)*4+a];
 const original=await s(base).extract({left:L,top:T,width:W,height:H}).ensureAlpha().raw().toBuffer();
 const matte=Buffer.alloc(W*H);
 for(let y=0;y<H;y++)for(let x=0;x<W;x++){let i=(y*W+x)*4,ox=x/k,oy=y/k;let a=Math.min(clamp(ox/8),clamp(oy/8),clamp((475-oy)/8),clamp((385-ox)/7));
 const r=original[i],g=original[i+1],b=original[i+2];
 const purple=ox>340&&b>r*.9&&b>g*1.2&&r>g*1.1;
 const trousers=ox>360&&oy>230&&Math.max(r,g,b)-Math.min(r,g,b)<35&&Math.max(r,g,b)<160;
 const adultFoot=ox>350&&oy>365&&((r>g*1.3&&b<g*.85)||(Math.max(r,g,b)<120));
 if(purple||trousers||adultFoot)a=0;
 matte[y*W+x]=Math.round(a*255);
 }
 const soft=await s(matte,{raw:{width:W,height:H,channels:1}}).blur(1.2).raw().toBuffer();
 for(let i=0;i<W*H;i++)p[i*4+3]=soft[i];
 const out='work/Pages_11-12_REV12_CANON_CORRECTIONS_PENDING_REVIEW.png';
 await s(base).composite([{input:await s(p,{raw:{width:W,height:H,channels:4}}).png().toBuffer(),left:L,top:T}]).withMetadata({density:300}).png().toFile(out);
 await s(out).resize(1774,887).png().toFile('work/Pages_11-12_REV12_PREVIEW.png');
 await s(out).extract({left:3700,top:1230,width:380,height:800}).png().toFile('work/REV12_JOIN_INSPECTION.png');
 const orig=await s(base).ensureAlpha().raw().toBuffer(),now=await s(out).ensureAlpha().raw().toBuffer();let outside=0,text=0;
 for(let y=0;y<2550;y++)for(let x=0;x<5100;x++){let i=(y*5100+x)*4;if(orig[i]!==now[i]||orig[i+1]!==now[i+1]||orig[i+2]!==now[i+2]){if(x<L||x>=L+W||y<T||y>=T+H)outside++;if(y<=885)text++;}}
 const v={...JSON.parse(fs.readFileSync('work/REV11_VERIFICATION.json')),revision:'REV12',base_revision:'REV9',base_sha256:hash(base),sha256:hash(out),outside_repair_changed_pixels:outside,existing_text_region_changed_pixels:text,seam_repair:'silhouette_aware_feather_preserving_original_adult_cloth',approved:false,all_pass:false};fs.writeFileSync('work/REV12_VERIFICATION.json',JSON.stringify(v,null,2));console.log(JSON.stringify({out,sha256:v.sha256,outside,text}));
})();
