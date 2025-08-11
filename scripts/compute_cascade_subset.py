#!/usr/bin/env python3
import os, yaml, json, subprocess, collections

# Load dependency graph and matrix
with open('dependency-graph.yaml', 'r') as f:
    dep = yaml.safe_load(f) or {}
with open('matrix.yaml', 'r') as f:
    mat = yaml.safe_load(f) or {}

images = mat.get('images', []) or []
all_names = {i['name'] for i in images if 'name' in i}

def changed_roots_from_git():
    try:
        out = subprocess.check_output(
            ["git", "diff", "--name-only", "HEAD~1..HEAD"],
            text=True
        )
    except Exception:
        return set()
    roots = set()
    for line in out.splitlines():
        parts = line.strip().split('/')
        # expects images/<category>/<name>/...
        if len(parts) >= 3 and parts[0] == "images":
            candidate = f"{parts[1]}-{parts[2]}".replace('_', '-')
            if candidate in all_names:
                roots.add(candidate)
    return roots

def walk(roots, graph):
    seen = set()
    stack = list(roots)
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        for c in (graph.get(n) or []):
            stack.append(c)
    return seen

roots_in = (os.getenv('ROOTS') or '').strip()
full = (os.getenv('FULL_REBUILD') or 'false').lower() == 'true'
schedule_event = (os.getenv('EVENT_NAME') == 'schedule')

selected = set()
if full or schedule_event:
    selected = all_names
else:
    if roots_in:
        roots = {x.strip() for x in roots_in.split(',') if x.strip()}
    else:
        roots = changed_roots_from_git()

    if roots:
        selected = walk(roots, dep)
    else:
        selected = set()

# Keep original matrix entries but filtered by name
matrix_subset = [i for i in images if i.get('name') in selected]
# Output only the list of names as the job output
names_subset = [i['name'] for i in matrix_subset]

# Write to GITHUB_OUTPUT
with open(os.environ['GITHUB_OUTPUT'], 'a') as gh:
    gh.write("subset=" + json.dumps(names_subset) + "\n")