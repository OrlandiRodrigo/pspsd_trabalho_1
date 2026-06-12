from sqlalchemy import Boolean, Column, Integer, String

from ..database import Base


class Funcionario(Base):
    __tablename__ = "funcionarios"

    id_funcionario = Column(Integer, primary_key=True, index=True)
    nome_completo = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    e_admin = Column(Boolean, default=False, nullable=False)
    e_ativado = Column(Boolean, default=True, nullable=False)
