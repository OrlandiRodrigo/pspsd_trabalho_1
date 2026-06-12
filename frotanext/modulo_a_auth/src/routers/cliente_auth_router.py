from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import  OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import seguranca as seguranca_service
from ..dependencies import  obter_sessao_banco
from ..schemas import auth_schema
from ..services import cliente_auth_service

router = APIRouter(prefix="/clientes", tags=["Autenticação - Clientes"])


@router.post("/token", response_model=auth_schema.SchemaToken)
def rota_login_cliente_para_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
):
    cliente_autenticado = cliente_auth_service.autenticar_cliente(
        sessao_banco=sessao_banco,
        email_formulario=form_data.username,
        senha_formulario=form_data.password,
    )

    if not cliente_autenticado:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha de cliente incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    dados_token = {
        "sub": str(cliente_autenticado.id_pessoa),
        "email": cliente_autenticado.email,
        "tipo": cliente_autenticado.tipo_pessoa,
    }

    token_acesso = seguranca_service.criar_token_acesso(dados=dados_token)

    return {"access_token": token_acesso, "token_type": "bearer"}
