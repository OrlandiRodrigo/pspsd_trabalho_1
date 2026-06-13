from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
import pytest
from src.models.reserva import StatusReservaEnum
from src.models.veiculo import StatusVeiculoEnum
from src.schemas import reserva_schema
from src.services.reserva_service import criar_reserva, finalizar_reserva


@pytest.mark.unit
def test_finalizar_reserva_calcula_multa_corretamente():
    mock_sessao = MagicMock()
    mock_veiculo = MagicMock()
    mock_reserva = MagicMock()

    agora = datetime.now()
    
    mock_reserva.status = StatusReservaEnum.EM_ANDAMENTO
    
    mock_reserva.data_retirada = agora - timedelta(days=5) 
    
    mock_reserva.data_devolucao = agora - timedelta(days=1) 
    
    mock_reserva.valor_diaria_no_momento = 100.00
    mock_reserva.valor_total_estimado = 500.00
    mock_reserva.veiculo = mock_veiculo

    mock_sessao.query.return_value.options.return_value.get.return_value = mock_reserva

    reserva_finalizada = finalizar_reserva(id_reserva=1, sessao_banco=mock_sessao)

    assert reserva_finalizada.status == StatusReservaEnum.FINALIZADA
    assert mock_veiculo.status == StatusVeiculoEnum.DISPONIVEL

    assert reserva_finalizada.valor_total_estimado > 500.00

    mock_sessao.commit.assert_called()


@pytest.mark.unit
def test_criar_reserva_nasce_com_status_pendente():
    mock_sessao = MagicMock()
    mock_cliente_logado = MagicMock()
    mock_cliente_logado.id_pessoa = 1

    mock_veiculo = MagicMock()
    mock_veiculo.status = StatusVeiculoEnum.DISPONIVEL
    mock_veiculo.valor_diaria = 100.00
    mock_sessao.get.return_value = mock_veiculo

    inicio = datetime.now() + timedelta(days=1)
    fim = datetime.now() + timedelta(days=5)

    dados_entrada = reserva_schema.SchemaReservaCriar(
        veiculo_id=1, data_retirada=inicio, data_devolucao=fim
    )

    with patch("src.services.reserva_service.Reserva") as mock_Reserva_Classe:
        mock_instancia = MagicMock()
        mock_Reserva_Classe.return_value = mock_instancia

        criar_reserva(
            dados_entrada_reserva=dados_entrada,
            cliente_logado=mock_cliente_logado,
            sessao_banco=mock_sessao,
        )

        args, kwargs = mock_Reserva_Classe.call_args
        assert kwargs["status"] == StatusReservaEnum.PENDENTE
