from datetime import datetime, timedelta
import pytest
from fastapi.testclient import TestClient
from httpx import Response

dados_validos_pessoa_fisica = [
    {
        "email": "teste.param1@email.com",
        "telefone": "11111111111",
        "nome_completo": "Cliente Param Um",
        "cpf": "11100011100",
        "cnh": "1000000001",
        "senha_texto_puro": "senhaValida1",
        "endereco": {
            "rua": "Rua P1",
            "numero": "1",
            "bairro": "B P1",
            "cidade": "C P1",
            "estado": "P1",
            "cep": "11111001",
        },
    }
]

dados_validos_pessoa_juridica = {
    "email": "empresa.valida@email.com",
    "telefone": "5555555555",
    "razao_social": "Empresa Valida LTDA",
    "cnpj": "98765432000188",
    "senha_texto_puro": "senhaEmpresaValida",
    "endereco": {
        "rua": "Rua PJ",
        "numero": "500",
        "bairro": "Bairro PJ",
        "cidade": "Cidade PJ",
        "estado": "PJ",
        "cep": "55555000",
    },
}

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
    "tipo_veiculo": "passeio",
    "qtde_portas": 4,
}


@pytest.fixture(scope="function")
def setup_para_teste_reserva(
    test_client: TestClient, admin_auth_headers: dict, client_auth_data: dict
):
    response_veiculo = test_client.post(
        "/veiculos/passeio", json=veiculo_passeio_valido, headers=admin_auth_headers
    )
    assert response_veiculo.status_code == 201, (
        f"Erro ao criar veículo: {response_veiculo.text}"
    )

    return {
        "headers_cliente": client_auth_data["headers"],
        "id_cliente": client_auth_data["cliente_id"],
        "headers_admin": admin_auth_headers,
        "id_veiculo": response_veiculo.json()["id_veiculo"],
    }


@pytest.mark.integration
def test_admin_lista_pessoas_fisicas_sucesso(
    test_client: TestClient, admin_auth_headers: dict, client_auth_data: dict
):
    response: Response = test_client.get(
        "/clientes/pessoas-fisicas/", headers=admin_auth_headers
    )
    assert response.status_code == 200
    lista_pf = response.json()
    assert isinstance(lista_pf, list)
    assert len(lista_pf) >= 1
    assert lista_pf[0]["email"] == client_auth_data["cliente_email"]
    print("\n[SUCESSO] Teste 'test_admin_lista_pessoas_fisicas_sucesso' passou!")


@pytest.mark.integration
def test_admin_lista_pessoas_juridicas_sucesso(
    test_client: TestClient, admin_auth_headers: dict, pj_auth_data: dict
):
    """
    Testa se o admin consegue listar todas as Pessoas Jurídicas.
    [Endpoint: GET /clientes/pessoas-juridicas]
    """
    response: Response = test_client.get(
        "/clientes/pessoas-juridicas/", headers=admin_auth_headers
    )
    assert response.status_code == 200
    lista_pj = response.json()
    assert isinstance(lista_pj, list)
    assert len(lista_pj) >= 1
    assert lista_pj[0]["email"] == pj_auth_data["cliente_email"]
    print("\n[SUCESSO] Teste 'test_admin_lista_pessoas_juridicas_sucesso' passou!")


@pytest.mark.integration
def test_admin_busca_pf_por_id_sucesso(
    test_client: TestClient, admin_auth_headers: dict, client_auth_data: dict
):
    id_pf = client_auth_data["cliente_id"]
    response: Response = test_client.get(
        f"/clientes/pessoas-fisicas/{id_pf}", headers=admin_auth_headers
    )
    assert response.status_code == 200
    assert response.json()["id_pessoa"] == id_pf
    print("\n[SUCESSO] Teste 'test_admin_busca_pf_por_id_sucesso' passou!")


