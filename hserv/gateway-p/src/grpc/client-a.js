const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

const PROTO_PATH = path.join(__dirname, '../../proto/service-a.proto');

const packageDef = protoLoader.loadSync(PROTO_PATH);
const grpcObject = grpc.loadPackageDefinition(packageDef);
const serviceA = grpcObject.servicea;

const clientA = new serviceA.ServiceA(
    "service-a:50051",
    grpc.credentials.createInsecure()
);

function callServiceA(data) {
    return new Promise((resolve, reject) => {
        clientA.ProcessA({ userId: "1", payload: data }, (err, res) => {
            if (err) reject(err);
            else resolve(res);
        });
    });
}

module.exports = { callServiceA };