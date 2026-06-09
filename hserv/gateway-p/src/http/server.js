const express = require('express');
const app = express();

app.use(express.json());

const { processData } = require('../controllers/processController');

app.get('/status', (req, res) => {
    res.json({ status: "Gateway P ativo" });
});

app.post('/process', processData);

const PORT = 3000;

app.listen(PORT, () => {
    console.log(`Gateway P rodando na porta ${PORT}`);
});