@pytest.mark.integration
def test_admin_busca_pf_por_id_inexistente_falha_404(
    test_client: TestClient, admin_auth_headers: dict
):
    """
    Testa se a API retorna 404 ao buscar um ID de PF inexistente.
    [Endpoint: GET /clientes/pessoas-fisicas/{id}]
    """
    response: Response = test_client.get(
        "/clientes/pessoas-fisicas/99999", headers=admin_auth_headers
    )
    assert response.status_code == 404
    print(
        "\n[SUCESSO] Teste 'test_admin_busca_pf_por_id_inexistente_falha_404' passou!"
    )


@pytest.mark.integration
def test_admin_atualiza_pf_sucesso(
    test_client: TestClient, admin_auth_headers: dict, client_auth_data: dict
):
    id_pf_para_atualizar = client_auth_data["cliente_id"]

    dados_atualizacao_pf = {
        "email": "email.atualizado@cliente.com",
        "telefone": "111111111",
        "nome_completo": "Nome Atualizado Pelo Admin",
        "cpf": "11122233344",
        "cnh": "44433322211",
        "senha_texto_puro": "novaSenhaAdmin",
        "endereco": {
            "rua": "Rua Atualizada",
            "numero": "99",
            "bairro": "Bairro Novo",
            "cidade": "Cidade Nova",
            "estado": "SP",
            "cep": "99999000",
        },
    }

    response: Response = test_client.put(
        f"/clientes/pessoas-fisicas/{id_pf_para_atualizar}",
        json=dados_atualizacao_pf,
        headers=admin_auth_headers,
    )

    assert response.status_code == 200
    dados_resposta = response.json()
    assert dados_resposta["nome_completo"] == "Nome Atualizado Pelo Admin"
    assert dados_resposta["email"] == "email.atualizado@cliente.com"
    assert dados_resposta["endereco"]["rua"] == "Rua Atualizada"
    print("\n[SUCESSO] Teste 'test_admin_atualiza_pf_sucesso' passou!")


@pytest.mark.integration
def test_admin_atualiza_pj_sucesso(
    test_client: TestClient, admin_auth_headers: dict, pj_auth_data: dict
):
    id_pj_para_atualizar = pj_auth_data["cliente_id"]

    dados_atualizacao_pj = {
        "email": "empresa.atualizada@email.com",
        "telefone": "555555555",
        "razao_social": "Empresa Atualizada Pelo Admin LTDA",
        "cnpj": "99888777000166",
        "senha_texto_puro": "novaSenhaAdminPJ",
        "endereco": {
            "rua": "Rua PJ Atualizada",
            "numero": "999",
            "bairro": "Bairro PJ Novo",
            "cidade": "Cidade PJ Nova",
            "estado": "RJ",
            "cep": "88888000",
        },
    }

    response: Response = test_client.put(
        f"/clientes/pessoas-juridicas/{id_pj_para_atualizar}",
        json=dados_atualizacao_pj,
        headers=admin_auth_headers,
    )

    assert response.status_code == 200
    dados_resposta = response.json()
    assert dados_resposta["razao_social"] == "Empresa Atualizada Pelo Admin LTDA"
    assert dados_resposta["cnpj"] == "99888777000166"
    print("\n[SUCESSO] Teste 'test_admin_atualiza_pj_sucesso' passou!")


@pytest.mark.integration
def test_admin_deleta_pf_sucesso_204(
    test_client: TestClient, admin_auth_headers: dict, client_auth_data: dict
):
    id_pf_para_deletar = client_auth_data["cliente_id"]

    response: Response = test_client.delete(
        f"/clientes/pessoas-fisicas/{id_pf_para_deletar}", headers=admin_auth_headers
    )

    assert response.status_code == 204

    response_get: Response = test_client.get(
        f"/clientes/pessoas-fisicas/{id_pf_para_deletar}", headers=admin_auth_headers
    )
    assert response_get.status_code == 404
    print("\n[SUCESSO] Teste 'test_admin_deleta_pf_sucesso_204' passou!")


