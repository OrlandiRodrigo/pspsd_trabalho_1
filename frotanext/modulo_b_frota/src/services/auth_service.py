from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .. import models
from .. import seguranca as seguranca_service
from ..schemas import auth_schema


def buscar_funcionario_por_email(
    sessao_banco: Session, email: str
) -> Optional[models.Funcionario]:
    return (
        sessao_banco.query(models.Funcionario)
        .filter(models.Funcionario.email == email)
        .first()
    )


def autenticar_funcionario(
    sessao_banco: Session, email_formulario: str, senha_formulario: str
) -> Optional[models.Funcionario]:
    funcionario_encontrado = buscar_funcionario_por_email(
        sessao_banco, email=email_formulario
    )

    if not funcionario_encontrado:
        return None

    if not funcionario_encontrado.e_ativado:
        return None

    if not seguranca_service.verificar_senha(
        senha_texto_puro=senha_formulario, senha_hashada=funcionario_encontrado.senha
    ):
        return None

    return funcionario_encontrado


def criar_funcionario(
    sessao_banco: Session, dados_funcionario: auth_schema.SchemaFuncionarioCriar
) -> models.Funcionario:
    funcionario_existente = buscar_funcionario_por_email(
        sessao_banco, email=dados_funcionario.email
    )
    if funcionario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um funcionário cadastrado com este email.",
        )

    hash_senha = seguranca_service.obter_hash_senha(dados_funcionario.senha_texto_puro)

    novo_funcionario_modelo = models.Funcionario(
        email=dados_funcionario.email,
        nome_completo=dados_funcionario.nome_completo,
        senha=hash_senha,
        e_admin=dados_funcionario.e_admin,
        e_ativado=dados_funcionario.e_ativado,
    )

    sessao_banco.add(novo_funcionario_modelo)
    sessao_banco.commit()
    sessao_banco.refresh(novo_funcionario_modelo)

    return novo_funcionario_modelo


def autenticar_cliente(
    sessao_banco: Session, email_formulario: str, senha_formulario: str
) -> Optional[models.Pessoa]:
    cliente_encontrado = (
        sessao_banco.query(models.Pessoa)
        .filter(models.Pessoa.email == email_formulario)
        .first()
    )

    if not cliente_encontrado:
        return None

    if not cliente_encontrado.e_ativo:
        return None

    if not seguranca_service.verificar_senha(
        senha_texto_puro=senha_formulario, senha_hashada=cliente_encontrado.senha
    ):
        return None

    return cliente_encontrado
