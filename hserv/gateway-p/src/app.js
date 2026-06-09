require('./http/server');

// Aqui entra a medição de tempo dos serviços 
const start = Date.now();

const resultA = await callServiceA(data);
const resultB = await callServiceB(data);

const end = Date.now();

return res.json({
  gateway: "P",
  serviceA: resultA,
  serviceB: resultB,
  tempo_ms: end - start
});