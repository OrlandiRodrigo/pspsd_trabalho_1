console.log("Iniciando Service B...");

const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

// Aqui dizendo quais funções tem esse serviço e qual o formato de dados utilizado
// Se você mudar estrutura de dados → mexe no .proto
const PROTO_PATH = path.join(__dirname, '../proto/service-b.proto');

console.log("Carregando proto em:", PROTO_PATH);

const packageDef = protoLoader.loadSync(PROTO_PATH);
const grpcObject = grpc.loadPackageDefinition(packageDef);
const serviceB = grpcObject.serviceb;

// Esse é o coração do serviço
function ProcessB(call, callback) {
    console.log("Request recebida no B:", call.request);   //Entrada

    callback(null, {
        status: "OK",
        output: `Processado por B: ${call.request.data}`  //Saída
    });
}

const server = new grpc.Server();

server.addService(serviceB.ServiceB.service, {
    ProcessB
});

server.bindAsync(
    "0.0.0.0:50052",
    grpc.ServerCredentials.createInsecure(),
    () => {
        console.log("Service B rodando na porta 50052");
    }
);