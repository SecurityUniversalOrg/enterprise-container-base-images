import yaml, os, sys

m=yaml.safe_load(open("matrix.yaml"))
ns=m.get("dockerhub_namespace")
owner=os.environ.get("GITHUB_REPOSITORY_OWNER","")
repo=f"docker.io/{ns}" if ns else f"docker.io/{owner}"
print(f"repo={repo}")