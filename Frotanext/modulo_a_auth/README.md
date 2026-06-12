# 🔐 FrotaNext - Auth Service (Identidade)

Este é o repositório do **Serviço de Autenticação** do projeto [FrotaNext](https://gg555-13.github.io/FrotaNext-Docs/). 
Ele é um microsserviço isolado responsável pela segurança, gestão de senhas e emissão de tokens JWT.

## 🛠️ Tecnologias
* **Python 3.11** + **FastAPI**
* **Argon2 / Passlib** (Hashing seguro de senhas)
* **PyJWT** (Geração e validação de tokens)
* **SQLAlchemy** (Acesso apenas à tabela de Usuários)

## 📌 Responsabilidades
* Login de Administradores, PF e PJ.
* Criação de novos acessos (hash de senhas).
* Validação de credenciais.

## ⚙️ Como Rodar Localmente
Para o projeto completo, veja o [Repositório de Documentação](https://github.com/GG555-13/FrotaNext-Docs). Para rodar isolado na porta 8001:

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8001