from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from ..models.enums import CorVeiculoEnum, StatusVeiculoEnum, TipoVeiculoEnum


class SchemaVeiculoBase(BaseModel):
    """Define a estrutura base comum a todos os veículos."""

    placa: str = Field(..., description="Placa única do veículo (ex: BRA2E19)")
    marca: str
    modelo: str
    cor: CorVeiculoEnum
    valor_diaria: float = Field(
        ..., gt=0, description="Valor da diária de locação deste veículo"
    )
    ano_fabricacao: int = Field(..., gt=1900)
    ano_modelo: int = Field(..., ge=1900)
    chassi: str = Field(..., description="Número único do chassi")
    renavam: Optional[str] = Field(None, description="Código RENAVAM")
    capacidade_tanque: float = Field(..., gt=0)
    cambio_automatico: bool = False
    ar_condicionado: bool = False
    imagem_url: Optional[str] = Field(None, description="URL da foto do veículo")


class SchemaPasseioCriar(SchemaVeiculoBase):
    tipo_veiculo: TipoVeiculoEnum = Field(TipoVeiculoEnum.PASSEIO, frozen=True)
    tipo_carroceria: Optional[str] = Field(None, description="Ex: Hatch, Sedan, SUV")
    qtde_portas: int = Field(..., ge=2)
    qtde_passageiros: int = Field(5, description="Capacidade de passageiros")


class SchemaUtilitarioCriar(SchemaVeiculoBase):
    tipo_veiculo: TipoVeiculoEnum = Field(TipoVeiculoEnum.UTILITARIO, frozen=True)
    tipo_utilitario: Optional[str] = Field(None, description="Ex: Van, Furgão")
    capacidade_carga_kg: Optional[float] = Field(None, gt=0)
    capacidade_carga_m3: Optional[float] = Field(
        None, description="Volume de carga (m³)"
    )
    tipo_carga: Optional[str] = None
    qtde_eixos: Optional[int] = None
    max_passageiros: Optional[int] = None


class SchemaMotocicletaCriar(SchemaVeiculoBase):
    tipo_veiculo: TipoVeiculoEnum = Field(TipoVeiculoEnum.MOTOCICLETA, frozen=True)
    cilindrada: Optional[int] = Field(None, description="Cilindrada (cc)")
    tipo_tracao: Optional[str] = None
    abs: bool = False
    partida_eletrica: bool = True
    modos_pilotagem: Optional[str] = None


class SchemaPasseio(SchemaPasseioCriar):
    id_veiculo: int
    status: StatusVeiculoEnum
    model_config = ConfigDict(from_attributes=True)


class SchemaUtilitario(SchemaUtilitarioCriar):
    id_veiculo: int
    status: StatusVeiculoEnum
    model_config = ConfigDict(from_attributes=True)


class SchemaMotocicleta(SchemaMotocicletaCriar):
    id_veiculo: int
    status: StatusVeiculoEnum
    model_config = ConfigDict(from_attributes=True)


class SchemaVeiculo(SchemaVeiculoBase):
    """Schema polimórfico genérico para listagens"""

    id_veiculo: int
    tipo_veiculo: TipoVeiculoEnum
    status: StatusVeiculoEnum

    tipo_carroceria: Optional[str] = None
    qtde_portas: Optional[int] = None
    qtde_passageiros: Optional[int] = None
    tipo_utilitario: Optional[str] = None
    capacidade_carga_kg: Optional[float] = None
    capacidade_carga_m3: Optional[float] = None
    cilindrada: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class SchemaVeiculoUpdateBase(BaseModel):
    placa: Optional[str] = Field(
        None, description="Nova placa única do veículo (ex: BRA2E19)"
    )
    imagem_url: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    cor: Optional[CorVeiculoEnum] = None
    valor_diaria: Optional[float] = Field(
        None, gt=0, description="Novo valor da diária"
    )
    ano_fabricacao: Optional[int] = Field(
        None, gt=1900, description="Novo ano de fabricação"
    )
    ano_modelo: Optional[int] = Field(None, ge=1900, description="Novo ano do modelo")
    chassi: Optional[str] = Field(None, description="Novo número único do chassi")
    capacidade_tanque: Optional[float] = Field(
        None, gt=0, description="Nova capacidade do tanque em litros"
    )
    cambio_automatico: Optional[bool] = None
    ar_condicionado: Optional[bool] = None
    status: Optional[StatusVeiculoEnum] = Field(None, description="Novo status operacional")


class SchemaPasseioUpdate(SchemaVeiculoUpdateBase):
    tipo_carroceria: Optional[str] = Field(None, description="Ex: Hatch, Sedan, SUV")
    qtde_portas: Optional[int] = Field(
        None, ge=2, description="Nova quantidade de portas"
    )


class SchemaUtilitarioUpdate(SchemaVeiculoUpdateBase):
    tipo_utilitario: Optional[str] = Field(
        None, description="Ex: Van, Furgão, Caminhonete"
    )
    capacidade_carga_kg: Optional[float] = Field(
        None, gt=0, description="Nova capacidade de carga em Kg"
    )
    tipo_carga: Optional[str] = Field(None, description="Novo tipo de carga principal")
    qtde_eixos: Optional[int] = Field(
        None, ge=2, description="Nova quantidade de eixos"
    )
    max_passageiros: Optional[int] = Field(
        None, ge=1, description="Novo número máximo de passageiros"
    )


class SchemaMotocicletaUpdate(SchemaVeiculoUpdateBase):
    tipo_tracao: Optional[str] = Field(None, description="Ex: Corrente, Correia, Cardã")
    abs: Optional[bool] = None
    partida_eletrica: Optional[bool] = None
    modos_pilotagem: Optional[str] = Field(None, description="Novos modos de pilotagem")
