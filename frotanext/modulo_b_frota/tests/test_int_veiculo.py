from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from httpx import Response
import pytest

# Testes de Integração (API/DB) para os endpoints de Veículos.
# Cobre: CRUD de Passeio, Utilitário e Motocicleta, incluindo regras de negócio.

veiculo_utilitario_valido = {
    "placa": "UTL5678",
    "marca": "Fiat",
    "modelo": "Fiorino",
    "cor": "Branco",
    "valor_diaria": 220.0,
    "ano_fabricacao": 2022,
    "ano_modelo": 2022,
    "chassi": "9BDZZZ2J2P4B56789",
    "capacidade_tanque": 60.0,
    "tipo_veiculo": "utilitario",
    "tipo_utilitario": "Furgão",
    "capacidade_carga_kg": 650.0,
    "qtde_eixos": 2,
    "max_passageiros": 2,
}

veiculo_motocicleta_valido = {
    "placa": "MTO9012",
    "marca": "Honda",
    "modelo": "CB 500",
    "cor": "Vermelho",
    "valor_diaria": 120.0,
    "ano_fabricacao": 2023,
    "ano_modelo": 2023,
    "chassi": "9CZZZZ3J2P4C90123",
    "capacidade_tanque": 17.0,
    "tipo_veiculo": "motocicleta",
    "abs": True,
    "partida_eletrica": True,
}

veiculo_passeio_valido = {
    "placa": "ABC1234",
    "marca": "Volkswagen",
    "modelo": "Golf",
    "cor": "Preto",
    "valor_diaria": 150.50,
    "ano_fabricacao": 2020,
    "ano_modelo": 2021,
    "chassi": "9BWZZZ1J2P4A12345",
    "capacidade_tanque": 50.0,
    "cambio_automatico": True,
    "ar_condicionado": True,
    "tipo_veiculo": "passeio",
    "tipo_carroceria": "Hatch",
    "qtde_portas": 4,
}


@pytest.mark.integration
def test_listar_veiculos_banco_vazio(test_client: TestClient):
    response: Response = test_client.get("/veiculos/")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.integration
def test_criar_veiculo_sem_token(test_client: TestClient):
    response: Response = test_client.post(
        "/veiculos/passeio", json=veiculo_passeio_valido
    )

    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]


@pytest.mark.integration
def test_criar_veiculo_com_token_de_cliente(
    test_client: TestClient, client_auth_data: dict
):
    headers_cliente = client_auth_data["headers"]

    response: Response = test_client.post(
        "/veiculos/passeio", json=veiculo_passeio_valido, headers=headers_cliente
    )

    assert response.status_code == 401


@pytest.mark.integration
def test_criar_veiculo_com_token_admin_sucesso(
    test_client: TestClient, admin_auth_headers: dict
):
    response: Response = test_client.post(
        "/veiculos/passeio", json=veiculo_passeio_valido, headers=admin_auth_headers
    )

    assert response.status_code == 201, f"Falha ao criar veículo: {response.text}"

    dados_resposta = response.json()
    assert dados_resposta["placa"] == veiculo_passeio_valido["placa"]
    assert dados_resposta["modelo"] == veiculo_passeio_valido["modelo"]
    assert dados_resposta["status"] == "disponível"
    assert "id_veiculo" in dados_resposta

    print("\n[SUCESSO] Teste 'test_criar_veiculo_com_token_admin_sucesso' passou!")


@pytest.mark.integration
def test_listar_veiculos_com_um_item(test_client: TestClient, admin_auth_headers: dict):
    """
    Testa se o endpoint GET /veiculos/ retorna o veículo que acabamos de criar.
    """
    test_client.post(
        "/veiculos/passeio", json=veiculo_passeio_valido, headers=admin_auth_headers
    )

    response: Response = test_client.get("/veiculos/")

    assert response.status_code == 200
    dados_resposta = response.json()

    assert isinstance(dados_resposta, list)
    assert len(dados_resposta) == 1
    assert dados_resposta[0]["placa"] == veiculo_passeio_valido["placa"]

    print("\n[SUCESSO] Teste 'test_listar_veiculos_com_um_item' passou!")


