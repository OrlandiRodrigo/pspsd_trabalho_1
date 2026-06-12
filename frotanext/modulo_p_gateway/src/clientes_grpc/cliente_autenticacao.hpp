#ifndef CLIENTE_AUTENTICACAO_HPP
#define CLIENTE_AUTENTICACAO_HPP

#include <string>
#include <memory>
#include <grpcpp/grpcpp.h>
#include <iostream>

#include "../../dependencias/json.hpp"
using json = nlohmann::json;

#include "../../protos_gerados/autenticacao.grpc.pb.h"

struct ResultadoLogin {
    bool sucesso;
    std::string token;
    std::string mensagem_erro;
};

struct ResultadoCriacaoCliente {
    bool sucesso;
    int id_pessoa;
    std::string email;
    std::string mensagem_erro;
};

class ClienteAutenticacao {
private:
    std::unique_ptr<autenticacao::ServicoAutenticacao::Stub> stub_autenticacao_;

public:
    explicit ClienteAutenticacao(std::shared_ptr<grpc::Channel> canal_comunicacao)
        : stub_autenticacao_(autenticacao::ServicoAutenticacao::NewStub(canal_comunicacao)) {}

    autenticacao::RespostaValidacao ValidarSessaoSegura(const std::string& token_jwt) {
        autenticacao::RequisicaoValidarToken requisicao_proto;
        requisicao_proto.set_token(token_jwt);

        autenticacao::RespostaValidacao resposta_proto;
        grpc::ClientContext contexto_rede;

        grpc::Status status_execucao = stub_autenticacao_->ValidarToken(&contexto_rede, requisicao_proto, &resposta_proto);

        if (!status_execucao.ok()) {
            std::cout << "[gRPC ERRO REDE] ValidarToken falhou. Codigo: " << status_execucao.error_code() 
                      << " | Mensagem: " << status_execucao.error_message() << std::endl;
            autenticacao::RespostaValidacao resposta_falha;
            resposta_falha.set_e_valido(false);
            return resposta_falha;
        }

        std::cout << "[gRPC SUCESSO] Resposta recebida. Token e_valido = " << resposta_proto.e_valido() << std::endl;
        return resposta_proto;
    }

    ResultadoLogin FazerLoginSeguro(const std::string& email_usuario, const std::string& senha_texto_puro) {
        autenticacao::RequisicaoLogin requisicao_proto;
        requisicao_proto.set_email(email_usuario);
        requisicao_proto.set_senha(senha_texto_puro);

        autenticacao::RespostaToken resposta_proto;
        grpc::ClientContext contexto_rede;

        grpc::Status status_execucao = stub_autenticacao_->Login(&contexto_rede, requisicao_proto, &resposta_proto);

        ResultadoLogin resultado;
        if (status_execucao.ok()) {
            resultado.sucesso = true;
            resultado.token = resposta_proto.access_token();
            resultado.mensagem_erro = "";
        } else {
            resultado.sucesso = false;
            resultado.token = "";
            resultado.mensagem_erro = status_execucao.error_message(); 
        }

        return resultado;
    }

    ResultadoCriacaoCliente CriarPessoaFisica(const json& dados) {
        autenticacao::RequisicaoCriarPessoaFisica requisicao_proto;
        requisicao_proto.set_email(dados.value("email", ""));
        requisicao_proto.set_telefone(dados.value("telefone", ""));
        requisicao_proto.set_nome_completo(dados.value("nome_completo", ""));
        requisicao_proto.set_cpf(dados.value("cpf", ""));
        requisicao_proto.set_cnh(dados.value("cnh", ""));
        requisicao_proto.set_senha_texto_puro(dados.value("senha_texto_puro", ""));
        
        if (dados.contains("endereco")) {
            auto endereco_proto = requisicao_proto.mutable_endereco();
            endereco_proto->set_rua(dados["endereco"].value("rua", ""));
            endereco_proto->set_numero(dados["endereco"].value("numero", ""));
            endereco_proto->set_complemento(dados["endereco"].value("complemento", ""));
            endereco_proto->set_bairro(dados["endereco"].value("bairro", ""));
            endereco_proto->set_cidade(dados["endereco"].value("cidade", ""));
            endereco_proto->set_estado(dados["endereco"].value("estado", ""));
            endereco_proto->set_cep(dados["endereco"].value("cep", ""));
        }

        autenticacao::RespostaCriarCliente resposta_proto;
        grpc::ClientContext contexto_rede;
        grpc::Status status_execucao = stub_autenticacao_->CriarPessoaFisica(&contexto_rede, requisicao_proto, &resposta_proto);

        ResultadoCriacaoCliente resultado;
        if(status_execucao.ok()) {
            resultado.sucesso = true;
            resultado.id_pessoa = resposta_proto.id_pessoa();
            resultado.email = resposta_proto.email();
        } else {
            resultado.sucesso = false;
            resultado.mensagem_erro = status_execucao.error_message();
        }
        return resultado;
    }

    ResultadoLogin FazerLoginClienteSeguro(const std::string& email_usuario, const std::string& senha_texto_puro) {
        autenticacao::RequisicaoLogin requisicao_proto;
        requisicao_proto.set_email(email_usuario);
        requisicao_proto.set_senha(senha_texto_puro);

        autenticacao::RespostaToken resposta_proto;
        grpc::ClientContext contexto_rede;

        grpc::Status status_execucao = stub_autenticacao_->LoginCliente(&contexto_rede, requisicao_proto, &resposta_proto);

        ResultadoLogin resultado;
        if (status_execucao.ok()) {
            resultado.sucesso = true;
            resultado.token = resposta_proto.access_token();
            resultado.mensagem_erro = "";
        } else {
            resultado.sucesso = false;
            resultado.token = "";
            resultado.mensagem_erro = status_execucao.error_message(); 
        }

        return resultado;


    }
};

#endif 