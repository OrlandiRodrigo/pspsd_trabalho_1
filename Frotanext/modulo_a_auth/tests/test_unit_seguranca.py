from datetime import timedelta

import pytest

# Testes Unitários para as funções de Segurança.
# Cobre: Hashing de senhas e criação/validação de tokens JWT.
from src.seguranca import (
    criar_token_acesso,
    obter_hash_senha,
    verificar_senha,
    verificar_token,
)


@pytest.mark.unit
def test_hash_senha_e_verificacao_roundtrip():
    senha_original = "MinhaSenha@123!"

    hash_da_senha = obter_hash_senha(senha_original)

    assert hash_da_senha is not None
    assert hash_da_senha != senha_original

    assert verificar_senha(senha_original, hash_da_senha) is True

    assert verificar_senha("SenhaErrada", hash_da_senha) is False


@pytest.mark.unit
def test_token_jwt_roundtrip_e_payload():
    dados_para_o_token = {"sub": "teste@frotanext.com", "id_usuario": 123}

    token_jwt = criar_token_acesso(dados=dados_para_o_token)

    assert token_jwt is not None

    payload_verificado = verificar_token(token_jwt)

    assert payload_verificado is not None
    assert payload_verificado["sub"] == "teste@frotanext.com"
    assert payload_verificado["id_usuario"] == 123
    assert "exp" in payload_verificado


@pytest.mark.unit
def test_verificar_token_invalido_retorna_none():
    token_falso = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"  # Token válido, mas com chave errada
    token_malformado = "nao.e.um.token"

    assert verificar_token(token_falso) is None
    assert verificar_token(token_malformado) is None
