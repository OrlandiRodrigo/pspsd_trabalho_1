from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from .. import models
from ..models.enums import StatusVeiculoEnum, TipoVeiculoEnum
from ..models.veiculo import (
    Motocicleta,
    Utilitario,
    Veiculo,
)
from ..schemas import veiculo_schema


def criar_veiculo_passeio(
    dados_entrada_veiculo: veiculo_schema.SchemaPasseioCriar, sessao_banco: Session
) -> models.Passeio:
    veiculo_existente_placa = (
        sessao_banco.query(models.Veiculo)
        .filter(models.Veiculo.placa == dados_entrada_veiculo.placa)
        .first()
    )

    if veiculo_existente_placa:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Já existe um veículo cadastrado com a placa {dados_entrada_veiculo.placa}.",
        )

    veiculo_existente_chassi = (
        sessao_banco.query(models.Veiculo)
        .filter(models.Veiculo.chassi == dados_entrada_veiculo.chassi)
        .first()
    )

    if veiculo_existente_chassi:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um veículo cadastrado com este número de chassi.",
        )

    if dados_entrada_veiculo.ano_modelo < dados_entrada_veiculo.ano_fabricacao:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O ano do modelo não pode ser anterior ao ano de fabricação.",
        )

    novo_veiculo_passeio_modelo = models.Passeio(**dados_entrada_veiculo.model_dump())

    sessao_banco.add(novo_veiculo_passeio_modelo)
    sessao_banco.commit()

    sessao_banco.refresh(novo_veiculo_passeio_modelo)

    return novo_veiculo_passeio_modelo


def _validar_duplicidade_veiculo(
    sessao_banco: Session,
    id_veiculo_atual: int,
    placa: Optional[str] = None,
    chassi: Optional[str] = None,
):
    if placa:
        outro_veiculo_placa = (
            sessao_banco.query(models.Veiculo)
            .filter(
                models.Veiculo.placa == placa,
                models.Veiculo.id_veiculo != id_veiculo_atual,
            )
            .first()
        )
        if outro_veiculo_placa:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Placa {placa} já cadastrada para outro veículo.",
            )

    if chassi:
        outro_veiculo_chassi = (
            sessao_banco.query(models.Veiculo)
            .filter(
                models.Veiculo.chassi == chassi,
                models.Veiculo.id_veiculo != id_veiculo_atual,
            )
            .first()
        )
        if outro_veiculo_chassi:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chassi já cadastrado para outro veículo.",
            )


def criar_veiculo_utilitario(
    dados_entrada_veiculo: veiculo_schema.SchemaUtilitarioCriar, sessao_banco: Session
) -> Utilitario:
    veiculo_existente_placa = (
        sessao_banco.query(Veiculo)
        .filter(Veiculo.placa == dados_entrada_veiculo.placa)
        .first()
    )
    if veiculo_existente_placa:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Placa {dados_entrada_veiculo.placa} já cadastrada.",
        )

    veiculo_existente_chassi = (
        sessao_banco.query(Veiculo)
        .filter(Veiculo.chassi == dados_entrada_veiculo.chassi)
        .first()
    )
    if veiculo_existente_chassi:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Chassi já cadastrado."
        )

    if dados_entrada_veiculo.ano_modelo < dados_entrada_veiculo.ano_fabricacao:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ano do modelo não pode ser anterior ao ano de fabricação.",
        )

    novo_veiculo_utilitario_modelo = Utilitario(**dados_entrada_veiculo.model_dump())

    sessao_banco.add(novo_veiculo_utilitario_modelo)
    sessao_banco.commit()
    sessao_banco.refresh(novo_veiculo_utilitario_modelo)

    return novo_veiculo_utilitario_modelo


def criar_veiculo_motocicleta(
    dados_entrada_veiculo: veiculo_schema.SchemaMotocicletaCriar, sessao_banco: Session
) -> Motocicleta:
    veiculo_existente_placa = (
        sessao_banco.query(Veiculo)
        .filter(Veiculo.placa == dados_entrada_veiculo.placa)
        .first()
    )
    if veiculo_existente_placa:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Placa {dados_entrada_veiculo.placa} já cadastrada.",
        )

    veiculo_existente_chassi = (
        sessao_banco.query(Veiculo)
        .filter(Veiculo.chassi == dados_entrada_veiculo.chassi)
        .first()
    )
    if veiculo_existente_chassi:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Chassi já cadastrado."
        )

    if dados_entrada_veiculo.ano_modelo < dados_entrada_veiculo.ano_fabricacao:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ano do modelo não pode ser anterior ao ano de fabricação.",
        )

    novo_veiculo_moto_modelo = Motocicleta(**dados_entrada_veiculo.model_dump())

    sessao_banco.add(novo_veiculo_moto_modelo)
    sessao_banco.commit()
    sessao_banco.refresh(novo_veiculo_moto_modelo)

    return novo_veiculo_moto_modelo


