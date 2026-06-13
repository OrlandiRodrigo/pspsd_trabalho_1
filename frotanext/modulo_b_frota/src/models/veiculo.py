from sqlalchemy import Boolean, Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base
from .enums import CorVeiculoEnum, StatusVeiculoEnum, TipoVeiculoEnum


class Veiculo(Base):
    __tablename__ = "veiculos"
    id_veiculo = Column(Integer, primary_key=True, index=True)

    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    ano_fabricacao = Column(Integer, nullable=False)
    ano_modelo = Column(Integer, nullable=False)
    cor = Column(Enum(CorVeiculoEnum), nullable=False)
    placa = Column(String, unique=True, index=True, nullable=False)
    chassi = Column(String, unique=True, nullable=False)
    renavam = Column(String, unique=True, nullable=True)

    valor_diaria = Column(Float, nullable=False)
    capacidade_tanque = Column(Float, nullable=False)
    cambio_automatico = Column(Boolean, default=False)
    ar_condicionado = Column(Boolean, default=False)
    imagem_url = Column(String, nullable=True)

    status = Column(
        Enum(StatusVeiculoEnum),
        nullable=False,
        default=StatusVeiculoEnum.DISPONIVEL,
        index=True,
    )

    reservas = relationship("Reserva", back_populates="veiculo")

    tipo_veiculo = Column(Enum(TipoVeiculoEnum), nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "veiculo",
        "polymorphic_on": tipo_veiculo,
    }


class Passeio(Veiculo):
    __tablename__ = "veiculos_passeio"
    id_veiculo = Column(Integer, ForeignKey("veiculos.id_veiculo"), primary_key=True)
    tipo_carroceria = Column(String)
    qtde_portas = Column(Integer, nullable=False)
    qtde_passageiros = Column(Integer, default=5)

    __mapper_args__ = {"polymorphic_identity": TipoVeiculoEnum.PASSEIO}


class Utilitario(Veiculo):
    __tablename__ = "veiculos_utilitario"
    id_veiculo = Column(Integer, ForeignKey("veiculos.id_veiculo"), primary_key=True)
    tipo_utilitario = Column(String)
    capacidade_carga_kg = Column(Float)
    capacidade_carga_m3 = Column(Float, nullable=True)
    tipo_carga = Column(String)
    qtde_eixos = Column(Integer)
    max_passageiros = Column(Integer)

    __mapper_args__ = {"polymorphic_identity": TipoVeiculoEnum.UTILITARIO}


class Motocicleta(Veiculo):
    __tablename__ = "veiculos_motocicleta"
    id_veiculo = Column(Integer, ForeignKey("veiculos.id_veiculo"), primary_key=True)
    cilindrada = Column(Integer, nullable=True)
    tipo_tracao = Column(String)
    abs = Column(Boolean, default=False)
    partida_eletrica = Column(Boolean, default=True)
    modos_pilotagem = Column(String)

    __mapper_args__ = {"polymorphic_identity": TipoVeiculoEnum.MOTOCICLETA}
