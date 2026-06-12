from datetime import datetime
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
    cnh: Optional[str] = None
    senha_texto_puro: str = Field(..., min_length=8)
    endereco: SchemaEnderecoBase


class SchemaPessoaFisica(BaseModel):
    id_pessoa: int
    email: EmailStr
    telefone: str
    nome_completo: str
    cpf: str
    cnh: Optional[str]
    e_ativo: bool
    data_criacao: datetime
    endereco: SchemaEndereco
    model_config = ConfigDict(from_attributes=True)


class SchemaPessoaJuridicaCriar(BaseModel):
    email: EmailStr
    telefone: str
    razao_social: str
    nome_fantasia: Optional[str] = None
    cnpj: str
    senha_texto_puro: str = Field(..., min_length=8)
    endereco: SchemaEnderecoBase
    motoristas_ids: Optional[List[int]] = Field(default=None)


class SchemaPessoaJuridica(BaseModel):
    id_pessoa: int
    email: EmailStr
    telefone: str
    razao_social: str
    nome_fantasia: Optional[str]
    cnpj: str
    e_ativo: bool
    data_criacao: datetime
    endereco: SchemaEndereco
    motoristas: List[SchemaPessoaFisica] = []
    model_config = ConfigDict(from_attributes=True)


class SchemaMotoristaAssociar(BaseModel):
    cpf_motorista: str


class SchemaPessoaFisicaUpdate(BaseModel):
    email: EmailStr
    telefone: str
    nome_completo: str
    cpf: str
    cnh: str
    endereco: SchemaEnderecoBase


class SchemaPessoaJuridicaUpdate(BaseModel):
    email: EmailStr
    telefone: str
    razao_social: str
    cnpj: str
    endereco: SchemaEnderecoBase
    motoristas_ids: Optional[List[int]] = None
