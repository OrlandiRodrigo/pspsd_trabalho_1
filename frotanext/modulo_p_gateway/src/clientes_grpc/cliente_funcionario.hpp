#ifndef CLIENTE_FUNCIONARIO_HPP
#define CLIENTE_FUNCIONARIO_HPP

#include <string>
#include <memory>
#include <grpcpp/grpcpp.h>

#include "../../protos_gerados/autenticacao.grpc.pb.h"

struct ResultadoCriacaoFuncionario {
    bool sucesso;
    std::string email;
    std::string mensagem_erro;
};

class ClienteFuncionario {
private:
    std::unique_ptr<autenticacao::ServicoFuncionario::Stub> stub_funcionario_;

public:
    explicit ClienteFuncionario(std::shared_ptr<grpc::Channel> canal_comunicacao)
        : stub_funcionario_(autenticacao::ServicoFuncionario::NewStub(canal_comunicacao)) {}

    ResultadoCriacaoFuncionario CriarFuncionario(
        const std::string& email,
        const std::string& nome_completo,
        const std::string& senha
    ) {
        autenticacao::RequisicaoCriarFuncionario requisicao_proto;
        requisicao_proto.set_email(email);
        requisicao_proto.set_nome_completo(nome_completo);
        requisicao_proto.set_senha_texto_puro(senha);
        requisicao_proto.set_e_admin(true); 
        requisicao_proto.set_e_ativado(true);

        autenticacao::Funcionario resposta_proto;
        grpc::ClientContext contexto_rede;

        grpc::Status status_execucao = stub_funcionario_->CriarFuncionario(&contexto_rede, requisicao_proto, &resposta_proto);

        ResultadoCriacaoFuncionario resultado;
        if (status_execucao.ok()) {
            resultado.sucesso = true;
            resultado.email = resposta_proto.email();
            resultado.mensagem_erro = "";
        } else {
            resultado.sucesso = false;
            resultado.email = "";
            resultado.mensagem_erro = status_execucao.error_message(); 
        }

        return resultado;
    }
};

#endif 