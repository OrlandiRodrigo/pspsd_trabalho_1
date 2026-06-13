from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from .routers import (
    auth_router,
    cliente_auth_router,
    pessoa_fisica_router,
    pessoa_juridica_router,
    empresa_router,
)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("Iniciando Auth Service...")

    yield

    print("Desligando Auth Service...")


app = FastAPI(
    title="FrotaNext Auth Service",
    description="API dedicada para autenticação e gestão de usuários da FrotaNext.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(auth_router.router)
app.include_router(cliente_auth_router.router)
app.include_router(pessoa_fisica_router.router)
app.include_router(pessoa_juridica_router.router)
app.include_router(empresa_router.router)

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
    return {"message": "FrotaNext Auth Service Online"}
