import sys, yaml
p=sys.argv[1]
d=yaml.safe_load(open(p,encoding="utf-8"))
required=["spread","status","version_b"]
missing=[k for k in required if k not in d]
print("PASS manifest" if not missing else "FAIL missing: "+", ".join(missing))
raise SystemExit(0 if not missing else 1)