@pytest.mark.integration
def test_admin_bloqueia_cliente_pf_sucesso(
    test_client: TestClient, admin_auth_headers: dict, client_auth_data: dict
):
    """
    Novo Teste: Verifica se o admin consegue bloquear um cliente PF (UI Page 17).
    """
    id_pf = client_auth_data["cliente_id"]

    payload = {"novo_status": "bloqueado"}
    response = test_client.patch(
        f"/clientes/pessoas-fisicas/{id_pf}/status",
        json=payload,
        headers=admin_auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["e_ativo"] is False

    payload_ativar = {"novo_status": "ativo"}
    response_ativar = test_client.patch(
        f"/clientes/pessoas-fisicas/{id_pf}/status",
        json=payload_ativar,
        headers=admin_auth_headers,
    )
    assert response_ativar.status_code == 200
    assert response_ativar.json()["e_ativo"] is True
    print("\n[SUCESSO] Teste 'test_admin_bloqueia_cliente_pf_sucesso' passou!")


@pytest.mark.integration
def test_admin_deleta_pf_com_reserva_ativa_falha_400(
    test_client: TestClient, setup_para_teste_reserva: dict
):
    admin_headers = setup_para_teste_reserva["headers_admin"]
    id_pf_com_reserva = setup_para_teste_reserva["id_cliente"]
    id_veiculo = setup_para_teste_reserva["id_veiculo"]
    headers_cliente = setup_para_teste_reserva["headers_cliente"]

    dados_reserva = {
        "veiculo_id": id_veiculo,
        "data_retirada": (datetime.now() + timedelta(days=1)).isoformat(),
        "data_devolucao": (datetime.now() + timedelta(days=5)).isoformat(),
        "seguro_pessoal": True,
    }

    response_criar = test_client.post(
        "/reservas/", json=dados_reserva, headers=headers_cliente
    )

    assert response_criar.status_code == 201, (
        f"Erro ao criar reserva: {response_criar.text}"
    )

    response_delete: Response = test_client.delete(
        f"/clientes/pessoas-fisicas/{id_pf_com_reserva}", headers=admin_headers
    )

    assert response_delete.status_code == 400
    assert "reservas associadas" in response_delete.json()["detail"]
    print(
        "\n[SUCESSO] Teste 'test_admin_deleta_pf_com_reserva_ativa_falha_400' passou!"
    )


@pytest.mark.parametrize("dados_novo_cliente", dados_validos_pessoa_fisica)
def test_criar_pessoa_fisica_sucesso(test_client, dados_novo_cliente):
    response: Response = test_client.post(
        "/clientes/pessoas-fisicas/", json=dados_novo_cliente
    )

    assert response.status_code == 201, f"Falha ao criar cliente: {response.text}"

    dados_resposta = response.json()

    assert dados_resposta["email"] == dados_novo_cliente["email"]
    assert dados_resposta["nome_completo"] == dados_novo_cliente["nome_completo"]
    assert dados_resposta["cpf"] == dados_novo_cliente["cpf"]
    assert dados_resposta["cnh"] == dados_novo_cliente["cnh"]
    assert dados_resposta["endereco"]["rua"] == dados_novo_cliente["endereco"]["rua"]
    if (
        "complemento" in dados_novo_cliente["endereco"]
        and dados_novo_cliente["endereco"]["complemento"]
    ):
        assert (
            dados_resposta["endereco"]["complemento"]
            == dados_novo_cliente["endereco"]["complemento"]
        )
    else:
        assert dados_resposta["endereco"].get("complemento") is None

    assert (
        "id_pessoa" in dados_resposta
        and isinstance(dados_resposta["id_pessoa"], int)
        and dados_resposta["id_pessoa"] > 0
    )
    assert (
        "id_endereco" in dados_resposta["endereco"]
        and isinstance(dados_resposta["endereco"]["id_endereco"], int)
        and dados_resposta["endereco"]["id_endereco"] > 0
    )

    print(
        f"\n[SUCESSO] Cliente '{dados_novo_cliente['nome_completo']}' criado com ID: {dados_resposta['id_pessoa']}"
    )


@pytest.mark.integration
def test_criar_pessoa_fisica_cpf_duplicado(test_client):
    """
    Testa a tentativa de criar uma Pessoa Física com um CPF duplicado (com banco de dados isolado).
    """
    dados_cliente_1 = {
        "email": "duplicado.cpf1@email.com",
        "telefone": "111111111",
        "nome_completo": "Teste Cpf Dup Um",
        "cpf": "12345678900",
        "cnh": "1111111111",
        "senha_texto_puro": "senha123",
        "endereco": {
            "rua": "Rua Dup",
            "numero": "1",
            "bairro": "B Dup",
            "cidade": "C Dup",
            "estado": "DP",
            "cep": "11111",
        },
    }
    response1: Response = test_client.post(
        "/clientes/pessoas-fisicas/", json=dados_cliente_1
    )
    assert response1.status_code == 201

    dados_cliente_2 = {
        "email": "duplicado.cpf2@email.com",
        "telefone": "222222222",
        "nome_completo": "Teste Cpf Dup Dois",
        "cpf": "12345678900",
        "cnh": "2222222222",
        "senha_texto_puro": "senha123",
        "endereco": {
            "rua": "Rua Dup 2",
            "numero": "2",
            "bairro": "B Dup 2",
            "cidade": "C Dup 2",
            "estado": "DP",
            "cep": "22222",
        },
    }
    response2: Response = test_client.post(
        "/clientes/pessoas-fisicas/", json=dados_cliente_2
    )

    assert response2.status_code == 400
    dados_resposta_erro = response2.json()
    assert "CPF" in dados_resposta_erro["detail"]
    print("\n[SUCESSO] Teste 'test_criar_pessoa_fisica_cpf_duplicado' passou")


@pytest.mark.integration
def test_criar_pessoa_fisica_email_invalido(test_client):
    dados_email_invalido = {
        "email": "email-sem-arroba.com",
        "telefone": "333333333",
        "nome_completo": "Teste Email Inv",
        "cpf": "98765432100",
        "cnh": "3333333333",
        "senha_texto_puro": "senha123",
        "endereco": {
            "rua": "Rua Inv",
            "numero": "3",
            "bairro": "B Inv",
            "cidade": "C Inv",
            "estado": "IV",
            "cep": "33333",
        },
    }

    response: Response = test_client.post(
        "/clientes/pessoas-fisicas/", json=dados_email_invalido
    )
    assert response.status_code == 422

    dados_resposta_erro = response.json()
    assert "detail" in dados_resposta_erro
    assert isinstance(dados_resposta_erro["detail"], list)
    assert len(dados_resposta_erro["detail"]) > 0
    assert dados_resposta_erro["detail"][0]["loc"] == ["body", "email"]
    print("\n[SUCESSO] Teste 'test_criar_pessoa_fisica_email_invalido' passou!")


@pytest.mark.integration
def test_criar_pessoa_juridica_sucesso(test_client):
    response: Response = test_client.post(
        "/clientes/pessoas-juridicas/", json=dados_validos_pessoa_juridica
    )

    assert response.status_code == 201, f"Falha ao criar PJ: {response.text}"
    dados_resposta = response.json()

    assert dados_resposta["email"] == dados_validos_pessoa_juridica["email"]
    assert (
        dados_resposta["razao_social"] == dados_validos_pessoa_juridica["razao_social"]
    )
    assert dados_resposta["cnpj"] == dados_validos_pessoa_juridica["cnpj"]
    assert "id_pessoa" in dados_resposta
    print("\n[SUCESSO] Teste 'test_criar_pessoa_juridica_sucesso' passou!")


@pytest.mark.integration
def test_criar_pessoa_juridica_cnpj_duplicado_falha_400(test_client):
    response1: Response = test_client.post(
        "/clientes/pessoas-juridicas/", json=dados_validos_pessoa_juridica
    )
    assert response1.status_code == 201

    dados_pj_2 = dados_validos_pessoa_juridica.copy()
    dados_pj_2["email"] = "empresa.diferente@email.com"

    response2: Response = test_client.post(
        "/clientes/pessoas-juridicas/", json=dados_pj_2
    )

    assert response2.status_code == 400
    assert "cnpj" in response2.json()["detail"].lower()
    print(
        "\n[SUCESSO] Teste 'test_criar_pessoa_juridica_cnpj_duplicado_falha_400' passou!"
    )


@pytest.mark.integration
def test_pessoa_fisica_tenta_acessar_rota_minha_empresa_falha_403(
    test_client: TestClient, client_auth_data: dict
):
    headers_cliente_pf = client_auth_data["headers"]
    dados_associacao = {"cpf_motorista": "000.000.000-00"}

    response_post = test_client.post(
        "/minha-empresa/motoristas", json=dados_associacao, headers=headers_cliente_pf
    )

    assert response_post.status_code == 403
    assert "permitida apenas para Pessoas Jurídicas" in response_post.json()["detail"]
    print(
        "\n[SUCESSO] Teste 'test_pessoa_fisica_tenta_acessar_rota_minha_empresa_falha_403' passou!"
    )


@pytest.mark.integration
def test_pj_adiciona_motorista_sucesso(
    test_client: TestClient, pj_auth_data: dict, client_auth_data: dict
):
    headers_pj = pj_auth_data["headers"]

    cpf_motorista_pf = client_auth_data["cliente_cpf"]
    id_motorista_pf = client_auth_data["cliente_id"]

    dados_associacao = {"cpf_motorista": cpf_motorista_pf}

    response = test_client.post(
        "/minha-empresa/motoristas", json=dados_associacao, headers=headers_pj
    )

    assert response.status_code == 200, f"Falha ao adicionar motorista: {response.text}"
    dados_resposta = response.json()

    assert isinstance(dados_resposta["motoristas"], list)
    assert len(dados_resposta["motoristas"]) > 0
    ids_motoristas_na_lista = [m["id_pessoa"] for m in dados_resposta["motoristas"]]
    assert id_motorista_pf in ids_motoristas_na_lista

    print("\n[SUCESSO] Teste 'test_pj_adiciona_motorista_sucesso' passou!")


@pytest.mark.integration
def test_criar_pessoa_juridica_com_motoristas_validos_sucesso(
    test_client: TestClient, client_auth_data: dict
):
    """
    Testa a criação de uma Pessoa Jurídica já associando um motorista (PF)
    existente no momento do cadastro.
    [Lógica de Negócio em cliente_service.py -> criar_pessoa_juridica - citar: cliente_service.py]
    """
    id_motorista_pf = client_auth_data["cliente_id"]

    dados_pj_com_motorista = {
        "email": "empresa.com.motorista@email.com",
        "telefone": "777777777",
        "razao_social": "Empresa Com Motorista LTDA",
        "cnpj": "77777777000177",
        "senha_texto_puro": "senhaEmpresaMotorista",
        "endereco": {
            "rua": "Rua PJ Motorista",
            "numero": "700",
            "bairro": "Bairro PJ M",
            "cidade": "Cidade PJ M",
            "estado": "PM",
            "cep": "77777000",
        },
        "motoristas_ids": [id_motorista_pf],
    }

    response: Response = test_client.post(
        "/clientes/pessoas-juridicas/", json=dados_pj_com_motorista
    )

    assert response.status_code == 201, (
        f"Falha ao criar PJ com motorista: {response.text}"
    )
    dados_resposta = response.json()

    assert isinstance(dados_resposta["motoristas"], list)
    assert len(dados_resposta["motoristas"]) == 1
    assert dados_resposta["motoristas"][0]["id_pessoa"] == id_motorista_pf
    print(
        "\n[SUCESSO] Teste 'test_criar_pessoa_juridica_com_motoristas_validos_sucesso' passou!"
    )
