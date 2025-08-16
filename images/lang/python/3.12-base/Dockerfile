FROM docker.io/securityuniversal/base-ubuntu:24.04-2025.08.P4
USER root
RUN apt-get update && apt-get install -y --no-install-recommends python3.12 python3.12-venv python3-pip && rm -rf /var/lib/apt/lists/*
USER appuser
CMD ["python3","--version"]
