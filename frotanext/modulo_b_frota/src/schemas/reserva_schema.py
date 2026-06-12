from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..models.enums import StatusReservaEnum
from .cliente_schema import SchemaPessoaFisica, SchemaPessoaJuridica
from .veiculo_schema import SchemaVeiculo

SchemaCliente = Union[SchemaPessoaFisica, SchemaPessoaJuridica]


class SchemaReservaSimulacao(BaseModel):
    veiculo_id: int
    data_retirada: datetime
    data_devolucao: datetime
    seguro_pessoal: bool = False
    seguro_terceiros: bool = False

    @field_validator("data_devolucao")
    @classmethod
    def validar_datas_simulacao(cls, v, values):
        inicio = values.data.get("data_retirada")
        if inicio and v <= inicio:
            raise ValueError("A devolução deve ser posterior à retirada.")
        return v


class SchemaReservaSimulacaoResultado(BaseModel):
    """Retorno para o frontend mostrar os valores antes de confirmar"""

    quantidade_diarias: int
    valor_diarias: float
    valor_seguros: float
    valor_total_estimado: float


class SchemaReservaBase(BaseModel):
    veiculo_id: int
    data_retirada: datetime = Field(..., description="Data e hora de retirada")
    data_devolucao: datetime = Field(..., description="Data e hora de devolução")
    seguro_pessoal: bool = False
    seguro_terceiros: bool = False
    motorista_id: Optional[int] = Field(None, description="ID do motorista responsável (Obrigatório para PJ)")


class SchemaReservaCriar(SchemaReservaBase):
    @field_validator("data_devolucao")
    @classmethod
    def validar_datas(cls, v, values):
        inicio = values.data.get("data_retirada")
        if inicio:
            if v <= inicio:
                raise ValueError("Devolução deve ser após retirada.")
            if inicio < datetime.now():
                raise ValueError("Não é possível reservar no passado.")
        return v


class SchemaReserva(SchemaReservaBase):
    """Schema de Saída Completo"""

    id_reserva: int
    data_criacao: datetime

    valor_diaria_no_momento: float
    valor_total_estimado: float

    status: StatusReservaEnum

    cliente_id: int
    cliente: SchemaCliente
    veiculo: SchemaVeiculo
    motorista_id: Optional[int]
    motorista: Optional[SchemaPessoaFisica] = None

    model_config = ConfigDict(from_attributes=True)


class SchemaReservaUpdate(BaseModel):
    data_retirada: Optional[datetime] = None
    data_devolucao: Optional[datetime] = None
    seguro_pessoal: Optional[bool] = None
    seguro_terceiros: Optional[bool] = None

    @field_validator("data_devolucao")
    @classmethod
    def validar_update(cls, v, values):
        inicio = values.data.get("data_retirada")
        if inicio and v <= inicio:
            raise ValueError("Devolução deve ser após retirada.")
        return v
