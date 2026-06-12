from concurrent import futures
from datetime import datetime
import grpc
from sqlalchemy.orm import Session
from src.database import engine
from src import models

import frota_pb2
import frota_pb2_grpc

from src.dependencies import obter_sessao_banco
from src.services import veiculo_service, reserva_service
from src.models.enums import (
    TipoVeiculoEnum,
    StatusVeiculoEnum,
    CorVeiculoEnum,
    StatusReservaEnum
)

# CONFIGURAÇÕES 

PORTA_SERVIDOR_FROTA = 50052
MAXIMO_TRABALHADORES_CONCORRENTES = 10

MAPEAR_COR_PYTHON_PARA_PROTO = {
    CorVeiculoEnum.PRETO: frota_pb2.COR_VEICULO_PRETO,
    CorVeiculoEnum.BRANCO: frota_pb2.COR_VEICULO_BRANCO,
    CorVeiculoEnum.PRATA: frota_pb2.COR_VEICULO_PRATA,
    CorVeiculoEnum.CINZA: frota_pb2.COR_VEICULO_CINZA,
    CorVeiculoEnum.VERMELHO: frota_pb2.COR_VEICULO_VERMELHO,
    CorVeiculoEnum.AZUL: frota_pb2.COR_VEICULO_AZUL,
    CorVeiculoEnum.VERDE: frota_pb2.COR_VEICULO_VERDE,
    CorVeiculoEnum.AMARELO: frota_pb2.COR_VEICULO_AMARELO,
    CorVeiculoEnum.OUTRO: frota_pb2.COR_VEICULO_OUTRO,
}

MAPEAR_STATUS_VEICULO_PYTHON_PARA_PROTO = {
    StatusVeiculoEnum.DISPONIVEL: frota_pb2.STATUS_VEICULO_DISPONIVEL,
    StatusVeiculoEnum.RESERVADO: frota_pb2.STATUS_VEICULO_RESERVADO,
    StatusVeiculoEnum.ALUGADO: frota_pb2.STATUS_VEICULO_ALUGADO,
    StatusVeiculoEnum.EM_MANUTENCAO: frota_pb2.STATUS_VEICULO_EM_MANUTENCAO,
    StatusVeiculoEnum.INDISPONIVEL: frota_pb2.STATUS_VEICULO_INDISPONIVEL,
}

MAPEAR_STATUS_RESERVA_PYTHON_PARA_PROTO = {
    StatusReservaEnum.PENDENTE: frota_pb2.STATUS_RESERVA_PENDENTE,
    StatusReservaEnum.CONFIRMADA: frota_pb2.STATUS_RESERVA_CONFIRMADA,
    StatusReservaEnum.EM_ANDAMENTO: frota_pb2.STATUS_RESERVA_EM_ANDAMENTO,
    StatusReservaEnum.FINALIZADA: frota_pb2.STATUS_RESERVA_FINALIZADA,
    StatusReservaEnum.CANCELADA: frota_pb2.STATUS_RESERVA_CANCELADA,
}



# CONVERTERS / MAPPERS

