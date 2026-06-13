cmake_minimum_required(VERSION 3.15)
project(FrotaNextGateway CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Protobuf REQUIRED)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/dependencias)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/protos_gerados)

set(FONTES_PROTO
    protos_gerados/autenticacao.pb.cc
    protos_gerados/autenticacao.grpc.pb.cc
    protos_gerados/frota.pb.cc
    protos_gerados/frota.grpc.pb.cc
)

add_executable(gateway_server src/main.cpp ${FONTES_PROTO})

target_link_libraries(gateway_server
    grpc++
    grpc
    ${PROTOBUF_LIBRARIES}
    pthread
)