from http.client import HTTPException
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import text

from src import models
from src import seguranca as seguranca_service
from src.database import Base, SessionLocal
from src.database import engine as engine_real
from src.main import app
from src.models import funcionario
from src.schemas import auth_schema, cliente_schema
from src.services import cliente_service


@pytest.fixture(scope="function")
def db_session():

    tabelas_para_limpar = [
        "funcionarios",
        "pessoas_fisicas",
        "pessoas_juridicas",
        "enderecos",
        "pessoas",
        "empresas" 
    ]
    
    with engine_real.connect() as connection:
        for tabela in tabelas_para_limpar:
            connection.execute(text(f"DROP TABLE IF EXISTS {tabela} CASCADE"))
        connection.commit()

    Base.metadata.create_all(bind=engine_real)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        with engine_real.connect() as connection:
            for tabela in tabelas_para_limpar:
                connection.execute(text(f"DROP TABLE IF EXISTS {tabela} CASCADE"))
            connection.commit()


@pytest.fixture(scope="function")
def test_client(db_session):
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def admin_auth_headers(db_session: Session):
    dados_admin = auth_schema.SchemaFuncionarioCriar(
        email="admin_test@locadora.com",
        nome_completo="Admin de Teste",
        e_admin=True,
        e_ativado=True,
        senha_texto_puro="senhasegura123",
    )

    hash_senha = seguranca_service.obter_hash_senha(dados_admin.senha_texto_puro)

    novo_admin_modelo = funcionario.Funcionario(
        email=dados_admin.email,
        nome_completo=dados_admin.nome_completo,
        senha=hash_senha,
        e_admin=dados_admin.e_admin,
        e_ativado=dados_admin.e_ativado,
    )

    db_session.add(novo_admin_modelo)
    db_session.commit()

    dados_token = {"sub": novo_admin_modelo.email}
    token_acesso = seguranca_service.criar_token_acesso(dados=dados_token)

    headers = {"Authorization": f"Bearer {token_acesso}"}
    return headers


@pytest.fixture(scope="function")
def client_auth_data(db_session: Session):
    """
    Fixture MODIFICADA para "plantar" um cliente PF no banco e
    gerar um token manualmente, sem depender da API.
    """
    dados_cliente_pf = {
        "email": "cliente_test@email.com",
        "telefone": "999999999",
        "nome_completo": "Cliente de Teste PF",
        "cpf": "12345678901",
        "cnh": "12345678901",
        "senha_texto_puro": "senhaCliente123",
        "endereco": {
            "rua": "Rua Teste Cliente",
            "numero": "100",
            "bairro": "Bairro Teste",
            "cidade": "Cidade Teste",
            "estado": "TS",
            "cep": "12345000",
        },
    }

    schema_dados = cliente_schema.SchemaPessoaFisicaCriar(**dados_cliente_pf)

    try:
        cliente_criado_modelo = cliente_service.criar_pessoa_fisica(
            dados_entrada_cliente=schema_dados, sessao_banco=db_session
        )
    except HTTPException as e:
        if "já cadastrado" in str(e.detail):
            cliente_criado_modelo = (
                db_session.query(models.PessoaFisica)
                .filter_by(email=dados_cliente_pf["email"])
                .first()
            )
        else:
            raise e

    dados_token = {
        "sub": str(cliente_criado_modelo.id_pessoa),
        "email": cliente_criado_modelo.email,
        "tipo": cliente_criado_modelo.tipo_pessoa,
    }

    token_acesso = seguranca_service.criar_token_acesso(dados=dados_token)

    return {
        "headers": {"Authorization": f"Bearer {token_acesso}"},
        "cliente_id": cliente_criado_modelo.id_pessoa,
        "cliente_email": cliente_criado_modelo.email,
    }


@pytest.fixture(scope="function")
def pj_auth_data(db_session: Session):
    """
    Fixture MODIFICADA para "plantar" um cliente PJ no banco e
    gerar um token manualmente, sem depender da API.
    """
    dados_cliente_pj = {
        "email": "empresa_teste@email.com",
        "telefone": "888888888",
        "razao_social": "Empresa de Teste LTDA",
        "cnpj": "12345678000199",
        "senha_texto_puro": "senhaEmpresa123",
        "endereco": {
            "rua": "Rua Teste Empresa",
            "numero": "200",
            "bairro": "Bairro Empresarial",
            "cidade": "Cidade Teste",
            "estado": "TS",
            "cep": "54321000",
        },
    }

    schema_dados = cliente_schema.SchemaPessoaJuridicaCriar(**dados_cliente_pj)

    try:
        pj_criada_modelo = cliente_service.criar_pessoa_juridica(
            dados_entrada_empresa=schema_dados, sessao_banco=db_session
        )
    except HTTPException as e:
        if "já cadastrado" in str(e.detail):
            pj_criada_modelo = (
                db_session.query(models.PessoaJuridica)
                .filter_by(email=dados_cliente_pj["email"])
                .first()
            )
        else:
            raise e

    dados_token = {
        "sub": str(pj_criada_modelo.id_pessoa),
        "email": pj_criada_modelo.email,
        "tipo": pj_criada_modelo.tipo_pessoa,
    }

    token_acesso = seguranca_service.criar_token_acesso(dados=dados_token)

    return {
        "headers": {"Authorization": f"Bearer {token_acesso}"},
        "cliente_id": pj_criada_modelo.id_pessoa,
        "cliente_email": pj_criada_modelo.email,
    }


@pytest.fixture(scope="function")
def funcionario_nao_admin_auth_headers(db_session: Session):
    dados_funcionario = auth_schema.SchemaFuncionarioCriar(
        email="funcionario_comum@frotanext.com",
        nome_completo="Funcionario Comum Teste",
        e_admin=False,
        e_ativado=True,
        senha_texto_puro="senhafuncionario123",
    )

    hash_senha = seguranca_service.obter_hash_senha(dados_funcionario.senha_texto_puro)
    novo_funcionario_modelo = funcionario.Funcionario(
        email=dados_funcionario.email,
        nome_completo=dados_funcionario.nome_completo,
        senha=hash_senha,
        e_admin=dados_funcionario.e_admin,
        e_ativado=dados_funcionario.e_ativado,
    )
    db_session.add(novo_funcionario_modelo)
    db_session.commit()

    dados_token = {"sub": novo_funcionario_modelo.email}
    token_acesso = seguranca_service.criar_token_acesso(dados=dados_token)

    headers = {"Authorization": f"Bearer {token_acesso}"}
    return headers
