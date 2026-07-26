FROM --platform=linux/amd64 ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive
ARG GEM5_VERSION=v25.1.0.1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git scons python3 python3-venv python3-dev pkg-config \
    m4 zlib1g zlib1g-dev libprotobuf-dev protobuf-compiler libprotoc-dev \
    libgoogle-perftools-dev libboost-all-dev libhdf5-dev libpng-dev file \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN git clone --branch "${GEM5_VERSION}" --depth 1 \
    https://github.com/gem5/gem5.git /opt/gem5 && \
    cd /opt/gem5 && \
    scons build/X86/gem5.opt -j2

COPY requirements.txt /tmp/requirements.txt
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt

ENV GEM5_BIN=/opt/gem5/build/X86/gem5.opt
ENV PATH=/opt/venv/bin:/opt/gem5/build/X86:${PATH}
WORKDIR /workspace
CMD ["/bin/bash"]
