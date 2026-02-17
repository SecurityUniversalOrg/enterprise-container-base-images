FROM mcr.microsoft.com/dotnet/runtime-deps:8.0-jammy AS fetch

ARG TARGETOS=linux
ARG TARGETARCH=amd64
ARG RUNNER_VERSION=2.331.0
ARG RUNNER_CONTAINER_HOOKS_VERSION=0.8.1
ARG CURL_VERSION=7.81.0-1ubuntu1.21
ARG UNZIP_VERSION=6.0-26ubuntu3.2
ARG CA_CERTIFICATES_VERSION=20240203~22.04.1

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      ca-certificates=${CA_CERTIFICATES_VERSION} \
      curl=${CURL_VERSION} \
      unzip=${UNZIP_VERSION}; \
    rm -rf /var/lib/apt/lists/*

WORKDIR /actions-runner

RUN set -eux; \
    RUNNER_ARCH="${TARGETARCH}"; \
    [ "${RUNNER_ARCH}" = "amd64" ] && RUNNER_ARCH="x64"; \
    curl -fsSL \
      "https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-${TARGETOS}-${RUNNER_ARCH}-${RUNNER_VERSION}.tar.gz" \
      -o runner.tar.gz; \
    tar xzf runner.tar.gz; \
    rm runner.tar.gz; \
    \
    curl -fsSL \
      "https://github.com/actions/runner-container-hooks/releases/download/v${RUNNER_CONTAINER_HOOKS_VERSION}/actions-runner-hooks-k8s-${RUNNER_CONTAINER_HOOKS_VERSION}.zip" \
      -o hooks.zip; \
    unzip hooks.zip -d ./k8s; \
    rm hooks.zip

FROM mcr.microsoft.com/dotnet/runtime-deps:8.0-jammy

ENV DEBIAN_FRONTEND=noninteractive \
    RUNNER_MANUALLY_TRAP_SIG=1 \
    ACTIONS_RUNNER_PRINT_LOG_TO_STDOUT=1 \
    ImageOS=ubuntu22

ARG SUDO_VERSION=1.9.9-1ubuntu2.5
ARG LSBD_VERSION=11.1.0ubuntu4
ARG GPG_AGENT_VERSION=2.2.27-3ubuntu2.5
ARG SOFTWARE_PROPERTIES_COMMON_VERSION=0.99.22.9
ARG JQ_VERSION=1.6-2.1ubuntu3.1
ARG CA_CERTIFICATES_VERSION=20240203~22.04.1
ARG GNUPG_VERSION=2.2.27-3ubuntu2.5
# Optional: switch to true if vulnerabilities are present
ARG USE_GIT_PPA=false
ARG GIT_VERSION=1:2.53.0-0ppa1~ubuntu22.04.1
ARG YQ_VERSION=v4.16.2
ARG GH_VERSION=2.86.0

# Create runner user early so we can COPY --chown later
RUN set -eux; \
    adduser --disabled-password --gecos "" --uid 1001 runner; \
    usermod -aG sudo runner; \
    echo "%sudo ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers; \
    echo "Defaults env_keep += \"DEBIAN_FRONTEND\"" >> /etc/sudoers

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      sudo=${SUDO_VERSION} \
      lsb-release=${LSBD_VERSION} \
      gpg-agent=${GPG_AGENT_VERSION} \
      software-properties-common=${SOFTWARE_PROPERTIES_COMMON_VERSION} \
      jq=${JQ_VERSION} \
      ca-certificates=${CA_CERTIFICATES_VERSION} \
      gnupg=${GNUPG_VERSION}; \
    rm -rf /var/lib/apt/lists/*

# Git (optionally via PPA)
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    set -eux; \
    if [ "${USE_GIT_PPA}" = "true" ]; then \
      add-apt-repository ppa:git-core/ppa; \
      apt-get update; \
      apt-get install -y --no-install-recommends git=${GIT_VERSION}; \
    else \
      apt-get update; \
      apt-get install -y --no-install-recommends git=${GIT_VERSION}; \
    fi; \
    rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    curl -fsSL "https://github.com/mikefarah/yq/releases/download/${YQ_VERSION}/yq_linux_amd64" -o /usr/local/bin/yq; \
    chmod +x /usr/local/bin/yq; \
    yq --version

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    set -eux; \
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
      -o /usr/share/keyrings/githubcli-archive-keyring.gpg; \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg; \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
      > /etc/apt/sources.list.d/github-cli.list; \
    apt-get update; \
    apt-get install -y --no-install-recommends "gh=${GH_VERSION}*"; \
    rm -rf /var/lib/apt/lists/*; \
    gh --version

WORKDIR /home/runner

COPY --from=fetch --chown=runner:runner /actions-runner /home/runner

USER runner
