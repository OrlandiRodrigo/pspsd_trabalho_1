import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

# Testes Unitários para a lógica de negócio dos Serviços de Veículo.
# Cobre: Validações de regras de negócio (ex: ano) e lógica de deleção.

from src.services.veiculo_service import criar_veiculo_passeio, deletar_veiculo
from src.models.veiculo import StatusVeiculoEnum
from src.schemas import veiculo_schema


@pytest.mark.unit
def test_criar_veiculo_ano_modelo_anterior_fabricacao_falha(mocker):
    mock_sessao = MagicMock()

    dados_invalidos = veiculo_schema.SchemaPasseioCriar(
        placa="ANO1234",
        marca="Teste",
        modelo="Teste",
        cor="Preto",
        valor_diaria=100.0,
        ano_fabricacao=2021,
        ano_modelo=2020,
        chassi="CHASSI123",
        capacidade_tanque=50.0,
        qtde_portas=4,
    )

    mock_sessao.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        criar_veiculo_passeio(
            dados_entrada_veiculo=dados_invalidos, sessao_banco=mock_sessao
        )

    assert exc_info.value.status_code == 400
    assert "anterior ao ano de fabricação" in exc_info.value.detail


@pytest.mark.unit
def test_deletar_veiculo_com_reservas_falha(mocker):
    mock_sessao = MagicMock()
    mock_veiculo = MagicMock()
    mock_veiculo.reservas = [MagicMock()]
    mock_veiculo.status = StatusVeiculoEnum.DISPONIVEL

    mocker.patch(
        "src.services.veiculo_service.buscar_veiculo_por_id", return_value=mock_veiculo
    )

    with pytest.raises(HTTPException) as exc_info:
        deletar_veiculo(id_veiculo=1, sessao_banco=mock_sessao)

    assert exc_info.value.status_code == 400
    assert "reservas associadas" in exc_info.value.detail


@pytest.mark.unit
def test_deletar_veiculo_com_status_alugado_falha(mocker):
    mock_sessao = MagicMock()
    mock_veiculo = MagicMock()
    mock_veiculo.reservas = []
    mock_veiculo.status = StatusVeiculoEnum.ALUGADO

    mocker.patch(
        "src.services.veiculo_service.buscar_veiculo_por_id", return_value=mock_veiculo
    )

    with pytest.raises(HTTPException) as exc_info:
        deletar_veiculo(id_veiculo=1, sessao_banco=mock_sessao)

    assert exc_info.value.status_code == 400
    assert "status é 'alugado'" in exc_info.value.detail


@pytest.mark.unit
def test_criar_veiculo_placa_duplicada_falha():
    mock_sessao = MagicMock()
    dados_entrada = veiculo_schema.SchemaPasseioCriar(
        placa="DUPLICADA",
        marca="Teste",
        modelo="Teste",
        cor="Preto",
        valor_diaria=100.0,
        ano_fabricacao=2020,
        ano_modelo=2021,
        chassi="CHASSI123",
        capacidade_tanque=50.0,
        qtde_portas=4,
    )

    mock_sessao.query.return_value.filter.return_value.first.return_value = MagicMock()

    with pytest.raises(HTTPException) as exc_info:
        criar_veiculo_passeio(
            dados_entrada_veiculo=dados_entrada, sessao_banco=mock_sessao
        )

    assert exc_info.value.status_code == 400
    assert "placa" in exc_info.value.detail.lower()


@pytest.mark.unit
def test_criar_veiculo_chassi_duplicado_falha():
    mock_sessao = MagicMock()
    dados_entrada = veiculo_schema.SchemaPasseioCriar(
        placa="PLACAUNICA",
        marca="Teste",
        modelo="Teste",
        cor="Preto",
        valor_diaria=100.0,
        ano_fabricacao=2020,
        ano_modelo=2021,
        chassi="CHASSIDUPLICADO",
        capacidade_tanque=50.0,
        qtde_portas=4,
    )

    mock_sessao.query.return_value.filter.return_value.first.side_effect = [
        None,
        MagicMock(),
    ]

    with pytest.raises(HTTPException) as exc_info:
        criar_veiculo_passeio(
            dados_entrada_veiculo=dados_entrada, sessao_banco=mock_sessao
        )

    assert exc_info.value.status_code == 400
    assert "chassi" in exc_info.value.detail.lower()