@pytest.mark.integration
def test_criar_veiculo_utilitario_com_token_admin_sucesso(
    test_client: TestClient, admin_auth_headers: dict
):
    """
    Testa a criação bem-sucedida de um veículo do tipo Utilitário.
    """
    response: Response = test_client.post(
        "/veiculos/utilitario",
        json=veiculo_utilitario_valido,
        headers=admin_auth_headers,
    )
    assert response.status_code == 201
    dados_resposta = response.json()
    assert dados_resposta["placa"] == veiculo_utilitario_valido["placa"]
    assert (
        dados_resposta["tipo_utilitario"]
        == veiculo_utilitario_valido["tipo_utilitario"]
    )
    print(
        "\n[SUCESSO] Teste 'test_criar_veiculo_utilitario_com_token_admin_sucesso' passou!"
    )


@pytest.mark.integration
def test_criar_veiculo_motocicleta_com_token_admin_sucesso(
    test_client: TestClient, admin_auth_headers: dict
):
    """
    Testa a criação bem-sucedida de um veículo do tipo Motocicleta.
    """
    response: Response = test_client.post(
        "/veiculos/motocicleta",
        json=veiculo_motocicleta_valido,
        headers=admin_auth_headers,
    )
    assert response.status_code == 201
    dados_resposta = response.json()
    assert dados_resposta["placa"] == veiculo_motocicleta_valido["placa"]
    assert dados_resposta["partida_eletrica"] is True
    print(
        "\n[SUCESSO] Teste 'test_criar_veiculo_motocicleta_com_token_admin_sucesso' passou!"
    )


@pytest.mark.integration
def test_criar_veiculo_placa_duplicada_falha_400(
    test_client: TestClient, admin_auth_headers: dict
):
    veiculo_1 = veiculo_passeio_valido.copy()
    response1: Response = test_client.post(
        "/veiculos/passeio", json=veiculo_1, headers=admin_auth_headers
    )
    assert response1.status_code == 201

    veiculo_2 = veiculo_utilitario_valido.copy()
    veiculo_2["placa"] = veiculo_1["placa"]

    response2: Response = test_client.post(
        "/veiculos/utilitario", json=veiculo_2, headers=admin_auth_headers
    )

    assert response2.status_code == 400
    assert "placa" in response2.json()["detail"].lower()
    print("\n[SUCESSO] Teste 'test_criar_veiculo_placa_duplicada_falha_400' passou!")


@pytest.mark.integration
def test_criar_veiculo_chassi_duplicado_falha_400(
    test_client: TestClient, admin_auth_headers: dict
):
    veiculo_1 = veiculo_passeio_valido.copy()
    response1: Response = test_client.post(
        "/veiculos/passeio", json=veiculo_1, headers=admin_auth_headers
    )
    assert response1.status_code == 201

    veiculo_2 = veiculo_utilitario_valido.copy()
    veiculo_2["chassi"] = veiculo_1["chassi"]

    response2: Response = test_client.post(
        "/veiculos/utilitario", json=veiculo_2, headers=admin_auth_headers
    )

    assert response2.status_code == 400
    assert "chassi" in response2.json()["detail"].lower()
    print("\n[SUCESSO] Teste 'test_criar_veiculo_chassi_duplicado_falha_400' passou!")


