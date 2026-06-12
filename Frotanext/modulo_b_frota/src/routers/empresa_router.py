from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models
from ..dependencies import obter_cliente_atual, obter_sessao_banco
from ..schemas import cliente_schema
from ..services import cliente_service


def obter_pj_logada(
    cliente_logado: Annotated[models.Pessoa, Depends(obter_cliente_atual)],
) -> models.PessoaJuridica:
    if not isinstance(cliente_logado, models.PessoaJuridica):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Esta ação é permitida apenas para Pessoas Jurídicas.",
        )
    return cliente_logado


router = APIRouter(
    prefix="/minha-empresa",
    tags=["Cliente - Gestão Empresa (PJ)"],
    dependencies=[Depends(obter_pj_logada)],
)


@router.post(
    "/motoristas",
    response_model=cliente_schema.SchemaPessoaJuridica,
    summary="Adiciona um motorista à empresa logada",
)
def rota_adicionar_motorista_empresa(
    dados_associacao: cliente_schema.SchemaMotoristaAssociar,
    empresa_logada: Annotated[models.PessoaJuridica, Depends(obter_pj_logada)],
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
):
    empresa_atualizada = cliente_service.adicionar_motorista_empresa(
        empresa_logada=empresa_logada,
        cpf_motorista=dados_associacao.cpf_motorista,
        sessao_banco=sessao_banco,
    )
    return empresa_atualizada


@router.delete(
    "/motoristas/{id_motorista}",
    response_model=cliente_schema.SchemaPessoaJuridica,
    summary="Remove um motorista da empresa logada",
)
def rota_remover_motorista_empresa(
    id_motorista: int,
    empresa_logada: Annotated[models.PessoaJuridica, Depends(obter_pj_logada)],
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
):
    empresa_atualizada = cliente_service.remover_motorista_empresa(
        empresa_logada=empresa_logada,
        id_motorista_remover=id_motorista,
        sessao_banco=sessao_banco,
    )
    return empresa_atualizada
