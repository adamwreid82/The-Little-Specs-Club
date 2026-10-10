const fs=require('fs'),s=require('sharp'),crypto=require('crypto');
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
function inside(x,y,p){let a=false;for(let i=0,j=p.length-1;i<p.length;j=i++){const [xi,yi]=p[i],[xj,yj]=p[j];if((yi>y)!==(yj>y)&&x<(xj-xi)*(y-yi)/(yj-yi)+xi)a=!a;}return a;}
async function patch(src,box,polygon,kind){const {left,top,width:W,height:H}=box;const d=await s(src).resize(W,H,{fit:'fill'}).ensureAlpha().raw().toBuffer();const original=await s('work/Pages_11-12_REV17_Version_A_ART_ONLY_DRAFT.png').extract(box).ensureAlpha().raw().toBuffer();const mask=Buffer.alloc(W*H);for(let y=0;y<H;y++)for(let x=0;x<W;x++){let a=inside(x,y,polygon)?255:0;const i=(y*W+x)*4,r=original[i],g=original[i+1],b=original[i+2];if(kind==='vinny'){
 // Protect the controlling original helmet, and every exposed pixel of Steph.
 if(y<275&&g>r*1.12&&g>b*1.08)a=0;
 if(x>375&&b>g*1.15&&r>g*1.1)a=0;
 if(x>445&&y>300)a=0;
 // Original front badge is outside this mask; do not regenerate any helmet graphics.
 }mask[y*W+x]=a;}
 const soft=await s(mask,{raw:{width:W,height:H,channels:1}}).blur(.8).toColourspace('b-w').raw().toBuffer();for(let i=0;i<W*H;i++)d[i*4+3]=soft[i];
 if(kind==='vinny'){
 // Restore the exact registered project sticker, with natural finger occlusion.
 const sticker=await s('work/11-12_Sticker_SOURCE.png').trim().resize(40,40).ensureAlpha().raw().toBuffer();
 for(let y=0;y<40;y++)for(let x=0;x<40;x++){const i=(y*40+x)*4,j=((y+425)*W+x+246)*4;const rr=d[j],gg=d[j+1],bb=d[j+2];if(!(rr>160&&gg>150&&bb>140))sticker[i+3]=0;}
 const q=await s(d,{raw:{width:W,height:H,channels:4}}).composite([{input:await s(sticker,{raw:{width:40,height:40,channels:4}}).png().toBuffer(),left:246,top:425}]).png().toBuffer();return {input:q,left,top};
 }return {input:await s(d,{raw:{width:W,height:H,channels:4}}).png().toBuffer(),left,top};}
(async()=>{
 const vinnyBox={left:2740,top:1170,width:660,height:1240},benBox={left:720,top:2110,width:430,height:340};
 const vp=[[224,155],[278,168],[340,194],[400,225],[465,252],[480,305],[455,345],[442,370],[477,444],[466,555],[444,655],[462,727],[451,806],[467,965],[478,1044],[478,1100],[440,1125],[336,1118],[311,1057],[291,851],[268,1016],[283,1066],[282,1099],[152,1120],[90,1091],[89,1043],[139,1000],[151,908],[175,773],[181,719],[150,680],[136,620],[148,582],[117,572],[96,525],[98,478],[118,430],[150,405],[191,344],[238,310],[212,283],[220,241],[218,203]];
 const bp=[[68,154],[137,161],[159,174],[190,162],[231,140],[259,137],[287,153],[307,169],[346,181],[369,201],[368,229],[335,242],[261,260],[182,260],[145,245],[114,239],[67,239],[59,214]];
 const vinny='generated_images/exec-c3eb207c-b3b8-48c4-97c0-e669eb3beb9b.png',ben='generated_images/exec-ae43021b-8ee5-45ae-8190-f15fa999157a.png';
 const patches=[await patch(vinny,vinnyBox,vp,'vinny'),await patch(ben,benBox,bp,'ben')];
 const art=await s('work/Pages_11-12_REV17_Version_A_ART_ONLY_DRAFT.png').composite(patches).png({compressionLevel:6}).toBuffer();
 const a='work/Pages_11-12_REV18_Version_A_ART_ONLY_DRAFT.png',b='work/Pages_11-12_REV18_Version_B_PENDING_REVIEW.png';
 // Use a fully decoded RGB raster for the art-only export, matching the verified re-encoding.
 const ar=await s(art).removeAlpha().raw().toBuffer({resolveWithObject:true});
 await s(ar.data,{raw:{width:ar.info.width,height:ar.info.height,channels:ar.info.channels}}).withMetadata({density:300}).png({compressionLevel:9}).toFile(a);await s(art).composite([{input:'work/Pages_11-12_REV2_TEXT_LAYER.png',left:0,top:0}]).withMetadata({density:300}).png({compressionLevel:6}).toFile(b);
 await s(b).resize(1774,887).jpeg({quality:95}).toFile('work/Pages_11-12_REV18_PREVIEW.jpg');
 await s(b).extract(vinnyBox).jpeg({quality:95}).toFile('work/REV18_VINNY_DETAIL.jpg');await s(b).extract(benBox).jpeg({quality:95}).toFile('work/REV18_BEN_SHOES_DETAIL.jpg');
 const before=await s('work/Pages_11-12_REV17_Version_B_PENDING_REVIEW.png').ensureAlpha().raw().toBuffer(),after=await s(b).ensureAlpha().raw().toBuffer();let outside=0,text=0,rest=0;for(let y=0;y<2550;y++)for(let x=0;x<5100;x++){let i=(y*5100+x)*4;if(before[i]!==after[i]||before[i+1]!==after[i+1]||before[i+2]!==after[i+2]){if(y<=885)text++;const allowed=[vinnyBox,benBox].some(r=>x>=r.left&&x<r.left+r.width&&y>=r.top&&y<r.top+r.height);if(!allowed)outside++;if(x>=3190&&y>=1600)rest++;}}
 for(const f of [a,b])await s(f).raw().toBuffer();
 const v={revision:'REV18',approved:false,all_pass:false,base_revision:'REV17',version_a_sha256:hash(a),version_b_sha256:hash(b),dimensions:[5100,2550],dpi:300,full_png_decode:'PASS',font_redesigned:false,existing_text_region_changed_pixels:text,outside_authorized_repair_changed_pixels:outside,far_right_group_changed_pixels:rest,repair_boxes:[vinnyBox,benBox],generated_inputs:[vinny,ben],version_a_and_b_same_art:true,source_files_modified:false,earlier_versions_preserved:true,exact_numeric_heights_verified:false,hidden_details_verified:false,print_ready:false};fs.writeFileSync('work/REV18_VERIFICATION.json',JSON.stringify(v,null,2));console.log(JSON.stringify(v));
})();
