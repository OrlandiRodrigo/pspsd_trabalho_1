from concurrent import futures
from datetime import datetime
import grpc
from sqlalchemy.orm import Session
from src.database import engine
from src import models
from src.schemas import reserva_schema
from src.schemas import reserva_schema
from src.models.pessoa import Pessoa, PessoaFisica
import traceback
from fastapi import HTTPException
from src.schemas import reserva_schema


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

REVERSO_COR_PROTO_PARA_PYTHON = {v: k for k, v in MAPEAR_COR_PYTHON_PARA_PROTO.items()}

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

def converter_modelo_reserva_para_proto(reserva_db) -> frota_pb2.Reserva:
    """Converte o modelo do SQLAlchemy em uma mensagem Protobuf de Reserva."""
    
    mapa_status_reserva = {
        StatusReservaEnum.PENDENTE: frota_pb2.STATUS_RESERVA_PENDENTE,
        StatusReservaEnum.CONFIRMADA: frota_pb2.STATUS_RESERVA_CONFIRMADA,
        StatusReservaEnum.EM_ANDAMENTO: frota_pb2.STATUS_RESERVA_EM_ANDAMENTO,
        StatusReservaEnum.FINALIZADA: frota_pb2.STATUS_RESERVA_FINALIZADA,
        StatusReservaEnum.CANCELADA: frota_pb2.STATUS_RESERVA_CANCELADA,
    }
    status_proto = mapa_status_reserva.get(reserva_db.status, frota_pb2.STATUS_RESERVA_NAO_ESPECIFICADO)

    data_criacao_str = reserva_db.data_criacao.isoformat() if reserva_db.data_criacao else ""

    return frota_pb2.Reserva(
        id_reserva=reserva_db.id_reserva,
        data_criacao=data_criacao_str,
        valor_diaria_no_momento=float(reserva_db.valor_diaria_no_momento),
        valor_total_estimado=float(reserva_db.valor_total_estimado),
        status=status_proto,
        cliente_id=reserva_db.cliente_id,
        motorista_id=reserva_db.motorista_id or 0,
        veiculo=converter_modelo_veiculo_para_proto(reserva_db.veiculo),
        
        data_retirada=reserva_db.data_retirada.isoformat() if reserva_db.data_retirada else "",
        data_devolucao=reserva_db.data_devolucao.isoformat() if reserva_db.data_devolucao else "",
        seguro_pessoal=reserva_db.seguro_pessoal,
        seguro_terceiros=reserva_db.seguro_terceiros
    )


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
    
    def CriarVeiculo(self, requisicao: frota_pb2.RequisicaoCriarVeiculo, contexto: grpc.ServicerContext) -> frota_pb2.Veiculo:
        gerador_banco_dados = obter_sessao_banco()
        sessao_banco_dados: Session = next(gerador_banco_dados)

        try:
            cor_python = REVERSO_COR_PROTO_PARA_PYTHON.get(requisicao.cor, CorVeiculoEnum.OUTRO)

            dados_comuns = {
                "placa": requisicao.placa,
                "marca": requisicao.marca,
                "modelo": requisicao.modelo,
                "cor": cor_python,
                "valor_diaria": requisicao.valor_diaria,
                "ano_fabricacao": requisicao.ano_fabricacao,
                "ano_modelo": requisicao.ano_modelo,
                "chassi": requisicao.chassi,
                "renavam": requisicao.renavam if requisicao.renavam else None,
                "capacidade_tanque": requisicao.capacidade_tanque,
                "cambio_automatico": requisicao.cambio_automatico,
                "ar_condicionado": requisicao.ar_condicionado,
                "imagem_url": requisicao.imagem_url if requisicao.imagem_url else None
            }

            if requisicao.tipo_veiculo == frota_pb2.TIPO_VEICULO_PASSEIO:
                from src.schemas.veiculo_schema import SchemaPasseioCriar
                dados_passeio = SchemaPasseioCriar(
                    **dados_comuns,
                    tipo_carroceria=requisicao.passeio.tipo_carroceria if requisicao.passeio.tipo_carroceria else None,
                    qtde_portas=requisicao.passeio.qtde_portas,
                    qtde_passageiros=requisicao.passeio.qtde_passageiros
                )
                novo_veiculo = veiculo_service.criar_veiculo_passeio(dados_passeio, sessao_banco_dados)

            elif requisicao.tipo_veiculo == frota_pb2.TIPO_VEICULO_UTILITARIO:
                from src.schemas.veiculo_schema import SchemaUtilitarioCriar
                dados_util = SchemaUtilitarioCriar(
                    **dados_comuns,
                    tipo_utilitario=requisicao.utilitario.tipo_utilitario if requisicao.utilitario.tipo_utilitario else None,
                    capacidade_carga_kg=requisicao.utilitario.capacidade_carga_kg,
                    capacidade_carga_m3=requisicao.utilitario.capacidade_carga_m3,
                    tipo_carga=requisicao.utilitario.tipo_carga if requisicao.utilitario.tipo_carga else None,
                    qtde_eixos=requisicao.utilitario.qtde_eixos,
                    max_passageiros=requisicao.utilitario.max_passageiros
                )
                novo_veiculo = veiculo_service.criar_veiculo_utilitario(dados_util, sessao_banco_dados)

            elif requisicao.tipo_veiculo == frota_pb2.TIPO_VEICULO_MOTOCICLETA:
                from src.schemas.veiculo_schema import SchemaMotocicletaCriar
                dados_moto = SchemaMotocicletaCriar(
                    **dados_comuns,
                    cilindrada=requisicao.motocicleta.cilindrada,
                    tipo_tracao=requisicao.motocicleta.tipo_tracao if requisicao.motocicleta.tipo_tracao else None,
                    abs=requisicao.motocicleta.abs,
                    partida_eletrica=requisicao.motocicleta.partida_eletrica,
                    modos_pilotagem=requisicao.motocicleta.modos_pilotagem if requisicao.motocicleta.modos_pilotagem else None
                )
                novo_veiculo = veiculo_service.criar_veiculo_motocicleta(dados_moto, sessao_banco_dados)
                
            else:
                contexto.abort(grpc.StatusCode.INVALID_ARGUMENT, "Tipo de veículo não especificado ou inválido.")

            return converter_modelo_veiculo_para_proto(novo_veiculo)

        except grpc.RpcError:
            raise
        except HTTPException as http_erro:
            contexto.abort(grpc.StatusCode.INVALID_ARGUMENT, str(http_erro.detail))
        except Exception as e:
            import traceback
            traceback.print_exc()
            contexto.abort(grpc.StatusCode.INTERNAL, f"Erro interno Python: {str(e)}")
        finally:
            sessao_banco_dados.close()

    def DeletarVeiculo(self, requisicao: frota_pb2.RequisicaoDeletarVeiculo, contexto: grpc.ServicerContext) -> frota_pb2.RespostaDeletarVeiculo:
        gerador_banco_dados = obter_sessao_banco()
        sessao_banco_dados: Session = next(gerador_banco_dados)
        try:
            veiculo_service.deletar_veiculo(id_veiculo=requisicao.id_veiculo, sessao_banco=sessao_banco_dados)
            return frota_pb2.RespostaDeletarVeiculo(sucesso=True, mensagem="Veículo deletado com sucesso.")
        except grpc.RpcError:
            raise
        except HTTPException as http_erro:
            contexto.abort(grpc.StatusCode.INVALID_ARGUMENT, str(http_erro.detail))
        except Exception as e:
            contexto.abort(grpc.StatusCode.INTERNAL, f"Erro interno Python: {str(e)}")
        finally:
            sessao_banco_dados.close()

    def AtualizarVeiculo(self, requisicao: frota_pb2.RequisicaoAtualizarVeiculo, contexto: grpc.ServicerContext) -> frota_pb2.Veiculo:
        gerador_banco_dados = obter_sessao_banco()
        sessao_banco_dados: Session = next(gerador_banco_dados)
        try:
            cor_python = REVERSO_COR_PROTO_PARA_PYTHON.get(requisicao.cor) if requisicao.cor != frota_pb2.COR_VEICULO_NAO_ESPECIFICADA else None

            dados_atualizacao = {}
            if requisicao.placa: dados_atualizacao["placa"] = requisicao.placa
            if requisicao.marca: dados_atualizacao["marca"] = requisicao.marca
            if requisicao.modelo: dados_atualizacao["modelo"] = requisicao.modelo
            if cor_python: dados_atualizacao["cor"] = cor_python
            if requisicao.valor_diaria > 0: dados_atualizacao["valor_diaria"] = requisicao.valor_diaria
            if requisicao.ano_fabricacao > 0: dados_atualizacao["ano_fabricacao"] = requisicao.ano_fabricacao
            if requisicao.ano_modelo > 0: dados_atualizacao["ano_modelo"] = requisicao.ano_modelo
            if requisicao.chassi: dados_atualizacao["chassi"] = requisicao.chassi
            if requisicao.capacidade_tanque > 0: dados_atualizacao["capacidade_tanque"] = requisicao.capacidade_tanque
            
            if requisicao.tipo_veiculo == frota_pb2.TIPO_VEICULO_PASSEIO:
                from src.schemas.veiculo_schema import SchemaPasseioUpdate
                if requisicao.passeio.tipo_carroceria: dados_atualizacao["tipo_carroceria"] = requisicao.passeio.tipo_carroceria
                if requisicao.passeio.qtde_portas > 0: dados_atualizacao["qtde_portas"] = requisicao.passeio.qtde_portas
                
                esquema_update = SchemaPasseioUpdate(**dados_atualizacao)
                veiculo_atualizado = veiculo_service.atualizar_veiculo_passeio(requisicao.id_veiculo, esquema_update, sessao_banco_dados)

            elif requisicao.tipo_veiculo == frota_pb2.TIPO_VEICULO_UTILITARIO:
                from src.schemas.veiculo_schema import SchemaUtilitarioUpdate
                if requisicao.utilitario.capacidade_carga_kg > 0: dados_atualizacao["capacidade_carga_kg"] = requisicao.utilitario.capacidade_carga_kg
                
                esquema_update = SchemaUtilitarioUpdate(**dados_atualizacao)
                veiculo_atualizado = veiculo_service.atualizar_veiculo_utilitario(requisicao.id_veiculo, esquema_update, sessao_banco_dados)

            elif requisicao.tipo_veiculo == frota_pb2.TIPO_VEICULO_MOTOCICLETA:
                from src.schemas.veiculo_schema import SchemaMotocicletaUpdate
                if requisicao.motocicleta.tipo_tracao: dados_atualizacao["tipo_tracao"] = requisicao.motocicleta.tipo_tracao
                
                esquema_update = SchemaMotocicletaUpdate(**dados_atualizacao)
                veiculo_atualizado = veiculo_service.atualizar_veiculo_motocicleta(requisicao.id_veiculo, esquema_update, sessao_banco_dados)
            else:
                contexto.abort(grpc.StatusCode.INVALID_ARGUMENT, "Tipo de veículo inválido.")

            return converter_modelo_veiculo_para_proto(veiculo_atualizado)

        except grpc.RpcError:
            raise
        except HTTPException as http_erro:
            contexto.abort(grpc.StatusCode.INVALID_ARGUMENT, str(http_erro.detail))
        except Exception as e:
            import traceback
            traceback.print_exc()
            contexto.abort(grpc.StatusCode.INTERNAL, f"Erro interno Python: {str(e)}")
        finally:
            sessao_banco_dados.close()


