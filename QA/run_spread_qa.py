import subprocess,sys
from pathlib import Path
spread=Path(sys.argv[1])
manifest=spread/"manifest.yaml"
checks=[[sys.executable,"QA/check_canon.py"], [sys.executable,"QA/check_manifest.py",str(manifest)]]
images=list((spread/"version-b").glob("*.png"))
if images: checks.append([sys.executable,"QA/check_dimensions.py",str(images[0])])
else: print("INFO no Version B PNG candidate yet")
failed=False
for c in checks:
    if subprocess.run(c).returncode: failed=True
raise SystemExit(1 if failed else 0)
