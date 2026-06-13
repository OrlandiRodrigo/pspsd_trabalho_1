from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.services import auth_service

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

    if not cliente_encontrado.e_ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sua conta está bloqueada ou suspensa.",
        )

    return cliente_encontrado


def obter_funcionario_atual(
    token: Annotated[str, Depends(oauth2_scheme_funcionario)],
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
) -> models.Funcionario:
    credenciais_excecao = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = seguranca_service.verificar_token(token)
    if payload is None:
        raise credenciais_excecao

    email: str = payload.get("sub")
    if email is None:
        raise credenciais_excecao

    funcionario = auth_service.buscar_funcionario_por_email(sessao_banco, email=email)
    if funcionario is None:
        raise credenciais_excecao

    if not funcionario.e_ativado:
        raise HTTPException(status_code=403, detail="Funcionário inativo.")

    return funcionario


def obter_admin_atual(
    funcionario_atual: Annotated[models.Funcionario, Depends(obter_funcionario_atual)],
) -> models.Funcionario:
    if not funcionario_atual.e_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Requer privilégios de administrador.",
        )
    return funcionario_atual
