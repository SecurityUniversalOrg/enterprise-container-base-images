
# Platform Container Base Images

Enterprise-grade **base images** for application containers and GitHub ARC runner images.  
**Security-first**, **layered**, and **automated** for robust CI/CD in regulated environments.

---

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Image Layering Model](#image-layering-model)
- [Tagging & Versioning](#tagging--versioning)
- [Cascade Rebuilds & Dependency Management](#cascade-rebuilds--dependency-management)
- [Security & Compliance](#security--compliance)
- [Contribution Guidelines](#contribution-guidelines)
- [Scripts & Automation](#scripts--automation)
- [Resources](#resources)
- [Contact & Support](#contact--support)

---

## Overview

This repository provides a suite of secure, maintainable, and composable container base images for enterprise workloads.  
Images are designed for use in production, CI/CD pipelines, and GitHub ARC runners, with strict controls for vulnerability management, reproducibility, and traceability.

---

## Repository Structure

```
images/
	base/
		ubuntu/24.04/
		ubuntu/24.04-slim/
		ubi9/fips/
	lang/
		python/3.12-base/
		java/21-jdk/
		java/21-jre/
		node/20-runtime/
		dotnet/8-aspnet/
		dotnet/8-sdk/
		go/1.22/
	web/
		apache/2.4/
		flask/py3.12/
scripts/
	build_matrix.py
	compute_cascade_subset.py
	find_dependencies.py
	patch_dockerfiles.py
	resolve_repo_prefix.py
matrix.yaml
dependency-graph.yaml
README.md
CONTRIBUTING.md
SECURITY.md
```

- **images/**: All Docker base images, organized by category and version.
- **scripts/**: Automation for build, dependency resolution, and tagging.
- **matrix.yaml**: Defines image build matrix, tags, and DockerHub namespace.
- **dependency-graph.yaml**: Explicit image dependency graph for cascade rebuilds.
- **CONTRIBUTING.md**: Contribution standards and workflow.
- **SECURITY.md**: Security policies and release criteria.

---

## Image Layering Model

Images are layered for composability and security.  
Example dependency chains:

```
base/ubuntu:24.04            -> web/apache:2.4
web/apache:2.4               -> web/flask:py3.12 (mod_wsgi)
base/ubi9:fips               -> (federal-only base)
lang/python:3.12-base        -> app-specific Python images
lang/java:21-jre             -> Java runtime images
lang/node:20-runtime         -> Node runtime images
lang/dotnet:8-aspnet         -> .NET runtime images
```

See `dependency-graph.yaml` for full relationships.

---

## Tagging & Versioning

- **Monthly tags**: `2025.08`
- **Latest stream**: `2025.08-latest`
- **Patch tags**: e.g. `24.04-2025.08.P1`
- **DockerHub namespace**: `securityuniversal`
- **Example**:  
	`docker.io/securityuniversal/base-ubuntu:24.04-2025.08`

See `matrix.yaml` for all image names, paths, and tags.

---

## Cascade Rebuilds & Dependency Management

- **Automatic rebuilds**: When a base image updates, all dependent images are rebuilt.
- **Repository dispatch**: Triggers downstream rebuilds in dependent repos (e.g., ARC runner images).
- **Scripts**:
	- `build_matrix.py`: Generates build matrix for CI.
	- `find_dependencies.py`: Resolves direct and transitive dependencies.
	- `compute_cascade_subset.py`: Determines which images to rebuild based on changes.
	- `patch_dockerfiles.py`: Updates Dockerfile `FROM` tags across the repo.
	- `resolve_repo_prefix.py`: Ensures correct DockerHub repo prefix.

---

## Security & Compliance

- **Vulnerability management**: HIGH/CRITICAL CVEs block release.
- **Image signing**: All images are signed.
- **SBOMs**: Software Bill of Materials are published for every release.
- **Federal compliance**: UBI9 FIPS images for regulated workloads.
- **Security policies**: See [`SECURITY.md`](SECURITY.md).

---

## Contribution Guidelines

- **Dockerfiles**: Keep minimal, pin all versions, update matrix and dependency graph on changes.
- **Pull requests**: Must pass security scans and automated tests.
- **Documentation**: Update `README.md`, `CONTRIBUTING.md`, and relevant scripts for new images or changes.
- **Release criteria**: No HIGH/CRITICAL CVEs, all images signed, SBOMs published.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for full details.

---

## Scripts & Automation

- **build_matrix.py**: Generates build matrix for CI workflows.
- **find_dependencies.py**: Finds direct/transitive dependencies for cascade rebuilds.
- **compute_cascade_subset.py**: Filters images for partial or full rebuilds.
- **patch_dockerfiles.py**: Bulk updates Dockerfile `FROM` tags.
- **resolve_repo_prefix.py**: Ensures correct DockerHub repo prefix.

Scripts are Python-based and use `matrix.yaml` and `dependency-graph.yaml` for orchestration.

---

## Resources

- **matrix.yaml**:  
	Defines all images, tags, and DockerHub namespace.
- **dependency-graph.yaml**:  
	Explicit dependency relationships for cascade rebuilds.
- **CONTRIBUTING.md**:  
	Contribution standards and workflow.
- **SECURITY.md**:  
	Security policies and release criteria.

---

## Contact & Support

For enterprise support, security disclosures, or questions, contact the repository owner or open an issue.

---

**Maintained by SecurityUniversalOrg.  
All rights reserved.**

---
