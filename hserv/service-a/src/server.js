console.log("Iniciando Service A...");

const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

// Aqui dizendo quais funções tem esse serviço e qual o formato de dados utilizado
// Se você mudar estrutura de dados → mexe no .proto
const PROTO_PATH = path.join(__dirname, '../proto/service-a.proto');

console.log("Carregando proto em:", PROTO_PATH);

const packageDef = protoLoader.loadSync(PROTO_PATH);
const grpcObject = grpc.loadPackageDefinition(packageDef);
const serviceA = grpcObject.servicea;

// Esse é o coração do serviço
function ProcessA(call, callback) {
    console.log("Request recebida:", call.request); //Entrada

    callback(null, {
        status: "OK",
        result: `Processado por A: ${call.request.payload}` //Saída
    });
}

const server = new grpc.Server();

server.addService(serviceA.ServiceA.service, {
    ProcessA
});

const PORT = "0.0.0.0:50051";

server.bindAsync(
    PORT,
    grpc.ServerCredentials.createInsecure(),
    () => {
        console.log("Service A rodando na porta 50051");
        server.start();
    }
);