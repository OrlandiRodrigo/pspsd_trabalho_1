import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from src.schemas import cliente_schema

from src.services.cliente_service import (
    adicionar_motorista_empresa,
    remover_motorista_empresa,
    criar_pessoa_fisica, 
    criar_pessoa_juridica
)
from src.models.pessoa import PessoaFisica, PessoaJuridica

@pytest.mark.unit
def test_adicionar_motorista_associado_outra_empresa_falha():
    mock_sessao = MagicMock()

    mock_empresa_logada = MagicMock(spec=PessoaJuridica)
    mock_empresa_logada.id_pessoa = 1
    mock_empresa_logada.motoristas = []

    mock_motorista = MagicMock(spec=PessoaFisica)
    mock_motorista.empresa_id = 2 
    mock_motorista.nome_completo = "Motorista Teste"

    mock_query = mock_sessao.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = mock_motorista

    with pytest.raises(HTTPException) as exc_info:
        adicionar_motorista_empresa(
            empresa_logada=mock_empresa_logada,
            cpf_motorista="123.456.789-00", 
            sessao_banco=mock_sessao,
        )

    assert exc_info.value.status_code == 400
    assert "vinculado a outra empresa" in exc_info.value.detail

@pytest.mark.unit
def test_adicionar_motorista_nao_encontrado_falha_404():
    mock_sessao = MagicMock()
    mock_empresa_logada = MagicMock(spec=PessoaJuridica)

    mock_sessao.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        adicionar_motorista_empresa(
            empresa_logada=mock_empresa_logada,
            cpf_motorista="999.999.999-99",
            sessao_banco=mock_sessao,
        )
    
    assert exc_info.value.status_code == 404
    assert "não encontrado" in exc_info.value.detail

@pytest.mark.unit
def test_adicionar_motorista_ja_associado_retorna_empresa(mocker):
    mock_sessao = MagicMock()

    mock_motorista = MagicMock(spec=PessoaFisica)
    mock_motorista.empresa_id = 1

    mock_empresa_logada = MagicMock(spec=PessoaJuridica)
    mock_empresa_logada.id_pessoa = 1
    mock_empresa_logada.motoristas = [mock_motorista] 

    mock_sessao.query.return_value.filter.return_value.first.return_value = mock_motorista

    resultado = adicionar_motorista_empresa(
        empresa_logada=mock_empresa_logada,
        cpf_motorista="123.456.789-00",
        sessao_banco=mock_sessao,
    )

    assert resultado == mock_empresa_logada
    mock_sessao.add.assert_not_called() 


@pytest.mark.unit
def test_remover_motorista_nao_associado_falha():
    mock_sessao = MagicMock()
    
    mock_motorista = MagicMock(spec=PessoaFisica)
    mock_empresa_logada = MagicMock(spec=PessoaJuridica)
    mock_empresa_logada.motoristas = []

    mock_sessao.get.return_value = mock_motorista 

    with pytest.raises(HTTPException) as exc_info:
        remover_motorista_empresa(
            empresa_logada=mock_empresa_logada,
            id_motorista_remover=10,
            sessao_banco=mock_sessao,
        )

    assert exc_info.value.status_code == 400
    assert "não está associado" in exc_info.value.detail


@pytest.mark.unit
def test_criar_pessoa_fisica_email_duplicado_falha():
    mock_sessao = MagicMock()

    dados_entrada = cliente_schema.SchemaPessoaFisicaCriar(
        email="duplicado@email.com",
        telefone="123",
        nome_completo="Teste",
        cpf="123",
        cnh="123",
        senha_texto_puro="senha1234",
        endereco={
            "rua": "R",
            "numero": "1",
            "bairro": "B",
            "cidade": "C",
            "estado": "E",
            "cep": "123",
        },
    )

    mock_sessao.query.return_value.filter.return_value.first.return_value = MagicMock()

    with pytest.raises(HTTPException) as exc_info:
        criar_pessoa_fisica(
            dados_entrada_cliente=dados_entrada, sessao_banco=mock_sessao
        )

    assert exc_info.value.status_code == 400
    assert "email já cadastrado" in exc_info.value.detail.lower()


@pytest.mark.unit
def test_criar_pessoa_fisica_cpf_duplicado_falha():
    mock_sessao = MagicMock()
    dados_entrada = cliente_schema.SchemaPessoaFisicaCriar(
        email="unico@email.com",
        telefone="123",
        nome_completo="Teste",
        cpf="12345678900",
        cnh="123",
        senha_texto_puro="senha1234",
        endereco={
            "rua": "R",
            "numero": "1",
            "bairro": "B",
            "cidade": "C",
            "estado": "E",
            "cep": "123",
        },
    )

    mock_sessao.query.return_value.filter.return_value.first.side_effect = [
        None,
        MagicMock(),
    ]

    with pytest.raises(HTTPException) as exc_info:
        criar_pessoa_fisica(
            dados_entrada_cliente=dados_entrada, sessao_banco=mock_sessao
        )

    assert exc_info.value.status_code == 400
    assert "cpf já cadastrado" in exc_info.value.detail.lower()


@pytest.mark.unit
def test_criar_pessoa_juridica_cnpj_duplicado_falha():
    mock_sessao = MagicMock()
    dados_entrada = cliente_schema.SchemaPessoaJuridicaCriar(
        email="empresa.unica@email.com",
        telefone="123",
        razao_social="Teste",
        cnpj="12345678000199",
        senha_texto_puro="senha1234",
        endereco={
            "rua": "R",
            "numero": "1",
            "bairro": "B",
            "cidade": "C",
            "estado": "E",
            "cep": "123",
        },
    )

    mock_sessao.query.return_value.filter.return_value.first.side_effect = [
        None,
        MagicMock(),
    ]

    with pytest.raises(HTTPException) as exc_info:
        criar_pessoa_juridica(
            dados_entrada_empresa=dados_entrada, sessao_banco=mock_sessao
        )

    assert exc_info.value.status_code == 400
    assert "cnpj já cadastrado" in exc_info.value.detail.lower()
