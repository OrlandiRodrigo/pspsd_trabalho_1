from concurrent import futures
import grpc
from sqlalchemy.orm import Session

import autenticacao_pb2
import autenticacao_pb2_grpc
from src.database import engine
from src import models
from src.services import cliente_auth_service
from src.schemas import cliente_schema
from src.services import cliente_service

from src.dependencies import obter_sessao_banco
from src.services import auth_service
from src.schemas.auth_schema import SchemaToken, SchemaFuncionarioCriar
from src import seguranca
import traceback

PORTA_SERVIDOR_AUTENTICACAO = 50051
MAXIMO_TRABALHADORES_CONCORRENTES = 10


class ImplementacaoServicoAutenticacao(autenticacao_pb2_grpc.ServicoAutenticacaoServicer):
    
    def Login(
        self,
        requisicao: autenticacao_pb2.RequisicaoLogin,
        contexto: grpc.ServicerContext
    ) -> autenticacao_pb2.RespostaToken:
        
        gerador_banco_dados = obter_sessao_banco()
        sessao_banco_dados: Session = next(gerador_banco_dados)
        
        funcionario_autenticado = None
        mensagem_erro_interno = None
        
        try:
            funcionario_autenticado = auth_service.autenticar_funcionario(
                sessao_banco=sessao_banco_dados,
                email_formulario=requisicao.email,
                senha_formulario=requisicao.senha
            )
        except Exception as erro_generico:
            print("ERRO FATAL NA REGRA DE NEGOCIO:", flush=True)
            traceback.print_exc()
            mensagem_erro_interno = str(getattr(erro_generico, "detail", str(erro_generico)))
        finally:
            sessao_banco_dados.close()

        if mensagem_erro_interno:
            contexto.abort(grpc.StatusCode.INTERNAL, mensagem_erro_interno)
            
        if not funcionario_autenticado:
            contexto.abort(
                grpc.StatusCode.UNAUTHENTICATED,
                "Credenciais inválidas, usuário não encontrado ou inativo."
            )

        token_jwt = seguranca.criar_token_acesso(
            dados={"sub": funcionario_autenticado.email, "tipo_perfil": "admin"}
        )
        
        return autenticacao_pb2.RespostaToken(
            access_token=token_jwt,
            token_type="bearer"
        )
    
    def LoginCliente(
        self,
        requisicao: autenticacao_pb2.RequisicaoLogin,
        contexto: grpc.ServicerContext
    ) -> autenticacao_pb2.RespostaToken:
        
        gerador_banco_dados = obter_sessao_banco()
        sessao_banco_dados: Session = next(gerador_banco_dados)
        
        cliente_autenticado = None
        
        try:
            cliente_autenticado = cliente_auth_service.autenticar_cliente(
                sessao_banco=sessao_banco_dados,
                email_formulario=requisicao.email,
                senha_formulario=requisicao.senha
            )
        except Exception as e:
            contexto.abort(grpc.StatusCode.INTERNAL, str(e))
        finally:
            sessao_banco_dados.close()

        if not cliente_autenticado:
            contexto.abort(
                grpc.StatusCode.UNAUTHENTICATED,
                "Credenciais inválidas ou conta inativa."
            )

        tipo_usuario = "pessoa_fisica"
        if type(cliente_autenticado).__name__ == "PessoaJuridica":
            tipo_usuario = "pessoa_juridica"

        token_jwt = seguranca.criar_token_acesso(
            dados={
                "sub": str(cliente_autenticado.id_pessoa), 
                "email": cliente_autenticado.email, 
                "tipo": tipo_usuario
            }
        )
        
        return autenticacao_pb2.RespostaToken(
            access_token=token_jwt,
            token_type="bearer"
        )
    
    def CriarPessoaFisica(self, requisicao, contexto):
        gerador_banco_dados = obter_sessao_banco()
        sessao_banco_dados = next(gerador_banco_dados)
        try:
            endereco_dict = {
                "rua": requisicao.endereco.rua, "numero": requisicao.endereco.numero,
                "complemento": requisicao.endereco.complemento, "bairro": requisicao.endereco.bairro,
                "cidade": requisicao.endereco.cidade, "estado": requisicao.endereco.estado, "cep": requisicao.endereco.cep
            }
            dados_cliente = cliente_schema.SchemaPessoaFisicaCriar(
                email=requisicao.email, telefone=requisicao.telefone, nome_completo=requisicao.nome_completo,
                cpf=requisicao.cpf, cnh=requisicao.cnh if requisicao.cnh else None,
                senha_texto_puro=requisicao.senha_texto_puro, endereco=endereco_dict
            )
            novo_cliente = cliente_service.criar_pessoa_fisica(dados_cliente, sessao_banco_dados)
            return autenticacao_pb2.RespostaCriarCliente(id_pessoa=novo_cliente.id_pessoa, email=novo_cliente.email)
        except Exception as e:
            contexto.abort(grpc.StatusCode.INVALID_ARGUMENT, str(getattr(e, "detail", str(e))))
        finally:
            sessao_banco_dados.close()

    def CriarPessoaJuridica(self, requisicao, contexto):
        gerador_banco_dados = obter_sessao_banco()
        sessao_banco_dados = next(gerador_banco_dados)
        try:
            endereco_dict = {
                "rua": requisicao.endereco.rua, "numero": requisicao.endereco.numero,
                "complemento": requisicao.endereco.complemento, "bairro": requisicao.endereco.bairro,
                "cidade": requisicao.endereco.cidade, "estado": requisicao.endereco.estado, "cep": requisicao.endereco.cep
            }
            dados_cliente = cliente_schema.SchemaPessoaJuridicaCriar(
                email=requisicao.email, telefone=requisicao.telefone, razao_social=requisicao.razao_social,
                nome_fantasia=requisicao.nome_fantasia if requisicao.nome_fantasia else None,
                cnpj=requisicao.cnpj, senha_texto_puro=requisicao.senha_texto_puro, endereco=endereco_dict
            )
            novo_cliente = cliente_service.criar_pessoa_juridica(dados_cliente, sessao_banco_dados)
            return autenticacao_pb2.RespostaCriarCliente(id_pessoa=novo_cliente.id_pessoa, email=novo_cliente.email)
        except Exception as e:
            contexto.abort(grpc.StatusCode.INVALID_ARGUMENT, str(getattr(e, "detail", str(e))))
        finally:
            sessao_banco_dados.close()
    
    def ValidarToken(
        self,
        requisicao: autenticacao_pb2.RequisicaoValidarToken,
        contexto: grpc.ServicerContext
    ) -> autenticacao_pb2.RespostaValidacao:
        
        print("\n--- INICIANDO VALIDACAO DE TOKEN ---", flush=True)
        print(f"Token recebido (tamanho {len(requisicao.token)}): '{requisicao.token}'", flush=True)
        
        try:
            payload = seguranca.verificar_token(requisicao.token)
            print(f"Resultado do Payload: {payload}", flush=True)
        except Exception as e:
            print(f"Excecao inesperada na verificacao: {e}", flush=True)
            payload = None
            
        if not payload:
            print("Status: NEGADO", flush=True)
            return autenticacao_pb2.RespostaValidacao(
                e_valido=False,
                subject_payload="",
                tipo_usuario=""
            )
            
        print("Status: AUTORIZADO", flush=True)
        return autenticacao_pb2.RespostaValidacao(
            e_valido=True,
            subject_payload=payload.get("sub", ""),
            #tipo_usuario=payload.get("tipo_perfil", "")
        )