def converter_modelo_veiculo_para_proto(veiculo_banco_dados) -> frota_pb2.Veiculo:
    """
    Converte um objeto de modelo SQLAlchemy de veículo para a mensagem gRPC.
    Trata o polimorfismo mapeando os campos específicos dentro do bloco 'oneof'.
    """
    cor_convertida = MAPEAR_COR_PYTHON_PARA_PROTO.get(
        veiculo_banco_dados.cor, frota_pb2.COR_VEICULO_OUTRO
    )
    status_convertido = MAPEAR_STATUS_VEICULO_PYTHON_PARA_PROTO.get(
        veiculo_banco_dados.status, frota_pb2.STATUS_VEICULO_NAO_ESPECIFICADO
    )

    veiculo_proto = frota_pb2.Veiculo(
        id_veiculo=veiculo_banco_dados.id_veiculo,
        placa=veiculo_banco_dados.placa,
        marca=veiculo_banco_dados.marca,
        modelo=veiculo_banco_dados.modelo,
        cor=cor_convertida,
        valor_diaria=float(veiculo_banco_dados.valor_diaria),
        ano_fabricacao=veiculo_banco_dados.ano_fabricacao,
        ano_modelo=veiculo_banco_dados.ano_modelo,
        chassi=veiculo_banco_dados.chassi,
        renavam=veiculo_banco_dados.renavam or "",
        capacidade_tanque=float(veiculo_banco_dados.capacidade_tanque),
        cambio_automatico=veiculo_banco_dados.cambio_automatico,
        ar_condicionado=veiculo_banco_dados.ar_condicionado,
        imagem_url=veiculo_banco_dados.imagem_url or "",
        status=status_convertido
    )

    if veiculo_banco_dados.tipo_veiculo == TipoVeiculoEnum.PASSEIO:
        veiculo_proto.tipo_veiculo = frota_pb2.TIPO_VEICULO_PASSEIO
        veiculo_proto.passeio.CopyFrom(frota_pb2.DetalhesPasseio(
            tipo_carroceria=veiculo_banco_dados.tipo_carroceria or "",
            qtde_portas=veiculo_banco_dados.qtde_portas or 0,
            qtde_passageiros=veiculo_banco_dados.qtde_passageiros or 0
        ))
    elif veiculo_banco_dados.tipo_veiculo == TipoVeiculoEnum.UTILITARIO:
        veiculo_proto.tipo_veiculo = frota_pb2.TIPO_VEICULO_UTILITARIO
        veiculo_proto.utilitario.CopyFrom(frota_pb2.DetalhesUtilitario(
            tipo_utilitario=veiculo_banco_dados.tipo_utilitario or "",
            capacidade_carga_kg=float(veiculo_banco_dados.capacidade_carga_kg or 0.0),
            capacidade_carga_m3=float(veiculo_banco_dados.capacidade_carga_m3 or 0.0),
            tipo_carga=veiculo_banco_dados.tipo_carga or "",
            qtde_eixos=veiculo_banco_dados.qtde_eixos or 0,
            max_passageiros=veiculo_banco_dados.max_passageiros or 0
        ))
    elif veiculo_banco_dados.tipo_veiculo == TipoVeiculoEnum.MOTOCICLETA:
        veiculo_proto.tipo_veiculo = frota_pb2.TIPO_VEICULO_MOTOCICLETA
        veiculo_proto.motocicleta.CopyFrom(frota_pb2.DetalhesMotocicleta(
            cilindrada=veiculo_banco_dados.cilindrada or 0,
            tipo_tracao=veiculo_banco_dados.tipo_tracao or "",
            abs=veiculo_banco_dados.abs or False,
            partida_eletrica=veiculo_banco_dados.partida_eletrica or False,
            modos_pilotagem=veiculo_banco_dados.modos_pilotagem or ""
        ))

    return veiculo_proto


# SERVIÇOS gRPC

class ImplementacaoServicoGestaoVeiculos(frota_pb2_grpc.ServicoGestaoVeiculosServicer):
    """
    Gerencia o catálogo de veículos exposto para a rede gRPC.
    """

    def ObterVeiculo(
        self,
        requisicao: frota_pb2.RequisicaoObterVeiculoPorId,
        contexto: grpc.ServicerContext
    ) -> frota_pb2.Veiculo:
        
        gerador_banco_dados = obter_sessao_banco()
        sessao_banco_dados: Session = next(gerador_banco_dados)

        try:
            veiculo_encontrado = veiculo_service.buscar_veiculo_por_id(
                id_veiculo=requisicao.id_veiculo,
                sessao_banco=sessao_banco_dados
            )
            return converter_modelo_veiculo_para_proto(veiculo_encontrado)

        except Exception as e:
            contexto.abort(grpc.StatusCode.NOT_FOUND, str(e))
        finally:
            sessao_banco_dados.close()

    def ListarVeiculos(
        self,
        requisicao: frota_pb2.RequisicaoListarVeiculos,
        contexto: grpc.ServicerContext
    ) -> frota_pb2.RespostaListaVeiculos:
        
        gerador_banco_dados = obter_sessao_banco()
        sessao_banco_dados: Session = next(gerador_banco_dados)

        try:
            lista_veiculos_banco = veiculo_service.listar_veiculos(sessao_banco=sessao_banco_dados)
            lista_veiculos_proto = []

            for veiculo in lista_veiculos_banco:
                lista_veiculos_proto.append(converter_modelo_veiculo_para_proto(veiculo))

            return frota_pb2.RespostaListaVeiculos(veiculos=lista_veiculos_proto)

        finally:
            sessao_banco_dados.close()


