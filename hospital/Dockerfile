# syntax=docker.io/docker/dockerfile:1
FROM --platform=linux/riscv64 cartesi/python:3.10-slim-jammy

# Install Rust
RUN apt-get update && apt-get install -y curl build-essential \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && . $HOME/.cargo/env \
    && rustup install stable

# Install Cryptography dependencies
RUN apt-get install -y libssl-dev libffi-dev gcc

ARG MACHINE_EMULATOR_TOOLS_VERSION=0.14.1
ADD https://github.com/cartesi/machine-emulator-tools/releases/download/v${MACHINE_EMULATOR_TOOLS_VERSION}/machine-emulator-tools-v${MACHINE_EMULATOR_TOOLS_VERSION}.deb /
RUN dpkg -i /machine-emulator-tools-v${MACHINE_EMULATOR_TOOLS_VERSION}.deb \
  && rm /machine-emulator-tools-v${MACHINE_EMULATOR_TOOLS_VERSION}.deb

LABEL io.cartesi.rollups.sdk_version=0.9.0
LABEL io.cartesi.rollups.ram_size=128Mi

ARG DEBIAN_FRONTEND=noninteractive
RUN <<EOF
set -e
apt-get update
apt-get install -y --no-install-recommends \
  busybox-static=1:1.30.1-7ubuntu3
rm -rf /var/lib/apt/lists/* /var/log/* /var/cache/*
useradd --create-home --user-group dapp
EOF

ENV PATH="/opt/cartesi/bin:${PATH}"
ENV PYTHONPATH="/opt/cartesi/dapp:${PYTHONPATH}"

WORKDIR /opt/cartesi/dapp
COPY ./requirements.txt .

RUN <<EOF
set -e
pip install -r requirements.txt --no-cache
find /usr/local/lib -type d -name __pycache__ -exec rm -r {} +
EOF

COPY . ./hospital

ENV ROLLUP_HTTP_SERVER_URL="http://127.0.0.1:5004"
ENV GRAPHQL_SERVER_URL="http://host.docker.internal:8080/graphql"
ENV DETTACHED=False

ENTRYPOINT ["rollup-init"]
CMD ["python3", "hospital/main.py"]
