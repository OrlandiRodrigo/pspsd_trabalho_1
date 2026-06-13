import math
from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from ..models.enums import StatusReservaEnum, StatusVeiculoEnum
from ..models.pessoa import Pessoa, PessoaJuridica
from ..models.reserva import Reserva
from ..models.veiculo import Veiculo
from ..schemas import reserva_schema


def _calcular_custos_reserva(
    data_retirada: datetime,
    data_devolucao: datetime,
    valor_diaria_veiculo: float,
    incluir_seguro_pessoal: bool,
    incluir_seguro_terceiros: bool,
) -> dict:
    if data_devolucao <= data_retirada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A data de devolução deve ser posterior à data de retirada.",
        )

    diferenca = data_devolucao - data_retirada
    quantidade_diarias = math.ceil(diferenca.total_seconds() / 86400)
    quantidade_diarias = max(quantidade_diarias, 1)

    valor_total_diarias = quantidade_diarias * valor_diaria_veiculo

    custo_seguros_por_dia = 0.0
    if incluir_seguro_pessoal:
        custo_seguros_por_dia += 25.0
    if incluir_seguro_terceiros:
        custo_seguros_por_dia += 35.0

    valor_total_seguros = custo_seguros_por_dia * quantidade_diarias
    valor_final_estimado = valor_total_diarias + valor_total_seguros

    return {
        "quantidade_diarias": quantidade_diarias,
        "valor_diarias": valor_total_diarias,
        "valor_seguros": valor_total_seguros,
        "valor_total_estimado": valor_final_estimado,
    }


