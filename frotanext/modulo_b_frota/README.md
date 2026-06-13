# ⚙️ FrotaNext - Backend Core (FastAPI)

Este é o repositório do **Backend Principal** do projeto [FrotaNext](https://gg555-13.github.io/FrotaNext-Docs/). 
Ele é um microsserviço focado exclusivamente nas regras de negócio: Gestão de Frota, Clientes, Operações de Pátio e Reservas.

## 🛠️ Tecnologias
* **Python 3.11**
* **FastAPI** (Framework assíncrono)
* **SQLAlchemy** (ORM) + Alembic (Migrações)
* **PostgreSQL**
* **Pytest** (Testes Automatizados)

## 📌 Arquitetura
Este serviço **não** lida com senhas ou geração de Tokens JWT. Toda requisição que exige autenticação passa por validação de token, mas a emissão do token é feita pelo [Auth Service](https://github.com/GG555-13/FrotaNext-Auth).

## ⚙️ Como Rodar Localmente
Para subir o ecossistema completo, utilize o [Repositório de Documentação](https://github.com/GG555-13/FrotaNext-Docs). Para testes locais isolados:

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000