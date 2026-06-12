#include <iostream>
#include <string>
#include <memory>
#include <cstdlib>

#include "../dependencias/httplib.h"
#include "../dependencias/json.hpp"

#include <grpcpp/grpcpp.h>
#include "clientes_grpc/cliente_autenticacao.hpp"
#include "clientes_grpc/cliente_funcionario.hpp"
#include "clientes_grpc/cliente_frota.hpp"

using json = nlohmann::json;

const int PORTA_SERVIDOR_GATEWAY = 8080;
const std::string ENDERECO_MODULO_AUTENTICACAO = "localhost:50051";
const std::string ENDERECO_MODULO_FROTA = "localhost:50052";


void aplicar_politicas_cors(httplib::Response& resposta) {
    resposta.set_header("Access-Control-Allow-Origin", "*");
    resposta.set_header("Access-Control-Allow-Methods", "POST, GET, PUT, DELETE, OPTIONS");
    resposta.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization");
}


std::string extrair_token_requisicao(const httplib::Request& requisicao) {
    if (requisicao.has_header("Authorization")) {
        std::string cabecalho_autorizacao = requisicao.get_header_value("Authorization");
        if (cabecalho_autorizacao.find("Bearer ") == 0) {
            return cabecalho_autorizacao.substr(7);
        }
    }
    return "";
}

std::string obter_endereco_host(const char* nome_variavel_ambiente, const std::string& valor_padrao) {
    if (const char* valor_ambiente = std::getenv(nome_variavel_ambiente)) {
        return std::string(valor_ambiente);
    }
    return valor_padrao;
}