@pytest.mark.integration
def test_criar_veiculo_ano_modelo_anterior_fabricacao_falha_400(
    test_client: TestClient, admin_auth_headers: dict
):
    veiculo_ano_errado = veiculo_passeio_valido.copy()
    veiculo_ano_errado["placa"] = "ANO1234"
    veiculo_ano_errado["chassi"] = "CHASSIANO123"
    veiculo_ano_errado["ano_fabricacao"] = 2022
    veiculo_ano_errado["ano_modelo"] = 2021

    response: Response = test_client.post(
        "/veiculos/passeio", json=veiculo_ano_errado, headers=admin_auth_headers
    )

    assert response.status_code == 400
    assert "anterior ao ano de fabricação" in response.json()["detail"]
    print(
        "\n[SUCESSO] Teste 'test_criar_veiculo_ano_modelo_anterior_fabricacao_falha_400' passou!"
    )


@pytest.mark.integration
def test_tentar_deletar_veiculo_com_reserva_ativa_falha_400(
    test_client: TestClient, admin_auth_headers: dict, client_auth_data: dict
):
    veiculo_para_reservar = veiculo_passeio_valido.copy()
    response_veiculo = test_client.post(
        "/veiculos/passeio", json=veiculo_para_reservar, headers=admin_auth_headers
    )
    assert response_veiculo.status_code == 201
    id_veiculo_criado = response_veiculo.json()["id_veiculo"]

    dados_reserva = {
        "veiculo_id": id_veiculo_criado,
        "data_retirada": (datetime.now() + timedelta(days=1)).isoformat(),
        "data_devolucao": (datetime.now() + timedelta(days=3)).isoformat(),
        "seguro_pessoal": True
    }
    response_reserva = test_client.post(
        "/reservas/", json=dados_reserva, headers=client_auth_data["headers"]
    )
    assert response_reserva.status_code == 201

    response_delete = test_client.delete(
        f"/veiculos/{id_veiculo_criado}", headers=admin_auth_headers
    )

    assert response_delete.status_code == 400
    assert "reservas associadas" in response_delete.json()["detail"]


@pytest.mark.integration
def test_buscar_veiculo_id_inexistente_falha_404(test_client: TestClient):
    """
    Testa se a API retorna 404 ao buscar um ID de veículo inexistente.
    [Endpoint: GET /veiculos/{id}]
    """
    response: Response = test_client.get("/veiculos/99999")
    assert response.status_code == 404
    assert "não encontrado" in response.json()["detail"].lower()
    print("\n[SUCESSO] Teste 'test_buscar_veiculo_id_inexistente_falha_404' passou!")


@pytest.mark.integration
def test_admin_atualiza_veiculo_passeio_sucesso_200(
    test_client: TestClient, admin_auth_headers: dict
):
    dados_criar = {
        "placa": "AAA1234",
        "marca": "Fiat",
        "modelo": "Argo",
        "cor": "Vermelho",
        "valor_diaria": 120.00,
        "ano_fabricacao": 2020,
        "ano_modelo": 2021,
        "chassi": "CHASSIARGO12345",
        "capacidade_tanque": 48.0,
        "tipo_carroceria": "Hatch",
        "qtde_portas": 4,
    }
    response_create: Response = test_client.post(
        "/veiculos/passeio/", json=dados_criar, headers=admin_auth_headers
    )
    assert response_create.status_code == 201
    veiculo_id = response_create.json()["id_veiculo"]

    dados_atualizar = {
        "placa": "BBB5678",
        "marca": "Ford",
        "modelo": "Ka",
        "cor": "Azul",
        "valor_diaria": 130.00,
        "ano_fabricacao": 2021,
        "ano_modelo": 2022,
        "chassi": "CHASSIKA67890",
        "capacidade_tanque": 50.0,
        "tipo_carroceria": "Sedan",
        "qtde_portas": 4,
    }
    response_update: Response = test_client.put(
        f"/veiculos/passeio/{veiculo_id}",
        json=dados_atualizar,
        headers=admin_auth_headers,
    )

    assert response_update.status_code == 200
    dados_resposta = response_update.json()
    assert dados_resposta["placa"] == "BBB5678"
    assert dados_resposta["modelo"] == "Ka"
    assert dados_resposta["cor"] == "Azul"
    print("\n[SUCESSO] Teste 'test_admin_atualiza_veiculo_passeio_sucesso_200' passou!")


