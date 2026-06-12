from pydantic import BaseModel, ConfigDict, EmailStr


class SchemaFuncionarioBase(BaseModel):
    email: EmailStr
    nome_completo: str
    e_admin: bool = False
    e_ativado: bool = True


class SchemaFuncionarioCriar(SchemaFuncionarioBase):
    """Schema para ENTRADA de dados ao criar um novo funcionário."""

    senha_texto_puro: str


class SchemaFuncionario(SchemaFuncionarioBase):
    """Schema para SAÍDA de dados de funcionário."""

    id_funcionario: int

    model_config = ConfigDict(from_attributes=True)


class SchemaToken(BaseModel):
    """Schema para a resposta do endpoint de login."""

    access_token: str
    token_type: str


class SchemaTokenPayload(BaseModel):
    """Schema para os dados (payload) dentro do token JWT."""

    sub: str
