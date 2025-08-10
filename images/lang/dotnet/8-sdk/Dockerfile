FROM mcr.microsoft.com/dotnet/sdk:8.0
# Remove optional tools that embed the vulnerable dependency in their deps trees
RUN set -eux; \
    rm -rf /usr/share/dotnet/sdk/*/DotnetTools/dotnet-format || true; \
    rm -rf /usr/share/dotnet/sdk/*/FSharp || true

