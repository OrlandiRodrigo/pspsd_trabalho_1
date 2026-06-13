from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import models
from ..dependencies import (
    obter_cliente_atual,
    obter_funcionario_atual,
    obter_sessao_banco,
)
from ..schemas import reserva_schema
from ..services import reserva_service

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.post(
    "/simulacao",
    response_model=reserva_schema.SchemaReservaSimulacaoResultado,
    summary="Simula o valor total de uma reserva antes da confirmação",
)
def rota_simular_preco_reserva(
    dados_simulacao: reserva_schema.SchemaReservaSimulacao,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
):
    """
    Retorna o valor estimado das diárias + seguros baseados nas datas e veículo escolhido.
    Não salva nada no banco.
    """
    resultado = reserva_service.simular_valor_reserva(
        dados_simulacao=dados_simulacao, sessao_banco=sessao_banco
    )
    return resultado


@router.post(
    "/",
    response_model=reserva_schema.SchemaReserva,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova reserva (Requer Login de Cliente)",
)
def rota_criar_reserva(
    dados_entrada_reserva: reserva_schema.SchemaReservaCriar,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    cliente_logado: Annotated[models.Pessoa, Depends(obter_cliente_atual)],
):
    reserva_criada = reserva_service.criar_reserva(
        dados_entrada_reserva=dados_entrada_reserva,
        cliente_logado=cliente_logado,
        sessao_banco=sessao_banco,
    )
    return reserva_criada


@router.get(
    "/minhas",
    response_model=List[reserva_schema.SchemaReserva],
    summary="Lista as reservas do cliente logado",
)
def rota_listar_minhas_reservas(
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    cliente_logado: Annotated[models.Pessoa, Depends(obter_cliente_atual)],
):
    lista_reservas = reserva_service.listar_reservas_por_cliente(
        cliente_logado=cliente_logado, sessao_banco=sessao_banco
    )
    return lista_reservas


@router.get(
    "/minhas/{id_reserva}",
    response_model=reserva_schema.SchemaReserva,
    summary="Detalhes de uma reserva específica do cliente logado",
)
def rota_buscar_minha_reserva_detalhes(
    id_reserva: int,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    cliente_logado: Annotated[models.Pessoa, Depends(obter_cliente_atual)],
):
    reserva = reserva_service.buscar_reserva_por_id_e_cliente(
        id_reserva=id_reserva,
        id_cliente=cliente_logado.id_pessoa,
        sessao_banco=sessao_banco,
    )
    return reserva


@router.put(
    "/{id_reserva}/cancelar",
    response_model=reserva_schema.SchemaReserva,
    summary="Cancela uma reserva (Requer Login de Cliente)",
)
def rota_cancelar_reserva(
    id_reserva: int,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    cliente_logado: Annotated[models.Pessoa, Depends(obter_cliente_atual)],
):
    reserva_para_cancelar = reserva_service.buscar_reserva_por_id(
        id_reserva, sessao_banco
    )
    if reserva_para_cancelar.cliente_id != cliente_logado.id_pessoa:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para cancelar esta reserva.",
        )
    reserva_cancelada = reserva_service.cancelar_reserva(
        id_reserva=id_reserva, sessao_banco=sessao_banco
    )
    return reserva_cancelada


@router.put(
    "/{id_reserva}",
    response_model=reserva_schema.SchemaReserva,
    summary="Modifica dados de uma reserva (Requer Login de Cliente)",
)
def rota_modificar_reserva(
    id_reserva: int,
    dados_atualizacao: reserva_schema.SchemaReservaUpdate,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    cliente_logado: Annotated[models.Pessoa, Depends(obter_cliente_atual)],
):
    reserva_para_modificar = reserva_service.buscar_reserva_por_id(
        id_reserva, sessao_banco
    )
    if reserva_para_modificar.cliente_id != cliente_logado.id_pessoa:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para modificar esta reserva.",
        )
    reserva_modificada = reserva_service.modificar_reserva(
        id_reserva=id_reserva,
        dados_atualizacao=dados_atualizacao,
        sessao_banco=sessao_banco,
    )
    return reserva_modificada


@router.get(
    "/",
    response_model=List[reserva_schema.SchemaReserva],
    summary="Lista todas as reservas (Painel Admin)",
)
def rota_listar_reservas(
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    _funcionario_logado: Annotated[
        models.Funcionario, Depends(obter_funcionario_atual)
    ],
    filtro_status: Annotated[str | None, Query(alias="status")] = None,
):
    lista_reservas = reserva_service.listar_reservas(
        sessao_banco=sessao_banco, filtro_status=filtro_status
    )
    return lista_reservas


@router.get(
    "/{id_reserva}",
    response_model=reserva_schema.SchemaReserva,
    summary="Busca uma reserva pelo ID (Requer Login de Funcionário)",
)
def rota_buscar_reserva_por_id(
    id_reserva: int,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    _funcionario_logado: Annotated[
        models.Funcionario, Depends(obter_funcionario_atual)
    ],
):
    reserva = reserva_service.buscar_reserva_por_id(
        id_reserva=id_reserva, sessao_banco=sessao_banco
    )
    return reserva


@router.put(
    "/{id_reserva}/finalizar",
    response_model=reserva_schema.SchemaReserva,
    summary="Finaliza uma locação (Requer Login de Funcionário)",
)
def rota_finalizar_reserva(
    id_reserva: int,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    _funcionario_logado: Annotated[
        models.Funcionario, Depends(obter_funcionario_atual)
    ],
):
    reserva_finalizada = reserva_service.finalizar_reserva(
        id_reserva=id_reserva, sessao_banco=sessao_banco
    )
    return reserva_finalizada


@router.put(
    "/{id_reserva}/confirmar",
    response_model=reserva_schema.SchemaReserva,
    summary="Confirma uma reserva pendente (Requer Funcionário)",
)
def rota_confirmar_reserva(
    id_reserva: int,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    _funcionario_logado: Annotated[
        models.Funcionario, Depends(obter_funcionario_atual)
    ],
):
    return reserva_service.confirmar_reserva(id_reserva, sessao_banco)


@router.put(
    "/{id_reserva}/retirar",
    response_model=reserva_schema.SchemaReserva,
    summary="Registra a retirada do veículo e muda status para ALUGADO",
)
def rota_registrar_retirada(
    id_reserva: int,
    sessao_banco: Annotated[Session, Depends(obter_sessao_banco)],
    _funcionario_logado: Annotated[
        models.Funcionario, Depends(obter_funcionario_atual)
    ],
):
    return reserva_service.registrar_retirada(id_reserva, sessao_banco)
