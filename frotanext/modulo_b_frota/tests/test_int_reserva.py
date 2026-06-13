from datetime import datetime, timedelta
import pytest
from fastapi.testclient import TestClient
from httpx import Response

veiculo_passeio_valido = {
    "placa": "TESTE123",
    "marca": "Marca Teste",
    "modelo": "Modelo Teste",
    "cor": "Preto",
    "valor_diaria": 150.0,
    "ano_fabricacao": 2023,
    "ano_modelo": 2023,
    "chassi": "CHASSIUNICO12345",
    "capacidade_tanque": 55.0,
    "cambio_automatico": True,
    "ar_condicionado": True,
    "tipo_veiculo": "passeio",
    "tipo_carroceria": "Sedan",
    "qtde_portas": 4,
}

@pytest.fixture(scope="function")
def setup_para_teste_reserva(
    test_client: TestClient, admin_auth_headers: dict, client_auth_data: dict
):
    test_client.post(
        "/veiculos/passeio", json=veiculo_passeio_valido, headers=admin_auth_headers
    )

    veiculos = test_client.get("/veiculos/?apenas_disponiveis=false").json()
    id_veiculo = veiculos[0]["id_veiculo"] if veiculos else 1

    return {
        "headers_cliente": client_auth_data["headers"],
        "id_cliente": client_auth_data["cliente_id"],
        "headers_admin": admin_auth_headers,
        "id_veiculo": id_veiculo,
    }

@pytest.mark.integration
def test_fluxo_completo_reserva_cliente_e_admin(
    test_client: TestClient, setup_para_teste_reserva: dict
):
    headers_cliente = setup_para_teste_reserva["headers_cliente"]
    headers_admin = setup_para_teste_reserva["headers_admin"]
    id_veiculo = setup_para_teste_reserva["id_veiculo"]

    dados_reserva = {
        "veiculo_id": id_veiculo,
        "data_retirada": str(datetime.today() + timedelta(days=1)),
        "data_devolucao": str(datetime.today() + timedelta(days=5)),
    }
    
    response_criar = test_client.post(
        "/reservas/", json=dados_reserva, headers=headers_cliente
    )
    assert response_criar.status_code == 201
    dados_reserva = response_criar.json()
    id_reserva = dados_reserva["id_reserva"]
    
    assert dados_reserva["status"] == "pendente"

    response_confirmar = test_client.put(
        f"/reservas/{id_reserva}/confirmar", headers=headers_admin
    )
    assert response_confirmar.status_code == 200
    assert response_confirmar.json()["status"] == "confirmada"

    response_retirar = test_client.put(
        f"/reservas/{id_reserva}/retirar", headers=headers_admin
    )
    assert response_retirar.status_code == 200
    assert response_retirar.json()["status"] == "em_andamento"

    response_finalizar = test_client.put(
        f"/reservas/{id_reserva}/finalizar", headers=headers_admin
    )
    assert response_finalizar.status_code == 200
    assert response_finalizar.json()["status"] == "finalizada"


@pytest.mark.integration
def test_admin_finaliza_reserva_com_sucesso_e_veiculo_retorna_disponivel(
    test_client: TestClient,
    setup_para_teste_reserva: dict,
):
    headers_cliente = setup_para_teste_reserva["headers_cliente"]
    headers_admin = setup_para_teste_reserva["headers_admin"]
    id_veiculo = setup_para_teste_reserva["id_veiculo"]

    dados_reserva = {
        "veiculo_id": id_veiculo,
        "data_retirada": str(datetime.today() + timedelta(days=1)),
        "data_devolucao": str(datetime.today() + timedelta(days=3)),
    }
    response_criar = test_client.post(
        "/reservas/", json=dados_reserva, headers=headers_cliente
    )
    id_reserva = response_criar.json()["id_reserva"]

    test_client.put(f"/reservas/{id_reserva}/confirmar", headers=headers_admin)
    test_client.put(f"/reservas/{id_reserva}/retirar", headers=headers_admin)

    response_finalizar: Response = test_client.put(
        f"/reservas/{id_reserva}/finalizar", headers=headers_admin
    )
    assert response_finalizar.status_code == 200
    assert response_finalizar.json()["status"] == "finalizada"

    veiculo_depois = test_client.get(f"/veiculos/{id_veiculo}").json()
    assert veiculo_depois["status"] == "disponível"


@pytest.mark.integration
def test_cliente_tenta_cancelar_reserva_ja_finalizada_falha_400(
    test_client: TestClient, 
    setup_para_teste_reserva: dict
):
    headers_cliente = setup_para_teste_reserva["headers_cliente"]
    headers_admin = setup_para_teste_reserva["headers_admin"]
    id_veiculo = setup_para_teste_reserva["id_veiculo"]

    dados_reserva = {
        "veiculo_id": id_veiculo,
        "data_retirada": str(datetime.today() + timedelta(days=1)),
        "data_devolucao": str(datetime.today() + timedelta(days=3)),
    }
    response_criar = test_client.post("/reservas/", json=dados_reserva, headers=headers_cliente)
    id_reserva = response_criar.json()["id_reserva"]

    test_client.put(f"/reservas/{id_reserva}/confirmar", headers=headers_admin)
    test_client.put(f"/reservas/{id_reserva}/retirar", headers=headers_admin)
    test_client.put(f"/reservas/{id_reserva}/finalizar", headers=headers_admin)

    response_cancelar: Response = test_client.put(
        f"/reservas/{id_reserva}/cancelar",
        headers=headers_cliente
    )
    
    assert response_cancelar.status_code == 400
    mensagem_erro = response_cancelar.json()["detail"].lower()
    assert any(x in mensagem_erro for x in ["não pode", "status", "cancelar", "finalizada"])