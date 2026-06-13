from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Endereco(Base):
    __tablename__ = "enderecos"
    id_endereco = Column(Integer, primary_key=True, index=True)
    rua = Column(String, nullable=False)
    numero = Column(String, nullable=False)
    complemento = Column(String, nullable=True)
    bairro = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    cep = Column(String, nullable=False, index=True)

    pessoa_id = Column(
        Integer, ForeignKey("pessoas.id_pessoa"), nullable=False, unique=True
    )
    pessoa = relationship("Pessoa", back_populates="endereco", uselist=False)


class Pessoa(Base):
    __tablename__ = "pessoas"
    id_pessoa = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    telefone = Column(String, nullable=False)
    senha = Column(String, nullable=False)

    e_ativo = Column(Boolean, default=True, nullable=False)
    data_criacao = Column(DateTime, default=datetime.now, nullable=False)

    endereco = relationship(
        "Endereco", back_populates="pessoa", uselist=False, cascade="all, delete-orphan"
    )

    reservas = relationship(
        "Reserva", back_populates="cliente", foreign_keys="Reserva.cliente_id"
    )

    tipo_pessoa = Column(String(50))
    __mapper_args__ = {
        "polymorphic_identity": "pessoa",
        "polymorphic_on": tipo_pessoa,
    }


class PessoaFisica(Pessoa):
    __tablename__ = "pessoas_fisicas"
    id_pessoa = Column(Integer, ForeignKey("pessoas.id_pessoa"), primary_key=True)
    nome_completo = Column(String, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)
    cnh = Column(String, unique=True, index=True, nullable=True)

    empresa_id = Column(
        Integer, ForeignKey("pessoas_juridicas.id_pessoa"), nullable=True
    )
    empresa = relationship(
        "PessoaJuridica", back_populates="motoristas", foreign_keys=[empresa_id]
    )

    __mapper_args__ = {"polymorphic_identity": "pessoa_fisica"}


class PessoaJuridica(Pessoa):
    __tablename__ = "pessoas_juridicas"
    id_pessoa = Column(Integer, ForeignKey("pessoas.id_pessoa"), primary_key=True)
    razao_social = Column(String, nullable=False)
    nome_fantasia = Column(String, nullable=True)
    cnpj = Column(String, unique=True, index=True, nullable=False)

    motoristas = relationship(
        "PessoaFisica", back_populates="empresa", foreign_keys=[PessoaFisica.empresa_id]
    )

    __mapper_args__ = {"polymorphic_identity": "pessoa_juridica"}
