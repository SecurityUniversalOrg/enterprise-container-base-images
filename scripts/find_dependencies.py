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
roots = {x.strip() for x in roots_in.split(',') if x.strip()}
selected = find_direct_dependencies(roots, dep)

# Keep original matrix entries but filtered by name
matrix_subset = [i for i in images if i.get('name') in selected]
# Output only the list of names as the job output
names_subset = [i['name'] for i in matrix_subset]

# Write to GITHUB_OUTPUT
with open(os.environ['GITHUB_OUTPUT'], 'a') as gh:
    gh.write("subset=" + json.dumps(names_subset) + "\n")