class ImplementacaoServicoGestaoReservas(frota_pb2_grpc.ServicoGestaoReservasServicer):
    """
    Processa simulações financeiras e a criação persistente de reservas.
    """

    def SimularReserva(
        self,
        requisicao: frota_pb2.RequisicaoSimularReserva,
        contexto: grpc.ServicerContext
    ) -> frota_pb2.RespostaSimularReserva:
        
        gerador_banco_dados = obter_sessao_banco()
        sessao_banco_dados: Session = next(gerador_banco_dados)

        try:
            data_retirada = datetime.fromisoformat(requisicao.data_retirada)
            data_devolucao = datetime.fromisoformat(requisicao.data_devolucao)

            resultado_calculo = reserva_service.calcular_valores_estimados(
                db=sessao_banco_dados,
                veiculo_id=requisicao.veiculo_id,
                data_retirada=data_retirada,
                data_devolucao=data_devolucao,
                seguro_pessoal=requisicao.seguro_pessoal,
                seguro_terceiros=requisicao.seguro_terceiros
            )

            return frota_pb2.RespostaSimularReserva(
                quantidade_diarias=resultado_calculo["quantidade_diarias"],
                valor_diarias=float(resultado_calculo["valor_diarias"]),
                valor_seguros=float(resultado_calculo["valor_seguros"]),
                valor_total_estimado=float(resultado_calculo["valor_total_estimado"])
            )

        except ValueError as erro_formatacao:
            contexto.abort(grpc.StatusCode.INVALID_ARGUMENT, str(erro_formatacao))
        finally:
            sessao_banco_dados.close()

    def CriarReserva(
        self,
        requisicao: frota_pb2.RequisicaoCriarReserva,
        contexto: grpc.ServicerContext
    ) -> frota_pb2.Reserva:
        
        gerador_banco_dados = obter_sessao_banco()
        sessao_banco_dados: Session = next(gerador_banco_dados)

        try:
            data_retirada = datetime.fromisoformat(requisicao.data_retirada)
            data_devolucao = datetime.fromisoformat(requisicao.data_devolucao)

            id_motorista_tratado = requisicao.motorista_id if requisicao.motorista_id != 0 else None

            reserva_criada = reserva_service.registrar_nova_reserva(
                db=sessao_banco_dados,
                cliente_id=requisicao.cliente_id,
                veiculo_id=requisicao.veiculo_id,
                data_retirada=data_retirada,
                data_devolucao=data_devolucao,
                seguro_pessoal=requisicao.seguro_pessoal,
                seguro_terceiros=requisicao.seguro_terceiros,
                motorista_id=id_motorista_tratado
            )

            status_reserva_convertido = MAPEAR_STATUS_RESERVA_PYTHON_PARA_PROTO.get(
                reserva_criada.status, frota_pb2.STATUS_RESERVA_PENDENTE
            )

            return frota_pb2.Reserva(
                id_reserva=reserva_criada.id_reserva,
                data_criacao=reserva_criada.data_criacao.isoformat(),
                valor_diaria_no_momento=float(reserva_criada.valor_diaria_no_momento),
                valor_total_estimado=float(reserva_criada.valor_total_estimado),
                status=status_reserva_convertido,
                cliente_id=reserva_criada.cliente_id,
                motorista_id=reserva_criada.motorista_id or 0,
                veiculo=converter_modelo_veiculo_para_proto(reserva_criada.veiculo)
            )

        except Exception as erro_execucao:
            contexto.abort(grpc.StatusCode.INTERNAL, f"Falha ao registrar reserva: {str(erro_execucao)}")
        finally:
            sessao_banco_dados.close()


# EXECUÇÃO DO INICIALIZADOR DO SERVIDOR

def iniciar_servidor_grpc_frota() -> None:
    """Configura o ambiente de execução e liga as portas do servidor gRPC."""

    models.Base.metadata.create_all(bind=engine)

    servidor = grpc.server(
        futures.ThreadPoolExecutor(max_workers=MAXIMO_TRABALHADORES_CONCORRENTES)
    )

    frota_pb2_grpc.add_ServicoGestaoVeiculosServicer_to_server(
        ImplementacaoServicoGestaoVeiculos(), servidor
    )
    frota_pb2_grpc.add_ServicoGestaoReservasServicer_to_server(
        ImplementacaoServicoGestaoReservas(), servidor
    )

    endereco_escuta_rede = f"[::]:{PORTA_SERVIDOR_FROTA}"
    servidor.add_insecure_port(endereco_escuta_rede)

    print(f"Servidor gRPC de Frota (Módulo B) operando com sucesso na porta {PORTA_SERVIDOR_FROTA}...")
    servidor.start()
    servidor.wait_for_termination()


if __name__ == "__main__":
    iniciar_servidor_grpc_frota()