def listar_veiculos(
    sessao_banco: Session,
    categoria: Optional[TipoVeiculoEnum] = None,
    apenas_disponiveis: bool = False,
    termo_busca: Optional[str] = None,
) -> List[Veiculo]:
    query = sessao_banco.query(Veiculo)

    if apenas_disponiveis:
        query = query.filter(Veiculo.status == StatusVeiculoEnum.DISPONIVEL)

    if categoria:
        query = query.filter(Veiculo.tipo_veiculo == categoria)

    if termo_busca:
        termo_limpo = f"%{termo_busca}%"
        query = query.filter(
            or_(Veiculo.modelo.ilike(termo_limpo), Veiculo.marca.ilike(termo_limpo))
        )

    return query.all()


def buscar_veiculo_por_id(id_veiculo: int, sessao_banco: Session) -> Veiculo:
    veiculo_encontrado = sessao_banco.get(Veiculo, id_veiculo)
    if not veiculo_encontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Veículo com ID {id_veiculo} não encontrado.",
        )
    return veiculo_encontrado


def deletar_veiculo(id_veiculo: int, sessao_banco: Session) -> None:
    veiculo_para_deletar = buscar_veiculo_por_id(id_veiculo, sessao_banco)

    if veiculo_para_deletar.reservas:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Não é possível deletar o veículo com ID {id_veiculo}, pois ele possui reservas associadas.",
        )

    if veiculo_para_deletar.status != StatusVeiculoEnum.DISPONIVEL:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Não é possível deletar o veículo com ID {id_veiculo}"
            f" pois seu status é '{veiculo_para_deletar.status.value}'.",
        )
    sessao_banco.delete(veiculo_para_deletar)
    sessao_banco.commit()


def atualizar_veiculo_passeio(
    id_veiculo: int,
    dados_atualizacao: veiculo_schema.SchemaPasseioUpdate,
    sessao_banco: Session,
) -> models.Passeio:
    veiculo_para_atualizar = buscar_veiculo_por_id(id_veiculo, sessao_banco)

    if not isinstance(veiculo_para_atualizar, models.Passeio):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro: Veículo com ID {id_veiculo} não é um veículo de Passeio.",
        )

    update_data = dados_atualizacao.model_dump(exclude_unset=True)

    _validar_duplicidade_veiculo(
        sessao_banco,
        id_veiculo_atual=id_veiculo,
        placa=update_data.get("placa"),
        chassi=update_data.get("chassi"),
    )

    for key, value in update_data.items():
        setattr(veiculo_para_atualizar, key, value)

    sessao_banco.add(veiculo_para_atualizar)
    sessao_banco.commit()
    sessao_banco.refresh(veiculo_para_atualizar)

    return veiculo_para_atualizar


def atualizar_veiculo_utilitario(
    id_veiculo: int,
    dados_atualizacao: veiculo_schema.SchemaUtilitarioUpdate,
    sessao_banco: Session,
) -> models.Utilitario:
    veiculo_para_atualizar = buscar_veiculo_por_id(id_veiculo, sessao_banco)

    if not isinstance(veiculo_para_atualizar, models.Utilitario):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro: Veículo com ID {id_veiculo} não é um veículo Utilitário.",
        )

    update_data = dados_atualizacao.model_dump(exclude_unset=True)
    _validar_duplicidade_veiculo(
        sessao_banco, id_veiculo, update_data.get("placa"), update_data.get("chassi")
    )

    for key, value in update_data.items():
        setattr(veiculo_para_atualizar, key, value)

    sessao_banco.add(veiculo_para_atualizar)
    sessao_banco.commit()
    sessao_banco.refresh(veiculo_para_atualizar)

    return veiculo_para_atualizar


def atualizar_veiculo_motocicleta(
    id_veiculo: int,
    dados_atualizacao: veiculo_schema.SchemaMotocicletaUpdate,
    sessao_banco: Session,
) -> models.Motocicleta:
    veiculo_para_atualizar = buscar_veiculo_por_id(id_veiculo, sessao_banco)

    if not isinstance(veiculo_para_atualizar, models.Motocicleta):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro: Veículo com ID {id_veiculo} não é uma Motocicleta.",
        )

    update_data = dados_atualizacao.model_dump(exclude_unset=True)
    _validar_duplicidade_veiculo(
        sessao_banco, id_veiculo, update_data.get("placa"), update_data.get("chassi")
    )

    for key, value in update_data.items():
        setattr(veiculo_para_atualizar, key, value)

    sessao_banco.add(veiculo_para_atualizar)
    sessao_banco.commit()
    sessao_banco.refresh(veiculo_para_atualizar)

    return veiculo_para_atualizar