def simular_valor_reserva(
    dados_simulacao: reserva_schema.SchemaReservaSimulacao, sessao_banco: Session
) -> reserva_schema.SchemaReservaSimulacaoResultado:
    veiculo = sessao_banco.get(Veiculo, dados_simulacao.veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado.")

    calculo = _calcular_custos_reserva(
        data_retirada=dados_simulacao.data_retirada,
        data_devolucao=dados_simulacao.data_devolucao,
        valor_diaria_veiculo=veiculo.valor_diaria,
        incluir_seguro_pessoal=dados_simulacao.seguro_pessoal,
        incluir_seguro_terceiros=dados_simulacao.seguro_terceiros,
    )

    return reserva_schema.SchemaReservaSimulacaoResultado(**calculo)


def criar_reserva(
    dados_entrada_reserva: reserva_schema.SchemaReservaCriar,
    cliente_logado: Pessoa,
    sessao_banco: Session,
) -> Reserva:
    veiculo_encontrado = sessao_banco.get(Veiculo, dados_entrada_reserva.veiculo_id)
    if not veiculo_encontrado:
        raise HTTPException(status_code=404, detail="Veículo não encontrado.")

    if veiculo_encontrado.status != StatusVeiculoEnum.DISPONIVEL:
        raise HTTPException(
            status_code=400,
            detail=f"Veículo indisponível (status: {veiculo_encontrado.status.value}).",
        )

    motorista_id_final = cliente_logado.id_pessoa

    if isinstance(cliente_logado, PessoaJuridica):
        if not dados_entrada_reserva.motorista_id:
            raise HTTPException(
                status_code=400,
                detail="Empresas devem selecionar qual motorista irá retirar o veículo.",
            )

        sessao_banco.refresh(cliente_logado)
        motorista_valido = any(
            m.id_pessoa == dados_entrada_reserva.motorista_id
            for m in cliente_logado.motoristas
        )

        if not motorista_valido:
            raise HTTPException(
                status_code=400,
                detail="O motorista selecionado não está vinculado à sua empresa.",
            )

        motorista_id_final = dados_entrada_reserva.motorista_id

    calculo = _calcular_custos_reserva(
        data_retirada=dados_entrada_reserva.data_retirada,
        data_devolucao=dados_entrada_reserva.data_devolucao,
        valor_diaria_veiculo=veiculo_encontrado.valor_diaria,
        incluir_seguro_pessoal=dados_entrada_reserva.seguro_pessoal,
        incluir_seguro_terceiros=dados_entrada_reserva.seguro_terceiros,
    )

    nova_reserva = Reserva(
        veiculo_id=dados_entrada_reserva.veiculo_id,
        cliente_id=cliente_logado.id_pessoa,
        motorista_id=motorista_id_final,
        data_retirada=dados_entrada_reserva.data_retirada,
        data_devolucao=dados_entrada_reserva.data_devolucao,
        seguro_pessoal=dados_entrada_reserva.seguro_pessoal,
        seguro_terceiros=dados_entrada_reserva.seguro_terceiros,
        valor_diaria_no_momento=veiculo_encontrado.valor_diaria,
        valor_total_estimado=calculo["valor_total_estimado"],
        status=StatusReservaEnum.PENDENTE,
    )

    veiculo_encontrado.status = StatusVeiculoEnum.RESERVADO

    sessao_banco.add(nova_reserva)
    sessao_banco.add(veiculo_encontrado)
    sessao_banco.commit()
    sessao_banco.refresh(nova_reserva)

    return nova_reserva


def confirmar_reserva(id_reserva: int, sessao_banco: Session) -> Reserva:
    reserva = sessao_banco.get(Reserva, id_reserva)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada.")

    if reserva.status != StatusReservaEnum.PENDENTE:
        raise HTTPException(
            status_code=400,
            detail=f"Apenas reservas pendentes podem ser confirmadas. Status atual: {reserva.status.value}",
        )

    reserva.status = StatusReservaEnum.CONFIRMADA
    sessao_banco.commit()
    sessao_banco.refresh(reserva)
    return reserva


def registrar_retirada(id_reserva: int, sessao_banco: Session) -> Reserva:
    reserva = (
        sessao_banco.query(Reserva).options(joinedload(Reserva.veiculo)).get(id_reserva)
    )
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada.")

    if reserva.status != StatusReservaEnum.CONFIRMADA:
        raise HTTPException(
            status_code=400,
            detail="Apenas reservas confirmadas podem ter retirada registrada.",
        )

    reserva.status = StatusReservaEnum.EM_ANDAMENTO

    if reserva.veiculo:
        reserva.veiculo.status = StatusVeiculoEnum.ALUGADO  # <--- VEÍCULO VIRA ALUGADO
        sessao_banco.add(reserva.veiculo)

    sessao_banco.commit()
    sessao_banco.refresh(reserva)
    return reserva


def finalizar_reserva(id_reserva: int, sessao_banco: Session) -> Reserva:
    reserva = (
        sessao_banco.query(Reserva).options(joinedload(Reserva.veiculo)).get(id_reserva)
    )

    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada.")

    if reserva.status != StatusReservaEnum.EM_ANDAMENTO:
        raise HTTPException(
            status_code=400,
            detail=f"Apenas reservas em andamento podem ser finalizadas. Status atual: {reserva.status.value}",
        )

    data_hoje = datetime.now()

    dias_reais = math.ceil((data_hoje - reserva.data_retirada).total_seconds() / 86400)
    dias_reais = max(dias_reais, 1)

    total_final = dias_reais * reserva.valor_diaria_no_momento

    custo_seguros = 0.0
    if reserva.seguro_pessoal:
        custo_seguros += 25.0
    if reserva.seguro_terceiros:
        custo_seguros += 35.0
    total_final += dias_reais * custo_seguros

    if data_hoje > reserva.data_devolucao:
        dias_atraso = math.ceil(
            (data_hoje - reserva.data_devolucao).total_seconds() / 86400
        )
        if dias_atraso > 0:
            multa = dias_atraso * (reserva.valor_diaria_no_momento * 0.5)
            total_final += multa

    reserva.valor_total_estimado = total_final
    reserva.status = StatusReservaEnum.FINALIZADA

    if reserva.veiculo:
        reserva.veiculo.status = StatusVeiculoEnum.DISPONIVEL
        sessao_banco.add(reserva.veiculo)

    sessao_banco.add(reserva)
    sessao_banco.commit()
    sessao_banco.refresh(reserva)

    return reserva


def listar_reservas(
    sessao_banco: Session, filtro_status: Optional[str] = None
) -> List[Reserva]:
    query = sessao_banco.query(Reserva)
    if filtro_status:
        query = query.filter(Reserva.status == filtro_status)
    return query.order_by(Reserva.data_retirada).all()


def buscar_reserva_por_id(id_reserva: int, sessao_banco: Session) -> Reserva:
    reserva = sessao_banco.get(Reserva, id_reserva)
    if not reserva:
        raise HTTPException(404, "Não encontrada")
    return reserva


def buscar_reserva_por_id_e_cliente(
    id_reserva: int, id_cliente: int, sessao_banco: Session
) -> Reserva:
    reserva = buscar_reserva_por_id(id_reserva, sessao_banco)
    if reserva.cliente_id != id_cliente:
        raise HTTPException(403, "Sem permissão")
    return reserva


def listar_reservas_por_cliente(
    cliente_logado: Pessoa, sessao_banco: Session
) -> List[Reserva]:
    return (
        sessao_banco.query(Reserva)
        .filter(Reserva.cliente_id == cliente_logado.id_pessoa)
        .order_by(Reserva.data_retirada.desc())
        .all()
    )


def cancelar_reserva(id_reserva: int, sessao_banco: Session) -> Reserva:
    reserva = (
        sessao_banco.query(Reserva).options(joinedload(Reserva.veiculo)).get(id_reserva)
    )
    if not reserva:
        raise HTTPException(404, "Não encontrada")

    if reserva.status not in [StatusReservaEnum.PENDENTE, StatusReservaEnum.CONFIRMADA]:
        raise HTTPException(400, "Não pode cancelar agora.")

    reserva.status = StatusReservaEnum.CANCELADA
    if reserva.veiculo:
        reserva.veiculo.status = StatusVeiculoEnum.DISPONIVEL
        sessao_banco.add(reserva.veiculo)

    sessao_banco.add(reserva)
    sessao_banco.commit()
    return reserva


def modificar_reserva(
    id_reserva: int,
    dados_atualizacao: reserva_schema.SchemaReservaUpdate,
    sessao_banco: Session,
) -> Reserva:
    reserva = buscar_reserva_por_id(id_reserva, sessao_banco)
    if dados_atualizacao.data_retirada:
        reserva.data_retirada = dados_atualizacao.data_retirada
    if dados_atualizacao.data_devolucao:
        reserva.data_devolucao = dados_atualizacao.data_devolucao
    if dados_atualizacao.seguro_pessoal is not None:
        reserva.seguro_pessoal = dados_atualizacao.seguro_pessoal
    if dados_atualizacao.seguro_terceiros is not None:
        reserva.seguro_terceiros = dados_atualizacao.seguro_terceiros

    calculo = _calcular_custos_reserva(
        reserva.data_retirada,
        reserva.data_devolucao,
        reserva.valor_diaria_no_momento,
        reserva.seguro_pessoal,
        reserva.seguro_terceiros,
    )
    reserva.valor_total_estimado = calculo["valor_total_estimado"]
    sessao_banco.commit()
    sessao_banco.refresh(reserva)
    return reserva
