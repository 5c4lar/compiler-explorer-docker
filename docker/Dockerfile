FROM ubuntu:24.04 AS base

RUN apt update && apt install -y git wget python3-pip curl npm

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN git clone https://github.com/compiler-explorer/infra.git --depth 1 /infra

WORKDIR /infra

RUN make ce

RUN git clone https://github.com/compiler-explorer/compiler-explorer.git --depth 1 /compiler-explorer

WORKDIR /compiler-explorer

RUN make prebuild

EXPOSE 10240

COPY c.local.properties /compiler-explorer/etc/config
COPY c++.local.properties /compiler-explorer/etc/config

CMD ["make", "EXTRA_ARGS=--language c,c++", "run-only"]