int main() {
    const char* env_host_a = std::getenv("HOST_MODULO_A");
    std::string host_modulo_a = env_host_a ? env_host_a : "localhost:50051";

    ClienteAutenticacao cliente_autenticacao(grpc::CreateChannel(host_modulo_a, grpc::InsecureChannelCredentials()));
    ClienteFuncionario cliente_funcionario(grpc::CreateChannel(host_modulo_a, grpc::InsecureChannelCredentials()));

    const char* env_host_b = std::getenv("HOST_MODULO_B");
    std::string host_modulo_b = env_host_b ? env_host_b : "localhost:50052";

    ClienteFrota cliente_frota(grpc::CreateChannel(host_modulo_b, grpc::InsecureChannelCredentials()));

    httplib::Server servidor_gateway;

    servidor_gateway.Options(".*", [](const httplib::Request&, httplib::Response& resposta) {
        aplicar_politicas_cors(resposta);
        resposta.status = 200; 
    });

    servidor_gateway.Get("/api/v1/auth/validar_sessao", [&](const httplib::Request& requisicao, httplib::Response& resposta) {
        aplicar_politicas_cors(resposta);

        std::string token_recebido = extrair_token_requisicao(requisicao);

        if (token_recebido.empty()) {
            resposta.status = 401;
            json erro = {{"mensagem", "Cabecalho de autorizacao ausente ou mal formatado."}};
            resposta.set_content(erro.dump(), "application/json");
            return;
        }

        autenticacao::RespostaValidacao resultado_validacao = cliente_autenticacao.ValidarSessaoSegura(token_recebido);

        if (resultado_validacao.e_valido()) {
            json sucesso = {
                {"mensagem", "Token valido e autenticado com sucesso."},
                {"identificador_usuario", resultado_validacao.subject_payload()},
                {"perfil_acesso", resultado_validacao.tipo_usuario()}
            };
            resposta.status = 200; 
            resposta.set_content(sucesso.dump(), "application/json");
        } else {
            resposta.status = 401; 
            json erro = {{"mensagem", "O token fornecido e invalido ou expirou."}};
            resposta.set_content(erro.dump(), "application/json");
        }
    });

    servidor_gateway.Post("/api/v1/auth/login", [&](const httplib::Request& requisicao, httplib::Response& resposta) {
        aplicar_politicas_cors(resposta);

        try {
            json corpo_requisicao = json::parse(requisicao.body);
            
            std::string email_usuario = corpo_requisicao.value("email", "");
            std::string senha_usuario = corpo_requisicao.value("senha", "");

            if (email_usuario.empty() || senha_usuario.empty()) {
                resposta.status = 400; 
                json erro = {{"mensagem", "O email e a senha sao obrigatorios."}};
                resposta.set_content(erro.dump(), "application/json");
                return;
            }

            ResultadoLogin resultado = cliente_autenticacao.FazerLoginSeguro(email_usuario, senha_usuario);

            if (resultado.sucesso) {
                json sucesso = {
                    {"access_token", resultado.token},
                    {"token_type", "bearer"}
                };
                resposta.status = 200; 
                resposta.set_content(sucesso.dump(), "application/json");
            } else {
                resposta.status = 401; 
                json erro = {{"mensagem", resultado.mensagem_erro}};
                resposta.set_content(erro.dump(), "application/json");
            }

        } catch (const json::parse_error& erro_analise) {
            resposta.status = 400; 
            json erro = {{"mensagem", "Formato JSON invalido."}};
            resposta.set_content(erro.dump(), "application/json");
        }
    });

    servidor_gateway.Post("/api/v1/auth/login-cliente", [&](const httplib::Request& requisicao, httplib::Response& resposta) {
        aplicar_politicas_cors(resposta);

        try {
            json corpo_requisicao = json::parse(requisicao.body);
            std::string email_usuario = corpo_requisicao.value("email", "");
            std::string senha_usuario = corpo_requisicao.value("senha", "");

            if (email_usuario.empty() || senha_usuario.empty()) {
                resposta.status = 400; 
                json erro = {{"mensagem", "O email e a senha sao obrigatorios."}};
                resposta.set_content(erro.dump(), "application/json");
                return;
            }

            ResultadoLogin resultado = cliente_autenticacao.FazerLoginClienteSeguro(email_usuario, senha_usuario);

            if (resultado.sucesso) {
                json sucesso = {
                    {"access_token", resultado.token},
                    {"token_type", "bearer"}
                };
                resposta.status = 200; 
                resposta.set_content(sucesso.dump(), "application/json");
            } else {
                resposta.status = 401; 
                json erro = {{"mensagem", resultado.mensagem_erro}};
                resposta.set_content(erro.dump(), "application/json");
            }

        } catch (const json::parse_error& erro_analise) {
            resposta.status = 400; 
            json erro = {{"mensagem", "Formato JSON invalido."}};
            resposta.set_content(erro.dump(), "application/json");
        }
    });

    servidor_gateway.Post("/api/v1/auth/registar-funcionario", [&](const httplib::Request& requisicao, httplib::Response& resposta) {
        aplicar_politicas_cors(resposta);

        try {
            json corpo_requisicao = json::parse(requisicao.body);
            
            std::string email = corpo_requisicao.value("email", "");
            std::string nome = corpo_requisicao.value("nome_completo", "");
            std::string senha = corpo_requisicao.value("senha", "");

            if (email.empty() || nome.empty() || senha.empty()) {
                resposta.status = 400; 
                json erro = {{"mensagem", "O email, nome_completo e senha sao obrigatorios."}};
                resposta.set_content(erro.dump(), "application/json");
                return;
            }

            ResultadoCriacaoFuncionario resultado = cliente_funcionario.CriarFuncionario(email, nome, senha);

            if (resultado.sucesso) {
                json sucesso = {
                    {"mensagem", "Funcionario criado com sucesso!"},
                    {"email", resultado.email}
                };
                resposta.status = 201; 
                resposta.set_content(sucesso.dump(), "application/json");
            } else {
                resposta.status = 400; 
                json erro = {{"mensagem", resultado.mensagem_erro}};
                resposta.set_content(erro.dump(), "application/json");
            }

        } catch (const json::parse_error& erro_analise) {
            resposta.status = 400; 
            json erro = {{"mensagem", "Formato JSON invalido."}};
            resposta.set_content(erro.dump(), "application/json");
        }
    });

    servidor_gateway.Get("/api/v1/reservas/", [&](const httplib::Request& requisicao, httplib::Response& resposta) {
        aplicar_politicas_cors(resposta);
        resposta.status = 200;
        resposta.set_content("[]", "application/json"); 
    });

    auto handler_criar_veiculo = [&](const httplib::Request& requisicao, httplib::Response& resposta, const std::string& tipo_veiculo) {
        aplicar_politicas_cors(resposta);

        std::string token_recebido = extrair_token_requisicao(requisicao);
        if (token_recebido.empty()) {
            resposta.status = 401;
            resposta.set_content(json({{"mensagem", "Acesso negado. Token ausente."}}).dump(), "application/json");
            return;
        }

        autenticacao::RespostaValidacao resultado_validacao = cliente_autenticacao.ValidarSessaoSegura(token_recebido);
        if (!resultado_validacao.e_valido()) {
            resposta.status = 401;
            resposta.set_content(json({{"mensagem", "Acesso negado. Token invalido."}}).dump(), "application/json");
            return;
        }

        try {
            json corpo_requisicao = json::parse(requisicao.body);
            
            corpo_requisicao["tipo_veiculo"] = tipo_veiculo; 
            
            ResultadoCriacaoVeiculo resultado_criacao = cliente_frota.CriarVeiculo(corpo_requisicao);

            if (resultado_criacao.sucesso) {
                resposta.status = 201; 
                resposta.set_content(resultado_criacao.veiculo.dump(), "application/json");
            } else {
                resposta.status = 400; 
                resposta.set_content(json({{"mensagem", resultado_criacao.mensagem_erro}}).dump(), "application/json");
            }
        } catch (const json::parse_error&) {
            resposta.status = 400;
            resposta.set_content(json({{"mensagem", "Formato JSON invalido."}}).dump(), "application/json");
        }
    };

    servidor_gateway.Post("/api/v1/veiculos/passeio", [&](const httplib::Request& req, httplib::Response& res) { 
        handler_criar_veiculo(req, res, "PASSEIO"); 
    });
    
    servidor_gateway.Post("/api/v1/veiculos/utilitario", [&](const httplib::Request& req, httplib::Response& res) { 
        handler_criar_veiculo(req, res, "UTILITARIO"); 
    });
    
    servidor_gateway.Post("/api/v1/veiculos/motocicleta", [&](const httplib::Request& req, httplib::Response& res) { 
        handler_criar_veiculo(req, res, "MOTOCICLETA"); 
    });

    servidor_gateway.Post("/api/v1/clientes/pessoas-fisicas", [&](const httplib::Request& requisicao, httplib::Response& resposta) {
        aplicar_politicas_cors(resposta);

        try {
            json corpo_requisicao = json::parse(requisicao.body);
            ResultadoCriacaoCliente resultado = cliente_autenticacao.CriarPessoaFisica(corpo_requisicao);

            if (resultado.sucesso) {
                json sucesso = {
                    {"mensagem", "Cliente criado com sucesso!"},
                    {"id_pessoa", resultado.id_pessoa},
                    {"email", resultado.email}
                };
                resposta.status = 201;
                resposta.set_content(sucesso.dump(), "application/json");
            } else {
                resposta.status = 400; 
                json erro = {{"mensagem", resultado.mensagem_erro}};
                resposta.set_content(erro.dump(), "application/json");
            }
        } catch (const json::parse_error& erro_analise) {
            resposta.status = 400;
            json erro = {{"mensagem", "Formato JSON invalido."}};
            resposta.set_content(erro.dump(), "application/json");
        }
    });

    std::cout << "Servidor Gateway (Modulo P) inicializado na porta " << PORTA_SERVIDOR_GATEWAY << "...\n";
    std::cout << "Aguardando requisicoes HTTP para rotear via gRPC.\n";

    servidor_gateway.Get("/api/v1/frota/veiculos", [&](const httplib::Request& requisicao, httplib::Response& resposta) {
        aplicar_politicas_cors(resposta);

        std::string token_recebido = extrair_token_requisicao(requisicao);
        if (token_recebido.empty()) {
            resposta.status = 401; 
            json erro = {{"mensagem", "Acesso negado. Token ausente ou mal formatado."}};
            resposta.set_content(erro.dump(), "application/json");
            return;
        }

        autenticacao::RespostaValidacao resultado_validacao = cliente_autenticacao.ValidarSessaoSegura(token_recebido);
        if (!resultado_validacao.e_valido()) {
            resposta.status = 401; 
            json erro = {{"mensagem", "Acesso negado. Token invalido ou expirado."}};
            resposta.set_content(erro.dump(), "application/json");
            return;
        }

        ResultadoListagemVeiculos resultado_frota = cliente_frota.ListarVeiculos();

        if (resultado_frota.sucesso) {
            resposta.status = 200; 
            resposta.set_content(resultado_frota.veiculos.dump(), "application/json");
        } else {
            resposta.status = 500; 
            json erro = {{"mensagem", "Falha de comunicacao com a Frota: " + resultado_frota.mensagem_erro}};
            resposta.set_content(erro.dump(), "application/json");
        }
    });

    

    servidor_gateway.Get("/api/v1/reservas/minhas", [&](const httplib::Request& requisicao, httplib::Response& resposta) {
        aplicar_politicas_cors(resposta);

        std::string token_recebido = extrair_token_requisicao(requisicao);
        if (token_recebido.empty()) {
            resposta.status = 401; 
            json erro = {{"mensagem", "Acesso negado. Token ausente."}};
            resposta.set_content(erro.dump(), "application/json");
            return;
        }

        autenticacao::RespostaValidacao resultado_validacao = cliente_autenticacao.ValidarSessaoSegura(token_recebido);
        if (!resultado_validacao.e_valido()) {
            resposta.status = 401; 
            json erro = {{"mensagem", "Acesso negado. Token invalido ou expirado."}};
            resposta.set_content(erro.dump(), "application/json");
            return;
        }

        resposta.status = 200; 
        try {
            int cliente_id = std::stoi(resultado_validacao.subject_payload());
            
            ResultadoListagemReservas resultado_reservas = cliente_frota.ListarMinhasReservas(cliente_id);

            if (resultado_reservas.sucesso) {
                resposta.status = 200; 
                resposta.set_content(resultado_reservas.reservas.dump(), "application/json");
            } else {
                resposta.status = 500; 
                json erro = {{"mensagem", "Erro ao buscar reservas: " + resultado_reservas.mensagem_erro}};
                resposta.set_content(erro.dump(), "application/json");
            }
        } catch (...) {
            resposta.status = 400;
            json erro = {{"mensagem", "Falha ao ler o ID do usuario no token."}};
            resposta.set_content(erro.dump(), "application/json");
        }
    });

    servidor_gateway.Post("/api/v1/reservas/", [&](const httplib::Request& requisicao, httplib::Response& resposta) {
        aplicar_politicas_cors(resposta);

        std::string token_recebido = extrair_token_requisicao(requisicao);
        if (token_recebido.empty()) {
            resposta.status = 401;
            json erro = {{"mensagem", "Acesso negado. Token ausente."}};
            resposta.set_content(erro.dump(), "application/json");
            return;
        }

        autenticacao::RespostaValidacao resultado_validacao = cliente_autenticacao.ValidarSessaoSegura(token_recebido);
        if (!resultado_validacao.e_valido()) {
            resposta.status = 401;
            json erro = {{"mensagem", "Acesso negado. Token invalido ou expirado."}};
            resposta.set_content(erro.dump(), "application/json");
            return;
        }

        try {
            int cliente_id = std::stoi(resultado_validacao.subject_payload());
            json corpo_requisicao = json::parse(requisicao.body);

            ResultadoCriacaoReserva resultado_criacao = cliente_frota.CriarReserva(cliente_id, corpo_requisicao);

            if (resultado_criacao.sucesso) {
                resposta.status = 201; 
                resposta.set_content(resultado_criacao.reserva.dump(), "application/json");
            } else {
                resposta.status = 400;
                json erro = {{"mensagem", resultado_criacao.mensagem_erro}};
                resposta.set_content(erro.dump(), "application/json");
            }
        } catch (const json::parse_error&) {
            resposta.status = 400;
            json erro = {{"mensagem", "Formato JSON invalido."}};
            resposta.set_content(erro.dump(), "application/json");
        } catch (...) {
            resposta.status = 400;
            json erro = {{"mensagem", "Falha ao processar os dados da reserva."}};
            resposta.set_content(erro.dump(), "application/json");
        }
    });

    servidor_gateway.Put(R"(/api/v1/reservas/(\d+)/cancelar)", [&](const httplib::Request& requisicao, httplib::Response& resposta) {
        aplicar_politicas_cors(resposta);

        std::string token_recebido = extrair_token_requisicao(requisicao);
        if (token_recebido.empty()) {
            resposta.status = 401; 
            json erro = {{"mensagem", "Acesso negado. Token ausente."}};
            resposta.set_content(erro.dump(), "application/json");
            return;
        }

        autenticacao::RespostaValidacao resultado_validacao = cliente_autenticacao.ValidarSessaoSegura(token_recebido);
        if (!resultado_validacao.e_valido()) {
            resposta.status = 401; 
            json erro = {{"mensagem", "Acesso negado."}};
            resposta.set_content(erro.dump(), "application/json");
            return;
        }

        try {
            int cliente_id = std::stoi(resultado_validacao.subject_payload());
            int reserva_id = std::stoi(requisicao.matches[1]); 

            ResultadoCancelamentoReserva resultado = cliente_frota.CancelarReserva(reserva_id, cliente_id);

            if (resultado.sucesso) {
                resposta.status = 200;
                resposta.set_content(resultado.reserva.dump(), "application/json");
            } else {
                resposta.status = 400;
                json erro = {{"mensagem", resultado.mensagem_erro}};
                resposta.set_content(erro.dump(), "application/json");
            }
        } catch (...) {
            resposta.status = 400;
            json erro = {{"mensagem", "Parametros invalidos na URL."}};
            resposta.set_content(erro.dump(), "application/json");
        }
    });

    
    servidor_gateway.listen("0.0.0.0", PORTA_SERVIDOR_GATEWAY);

    return 0;
}