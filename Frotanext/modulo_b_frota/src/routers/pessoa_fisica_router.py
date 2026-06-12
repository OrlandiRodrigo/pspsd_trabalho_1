from typing import Annotated, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models
from ..dependencies import (
    obter_sessao_banco,
    obter_funcionario_atual,
    obter_cliente_atual,
)
from ..models.enums import StatusContaEnum
from ..schemas import cliente_schema
from ..services import cliente_service

router = APIRouter(
    prefix="/clientes/pessoas-fisicas", tags=["Clientes - Pessoa Física"]
)


@router.post(
    "/",
    response_model=cliente_schema.SchemaPessoaFisica,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo cliente Pessoa Física (Auto-cadastro)",
)
def rota_criar_pessoa_fisica(
    dados_entrada_cliente: cliente_schema.SchemaPessoaFisicaCriar,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
):
    cliente_criado = cliente_service.criar_pessoa_fisica(
        dados_entrada_cliente=dados_entrada_cliente, sessao_banco=sessao_banco
    )
    return cliente_criado


@router.get(
    "/",
    response_model=List[cliente_schema.SchemaPessoaFisica],
    summary="Lista todas as Pessoas Físicas (Requer Funcionário)",
)
def rota_listar_pessoas_fisicas(
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    _funcionario_logado: Annotated[
        models.Funcionario, Depends(obter_funcionario_atual)
    ],
):
    lista_clientes = cliente_service.listar_pessoas_fisicas(sessao_banco=sessao_banco)
    return lista_clientes


@router.get(
    "/me",
    response_model=cliente_schema.SchemaPessoaFisica,
    summary="Dados do cliente logado (Meu Perfil)",
)
def rota_ler_meus_dados_pf(
    cliente_logado: Annotated[models.Pessoa, Depends(obter_cliente_atual)],
):
    if not isinstance(cliente_logado, models.PessoaFisica):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Este token não pertence a uma Pessoa Física.",
        )
    return cliente_logado


@router.put(
    "/me",
    response_model=cliente_schema.SchemaPessoaFisica,
    summary="Atualiza os próprios dados (Cliente Logado)",
)
def rota_atualizar_meus_dados_pf(
    dados_atualizacao: cliente_schema.SchemaPessoaFisicaUpdate,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    cliente_logado: Annotated[models.Pessoa, Depends(obter_cliente_atual)],
):
    if not isinstance(cliente_logado, models.PessoaFisica):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Este token não pertence a uma Pessoa Física.",
        )

    return cliente_service.atualizar_pessoa_fisica(
        id_pessoa=cliente_logado.id_pessoa,
        dados_atualizacao=dados_atualizacao,
        sessao_banco=sessao_banco,
    )


@router.get(
    "/{id_pessoa}",
    response_model=cliente_schema.SchemaPessoaFisica,
    summary="Busca Pessoa Física por ID (Requer Funcionário)",
)
def rota_buscar_pessoa_fisica_por_id(
    id_pessoa: int,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    _funcionario_logado: Annotated[
        models.Funcionario, Depends(obter_funcionario_atual)
    ],
):
    cliente = cliente_service.buscar_pessoa_fisica_por_id(
        id_pessoa=id_pessoa, sessao_banco=sessao_banco
    )
    return cliente


@router.put(
    "/{id_pessoa}",
    response_model=cliente_schema.SchemaPessoaFisica,
    summary="Atualiza Pessoa Física por ID (Requer Funcionário)",
)
def rota_atualizar_pessoa_fisica(
    id_pessoa: int,
    dados_atualizacao: cliente_schema.SchemaPessoaFisicaCriar,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    _funcionario_logado: Annotated[
        models.Funcionario, Depends(obter_funcionario_atual)
    ],
):
    cliente_atualizado = cliente_service.atualizar_pessoa_fisica(
        id_pessoa=id_pessoa,
        dados_atualizacao=dados_atualizacao,
        sessao_banco=sessao_banco,
    )
    return cliente_atualizado


@router.delete(
    "/{id_pessoa}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta Pessoa Física por ID (Requer Funcionário)",
)
def rota_deletar_pessoa_fisica(
    id_pessoa: int,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    _funcionario_logado: Annotated[
        models.Funcionario, Depends(obter_funcionario_atual)
    ],
):
    cliente_service.deletar_pessoa_fisica(
        id_pessoa=id_pessoa, sessao_banco=sessao_banco
    )


@router.patch(
    "/{id_pessoa}/status",
    response_model=cliente_schema.SchemaPessoaFisica,
    summary="Altera status do cliente (Bloquear/Desbloquear) - Requer Admin",
)
def rota_alterar_status_cliente_pf(
    id_pessoa: int,
    novo_status: Annotated[StatusContaEnum, Body(embed=True)],
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    _funcionario_logado: Annotated[
        models.Funcionario, Depends(obter_funcionario_atual)
    ],
):
    cliente_atualizado = cliente_service.alterar_status_pessoa_fisica(
        id_pessoa=id_pessoa, novo_status=novo_status, sessao_banco=sessao_banco
    )
    return cliente_atualizado
