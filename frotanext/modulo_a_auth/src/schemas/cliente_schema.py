from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SchemaEnderecoBase(BaseModel):
    rua: str
    numero: str
    complemento: Optional[str] = None
    bairro: str
    cidade: str
    estado: str
    cep: str


class SchemaEndereco(SchemaEnderecoBase):
    id_endereco: int

    model_config = ConfigDict(from_attributes=True)


class SchemaPessoaFisicaCriar(BaseModel):
    email: EmailStr
    telefone: str
    nome_completo: str
    cpf: str
    cnh: str

    senha_texto_puro: str = Field(
        ...,
        min_length=8,
        description="Senha para a conta do cliente (mínimo 8 caracteres)",
    )

    endereco: SchemaEnderecoBase


class SchemaPessoaFisica(BaseModel):
    id_pessoa: int
    email: EmailStr
    telefone: str
    nome_completo: str
    cpf: str
    cnh: str

    endereco: SchemaEndereco

    model_config = ConfigDict(from_attributes=True)


class SchemaPessoaJuridicaCriar(BaseModel):
    email: EmailStr
    telefone: str
    razao_social: str
    cnpj: str
    nome_fantasia: Optional[str] = None
    senha_texto_puro: str = Field(..., min_length=8)
    endereco: SchemaEnderecoBase

    motoristas_ids: Optional[List[int]] = Field(default=None)


class SchemaPessoaJuridica(BaseModel):
    id_pessoa: int
    email: EmailStr
    telefone: str
    razao_social: str
    cnpj: str

    endereco: SchemaEndereco

    motoristas: List[SchemaPessoaFisica] = []

    model_config = ConfigDict(from_attributes=True)


class SchemaMotoristaAssociar(BaseModel):
    id_pessoa_fisica: int = Field(
        ..., description="ID da Pessoa Física (motorista) a ser associada."
    )
