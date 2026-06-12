from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..database import Base
from .enums import StatusReservaEnum


class Reserva(Base):
    __tablename__ = "reservas"
    id_reserva = Column(Integer, primary_key=True, index=True)

    data_retirada = Column(DateTime, nullable=False)
    data_devolucao = Column(DateTime, nullable=False)
    data_criacao = Column(DateTime, default=datetime.now)

    valor_diaria_no_momento = Column(Float, nullable=False)
    valor_total_estimado = Column(Float, nullable=False)

    seguro_pessoal = Column(Boolean, nullable=False, default=False)
    seguro_terceiros = Column(Boolean, nullable=False, default=False)

    status = Column(
        Enum(StatusReservaEnum),
        nullable=False,
        default=StatusReservaEnum.PENDENTE,
        index=True,
    )

    cliente_id = Column(Integer, ForeignKey("pessoas.id_pessoa"), nullable=False)
    veiculo_id = Column(Integer, ForeignKey("veiculos.id_veiculo"), nullable=False)
    motorista_id = Column(Integer, ForeignKey("pessoas.id_pessoa"), nullable=True)

    cliente = relationship(
        "Pessoa", back_populates="reservas", foreign_keys=[cliente_id]
    )

    motorista = relationship("Pessoa", foreign_keys=[motorista_id])

    veiculo = relationship("Veiculo", back_populates="reservas")