@pytest.mark.integration
def test_admin_atualiza_veiculo_utilitario_sucesso_200(
    test_client: TestClient, admin_auth_headers: dict
):
    dados_criar = {
        "placa": "CCC9012",
        "marca": "Renault",
        "modelo": "Kangoo",
        "cor": "Branco",
        "valor_diaria": 180.00,
        "ano_fabricacao": 2019,
        "ano_modelo": 2020,
        "chassi": "CHASSIKANGOO123",
        "capacidade_tanque": 50.0,
        "tipo_utilitario": "Furgão",
        "capacidade_carga_kg": 750.0,
    }
    response_create: Response = test_client.post(
        "/veiculos/utilitario/", json=dados_criar, headers=admin_auth_headers
    )
    assert response_create.status_code == 201
    veiculo_id = response_create.json()["id_veiculo"]

    dados_atualizar = {
        "placa": "DDD3456",
        "marca": "Fiat",
        "modelo": "Fiorino",
        "cor": "Branco",
        "valor_diaria": 190.00,
        "ano_fabricacao": 2020,
        "ano_modelo": 2021,
        "chassi": "CHASIFIORINO456",
        "capacidade_tanque": 55.0,
        "tipo_utilitario": "Van",
        "capacidade_carga_kg": 800.0,
        "qtde_eixos": 2,
    }
    response_update: Response = test_client.put(
        f"/veiculos/utilitario/{veiculo_id}",
        json=dados_atualizar,
        headers=admin_auth_headers,
    )

    assert response_update.status_code == 200
    dados_resposta = response_update.json()
    assert dados_resposta["placa"] == "DDD3456"
    assert dados_resposta["modelo"] == "Fiorino"
    assert dados_resposta["capacidade_carga_kg"] == 800.0
    print(
        "\n[SUCESSO] Teste 'test_admin_atualiza_veiculo_utilitario_sucesso_200' passou!"
    )


@pytest.mark.integration
def test_admin_atualiza_veiculo_motocicleta_sucesso_200(
    test_client: TestClient, admin_auth_headers: dict
):
    dados_criar = {
        "placa": "EEE7890",
        "marca": "Honda",
        "modelo": "CG 160",
        "cor": "Preto",
        "valor_diaria": 80.00,
        "ano_fabricacao": 2022,
        "ano_modelo": 2023,
        "chassi": "CHASSIMOTO78901",
        "capacidade_tanque": 14.0,
        "abs": False,
    }
    response_create: Response = test_client.post(
        "/veiculos/motocicleta/", json=dados_criar, headers=admin_auth_headers
    )
    assert response_create.status_code == 201
    veiculo_id = response_create.json()["id_veiculo"]

    dados_atualizar = {
        "placa": "FFF1234",
        "marca": "Yamaha",
        "modelo": "Factor 150",
        "cor": "Branco",
        "valor_diaria": 85.00,
        "ano_fabricacao": 2023,
        "ano_modelo": 2024,
        "chassi": "CHASSIMOTO23456",
        "capacidade_tanque": 15.0,
        "abs": True,
        "partida_eletrica": True,
        "modos_pilotagem": "Eco",
    }
    response_update: Response = test_client.put(
        f"/veiculos/motocicleta/{veiculo_id}",
        json=dados_atualizar,
        headers=admin_auth_headers,
    )

    assert response_update.status_code == 200
    dados_resposta = response_update.json()
    assert dados_resposta["placa"] == "FFF1234"
    assert dados_resposta["modelo"] == "Factor 150"
    assert dados_resposta["abs"] is True
    print(
        "\n[SUCESSO] Teste 'test_admin_atualiza_veiculo_motocicleta_sucesso_200' passou!"
    )


