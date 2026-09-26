from PIL import Image
import sys
p=sys.argv[1]; im=Image.open(p)
ok=im.size==(5100,2550)
print(("PASS" if ok else "FAIL")+f" dimensions {im.size[0]}x{im.size[1]}")
raise SystemExit(0 if ok else 1)
