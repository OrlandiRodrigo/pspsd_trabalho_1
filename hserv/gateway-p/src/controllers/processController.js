const { callServiceA } = require('../grpc/client-a');
const { callServiceB } = require('../grpc/client-b');

async function processData(req, res) {
    try {
        const input = req.body.data;

        const [resultA, resultB] = await Promise.all([
            callServiceA(input),
            callServiceB(input)
        ]);

        res.json({
            gateway: "P",
            serviceA: resultA,
            serviceB: resultB
        });

    } catch (err) {
        res.status(500).json({
            error: err.message
        });
    }
}

module.exports = { processData };