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
    prefix="/clientes/pessoas-juridicas", tags=["Clientes - Pessoa Jurídica"]
)


@router.post(
    "/",
    response_model=cliente_schema.SchemaPessoaJuridica,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo cliente Pessoa Jurídica (Auto-cadastro)",
)
def rota_criar_pessoa_juridica(
    dados_entrada_empresa: cliente_schema.SchemaPessoaJuridicaCriar,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
):
    empresa_criada = cliente_service.criar_pessoa_juridica(
        dados_entrada_empresa=dados_entrada_empresa, sessao_banco=sessao_banco
    )
    return empresa_criada


@router.get(
    "/",
    response_model=List[cliente_schema.SchemaPessoaJuridica],
    summary="Lista todas as Pessoas Jurídicas (Requer Funcionário)",
)
def rota_listar_pessoas_juridicas(
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    _funcionario_logado: Annotated[
        models.Funcionario, Depends(obter_funcionario_atual)
    ],
):
    lista_empresas = cliente_service.listar_pessoas_juridicas(sessao_banco=sessao_banco)
    return lista_empresas


@router.get("/me", response_model=cliente_schema.SchemaPessoaJuridica)
def rota_ler_meus_dados_pj(
    cliente_logado: Annotated[models.Pessoa, Depends(obter_cliente_atual)],
):
    if not isinstance(cliente_logado, models.PessoaJuridica):
        raise HTTPException(status_code=403, detail="Token inválido.")
    return cliente_logado


@router.put("/me", response_model=cliente_schema.SchemaPessoaJuridica)
def rota_atualizar_meus_dados_pj(
    dados_atualizacao: cliente_schema.SchemaPessoaJuridicaUpdate,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    cliente_logado: Annotated[models.Pessoa, Depends(obter_cliente_atual)],
):
    if not isinstance(cliente_logado, models.PessoaJuridica):
        raise HTTPException(status_code=403, detail="Token inválido.")
    return cliente_service.atualizar_pessoa_juridica(
        id_pessoa=cliente_logado.id_pessoa,
        dados_atualizacao=dados_atualizacao,
        sessao_banco=sessao_banco,
    )


@router.get(
    "/{id_pessoa}",
    response_model=cliente_schema.SchemaPessoaJuridica,
    summary="Busca Pessoa Jurídica por ID (Requer Funcionário)",
)
def rota_buscar_pessoa_juridica_por_id(
    id_pessoa: int,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    _funcionario_logado: Annotated[
        models.Funcionario, Depends(obter_funcionario_atual)
    ],
):
    empresa = cliente_service.buscar_pessoa_juridica_por_id(
        id_pessoa=id_pessoa, sessao_banco=sessao_banco
    )
    return empresa


@router.put(
    "/{id_pessoa}",
    response_model=cliente_schema.SchemaPessoaJuridica,
    summary="Atualiza Pessoa Jurídica por ID (Requer Funcionário)",
)
def rota_atualizar_pessoa_juridica(
    id_pessoa: int,
    dados_atualizacao: cliente_schema.SchemaPessoaJuridicaCriar,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    _funcionario_logado: Annotated[
        models.Funcionario, Depends(obter_funcionario_atual)
    ],
):
    empresa_atualizada = cliente_service.atualizar_pessoa_juridica(
        id_pessoa=id_pessoa,
        dados_atualizacao=dados_atualizacao,
        sessao_banco=sessao_banco,
    )
    return empresa_atualizada


@router.delete(
    "/{id_pessoa}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta Pessoa Jurídica por ID (Requer Funcionário)",
)
def rota_deletar_pessoa_juridica(
    id_pessoa: int,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    _funcionario_logado: Annotated[
        models.Funcionario, Depends(obter_funcionario_atual)
    ],
):
    cliente_service.deletar_pessoa_juridica(
        id_pessoa=id_pessoa, sessao_banco=sessao_banco
    )


@router.patch(
    "/{id_pessoa}/status",
    response_model=cliente_schema.SchemaPessoaJuridica,
    summary="Altera status do cliente (Bloquear/Desbloquear) - Requer Admin",
)
def rota_alterar_status_cliente_pj(
    id_pessoa: int,
    novo_status: Annotated[StatusContaEnum, Body(embed=True)],
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    _funcionario_logado: Annotated[
        models.Funcionario, Depends(obter_funcionario_atual)
    ],
):
    cliente_atualizado = cliente_service.alterar_status_pessoa_juridica(
        id_pessoa=id_pessoa, novo_status=novo_status, sessao_banco=sessao_banco
    )
    return cliente_atualizado
