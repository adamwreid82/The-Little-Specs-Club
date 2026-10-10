const s=require('sharp'),fs=require('fs'),c=require('crypto');
const hash=p=>c.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
(async()=>{
const W=5100,H=2550,L=2850,T=1540,CW=320,CH=340,cx=143,cy=89,r=35.7;
const base='work/Pages_11-12_REV26_Version_A_ART_ONLY_DRAFT.png';
const clean='generated_images/exec-e6b8d82a-4adb-4d7d-94d5-6a7b99b7e820.png';
const orig=await s(base).removeAlpha().raw().toBuffer();
const crop=await s(base).extract({left:L,top:T,width:CW,height:CH}).removeAlpha().raw().toBuffer();
const generatedCrop=await s(clean).resize(CW,CH,{fit:'fill'}).png().toBuffer();
// Use only clean central paper texture, avoiding generated finger boundaries.
const blank=await s(generatedCrop).extract({left:133,top:72,width:20,height:30}).resize(CW,CH,{fit:'fill'}).removeAlpha().raw().toBuffer();
// Reconstruct the existing native Vinny layer before the large decal insert.
// This recovers contact-edge/nail pixels covered by the old print, without a new hand pose.
const nativeInput='generated_images/exec-98ecc5e7-e053-48f4-a8d5-bc46f56ab54f.png';
const nd=await s(nativeInput).ensureAlpha().raw().toBuffer({resolveWithObject:true});let x0=nd.info.width,y0=nd.info.height,x1=0,y1=0;
for(let y=0;y<nd.info.height;y++)for(let x=0;x<nd.info.width;x++){const i=(y*nd.info.width+x)*4,a=nd.data[i+3];if(a>127){x0=Math.min(x0,x);x1=Math.max(x1,x);y0=Math.min(y0,y);y1=Math.max(y1,y);}nd.data[i+3]=a>=250?255:Math.round(a*255/253);}
let native=await s(nd.data,{raw:{width:nd.info.width,height:nd.info.height,channels:4}}).extract({left:x0,top:y0,width:x1-x0+1,height:y1-y0+1}).resize({height:1035}).png().toBuffer();
const nm=await s(native).metadata(),nl=Math.round(2960-nm.width/2),nt=2278-nm.height;
const nativeCrop=await s(native).extract({left:L-nl,top:T-nt,width:CW,height:CH}).removeAlpha().raw().toBuffer();
// Only copy the generated disk surface; preserve original hands using connected skin components.
const skin=(x,y)=>{const i=(y*CW+x)*3;return crop[i]>180&&crop[i+1]>70&&crop[i+2]<170&&crop[i]>crop[i+1]*1.08&&crop[i+1]>crop[i+2]*1.08;};
const hand=new Uint8Array(CW*CH),q=[[95,105],[195,110]];
for(let j=0;j<q.length;j++){const [x,y]=q[j];if(x<0||y<0||x>=CW||y>=CH||hand[y*CW+x]||!skin(x,y))continue;hand[y*CW+x]=1;for(const [dx,dy]of [[1,0],[-1,0],[0,1],[0,-1]])q.push([x+dx,y+dy]);}
const protectedHand=new Uint8Array(CW*CH);
for(let y=0;y<CH;y++)for(let x=0;x<CW;x++)if(hand[y*CW+x])protectedHand[y*CW+x]=1;
let art=Buffer.from(orig),mask=new Uint8Array(CW*CH);
for(let y=0;y<CH;y++)for(let x=0;x<CW;x++){
const dist=Math.hypot(x-cx,y-cy);
if(dist>=r||protectedHand[y*CW+x])continue;
const a=Math.min(1,(r-dist)/.8),i=((y+T)*W+x+L)*3,j=(y*CW+x)*3;
mask[y*CW+x]=Math.round(a*255);
// Source-native warm skin at contact artifacts, generated clean paper on the disk.
const nativeSkin=nativeCrop[j]>180&&nativeCrop[j+1]>70&&nativeCrop[j+2]<180&&nativeCrop[j]>nativeCrop[j+1]*1.06&&nativeCrop[j+1]>nativeCrop[j+2]*1.04;
for(let k=0;k<3;k++)art[i+k]=Math.round(orig[i+k]*(1-a)+(nativeSkin?nativeCrop[j+k]:blank[j+k])*a);
}
// Exact approved asset, reduced printed diameter; blank backing is held by original fingers.
const diameter=40,left=L+123,top=T+69;
let glyph=await s('work/11-12_Sticker_SOURCE.png').trim().resize(diameter,diameter).ensureAlpha().raw().toBuffer();
for(let y=0;y<diameter;y++)for(let x=0;x<diameter;x++)if(protectedHand[(y+69)*CW+x+123])glyph[(y*diameter+x)*4+3]=0;
art=await s(art,{raw:{width:W,height:H,channels:3}}).composite([{input:await s(glyph,{raw:{width:diameter,height:diameter,channels:4}}).png().toBuffer(),left,top}]).removeAlpha().raw().toBuffer();
const A='work/Pages_11-12_REV27_Version_A_ART_ONLY_DRAFT.png',B='work/Pages_11-12_REV27_Version_B_STICKER_SCALE_CORRECTION_PENDING_REVIEW.png';
fs.writeFileSync(A,await s(art,{raw:{width:W,height:H,channels:3}}).withMetadata({density:300}).png({compressionLevel:9}).toBuffer());
fs.writeFileSync(B,await s(art,{raw:{width:W,height:H,channels:3}}).composite([{input:'work/Pages_11-12_REV2_TEXT_LAYER.png',left:0,top:0}]).withMetadata({density:300}).png({compressionLevel:9}).toBuffer());
const previous=await s('work/Pages_11-12_REV26_Version_B_LOCKED_HELMET_APPLICATION_PENDING_REVIEW.png').removeAlpha().raw().toBuffer(),now=await s(B).removeAlpha().raw().toBuffer();
let changed=0,outside=0,text=0,handChanges=0;
for(let y=0;y<H;y++)for(let x=0;x<W;x++){const i=(y*W+x)*3;if(previous[i]===now[i]&&previous[i+1]===now[i+1]&&previous[i+2]===now[i+2])continue;changed++;const xx=x-L,yy=y-T;if(xx<0||yy<0||xx>=CW||yy>=CH||Math.hypot(xx-cx,yy-cy)>=r)outside++;if(y<=885)text++;if(xx>=0&&xx<CW&&yy>=0&&yy<CH&&protectedHand[yy*CW+xx])handChanges++;}
const ab=await s(A).composite([{input:'work/Pages_11-12_REV2_TEXT_LAYER.png',left:0,top:0}]).removeAlpha().raw().toBuffer();let mismatch=0;for(let i=0;i<now.length;i++)if(ab[i]!==now[i])mismatch++;
for(const f of[A,B])await s(f).raw().toBuffer();
const v={revision:'REV27',base_revision:'REV26',approved:false,all_pass:false,visible_canon_result:'PENDING_MANUAL_INSPECTION',version_a_sha256:hash(A),version_b_sha256:hash(B),dimensions:[W,H],dpi:300,full_png_decode:'PASS',changed_pixels:changed,outside_sticker_circle_changed_pixels:outside,protected_original_hand_changed_pixels:handChanges,existing_text_region_changed_pixels:text,version_a_plus_original_text_vs_b_changed_channels:mismatch,helmet_face_body_and_background_pixels_preserved:outside===0,printed_sticker_diameter_pixels:diameter,prior_printed_diameter_pixels_approx:70,peer_diameter_pixels_approx:[35,40],physical_inches_not_certified:true,exact_sticker_asset_sha256:hash('work/11-12_Sticker_SOURCE.png'),generated_input:clean,edit_region:{left:L+cx-r,top:T+cy-r,radius:r},source_files_modified:false,font_redesigned:false,prior_versions_preserved:true,archived:false,print_ready:false};
if(outside||text||handChanges||mismatch)throw Error('Preservation failed '+JSON.stringify(v));
fs.writeFileSync('work/REV27_VERIFICATION.json',JSON.stringify(v,null,2));
await s(B).resize(1774,887).jpeg({quality:96}).toFile('work/Pages_11-12_REV27_PREVIEW.jpg');
await s(B).extract({left:L,top:T,width:CW,height:CH}).resize(640,680).png().toFile('work/REV27_HAND_DETAIL_AFTER.png');
await s(B).extract({left:2710,top:1220,width:1160,height:1210}).png().toFile('work/REV27_RIGHT_CHILDREN.png');
console.log(JSON.stringify(v));
})();
