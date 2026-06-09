const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

const PROTO_PATH = path.join(__dirname, '../../proto/service-b.proto');

const packageDef = protoLoader.loadSync(PROTO_PATH);
const grpcObject = grpc.loadPackageDefinition(packageDef);
const serviceB = grpcObject.serviceb;

const clientB = new serviceB.ServiceB(
    "service-b:50052",
    grpc.credentials.createInsecure()
);

function callServiceB(data) {
    return new Promise((resolve, reject) => {
        clientB.ProcessB({ userId: "1", data }, (err, res) => {
            if (err) reject(err);
            else resolve(res);
        });
    });
}

module.exports = { callServiceB };