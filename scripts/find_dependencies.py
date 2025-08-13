#!/usr/bin/env python3
import os, yaml, json

# Load dependency graph
with open('dependency-graph.yaml', 'r') as f:
    dep = yaml.safe_load(f) or {}

# Load matrix
with open('matrix.yaml', 'r') as f:
    mat = yaml.safe_load(f) or {}

images = mat.get('images', []) or []
all_names = {i['name'] for i in images if 'name' in i}


def find_transitive_dependencies(roots, graph):
    seen = set()
    stacks = {
        "roots": list(roots),
        "stack": list(roots)
    }
    while stacks["stack"]:
        n = stacks["stack"].pop()
        if n in seen:
            continue
        if n not in stacks["roots"]:
            seen.add(n)
        for c in (graph.get(n) or []):
            stacks["stack"].append(c)
    return seen

def find_direct_dependencies(roots, graph):
    seen = set()
    roots = list(roots),
    for root in roots:
        root_name = root[0]
        dependents = graph.get(root_name, [])
        for n in dependents:
            for image in n:
                for repo in n[image]:
                    add_name = f"{image}:{repo}"
                    seen.add(add_name)
    return seen

roots_in = (os.getenv('ROOTS') or '')
roots_in = 'base-ubuntu'
print(f"Roots input: {roots_in}")

roots = {x.strip() for x in roots_in.split(',') if x.strip()}
print(f"Parsed roots: {roots}")
selected = find_direct_dependencies(roots, dep)
print(f"Selected dependencies: {selected}")

# Keep original matrix entries but filtered by name
matrix_subset = []
for i in images:
    for s in selected:
        if i.get('name') == s.split(':')[0]:
            matrix_subset.append(i)
print(f"Filtered matrix entries: {matrix_subset}")
# Output only the list of names as the job output

# Write to GITHUB_OUTPUT
with open(os.environ['GITHUB_OUTPUT'], 'a') as gh:
    gh.write("subset=" + json.dumps(matrix_subset) + "\n")