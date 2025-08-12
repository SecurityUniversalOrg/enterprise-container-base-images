import os, json, yaml

m = yaml.safe_load(open('matrix.yaml'))
subset = os.getenv('SUBSET','').strip()
images = m.get('images', [])
if subset:
    wanted = {x.strip() for x in subset.split(',') if x.strip()}
    images = [i for i in images if i.get('name') in wanted]
open(os.environ['GITHUB_OUTPUT'],'a').write("matrix="+json.dumps(images)+"\n")