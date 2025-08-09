# platform-container-base-images

Enterprise **base images** used by application containers **and** GitHub ARC runner images.  
Design goals: **security-first**, **layered**, **predictable tagging**, **automatic cascade rebuilds**.

## Layering model
```
base/ubuntu:24.04            -> web/apache:2.4
web/apache:2.4               -> web/flask:py3.12 (mod_wsgi)
base/ubi9:fips               -> (federal-only base)
lang/python:3.12-base        -> app-specific Python images
lang/java:21-jre             -> Java runtime images
lang/node:20-runtime         -> Node runtime images
lang/dotnet:8-aspnet         -> .NET runtime images
```

## Tagging
- Monthly: `2025.08`
- Latest within stream: `2025.08-latest`
- Example: `docker.io/kaiserbros/base-ubuntu:24.04-2025.08`

## Cascading rebuilds
- If `base/ubuntu` updates, workflows **rebuild** `web/apache` and `web/flask`.
- After successful publish, a **repository_dispatch** triggers the **platform-arc-runner-images** repo to rebuild dependent runner images.

See `.github/workflows/build-scan-sign-publish.yml`.
