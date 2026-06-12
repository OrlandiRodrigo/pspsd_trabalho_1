from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import models
from . import seguranca as seguranca_service
from .database import SessionLocal


def obter_sessao_banco() -> Session:
    sessao_banco: Session | None = None
    try:
        sessao_banco = SessionLocal()
        yield sessao_banco
    finally:
        if sessao_banco is not None:
            sessao_banco.close()


oauth2_scheme_funcionario = OAuth2PasswordBearer(tokenUrl="auth/token")

oauth2_scheme_cliente = OAuth2PasswordBearer(tokenUrl="clientes/token")


def obter_cliente_atual(
    token: Annotated[str, Depends(oauth2_scheme_cliente)],
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
) -> models.Pessoa:
    credenciais_excecao = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais do cliente.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = seguranca_service.verificar_token(token)
    if payload is None:
        raise credenciais_excecao

    cliente_id_str = payload.get("sub")
    if cliente_id_str is None:
        raise credenciais_excecao

    try:
        id_pessoa = int(cliente_id_str)
    except ValueError as exc:
        raise credenciais_excecao from exc

    cliente_encontrado = sessao_banco.get(models.Pessoa, id_pessoa)

    if cliente_encontrado is None:
        raise credenciais_excecao

    return cliente_encontrado