@pytest.mark.integration
def test_admin_atualiza_veiculo_com_placa_ja_existente_falha_400(
    test_client: TestClient, admin_auth_headers: dict
):
    dados_veiculo1 = {
        "placa": "DUPLA11",
        "marca": "GM",
        "modelo": "Onix",
        "cor": "Prata",
        "valor_diaria": 100.00,
        "ano_fabricacao": 2020,
        "ano_modelo": 2021,
        "chassi": "CHASIONIX11111",
        "capacidade_tanque": 45.0,
        "tipo_carroceria": "Hatch",
        "qtde_portas": 4,
    }
    response_create1: Response = test_client.post(
        "/veiculos/passeio/", json=dados_veiculo1, headers=admin_auth_headers
    )
    assert response_create1.status_code == 201

    dados_veiculo2 = {
        "placa": "DUPLA22",
        "marca": "VW",
        "modelo": "Gol",
        "cor": "Branco",
        "valor_diaria": 90.00,
        "ano_fabricacao": 2019,
        "ano_modelo": 2020,
        "chassi": "CHASSIGOL22222",
        "capacidade_tanque": 40.0,
        "tipo_carroceria": "Hatch",
        "qtde_portas": 4,
    }
    response_create2: Response = test_client.post(
        "/veiculos/passeio/", json=dados_veiculo2, headers=admin_auth_headers
    )
    assert response_create2.status_code == 201
    veiculo2_id = response_create2.json()["id_veiculo"]

    dados_atualizar_com_placa_duplicada = {**dados_veiculo2, "placa": "DUPLA11"}
    response_update: Response = test_client.put(
        f"/veiculos/passeio/{veiculo2_id}",
        json=dados_atualizar_com_placa_duplicada,
        headers=admin_auth_headers,
    )

    assert response_update.status_code == 400
    assert "placa" in response_update.json()["detail"].lower()
    print(
        "\n[SUCESSO] Teste 'test_admin_atualiza_veiculo_com_placa_ja_existente_falha_400' passou!"
    )


@pytest.mark.integration
def test_cliente_tenta_atualizar_veiculo_falha_401(
    test_client: TestClient, client_auth_data: dict
):
    response: Response = test_client.put(
        "/veiculos/passeio/1",
        json={"placa": "XYZ7890"},
        headers=client_auth_data["headers"],
    )

    assert response.status_code == 401
    assert "validar as credenciais" in response.json()["detail"].lower()
    print("\n[SUCESSO] Teste 'test_cliente_tenta_atualizar_veiculo_falha_401' passou!")


@pytest.mark.integration
def test_admin_deleta_veiculo_sem_reserva_sucesso_204(
    test_client: TestClient, admin_auth_headers: dict
):
    dados_criar = {
        "placa": "ZZZ0000",
        "marca": "Tesla",
        "modelo": "Model 3",
        "cor": "Preto",
        "valor_diaria": 500.00,
        "ano_fabricacao": 2023,
        "ano_modelo": 2023,
        "chassi": "CHASSITESLA0000",
        "capacidade_tanque": 1.0,
        "tipo_carroceria": "Sedan",
        "qtde_portas": 4,
    }
    response_create: Response = test_client.post(
        "/veiculos/passeio/", json=dados_criar, headers=admin_auth_headers
    )
    assert response_create.status_code == 201
    veiculo_id = response_create.json()["id_veiculo"]

    response_delete: Response = test_client.delete(
        f"/veiculos/{veiculo_id}", headers=admin_auth_headers
    )
    assert response_delete.status_code == 204

    response_get: Response = test_client.get(
        f"/veiculos/{veiculo_id}", headers=admin_auth_headers
    )
    assert response_get.status_code == 404
    print(
        "\n[SUCESSO] Teste 'test_admin_deleta_veiculo_sem_reserva_sucesso_204' passou!"
    )