class ImplementacaoServicoGestaoReservas(frota_pb2_grpc.ServicoGestaoReservasServicer):
    """
    Processa simulações financeiras e a criação persistente de reservas.
    """

    def SimularReserva(self, requisicao, contexto):
        gerador_banco_dados = obter_sessao_banco()
        sessao_banco_dados: Session = next(gerador_banco_dados)

        try:
            data_retirada = datetime.fromisoformat(requisicao.data_retirada)
            data_devolucao = datetime.fromisoformat(requisicao.data_devolucao)

            dados_simulacao = reserva_schema.SchemaReservaSimulacao(
                veiculo_id=requisicao.veiculo_id,
                data_retirada=data_retirada,
                data_devolucao=data_devolucao,
                seguro_pessoal=requisicao.seguro_pessoal,
                seguro_terceiros=requisicao.seguro_terceiros
            )

            resultado_calculo = reserva_service.simular_valor_reserva(
                dados_simulacao=dados_simulacao,
                sessao_banco=sessao_banco_dados
            )

            return frota_pb2.RespostaSimularReserva(
                quantidade_diarias=resultado_calculo.quantidade_diarias,
                valor_diarias=float(resultado_calculo.valor_diarias),
                valor_seguros=float(resultado_calculo.valor_seguros),
                valor_total_estimado=float(resultado_calculo.valor_total_estimado)
            )

        except grpc.RpcError:
            raise 
        except HTTPException as http_erro:
            contexto.abort(grpc.StatusCode.INVALID_ARGUMENT, str(http_erro.detail))
        except Exception as e:
            traceback.print_exc() 
            contexto.abort(grpc.StatusCode.INTERNAL, f"Erro interno Python: {str(e)}")
        finally:
            sessao_banco_dados.close()

    def CriarReserva(self, requisicao, contexto):
        gerador_banco_dados = obter_sessao_banco()
        sessao_banco_dados: Session = next(gerador_banco_dados)

        try:
            cliente_fantasma = PessoaFisica()
            cliente_fantasma.id_pessoa = requisicao.cliente_id

            data_retirada = datetime.fromisoformat(requisicao.data_retirada)
            data_devolucao = datetime.fromisoformat(requisicao.data_devolucao)
            id_motorista_tratado = requisicao.motorista_id if requisicao.motorista_id != 0 else None

            dados_para_criar = reserva_schema.SchemaReservaCriar(
                veiculo_id=requisicao.veiculo_id,
                data_retirada=data_retirada,
                data_devolucao=data_devolucao,
                seguro_pessoal=requisicao.seguro_pessoal,
                seguro_terceiros=requisicao.seguro_terceiros,
                motorista_id=id_motorista_tratado
            )

            reserva_criada = reserva_service.criar_reserva(
                dados_entrada_reserva=dados_para_criar,
                cliente_logado=cliente_fantasma,
                sessao_banco=sessao_banco_dados
            )

            return converter_modelo_reserva_para_proto(reserva_criada)

        except grpc.RpcError:
            raise 
        except HTTPException as http_erro:
            contexto.abort(grpc.StatusCode.INVALID_ARGUMENT, str(http_erro.detail))
        except Exception as e:
            import traceback
            traceback.print_exc()
            contexto.abort(grpc.StatusCode.INTERNAL, f"Erro interno Python: {str(e)}")
        finally:
            sessao_banco_dados.close()

    def ListarMinhasReservas(self, requisicao, contexto):
        gerador_banco_dados = obter_sessao_banco()
        sessao_banco_dados: Session = next(gerador_banco_dados)

        try:
            cliente_fantasma = PessoaFisica()
            cliente_fantasma.id_pessoa = requisicao.cliente_id

            lista_reservas_banco = reserva_service.listar_reservas_por_cliente(
                cliente_logado=cliente_fantasma, 
                sessao_banco=sessao_banco_dados
            )
            
            lista_proto = []
            for reserva in lista_reservas_banco:
                lista_proto.append(converter_modelo_reserva_para_proto(reserva))

            return frota_pb2.RespostaListaReservas(reservas=lista_proto)

        except grpc.RpcError:
            raise 
        except HTTPException as http_erro:
            contexto.abort(grpc.StatusCode.INVALID_ARGUMENT, str(http_erro.detail))
        except Exception as e:
            import traceback
            traceback.print_exc()
            contexto.abort(grpc.StatusCode.INTERNAL, f"Erro interno Python: {str(e)}")
        finally:
            sessao_banco_dados.close()
    
    def CancelarReserva(self, requisicao, contexto):
        gerador_banco_dados = obter_sessao_banco()
        sessao_banco_dados: Session = next(gerador_banco_dados)

        try:
            reserva_service.buscar_reserva_por_id_e_cliente(
                id_reserva=requisicao.id_reserva,
                id_cliente=requisicao.cliente_id,
                sessao_banco=sessao_banco_dados
            )

            reserva_cancelada = reserva_service.cancelar_reserva(
                id_reserva=requisicao.id_reserva,
                sessao_banco=sessao_banco_dados
            )

            return converter_modelo_reserva_para_proto(reserva_cancelada)

        except grpc.RpcError:
            raise
        except HTTPException as http_erro:
            contexto.abort(grpc.StatusCode.INVALID_ARGUMENT, str(http_erro.detail))
        except Exception as e:
            import traceback
            traceback.print_exc()
            contexto.abort(grpc.StatusCode.INTERNAL, f"Erro interno: {str(e)}")
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