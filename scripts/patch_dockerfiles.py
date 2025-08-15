import os, re, sys
base_name  = os.environ['BASE_NAME']
old_tag    = os.environ['OLD_TAG']
new_tag    = os.environ['NEW_TAG']

# FROM <anything/>BASE:TAG [AS stage]
pat = re.compile(
    r'^(?P<prefix>\s*FROM\s+)(?P<ref>\S*/)?(?P<name>%s):(?P<tag>[^\s]+)(?P<suffix>(\s+AS\s+\S+)?\s*)$' % re.escape(base_name)
)
print(f"Regex pattern: {pat.pattern}")
print(f"Environment variables: BASE_NAME={base_name}, OLD_TAG={old_tag}, NEW_TAG={new_tag}")
def patch_text(s):
    out, changed=[], False
    for line in s.splitlines(keepends=False):
        m = pat.match(line)
        if m and m.group('tag') == old_tag:
            line = f"{m.group('prefix')}{m.group('ref') or ''}{m.group('name')}:{new_tag}{m.group('suffix')}"
            changed=True
        out.append(line)
    return ("\n".join(out) + ("\n" if s.endswith("\n") else "")), changed

def find_files(root):
    for d, _, files in os.walk(root):
        for f in files:
            if f.lower() in ('dockerfile',) or f.lower().endswith('.dockerfile'):
                yield os.path.join(d,f)

root = sys.argv[1] if len(sys.argv)>1 else "."
print(f"Searching for Dockerfiles in: {root}")
touched=[]
for p in list(find_files(root)):
    with open(p,'r',encoding='utf-8',errors='ignore') as fh: src = fh.read()
    dst, ch = patch_text(src)
    if ch:
        with open(p,'w',encoding='utf-8') as fh: fh.write(dst)
        touched.append(p)
if touched:
    print("\n".join(touched))
    sys.exit(0)
else:
    sys.exit(10)