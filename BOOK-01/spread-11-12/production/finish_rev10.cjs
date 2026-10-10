const fs=require('fs'),s=require('sharp'),crypto=require('crypto'),path=require('path');
const root=path.resolve(process.env.LITTLE_SPECS_WORKSPACE||process.cwd());
const f=p=>path.join(root,p),hash=p=>crypto.createHash('sha256').update(fs.readFileSync(f(p))).digest('hex');
const k=5100/1774, W=Math.round(390*k),H=Math.round(475*k),L=Math.round(965*k),T=Math.round(390*k);
const clamp=n=>Math.max(0,Math.min(1,n));
(async()=>{
 const first='generated_images/exec-babd1d09-7b3e-4eb4-acd0-eac5c1227587.png',second=process.argv[2];
 let crop=await s(f(first)).resize(W,H,{fit:'fill'}).ensureAlpha().png().toBuffer();
 const d=await s(f(second)).resize(W,H,{fit:'fill'}).ensureAlpha().raw().toBuffer();
 for(let y=0;y<H;y++)for(let x=0;x<W;x++){
 const ox=x/k,oy=y/k;
 const hats=(ox>67&&ox<132&&oy>32&&oy<94)||(ox>158&&ox<219&&oy>53&&oy<110)||(ox>263&&ox<320&&oy>67&&oy<126);
 const face=ox>154&&ox<224&&oy>101&&oy<155;
 const discs=(Math.hypot(ox-81,oy-173)<12)||(Math.hypot(ox-165,oy-190)<12)||(Math.hypot(ox-257,oy-205)<12);
 d[(y*W+x)*4+3]=hats||face||discs?255:0;
 }
 crop=await s(crop).composite([{input:await s(d,{raw:{width:W,height:H,channels:4}}).png().toBuffer(),left:0,top:0}]).png().toBuffer();
 const assets={LS:await s(f('work/11-12_LS_ASSET_fresh.png')).trim().png().toBuffer(),Sticker:await s(f('work/11-12_Sticker_SOURCE.png')).trim().png().toBuffer()};
 const placements=[['LS','Vinny',105,59,16,17,14],['LS','Steph',192,76,16,17,15],['LS','Maya',287,94,16,17,15],['Sticker','Vinny-held',81,173,12,13,0],['Sticker','Steph-held',165,190,12,13,0],['Sticker','Maya-held',257,205,12,13,0]];
 const raw=await s(crop).ensureAlpha().raw().toBuffer(),layers=[];
 for(const [asset,name,cx,cy,w,h,a] of placements){let b=await s(assets[asset]).resize(Math.round(w*k),Math.round(h*k),{fit:'fill'}).rotate(a,{background:'#00000000'}).png().toBuffer();const m=await s(b).metadata(),left=Math.round(cx*k-m.width/2),top=Math.round(cy*k-m.height/2);
 if(asset==='Sticker'){const p=await s(b).ensureAlpha().raw().toBuffer();for(let y=0;y<m.height;y++)for(let x=0;x<m.width;x++){let i=(y*m.width+x)*4,j=((top+y)*W+left+x)*4;if(!(raw[j]>180&&raw[j+1]>165&&raw[j+2]>140))p[i+3]=0;}b=await s(p,{raw:{width:m.width,height:m.height,channels:4}}).png().toBuffer();}layers.push({input:b,left,top});}
 crop=await s(crop).composite(layers).png().toBuffer();
 await s(crop).png().toFile(f('work/REV10_CORRECTED_CHILDREN_DETAIL.png'));
 const p=await s(crop).ensureAlpha().raw().toBuffer();
 for(let y=0;y<H;y++)for(let x=0;x<W;x++){const ox=x/k,oy=y/k;
 // Preserve Harper and blend only surrounding gravel/fence, not child anatomy.
 let a=Math.min(clamp(ox/8),clamp(oy/8),clamp((475-oy)/8));
 if(ox>350&&oy<170)a=0;
 if(ox>374)a=0;
 else if(ox>367)a*=clamp((374-ox)/7);
 p[(y*W+x)*4+3]=Math.round(255*a);
 }
 const out='work/Pages_11-12_REV10_LOCAL_CANON_CORRECTIONS_PENDING_REVIEW.png',base='work/Pages_11-12_REV9_PERSPECTIVE_CORRECTIONS_PENDING_REVIEW.png';
 await s(f(base)).composite([{input:await s(p,{raw:{width:W,height:H,channels:4}}).png().toBuffer(),left:L,top:T}]).withMetadata({density:300}).png().toFile(f(out));
 await s(f(out)).resize(1774,887).png().toFile(f('work/Pages_11-12_REV10_PREVIEW.png'));
 const b=await s(f(base)).ensureAlpha().raw().toBuffer(),n=await s(f(out)).ensureAlpha().raw().toBuffer();let outside=0,changes=0,textChanges=0;
 for(let y=0;y<2550;y++)for(let x=0;x<5100;x++){let i=(y*5100+x)*4;const changed=b[i]!==n[i]||b[i+1]!==n[i+1]||b[i+2]!==n[i+2];if(changed){changes++;if(x<L||x>=L+W||y<T||y>=T+H)outside++;if(y<=885)textChanges++;}}
 const v={revision:'REV10',approved:false,all_pass:false,base_sha256:hash(base),sha256:hash(out),export:[5100,2550],dpi:300,repair_bbox:[L,T,W,H],changed_pixels:changes,outside_repair_changed_pixels:outside,existing_text_region_changed_pixels:textChanges,exact_asset_hashes:{LS:hash('work/11-12_LS_ASSET_fresh.png'),Sticker:hash('work/11-12_Sticker_SOURCE.png')},local_asset_placements_crop_pixels:placements,generated_inputs:[first,second],new_full_scene_regeneration:false,preserved_previous_versions:true,physical_height_certification:false,print_proof:false};
 fs.writeFileSync(f('work/REV10_VERIFICATION.json'),JSON.stringify(v,null,2));console.log(JSON.stringify(v));
})();
