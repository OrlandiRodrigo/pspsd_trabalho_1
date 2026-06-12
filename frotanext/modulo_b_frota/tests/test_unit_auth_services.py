from unittest.mock import MagicMock, patch

import pytest

from src.services import auth_service, cliente_auth_service


@pytest.mark.unit
@patch("src.services.auth_service.buscar_funcionario_por_email")
@patch("src.services.auth_service.seguranca_service.verificar_senha")
def test_autenticar_funcionario_sucesso(
    mock_verificar_senha, mock_buscar_por_email, mocker
):
    mock_sessao = MagicMock()

    mock_funcionario = MagicMock()
    mock_funcionario.e_ativado = True
    mock_funcionario.senha = "hash_secreto_do_banco"

    mock_buscar_por_email.return_value = mock_funcionario
    mock_verificar_senha.return_value = True

    resultado = auth_service.autenticar_funcionario(
        sessao_banco=mock_sessao,
        email_formulario="admin@frotanext.com",
        senha_formulario="senha123",
    )

    assert resultado == mock_funcionario
    mock_buscar_por_email.assert_called_with(mock_sessao, email="admin@frotanext.com")
    mock_verificar_senha.assert_called_with(
        senha_texto_puro="senha123", senha_hashada="hash_secreto_do_banco"
    )


@pytest.mark.unit
@patch("src.services.auth_service.buscar_funcionario_por_email")
@patch("src.services.auth_service.seguranca_service.verificar_senha")
def test_autenticar_funcionario_nao_encontrado(
    mock_verificar_senha, mock_buscar_por_email
):
    mock_sessao = MagicMock()
    mock_buscar_por_email.return_value = None

    resultado = auth_service.autenticar_funcionario(
        sessao_banco=mock_sessao,
        email_formulario="falso@frotanext.com",
        senha_formulario="senha123",
    )

    assert resultado is None
    mock_verificar_senha.assert_not_called()


@pytest.mark.unit
@patch("src.services.auth_service.buscar_funcionario_por_email")
@patch("src.services.auth_service.seguranca_service.verificar_senha")
def test_autenticar_funcionario_inativo(mock_verificar_senha, mock_buscar_por_email):
    mock_sessao = MagicMock()

    mock_funcionario_inativo = MagicMock()
    mock_funcionario_inativo.e_ativado = False
    mock_buscar_por_email.return_value = mock_funcionario_inativo

    resultado = auth_service.autenticar_funcionario(
        sessao_banco=mock_sessao,
        email_formulario="inativo@frotanext.com",
        senha_formulario="senha123",
    )

    assert resultado is None
    mock_verificar_senha.assert_not_called()


@pytest.mark.unit
@patch("src.services.auth_service.buscar_funcionario_por_email")
@patch("src.services.auth_service.seguranca_service.verificar_senha")
def test_autenticar_funcionario_senha_incorreta(
    mock_verificar_senha, mock_buscar_por_email
):
    mock_sessao = MagicMock()

    mock_funcionario = MagicMock()
    mock_funcionario.e_ativado = True
    mock_funcionario.senha = "hash_secreto_do_banco"

    mock_buscar_por_email.return_value = mock_funcionario
    mock_verificar_senha.return_value = False

    resultado = auth_service.autenticar_funcionario(
        sessao_banco=mock_sessao,
        email_formulario="admin@frotanext.com",
        senha_formulario="senhaErrada",
    )

    assert resultado is None
    mock_verificar_senha.assert_called_with(
        senha_texto_puro="senhaErrada", senha_hashada="hash_secreto_do_banco"
    )


@pytest.mark.unit
@patch("src.services.cliente_auth_service.seguranca_service.verificar_senha")
def test_autenticar_cliente_sucesso(mock_verificar_senha, mocker):
    mock_sessao = MagicMock()

    mock_cliente = MagicMock()
    mock_cliente.e_ativado = True
    mock_cliente.senha = "hash_cliente_secreto"

    mock_query = mock_sessao.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = mock_cliente

    mock_verificar_senha.return_value = True

    resultado = cliente_auth_service.autenticar_cliente(
        sessao_banco=mock_sessao,
        email_formulario="cliente@email.com",
        senha_formulario="senhaCliente",
    )

    assert resultado == mock_cliente
    mock_verificar_senha.assert_called_with(
        senha_texto_puro="senhaCliente", senha_hashada="hash_cliente_secreto"
    )


@pytest.mark.unit
@patch("src.services.cliente_auth_service.seguranca_service.verificar_senha")
def test_autenticar_cliente_nao_encontrado(mock_verificar_senha, mocker):
    mock_sessao = MagicMock()
    mock_sessao.query.return_value.filter.return_value.first.return_value = None

    resultado = cliente_auth_service.autenticar_cliente(
        sessao_banco=mock_sessao,
        email_formulario="falso@cliente.com",
        senha_formulario="senhaCliente",
    )

    assert resultado is None
    mock_verificar_senha.assert_not_called()


@pytest.mark.unit
@patch("src.services.cliente_auth_service.seguranca_service.verificar_senha")
def test_autenticar_cliente_inativo_retorna_none(mock_verificar_senha, mocker):
    """
    NOVO TESTE: Verifica se um cliente com 'e_ativo=False' é bloqueado no login.
    """
    mock_sessao = MagicMock()

    mock_cliente = MagicMock()
    mock_cliente.e_ativo = False 
    mock_cliente.senha = "hash_cliente_secreto"

    mock_sessao.query.return_value.filter.return_value.first.return_value = mock_cliente

    resultado = cliente_auth_service.autenticar_cliente(
        sessao_banco=mock_sessao,
        email_formulario="bloqueado@cliente.com",
        senha_formulario="senhaCliente",
    )

    assert resultado is None
    mock_verificar_senha.assert_not_called()
