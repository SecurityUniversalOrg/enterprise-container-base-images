# scripts/patch_dockerfiles.py
import os, re, sys

base_name  = os.environ['BASE_NAME']
old_tag    = os.environ.get('OLD_TAG', '')
new_tag    = os.environ['NEW_TAG']

# Match:
#   FROM [--platform=xxx ] [registry/...]<base_name>:<tag> [AS stage]
pat = re.compile(
    r'^(?P<prefix>\s*FROM\s+)'                # FROM (with leading spaces)
    r'(?P<platform>--platform=\S+\s+)?'       # optional --platform=
    r'(?P<ref>\S*/)?'                         # optional registry/repo/
    r'(?P<name>%s):(?P<tag>[^\s]+)'           # name:tag
    r'(?P<suffix>(\s+AS\s+\S+)?\s*)$' % re.escape(base_name),
    flags=re.IGNORECASE
)

def patch_text(s):
    out, changed=[], False
    for line in s.splitlines(keepends=False):
        m = pat.match(line)
        if m:
            current_tag = m.group('tag')
            # If OLD_TAG provided, only replace when it matches; if not provided, replace any tag
            if (old_tag and current_tag == old_tag) or (not old_tag and current_tag != new_tag):
                line = f"{m.group('prefix')}{m.group('platform') or ''}{m.group('ref') or ''}" \
                       f"{m.group('name')}:{new_tag}{m.group('suffix')}"
                changed=True
        out.append(line)
    return ("\n".join(out) + ("\n" if s.endswith("\n") else "")), changed

def find_files(root):
    for d, _, files in os.walk(root):
        for f in files:
            if f.lower() in ('dockerfile',) or f.lower().endswith('.dockerfile'):
                yield os.path.join(d,f)

root = sys.argv[1] if len(sys.argv)>1 else "."
touched=[]
for p in list(find_files(root)):
    with open(p,'r',encoding='utf-8',errors='ignore') as fh:
        src = fh.read()
    dst, ch = patch_text(src)
    if ch:
        with open(p,'w',encoding='utf-8') as fh:
            fh.write(dst)
        touched.append(p)

if touched:
    print("\n".join(touched))
    sys.exit(0)
else:
    # exit code 10 = no changes (so caller can skip PR cleanly)
    sys.exit(10)
