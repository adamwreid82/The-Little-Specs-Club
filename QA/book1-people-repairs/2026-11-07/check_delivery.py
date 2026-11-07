"""Mechanical delivery checks. Does not certify character likeness or grant approval."""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest',type=Path);p.add_argument('--candidates',type=Path,required=True);p.add_argument('--originals',type=Path,required=True);a=p.parse_args()
 m=json.loads(a.manifest.read_text());rows=m['repaired_spreads'];assert len(rows)==11
 assert m['status']=='VERSION B - REVIEW REQUIRED' and m['author_approval'] is None
 ids=[f['id'] for r in rows for f in r['findings']];assert sorted(ids)==[f'F{i:02}' for i in range(1,21)]
 for r in rows:
  assert r['author_approval'] is None and r['status']=='VERSION B - REVIEW REQUIRED'
  assert r['changed_outside_repair_masks']==0 and r['dimensions']==[5100,2550]
  file=a.candidates/r['filename'];old=a.originals/r['source_filename']
  assert hashlib.sha256(file.read_bytes()).hexdigest()==r['sha256'],r['pages']
  assert hashlib.sha256(old.read_bytes()).hexdigest()==r['source_sha256'],r['pages']
  im=Image.open(file);assert list(im.size)==r['dimensions']
  assert hashlib.sha256(im.convert('RGB').tobytes()).hexdigest()==r['pixel_sha256']
  assert r['drive_id']!=r['original_drive_id']
  assert all(p['source_image_id'] and p['profile_id'] and len(p['source_image_sha256'])==64 and len(p['profile_sha256'])==64 and p['approved_references'] for p in r['source_bindings'])
  assert r['unverified']
 assert len({r['pages'] for r in rows}|{r['pages'] for r in m['unchanged_spreads']})==16
 assert all(r['exact_drive_bytes_match'] for r in m['verification']['drive_candidate_bytes'])
 print('PASS: 11 exact candidates, 20 findings, 16 active page ranges, original hashes retained, current source bindings and review-only approval states.')
if __name__=='__main__':main()
