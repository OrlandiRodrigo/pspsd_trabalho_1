from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import  OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models
from .. import seguranca as seguranca_service
from ..dependencies import oauth2_scheme_funcionario, obter_sessao_banco
from ..schemas import auth_schema
from ..services import auth_service

router = APIRouter(prefix="/auth", tags=["Autenticação e Funcionários"])


@router.post("/token", response_model=auth_schema.SchemaToken)
def rota_login_para_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
):
    """
    Endpoint de login. Recebe um formulário com 'username' (nosso email)
    e 'password'. Retorna um token de acesso.
    """
    funcionario_autenticado = auth_service.autenticar_funcionario(
        sessao_banco=sessao_banco,
        email_formulario=form_data.username,
        senha_formulario=form_data.password,
    )

    if not funcionario_autenticado:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    dados_token = {"sub": funcionario_autenticado.email}

    token_acesso = seguranca_service.criar_token_acesso(dados=dados_token)

    return {"access_token": token_acesso, "token_type": "bearer"}


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
    """
    Dependência que exige que o usuário logado seja um admin.
    """
    if not funcionario_atual.e_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Requer privilégios de administrador.",
        )
    return funcionario_atual


@router.get("/funcionarios/eu", response_model=auth_schema.SchemaFuncionario)
def rota_ler_funcionario_logado(
    funcionario_atual: Annotated[models.Funcionario, Depends(obter_funcionario_atual)],
):
    return funcionario_atual


@router.post(
    "/funcionarios",
    response_model=auth_schema.SchemaFuncionario,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo funcionário (Requer Admin)",
)
def rota_criar_funcionario(
    dados_funcionario: auth_schema.SchemaFuncionarioCriar,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    _admin_logado: Annotated[models.Funcionario, Depends(obter_admin_atual)],
):
    return auth_service.criar_funcionario(
        sessao_banco=sessao_banco, dados_funcionario=dados_funcionario
    )
