import pytest
from fastapi.testclient import TestClient
from httpx import Response
from sqlalchemy.orm import Session

# Testes de Integração (API/DB) para os endpoints de Autenticação.
# Cobre: /auth/token, /clientes/token, criação de funcionários e permissões de acesso.

@pytest.mark.integration
def test_login_cliente_email_inexistente_falha_401(test_client: TestClient):
    login_data = {"username": "email.falso@cliente.com", "password": "senhaqualquer"}

    response: Response = test_client.post("/clientes/token", data=login_data)

    assert response.status_code == 401
    assert "incorretos" in response.json()["detail"].lower()
    print("\n[SUCESSO] Teste 'test_login_cliente_email_inexistente_falha_401' passou!")


@pytest.mark.integration
def test_login_cliente_senha_incorreta_falha_401(
    test_client: TestClient, client_auth_data: dict, db_session: Session
):
    email_valido = client_auth_data["cliente_email"]

    login_data = {"username": email_valido, "password": "senha-completamente-errada"}

    response: Response = test_client.post("/clientes/token", data=login_data)

    assert response.status_code == 401
    assert "incorretos" in response.json()["detail"].lower()
    print("\n[SUCESSO] Teste 'test_login_cliente_senha_incorreta_falha_401' passou!")


@pytest.mark.integration
def test_pj_remove_motorista_sucesso_200(
    test_client: TestClient,
    pj_auth_data: dict,
    client_auth_data: dict,
    db_session: Session,
):
    headers_pj = pj_auth_data["headers"]
    id_motorista_pf = client_auth_data["cliente_id"]

    dados_associacao = {"id_pessoa_fisica": id_motorista_pf}
    response_add: Response = test_client.post(
        "/minha-empresa/motoristas", json=dados_associacao, headers=headers_pj
    )
    assert response_add.status_code == 200
    assert len(response_add.json()["motoristas"]) >= 1

    response_remove: Response = test_client.delete(
        f"/minha-empresa/motoristas/{id_motorista_pf}", headers=headers_pj
    )

    assert response_remove.status_code == 200

    motoristas_restantes = response_remove.json().get("motoristas", [])
    ids_motoristas_restantes = [m["id_pessoa"] for m in motoristas_restantes]
    assert id_motorista_pf not in ids_motoristas_restantes

    print("\n[SUCESSO] Teste 'test_pj_remove_motorista_sucesso_200' passou!")


@pytest.mark.integration
def test_pj_tenta_remover_motorista_nao_associado_falha_400(
    test_client: TestClient,
    pj_auth_data: dict,
    client_auth_data: dict,
    db_session: Session,
):
    headers_pj = pj_auth_data["headers"]
    id_motorista_nao_associado = client_auth_data["cliente_id"]

    response_remove: Response = test_client.delete(
        f"/minha-empresa/motoristas/{id_motorista_nao_associado}", headers=headers_pj
    )

    assert response_remove.status_code == 400
    assert "não está associado à sua empresa" in response_remove.json()["detail"]
    print(
        "\n[SUCESSO] Teste 'test_pj_tenta_remover_motorista_nao_associado_falha_400' passou!"
    )


@pytest.mark.integration
def test_login_admin_senha_incorreta_falha_401(
    test_client: TestClient, admin_auth_headers: dict, db_session: Session
):
    email_admin_valido = "admin_test@locadora.com"

    login_data = {"username": email_admin_valido, "password": "senha-admin-errada"}

    response: Response = test_client.post("/auth/token", data=login_data)

    assert response.status_code == 401
    assert "incorretos" in response.json()["detail"].lower()
    print("\n[SUCESSO] Teste 'test_login_admin_senha_incorreta_falha_401' passou!")


@pytest.mark.integration
def test_login_admin_email_inexistente_falha_401(test_client: TestClient):
    login_data = {"username": "admin.falso@frotanext.com", "password": "senhaqualquer"}

    response: Response = test_client.post("/auth/token", data=login_data)

    assert response.status_code == 401
    assert "incorretos" in response.json()["detail"].lower()
    print("\n[SUCESSO] Teste 'test_login_admin_email_inexistente_falha_401' passou!")


@pytest.mark.integration
def test_admin_le_proprios_dados_sucesso_200(
    test_client: TestClient, admin_auth_headers: dict
):
    response: Response = test_client.get(
        "/auth/funcionarios/eu", headers=admin_auth_headers
    )

    assert response.status_code == 200
    dados_resposta = response.json()
    assert dados_resposta["email"] == "admin_test@locadora.com"
    assert dados_resposta["e_admin"] is True
    print("\n[SUCESSO] Teste 'test_admin_le_proprios_dados_sucesso_200' passou!")


@pytest.mark.integration
def test_funcionario_nao_admin_le_proprios_dados_sucesso_200(
    test_client: TestClient, funcionario_nao_admin_auth_headers: dict
):
    response: Response = test_client.get(
        "/auth/funcionarios/eu", headers=funcionario_nao_admin_auth_headers
    )

    assert response.status_code == 200
    dados_resposta = response.json()
    assert dados_resposta["email"] == "funcionario_comum@frotanext.com"
    assert dados_resposta["e_admin"] is False
    print(
        "\n[SUCESSO] Teste 'test_funcionario_nao_admin_le_proprios_dados_sucesso_200' passou!"
    )


@pytest.mark.integration
def test_criar_funcionario_com_token_cliente_falha_401(
    test_client: TestClient, client_auth_data: dict
):
    dados_novo_funcionario = {
        "email": "tentativa_cliente@frotanext.com",
        "nome_completo": "Tentativa Invasao Cliente",
        "senha_texto_puro": "senha123",
        "e_admin": True,
    }

    response: Response = test_client.post(
        "/auth/funcionarios",
        json=dados_novo_funcionario,
        headers=client_auth_data["headers"],
    )

    assert response.status_code == 401
    print(
        "\n[SUCESSO] Teste 'test_criar_funcionario_com_token_cliente_falha_401' passou!"
    )


@pytest.mark.integration
def test_funcionario_nao_admin_tenta_criar_outro_falha_403(
    test_client: TestClient, funcionario_nao_admin_auth_headers: dict
):
    dados_novo_funcionario = {
        "email": "tentativa_naoadmin@frotanext.com",
        "nome_completo": "Tentativa Nao Admin",
        "senha_texto_puro": "senha123",
    }

    response: Response = test_client.post(
        "/auth/funcionarios",
        json=dados_novo_funcionario,
        headers=funcionario_nao_admin_auth_headers,
    )

    assert response.status_code == 403
    assert "privilégios de administrador" in response.json()["detail"].lower()
    print(
        "\n[SUCESSO] Teste 'test_funcionario_nao_admin_tenta_criar_outro_falha_403' passou!"
    )


@pytest.mark.integration
def test_admin_tenta_criar_funcionario_email_duplicado_falha_400(
    test_client: TestClient, admin_auth_headers: dict
):
    dados_funcionario_duplicado = {
        "email": "admin_test@locadora.com",
        "nome_completo": "Admin Duplicado",
        "senha_texto_puro": "senha123",
    }

    response: Response = test_client.post(
        "/auth/funcionarios",
        json=dados_funcionario_duplicado,
        headers=admin_auth_headers,
    )

    assert response.status_code == 400
    assert "email" in response.json()["detail"].lower()
    print(
        "\n[SUCESSO] Teste 'test_admin_tenta_criar_funcionario_email_duplicado_falha_400' passou!"
    )
