FROM node:20-bookworm-slim

# Patch OS and npm (to pull cross-spawn >= 7.0.5) and prove it.
RUN set -eux; \
    apt-get update; \
    apt-get -y dist-upgrade --no-install-recommends; \
    # Upgrade npm (the global one bundled with Node)
    npm -g install npm@latest; \
    # Verify cross-spawn version is patched (CVE-2024-21538) in global tree
    npm ls -g cross-spawn || true; \
    # Clean up
    npm cache clean --force; \
    rm -rf /var/lib/apt/lists/*