class ImplementacaoServicoFuncionario(autenticacao_pb2_grpc.ServicoFuncionarioServicer):
    
    def CriarFuncionario(
        self,
        requisicao: autenticacao_pb2.RequisicaoCriarFuncionario,
        contexto: grpc.ServicerContext
    ) -> autenticacao_pb2.Funcionario:
        
        gerador_banco_dados = obter_sessao_banco()
        sessao_banco_dados: Session = next(gerador_banco_dados)
        
        novo_funcionario = None
        mensagem_erro_interno = None
        
        try:
            dados_criar = SchemaFuncionarioCriar(
                email=requisicao.email,
                nome_completo=requisicao.nome_completo,
                senha_texto_puro=requisicao.senha_texto_puro,
                e_admin=requisicao.e_admin,
                e_ativado=requisicao.e_ativado
            )
            
            novo_funcionario = auth_service.criar_funcionario(
                sessao_banco=sessao_banco_dados,
                dados_funcionario=dados_criar
            )

            
        except Exception as erro_generico:
            print("ERRO NA CRIAÇÃO DE FUNCIONÁRIO:", flush=True)
            traceback.print_exc()
            mensagem_erro_interno = str(getattr(erro_generico, "detail", str(erro_generico)))
        finally:
            sessao_banco_dados.close()
            
        if mensagem_erro_interno:
            contexto.abort(grpc.StatusCode.INTERNAL, mensagem_erro_interno)
            
        return autenticacao_pb2.Funcionario(
            id_funcionario=novo_funcionario.id_funcionario, 
            email=novo_funcionario.email,
            nome_completo=novo_funcionario.nome_completo,
            e_admin=novo_funcionario.e_admin,
            e_ativado=novo_funcionario.e_ativado
        )

def iniciar_servidor_grpc() -> None:
    
    models.Base.metadata.create_all(bind=engine)
    
    servidor = grpc.server(
        futures.ThreadPoolExecutor(max_workers=MAXIMO_TRABALHADORES_CONCORRENTES)
    )
    
    autenticacao_pb2_grpc.add_ServicoAutenticacaoServicer_to_server(
        ImplementacaoServicoAutenticacao(),
        servidor
    )

    autenticacao_pb2_grpc.add_ServicoFuncionarioServicer_to_server(
        ImplementacaoServicoFuncionario(),
        servidor
    )
    
    endereco_conexao = f"[::]:{PORTA_SERVIDOR_AUTENTICACAO}"
    servidor.add_insecure_port(endereco_conexao)
    
    print(f"Servidor gRPC de Autenticação iniciado na porta {PORTA_SERVIDOR_AUTENTICACAO}...", flush=True)
    
    servidor.start()
    servidor.wait_for_termination()


if __name__ == "__main__":
    iniciar_servidor_grpc()