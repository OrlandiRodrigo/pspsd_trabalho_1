from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from .. import models
from ..dependencies import obter_funcionario_atual, obter_sessao_banco
from ..models.enums import TipoVeiculoEnum
from ..schemas import veiculo_schema
from ..services import veiculo_service

router = APIRouter(prefix="/veiculos", tags=["Veículos"])


@router.post(
    "/passeio",
    response_model=veiculo_schema.SchemaPasseio,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo veículo Passeio (Requer Funcionário)",
)
def rota_criar_veiculo_passeio(
    dados_entrada_veiculo: veiculo_schema.SchemaPasseioCriar,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    _funcionario_logado: Annotated[
        models.Funcionario, Depends(obter_funcionario_atual)
    ],
):
    veiculo_criado = veiculo_service.criar_veiculo_passeio(
        dados_entrada_veiculo=dados_entrada_veiculo, sessao_banco=sessao_banco
    )
    return veiculo_criado


@router.post(
    "/utilitario",
    response_model=veiculo_schema.SchemaUtilitario,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo veículo Utilitário (Requer Funcionário)",
)
def rota_criar_veiculo_utilitario(
    dados_entrada_veiculo: veiculo_schema.SchemaUtilitarioCriar,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    _funcionario_logado: Annotated[
        models.Funcionario, Depends(obter_funcionario_atual)
    ],
):
    veiculo_criado = veiculo_service.criar_veiculo_utilitario(
        dados_entrada_veiculo=dados_entrada_veiculo, sessao_banco=sessao_banco
    )
    return veiculo_criado


@router.post(
    "/motocicleta",
    response_model=veiculo_schema.SchemaMotocicleta,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra uma nova Motocicleta (Requer Funcionário)",
)
def rota_criar_veiculo_motocicleta(
    dados_entrada_veiculo: veiculo_schema.SchemaMotocicletaCriar,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    _funcionario_logado: Annotated[
        models.Funcionario, Depends(obter_funcionario_atual)
    ],
):
    veiculo_criado = veiculo_service.criar_veiculo_motocicleta(
        dados_entrada_veiculo=dados_entrada_veiculo, sessao_banco=sessao_banco
    )
    return veiculo_criado


@router.get(
    "/",
    response_model=List[veiculo_schema.SchemaVeiculo],
    summary="Lista veículos com filtros (Aberto para Clientes)",
)
def rota_listar_veiculos(
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    categoria: Annotated[
        Optional[TipoVeiculoEnum], Query(description="Filtrar por tipo de veículo")
    ] = None,
    apenas_disponiveis: Annotated[
        bool, Query(description="Listar apenas veículos disponíveis para aluguel")
    ] = True,
    termo_busca: Annotated[
        Optional[str], Query(description="Buscar por modelo ou marca")
    ] = None,
):
    lista_veiculos = veiculo_service.listar_veiculos(
        sessao_banco=sessao_banco,
        categoria=categoria,
        apenas_disponiveis=apenas_disponiveis,
        termo_busca=termo_busca,
    )
    return lista_veiculos


@router.get(
    "/{id_veiculo}",
    response_model=veiculo_schema.SchemaVeiculo,
    summary="Busca veículo por ID (Aberto para Clientes)",
)
def rota_buscar_veiculo_por_id(
    id_veiculo: int,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
):
    veiculo = veiculo_service.buscar_veiculo_por_id(
        id_veiculo=id_veiculo, sessao_banco=sessao_banco
    )
    return veiculo


@router.put(
    "/passeio/{id_veiculo}",
    response_model=veiculo_schema.SchemaPasseio,
    summary="Atualiza um veículo de Passeio por ID (Requer Funcionário)",
)
def rota_atualizar_veiculo_passeio(
    id_veiculo: int,
    dados_atualizacao: veiculo_schema.SchemaPasseioUpdate,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    _funcionario_logado: Annotated[
        models.Funcionario, Depends(obter_funcionario_atual)
    ],
):
    return veiculo_service.atualizar_veiculo_passeio(
        id_veiculo=id_veiculo,
        dados_atualizacao=dados_atualizacao,
        sessao_banco=sessao_banco,
    )


@router.put(
    "/utilitario/{id_veiculo}",
    response_model=veiculo_schema.SchemaUtilitario,
    summary="Atualiza um veículo Utilitário por ID (Requer Funcionário)",
)
def rota_atualizar_veiculo_utilitario(
    id_veiculo: int,
    dados_atualizacao: veiculo_schema.SchemaUtilitarioUpdate,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    _funcionario_logado: Annotated[
        models.Funcionario, Depends(obter_funcionario_atual)
    ],
):
    return veiculo_service.atualizar_veiculo_utilitario(
        id_veiculo=id_veiculo,
        dados_atualizacao=dados_atualizacao,
        sessao_banco=sessao_banco,
    )


@router.put(
    "/motocicleta/{id_veiculo}",
    response_model=veiculo_schema.SchemaMotocicleta,
    summary="Atualiza uma Motocicleta por ID (Requer Funcionário)",
)
def rota_atualizar_veiculo_motocicleta(
    id_veiculo: int,
    dados_atualizacao: veiculo_schema.SchemaMotocicletaUpdate,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    _funcionario_logado: Annotated[
        models.Funcionario, Depends(obter_funcionario_atual)
    ],
):
    return veiculo_service.atualizar_veiculo_motocicleta(
        id_veiculo=id_veiculo,
        dados_atualizacao=dados_atualizacao,
        sessao_banco=sessao_banco,
    )


@router.delete(
    "/{id_veiculo}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta veículo por ID (Requer Funcionário)",
)
def rota_deletar_veiculo(
    id_veiculo: int,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    _funcionario_logado: Annotated[
        models.Funcionario, Depends(obter_funcionario_atual)
    ],
):
    veiculo_service.deletar_veiculo(id_veiculo=id_veiculo, sessao_banco=sessao_banco)
