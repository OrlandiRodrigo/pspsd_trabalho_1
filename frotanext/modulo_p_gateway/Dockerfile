FROM ubuntu:22.04


ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Sao_Paulo

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    autoconf \
    libtool \
    pkg-config \
    libgrpc++-dev \
    protobuf-compiler-grpc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./contratos_grpc /app/contratos_grpc
COPY ./modulo_p_gateway /app/modulo_p_gateway

WORKDIR /app/modulo_p_gateway

RUN rm -rf protos_gerados/* && \
    mkdir -p protos_gerados && \
    protoc -I=../contratos_grpc --cpp_out=protos_gerados --grpc_out=protos_gerados --plugin=protoc-gen-grpc=$(which grpc_cpp_plugin) ../contratos_grpc/autenticacao.proto && \
    protoc -I=../contratos_grpc --cpp_out=protos_gerados --grpc_out=protos_gerados --plugin=protoc-gen-grpc=$(which grpc_cpp_plugin) ../contratos_grpc/frota.proto

RUN rm -rf build && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make

EXPOSE 8080

CMD ["./build/gateway_server"]