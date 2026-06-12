import time
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from sqlalchemy.exc import OperationalError, ProgrammingError

from .database import Base, engine

from .routers import (
    empresa_router,
    pessoa_fisica_router,
    pessoa_juridica_router,
    reserva_router,
    veiculo_router,
)


def criar_banco_de_dados_e_tablelas_com_tentaivas():
    MAX_RETRIES = 5
    RETRY_DELAY_SECONDS = 3
    retries = 0
    while retries < MAX_RETRIES:
        try:
            print(
                f"Tentando conectar ao banco de dados (tentativa {retries + 1}/{MAX_RETRIES})..."
            )

            Base.metadata.create_all(bind=engine)

            print("Tabelas verificadas/criadas com sucesso.")
            break

        except OperationalError as e:
            print(
                f"Banco indisponível: {e}. Tentando novamente em {RETRY_DELAY_SECONDS}s..."
            )
            retries += 1
            time.sleep(RETRY_DELAY_SECONDS)

        except ProgrammingError as e:
            print(f"Aviso de criação de tabela (provavelmente já existem): {e}")
            break

        except Exception as e: # pylint: disable=broad-exception-caught
            print(f"Erro inesperado ao criar tabelas: {e}")
            break

    if retries == MAX_RETRIES:
        print(
            "ERRO CRÍTICO: Não foi possível conectar ao banco após várias tentativas."
        )


@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("Iniciando FrotaNext Backend...")
    criar_banco_de_dados_e_tablelas_com_tentaivas()
    yield
    print("Desligando aplicação...")


app = FastAPI(
    title="API da Locadora FrotaNext Main",
    description="API principal para gerenciamento de veículos, reservas e clientes.",
    version="0.2.0",
    lifespan=lifespan,
)

app.include_router(empresa_router.router)
app.include_router(pessoa_fisica_router.router)
app.include_router(pessoa_juridica_router.router)
app.include_router(veiculo_router.router)
app.include_router(reserva_router.router)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API Principal da FrotaNext!"}
