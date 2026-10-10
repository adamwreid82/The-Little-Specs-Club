const fs=require('fs'),s=require('sharp'),c=require('crypto');
const hash=p=>c.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
(async()=>{
 const base='work/Pages_11-12_REV10_LOCAL_CANON_CORRECTIONS_PENDING_REVIEW.png',generated='generated_images/exec-3f3e8697-e4cc-4293-b2bd-fe27438bc6a5.png';
 const left=2774+190,top=1121+238,W=150,H=100;
 const old=await s(base).extract({left,top,width:W,height:H}).ensureAlpha().raw().toBuffer(),d=await s(generated).resize(W,H,{fit:'fill'}).ensureAlpha().raw().toBuffer();let mask=0;
 for(let y=0;y<H;y++)for(let x=0;x<W;x++){let i=(y*W+x)*4;const iris=(x>28&&x<60&&y>16&&y<56)||(x>78&&x<112&&y>32&&y<74);const green=old[i+1]>old[i]*1.12&&old[i+1]>old[i+2]*1.3;d[i+3]=iris&&green?255:0;if(d[i+3])mask++;}
 const out='work/Pages_11-12_REV11_CANON_CORRECTIONS_PENDING_REVIEW.png';
 await s(base).composite([{input:await s(d,{raw:{width:W,height:H,channels:4}}).png().toBuffer(),left,top}]).withMetadata({density:300}).png().toFile(out);
 await s(out).resize(1774,887).png().toFile('work/Pages_11-12_REV11_PREVIEW.png');
 await s(out).extract({left:2774,top:1121,width:1121,height:1366}).png().toFile('work/REV11_CHILDREN_DETAIL.png');
 const b=await s(base).ensureAlpha().raw().toBuffer(),n=await s(out).ensureAlpha().raw().toBuffer();let outside=0,count=0;
 for(let y=0;y<2550;y++)for(let x=0;x<5100;x++){let i=(y*5100+x)*4;if(b[i]!==n[i]||b[i+1]!==n[i+1]||b[i+2]!==n[i+2]){count++;if(x<left||x>=left+W||y<top||y>=top+H)outside++;}}
 const v={...JSON.parse(fs.readFileSync('work/REV10_VERIFICATION.json')),revision:'REV11',base_revision:'REV10',base_sha256:hash(base),sha256:hash(out),iris_repair_bbox:[left,top,W,H],iris_mask_pixels:mask,iris_changed_pixels:count,changed_pixels_outside_iris_crop:outside,generated_iris_input:generated,all_pass:false,approved:false,remaining_unverified:['exact_numeric_heights','full_source_likeness','pose_rectified_graphic_baseline','hidden_details','full_site_geometry','native_print_proof_and_bleed_preflight']};
 fs.writeFileSync('work/REV11_VERIFICATION.json',JSON.stringify(v,null,2));console.log(JSON.stringify(v));
})();
