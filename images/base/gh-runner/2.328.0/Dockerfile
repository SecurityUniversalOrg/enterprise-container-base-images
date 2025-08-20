FROM mcr.microsoft.com/dotnet/runtime-deps:8.0-jammy AS build

ARG TARGETOS=linux
ARG TARGETARCH=amd64
ARG RUNNER_VERSION=2.328.0
ARG RUNNER_CONTAINER_HOOKS_VERSION=0.7.0

RUN apt update -y && apt install curl unzip -y

WORKDIR /actions-runner
RUN export RUNNER_ARCH=${TARGETARCH} \
    && if [ "$RUNNER_ARCH" = "amd64" ]; then export RUNNER_ARCH=x64 ; fi \
    && curl -f -L -o runner.tar.gz https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-${TARGETOS}-${RUNNER_ARCH}-${RUNNER_VERSION}.tar.gz \
    && tar xzf ./runner.tar.gz \
    && rm runner.tar.gz

RUN curl -f -L -o runner-container-hooks.zip https://github.com/actions/runner-container-hooks/releases/download/v${RUNNER_CONTAINER_HOOKS_VERSION}/actions-runner-hooks-k8s-${RUNNER_CONTAINER_HOOKS_VERSION}.zip \
    && unzip ./runner-container-hooks.zip -d ./k8s \
    && rm runner-container-hooks.zip

FROM mcr.microsoft.com/dotnet/runtime-deps:8.0-jammy

ENV DEBIAN_FRONTEND=noninteractive
ENV RUNNER_MANUALLY_TRAP_SIG=1
ENV ACTIONS_RUNNER_PRINT_LOG_TO_STDOUT=1
ENV ImageOS=ubuntu22

# 'gpg-agent' and 'software-properties-common' are needed for the 'add-apt-repository' command that follows
RUN apt update -y \
    && apt install -y --no-install-recommends sudo lsb-release gpg-agent software-properties-common curl jq unzip \
    && rm -rf /var/lib/apt/lists/*

# Configure git-core/ppa based on guidance here:  https://git-scm.com/download/linux
RUN add-apt-repository ppa:git-core/ppa \
    && apt update -y \
    && apt install -y git \
    && rm -rf /var/lib/apt/lists/*

## Start of Custom Updates

# Install jq - already installed in line 30

# Install yq
RUN add-apt-repository ppa:rmescandon/yq \
    && apt update -y \
    && apt install -y yq

# Install git - already installed in line 36

# Install gh cli
ARG GH_VERSION="2.76.2"

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends curl ca-certificates gnupg; \
    rm -rf /var/lib/apt/lists/*; \
    \
    # Install GitHub CLI apt repo key (keyring)
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
      -o /usr/share/keyrings/githubcli-archive-keyring.gpg; \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg; \
    \
    # Add GitHub CLI apt source (architecture-aware)
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
      > /etc/apt/sources.list.d/github-cli.list; \
    \
    # Install gh (optionally pinned)
    apt-get update; \
    if [ -n "$GH_VERSION" ]; then \
      apt-get install -y --no-install-recommends "gh=${GH_VERSION}*"; \
    else \
      apt-get install -y --no-install-recommends gh; \
    fi; \
    \
    # Cleanup
    rm -rf /var/lib/apt/lists/*

# Quick self-check
RUN gh --version

## End of Custom Updates

WORKDIR /home/runner

RUN adduser --disabled-password --gecos "" --uid 1001 runner \
  && usermod -aG sudo runner \
  && echo "%sudo   ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers \
  && echo "Defaults env_keep += \"DEBIAN_FRONTEND\"" >> /etc/sudoers

COPY --chown=runner:runner --from=build /actions-runner .

## Patch for CVE-2024-21538 by upgrading npm (pulls fixed cross-spawn)
RUN set -eux; \
  # locate bundled Node and put it on PATH
  NODEBIN=""; \
  for v in 24 22 20 18 16; do \
    if [ -x "/home/runner/externals/node${v}/bin/node" ]; then NODEBIN="/home/runner/externals/node${v}/bin"; break; fi; \
  done; \
  [ -n "$NODEBIN" ] || { echo "No bundled Node found under /home/runner/externals"; exit 1; }; \
  export PATH="$NODEBIN:$PATH"; \
  node -v; npm -v || true; \
  \
  # upgrade npm globally (no scripts) and force public registry
  npm config set registry https://registry.npmjs.org/; \
  npm config set @npmcli:registry https://registry.npmjs.org/; \
  npm i -g npm@11.5.2 --ignore-scripts --no-audit --no-fund --registry=https://registry.npmjs.org/; \
  \
  # verify the cross-spawn version that npm now vendors (resolve via npm's global root)
  node -e 'const {execSync}=require("child_process"); \
           const p=require("path"); \
           const root=execSync("npm root -g").toString().trim(); \
           const cs=p.join(root,"npm","node_modules","cross-spawn","package.json"); \
           console.log("cross-spawn:", require(cs).version);'
##

RUN chown runner:runner /home/runner

USER runner
