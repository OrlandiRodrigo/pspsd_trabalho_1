# 🧩 Trabalho 1 — Sistema Distribuído com Microserviços

Este projeto implementa uma aplicação distribuída baseada em **microserviços**, utilizando **Node.js**, **gRPC**, **Docker**, **WSL2** e **Kubernetes (Minikube)**.

---

# 🧠 Visão Geral da Arquitetura

O sistema é composto por três camadas principais:


HClient (Interface HTTP)
↓
Gateway P (API Gateway - Node.js)
↓ gRPC
Service A Service B
(50051) (50052)


---

# 🧱 Componentes do Sistema

## 🟦 HClient
- Interface de consumo da aplicação
- Comunicação via HTTP tradicional
- Pode ser desktop/web client
- Envia requisições para o Gateway P

---

## 🟨 Gateway P (API Gateway)

Tecnologia:
- Node.js + Express
- gRPC Client (A e B)

Responsabilidades:
- Expõe API HTTP (`/process`)
- Recebe requisições do HClient
- Orquestra chamadas gRPC para serviços internos
- Agrega respostas de Service A e B

Porta:
- HTTP: `3000`

---

## 🟩 Service A

Tecnologia:
- Node.js
- gRPC Server

Porta:
- `50051`

Responsabilidade:
- Processamento de dados do tipo A
- Retorna resposta via gRPC

---

## 🟩 Service B

Tecnologia:
- Node.js
- gRPC Server

Porta:
- `50052`

Responsabilidade:
- Processamento de dados do tipo B
- Retorna resposta via gRPC

---

# 🔗 Comunicação entre Serviços

## Fluxo principal:

HClient → HTTP → Gateway P → gRPC → Service A
↓
Service B

Protocolos utilizados:
HTTP/REST → comunicação externa (HClient → Gateway P)
gRPC (HTTP/2) → comunicação interna entre serviços
⚙️ Tecnologias Utilizadas
Node.js
Express
gRPC (@grpc/grpc-js)
Protocol Buffers (.proto)
Docker (base futura de containerização)
Kubernetes (Minikube)
WSL2 (ambiente Linux no Windows)

### 📦 Estrutura do Projeto
```
trabalho1/
│
├── hserv/
│   ├── service-a/
│   ├── service-b/
│   └── gateway-p/
│
└── shared/
    └── k8s/
        ├── service-a/
        │   ├── deployment.yaml
        │   └── service.yaml
        │
        ├── service-b/
        │   ├── deployment.yaml
        │   └── service.yaml
        │
        ├── gateway/
        │   ├── deployment.yaml
        │   └── service.yaml
        │
        └── namespace.yaml (opcional)
```

🚀 Como Executar o Projeto

(Após dar NPM Install nas três estruturas)

1. Iniciar Service A
```
cd hserv/service-a
npm start
```
3. Iniciar Service B
```
cd hserv/service-b
npm start
```
5. Iniciar Gateway P
```
cd hserv/gateway-p
node src/app.js
```
7. Testar API
Comando: 
```
$response = Invoke-RestMethod -Method POST `
  -Uri "http://localhost:3000/process" `
  -ContentType "application/json" `
  -Body '{"data":"teste distribuído"}'

$response | ConvertTo-Json -Depth 5
```
Endpoint:

```
POST http://localhost:3000/process
Body:
{
  "data": "teste distribuído"
}
🧪 Resultado Esperado
{
  "gateway": "P",
  "serviceA": {
    "status": "OK",
    "result": "Processado por A: teste distribuído"
  },
  "serviceB": {
    "status": "OK",
    "output": "Processado por B: teste distribuído"
  }
}
```
☁️ Infraestrutura e DevOps
Ambiente configurado:
Windows 10
WSL2 (Ubuntu)
Docker Desktop
Minikube (driver Docker)
kubectl
Cluster Kubernetes:
cluster local via Minikube
pronto para deploy dos microserviços
📌 Objetivos Acadêmicos Atendidos

✔ Arquitetura de microserviços
✔ Comunicação entre serviços via gRPC
✔ API Gateway
✔ Uso de containers (base para Docker/Kubernetes)
✔ Ambiente cloud-native local
✔ Separação de responsabilidades
✔ Sistema distribuído funcional

🔜 Próximos Passos
Containerizar serviços com Docker
Criar Deployments no Kubernetes
Criar Services (ClusterIP / NodePort)
Criar HClient funcional
Implementar Ingress Controller
Automatizar deploy com scripts
