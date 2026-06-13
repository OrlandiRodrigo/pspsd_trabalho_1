#ifndef CLIENTE_FROTA_HPP
#define CLIENTE_FROTA_HPP

#include <string>
#include <memory>
#include <grpcpp/grpcpp.h>
#include "../../dependencias/json.hpp"

#include "../../protos_gerados/frota.grpc.pb.h"

using json = nlohmann::json;

struct ResultadoListagemVeiculos {
    bool sucesso;
    std::string mensagem_erro;
    json veiculos;
};

struct ResultadoCriacaoVeiculo {
    bool sucesso;
    std::string mensagem_erro;
    json veiculo;
};

struct ResultadoAtualizacaoVeiculo {
    bool sucesso;
    std::string mensagem_erro;
    json veiculo;
};

struct ResultadoDelecaoVeiculo {
    bool sucesso;
    std::string mensagem_erro;
};

struct ResultadoListagemReservas {
    bool sucesso;
    std::string mensagem_erro;
    json reservas;
};

struct ResultadoCriacaoReserva {
    bool sucesso;
    std::string mensagem_erro;
    json reserva;
};

struct ResultadoCancelamentoReserva {
    bool sucesso;
    std::string mensagem_erro;
    json reserva;
};

struct ResultadoSimulacaoReserva {
    bool sucesso;
    std::string mensagem_erro;
    json simulacao;
};

class ClienteFrota {
private:
    std::unique_ptr<frota::ServicoGestaoVeiculos::Stub> stub_veiculos_;
    std::unique_ptr<frota::ServicoGestaoReservas::Stub> stub_reservas_;

public:
    explicit ClienteFrota(std::shared_ptr<grpc::Channel> canal_comunicacao)
        : stub_veiculos_(frota::ServicoGestaoVeiculos::NewStub(canal_comunicacao)),
          stub_reservas_(frota::ServicoGestaoReservas::NewStub(canal_comunicacao)) {}

    ResultadoListagemVeiculos ListarVeiculos() {
        frota::RequisicaoListarVeiculos requisicao_proto;
        frota::RespostaListaVeiculos resposta_proto;
        grpc::ClientContext contexto_rede;

        grpc::Status status_execucao = stub_veiculos_->ListarVeiculos(&contexto_rede, requisicao_proto, &resposta_proto);

        ResultadoListagemVeiculos resultado;
        resultado.veiculos = json::array();

        if (status_execucao.ok()) {
            resultado.sucesso = true;
            resultado.mensagem_erro = "";
            
            for (const auto& veiculo_proto : resposta_proto.veiculos()) {
                json v_json;
                v_json["id_veiculo"] = veiculo_proto.id_veiculo();
                v_json["placa"] = veiculo_proto.placa();
                v_json["marca"] = veiculo_proto.marca();
                v_json["modelo"] = veiculo_proto.modelo();
                v_json["valor_diaria"] = veiculo_proto.valor_diaria();
                v_json["ano_fabricacao"] = veiculo_proto.ano_fabricacao();
                v_json["imagem_url"] = veiculo_proto.imagem_url();
                v_json["status"] = veiculo_proto.status();
                v_json["tipo_veiculo"] = veiculo_proto.tipo_veiculo();
                
                resultado.veiculos.push_back(v_json);
            }
        } else {
            resultado.sucesso = false;
            resultado.mensagem_erro = status_execucao.error_message(); 
        }

        return resultado;
    }

    ResultadoListagemReservas ListarMinhasReservas(int cliente_id) {
        frota::RequisicaoListarMinhasReservas requisicao_proto;
        requisicao_proto.set_cliente_id(cliente_id);

        frota::RespostaListaReservas resposta_proto;
        grpc::ClientContext contexto_rede;

        grpc::Status status_execucao = stub_reservas_->ListarMinhasReservas(&contexto_rede, requisicao_proto, &resposta_proto);

        ResultadoListagemReservas resultado;
        resultado.reservas = json::array();

        if (status_execucao.ok()) {
            resultado.sucesso = true;
            resultado.mensagem_erro = "";
            
            for (const auto& reserva_proto : resposta_proto.reservas()) {
                json r_json;
                r_json["id_reserva"] = reserva_proto.id_reserva();
                r_json["data_criacao"] = reserva_proto.data_criacao();
                r_json["valor_total_estimado"] = reserva_proto.valor_total_estimado();
                
                r_json["data_retirada"] = reserva_proto.data_retirada();
                r_json["dataRetirada"] = reserva_proto.data_retirada();
                r_json["data_devolucao"] = reserva_proto.data_devolucao();
                r_json["dataDevolucao"] = reserva_proto.data_devolucao();
                r_json["seguro_pessoal"] = reserva_proto.seguro_pessoal();
                r_json["seguro_terceiros"] = reserva_proto.seguro_terceiros();
                
                switch(reserva_proto.status()) {
                    case frota::STATUS_RESERVA_PENDENTE: r_json["status"] = "pendente"; break;
                    case frota::STATUS_RESERVA_CONFIRMADA: r_json["status"] = "confirmada"; break;
                    case frota::STATUS_RESERVA_EM_ANDAMENTO: r_json["status"] = "em_andamento"; break;
                    case frota::STATUS_RESERVA_FINALIZADA: r_json["status"] = "finalizada"; break;
                    case frota::STATUS_RESERVA_CANCELADA: r_json["status"] = "cancelada"; break;
                    default: r_json["status"] = "desconhecido"; break;
                }
                
                r_json["veiculo"] = {
                    {"marca", reserva_proto.veiculo().marca()},
                    {"modelo", reserva_proto.veiculo().modelo()},
                    {"placa", reserva_proto.veiculo().placa()},
                    {"imagem_url", reserva_proto.veiculo().imagem_url()}
                };
                
                resultado.reservas.push_back(r_json);
            }
        } else {
            resultado.sucesso = false;
            resultado.mensagem_erro = status_execucao.error_message();
        }

        return resultado;
    }

    ResultadoCriacaoReserva CriarReserva(int cliente_id, const json& dados) {
        frota::RequisicaoCriarReserva requisicao_proto;
        
        requisicao_proto.set_cliente_id(cliente_id); 
        
        requisicao_proto.set_veiculo_id(dados.value("veiculo_id", 0));
        requisicao_proto.set_data_retirada(dados.value("data_retirada", ""));
        requisicao_proto.set_data_devolucao(dados.value("data_devolucao", ""));
        requisicao_proto.set_seguro_pessoal(dados.value("seguro_pessoal", false));
        requisicao_proto.set_seguro_terceiros(dados.value("seguro_terceiros", false));

        frota::Reserva resposta_proto;
        grpc::ClientContext contexto_rede;

        grpc::Status status_execucao = stub_reservas_->CriarReserva(&contexto_rede, requisicao_proto, &resposta_proto);

        ResultadoCriacaoReserva resultado;
        if (status_execucao.ok()) {
            resultado.sucesso = true;
            resultado.mensagem_erro = "";
            resultado.reserva["id_reserva"] = resposta_proto.id_reserva();
            resultado.reserva["valor_total_estimado"] = resposta_proto.valor_total_estimado();
        } else {
            resultado.sucesso = false;
            resultado.mensagem_erro = status_execucao.error_message();
        }
        return resultado;
    }

    ResultadoSimulacaoReserva SimularReserva(const json& dados) {
        frota::RequisicaoSimularReserva requisicao_proto;

        std::string dt_ret = dados.contains("data_retirada") ? dados.value("data_retirada", "") : dados.value("dataRetirada", "");
        std::string dt_dev = dados.contains("data_devolucao") ? dados.value("data_devolucao", "") : dados.value("dataDevolucao", "");

        requisicao_proto.set_veiculo_id(dados.value("veiculo_id", 0));
        requisicao_proto.set_data_retirada(dt_ret);
        requisicao_proto.set_data_devolucao(dt_dev);
        requisicao_proto.set_seguro_pessoal(dados.value("seguro_pessoal", false));
        requisicao_proto.set_seguro_terceiros(dados.value("seguro_terceiros", false));

        frota::RespostaSimularReserva resposta_proto;
        grpc::ClientContext contexto_rede;
        grpc::Status status_execucao = stub_reservas_->SimularReserva(&contexto_rede, requisicao_proto, &resposta_proto);

        ResultadoSimulacaoReserva resultado;
        if (status_execucao.ok()) {
            resultado.sucesso = true;
            resultado.mensagem_erro = "";

            resultado.simulacao["data_retirada"] = dt_ret;
            resultado.simulacao["dataRetirada"] = dt_ret;
            resultado.simulacao["data_devolucao"] = dt_dev;
            resultado.simulacao["dataDevolucao"] = dt_dev;

            int qtd = resposta_proto.quantidade_diarias();
            float total_diarias = resposta_proto.valor_diarias();
            float total_seguros = resposta_proto.valor_seguros();
            float unitario = (qtd > 0) ? (total_diarias / qtd) : 0.0;

            resultado.simulacao["quantidade_diarias"] = qtd;
            resultado.simulacao["valor_diarias"] = total_diarias;
            resultado.simulacao["valor_diaria"] = unitario;
            resultado.simulacao["valor_diaria_no_momento"] = unitario; 
            
            resultado.simulacao["valor_seguros"] = total_seguros;
            resultado.simulacao["taxas"] = total_seguros; 
            
            resultado.simulacao["valor_total_estimado"] = resposta_proto.valor_total_estimado();

            resultado.simulacao["veiculo"] = {
                {"valor_diaria", unitario},
                {"valor_diaria_no_momento", unitario}
            };

        } else {
            resultado.sucesso = false;
            resultado.mensagem_erro = status_execucao.error_message();
        }
        return resultado;
    }

    ResultadoCancelamentoReserva CancelarReserva(int reserva_id, int cliente_id) {
        frota::RequisicaoCancelarReserva requisicao_proto;
        requisicao_proto.set_id_reserva(reserva_id);
        requisicao_proto.set_cliente_id(cliente_id);

        frota::Reserva resposta_proto;
        grpc::ClientContext contexto_rede;

        grpc::Status status_execucao = stub_reservas_->CancelarReserva(&contexto_rede, requisicao_proto, &resposta_proto);

        ResultadoCancelamentoReserva resultado;
        if (status_execucao.ok()) {
            resultado.sucesso = true;
            resultado.mensagem_erro = "";
            resultado.reserva["id_reserva"] = resposta_proto.id_reserva();
            resultado.reserva["status"] = "cancelada";
        } else {
            resultado.sucesso = false;
            resultado.mensagem_erro = status_execucao.error_message();
        }
        return resultado;
    }

    ResultadoCriacaoVeiculo CriarVeiculo(const json& dados) {
        frota::RequisicaoCriarVeiculo requisicao_proto;
        
        requisicao_proto.set_placa(dados.value("placa", ""));
        requisicao_proto.set_marca(dados.value("marca", ""));
        requisicao_proto.set_modelo(dados.value("modelo", ""));
        requisicao_proto.set_valor_diaria(dados.value("valor_diaria", 0.0));
        requisicao_proto.set_ano_fabricacao(dados.value("ano_fabricacao", 0));
        requisicao_proto.set_ano_modelo(dados.value("ano_modelo", 0));
        requisicao_proto.set_chassi(dados.value("chassi", ""));
        requisicao_proto.set_renavam(dados.value("renavam", ""));
        requisicao_proto.set_capacidade_tanque(dados.value("capacidade_tanque", 0.0));
        requisicao_proto.set_cambio_automatico(dados.value("cambio_automatico", false));
        requisicao_proto.set_ar_condicionado(dados.value("ar_condicionado", false));
        requisicao_proto.set_imagem_url(dados.value("imagem_url", ""));

        if (dados["cor"].is_number()) {
            requisicao_proto.set_cor(static_cast<frota::CorVeiculo>(dados.value("cor", 1)));
        } else {
            requisicao_proto.set_cor(frota::COR_VEICULO_PRETO); 
        }

        std::string tipo_str = dados["tipo_veiculo"].is_string() ? dados.value("tipo_veiculo", "") : "";
        int tipo_int = dados["tipo_veiculo"].is_number() ? dados.value("tipo_veiculo", 0) : 0;

        if (tipo_str == "PASSEIO" || tipo_int == 1) {
            requisicao_proto.set_tipo_veiculo(frota::TIPO_VEICULO_PASSEIO);
            auto detalhes = requisicao_proto.mutable_passeio();
            detalhes->set_tipo_carroceria(dados.value("tipo_carroceria", ""));
            detalhes->set_qtde_portas(dados.value("qtde_portas", 0));
            detalhes->set_qtde_passageiros(dados.value("qtde_passageiros", 0));

        } else if (tipo_str == "UTILITARIO" || tipo_int == 2) {
            requisicao_proto.set_tipo_veiculo(frota::TIPO_VEICULO_UTILITARIO);
            auto detalhes = requisicao_proto.mutable_utilitario();
            detalhes->set_tipo_utilitario(dados.value("tipo_utilitario", ""));
            detalhes->set_capacidade_carga_kg(dados.value("capacidade_carga_kg", 0.0));
            detalhes->set_capacidade_carga_m3(dados.value("capacidade_carga_m3", 0.0));
            detalhes->set_tipo_carga(dados.value("tipo_carga", ""));
            detalhes->set_qtde_eixos(dados.value("qtde_eixos", 0));
            detalhes->set_max_passageiros(dados.value("max_passageiros", 0));

        } else if (tipo_str == "MOTOCICLETA" || tipo_int == 3) {
            requisicao_proto.set_tipo_veiculo(frota::TIPO_VEICULO_MOTOCICLETA);
            auto detalhes = requisicao_proto.mutable_motocicleta();
            detalhes->set_cilindrada(dados.value("cilindrada", 0));
            detalhes->set_tipo_tracao(dados.value("tipo_tracao", ""));
            detalhes->set_abs(dados.value("abs", false));
            detalhes->set_partida_eletrica(dados.value("partida_eletrica", false));
            detalhes->set_modos_pilotagem(dados.value("modos_pilotagem", ""));
        }

        frota::Veiculo resposta_proto;
        grpc::ClientContext contexto_rede;
        grpc::Status status_execucao = stub_veiculos_->CriarVeiculo(&contexto_rede, requisicao_proto, &resposta_proto);
        
        ResultadoCriacaoVeiculo resultado;
        if (status_execucao.ok()) {
            resultado.sucesso = true;
            resultado.mensagem_erro = "";
            resultado.veiculo["id_veiculo"] = resposta_proto.id_veiculo();
            resultado.veiculo["placa"] = resposta_proto.placa();
        } else {
            resultado.sucesso = false;
            resultado.mensagem_erro = status_execucao.error_message();
        }
        return resultado;
    }

    ResultadoDelecaoVeiculo DeletarVeiculo(int id_veiculo) {
        frota::RequisicaoDeletarVeiculo requisicao_proto;
        requisicao_proto.set_id_veiculo(id_veiculo);

        frota::RespostaDeletarVeiculo resposta_proto;
        grpc::ClientContext contexto_rede;

        grpc::Status status_execucao = stub_veiculos_->DeletarVeiculo(&contexto_rede, requisicao_proto, &resposta_proto);

        ResultadoDelecaoVeiculo resultado;
        if (status_execucao.ok()) {
            resultado.sucesso = resposta_proto.sucesso();
            resultado.mensagem_erro = resposta_proto.mensagem();
        } else {
            resultado.sucesso = false;
            resultado.mensagem_erro = status_execucao.error_message();
        }
        return resultado;
    }

    ResultadoAtualizacaoVeiculo AtualizarVeiculo(int id_veiculo, const json& dados) {
        frota::RequisicaoAtualizarVeiculo requisicao_proto;
        requisicao_proto.set_id_veiculo(id_veiculo);
        
        if(dados.contains("placa")) requisicao_proto.set_placa(dados.value("placa", ""));
        if(dados.contains("marca")) requisicao_proto.set_marca(dados.value("marca", ""));
        if(dados.contains("modelo")) requisicao_proto.set_modelo(dados.value("modelo", ""));
        
        if(dados.contains("valor_diaria")) {
            if(dados["valor_diaria"].is_number()) requisicao_proto.set_valor_diaria(dados.value("valor_diaria", 0.0));
            else if(dados["valor_diaria"].is_string()) requisicao_proto.set_valor_diaria(std::stod(dados.value("valor_diaria", "0.0")));
        }
        
        if(dados.contains("ano_fabricacao")) {
            if(dados["ano_fabricacao"].is_number()) requisicao_proto.set_ano_fabricacao(dados.value("ano_fabricacao", 0));
            else if(dados["ano_fabricacao"].is_string()) requisicao_proto.set_ano_fabricacao(std::stoi(dados.value("ano_fabricacao", "0")));
        }

        if(dados.contains("ano_modelo")) {
            if(dados["ano_modelo"].is_number()) requisicao_proto.set_ano_modelo(dados.value("ano_modelo", 0));
            else if(dados["ano_modelo"].is_string()) requisicao_proto.set_ano_modelo(std::stoi(dados.value("ano_modelo", "0")));
        }

        if(dados.contains("chassi")) requisicao_proto.set_chassi(dados.value("chassi", ""));
        if(dados.contains("renavam")) requisicao_proto.set_renavam(dados.value("renavam", ""));
        
        if(dados.contains("capacidade_tanque")) {
            if(dados["capacidade_tanque"].is_number()) requisicao_proto.set_capacidade_tanque(dados.value("capacidade_tanque", 0.0));
            else if(dados["capacidade_tanque"].is_string()) requisicao_proto.set_capacidade_tanque(std::stod(dados.value("capacidade_tanque", "0.0")));
        }

        if(dados.contains("cambio_automatico")) requisicao_proto.set_cambio_automatico(dados.value("cambio_automatico", false));
        if(dados.contains("ar_condicionado")) requisicao_proto.set_ar_condicionado(dados.value("ar_condicionado", false));
        if(dados.contains("imagem_url")) requisicao_proto.set_imagem_url(dados.value("imagem_url", ""));

        if (dados.contains("cor") && dados["cor"].is_number()) {
            requisicao_proto.set_cor(static_cast<frota::CorVeiculo>(dados.value("cor", 1)));
        }
        
        std::string tipo_str = "";
        int tipo_int = 0;
        if (dados.contains("tipo_veiculo")) {
            if (dados["tipo_veiculo"].is_string()) tipo_str = dados.value("tipo_veiculo", "");
            if (dados["tipo_veiculo"].is_number()) tipo_int = dados.value("tipo_veiculo", 0);
        }

        if (tipo_str == "PASSEIO" || tipo_int == 1) {
            requisicao_proto.set_tipo_veiculo(frota::TIPO_VEICULO_PASSEIO);
            auto detalhes = requisicao_proto.mutable_passeio();
            if(dados.contains("tipo_carroceria")) detalhes->set_tipo_carroceria(dados.value("tipo_carroceria", ""));
            
            if(dados.contains("qtde_portas")) {
                if(dados["qtde_portas"].is_number()) detalhes->set_qtde_portas(dados.value("qtde_portas", 0));
                else if(dados["qtde_portas"].is_string()) detalhes->set_qtde_portas(std::stoi(dados.value("qtde_portas", "0")));
            }
        } else if (tipo_str == "UTILITARIO" || tipo_int == 2) {
            requisicao_proto.set_tipo_veiculo(frota::TIPO_VEICULO_UTILITARIO);
            auto detalhes = requisicao_proto.mutable_utilitario();
            if(dados.contains("tipo_utilitario")) detalhes->set_tipo_utilitario(dados.value("tipo_utilitario", ""));
            
            if(dados.contains("capacidade_carga_kg")) {
                if(dados["capacidade_carga_kg"].is_number()) detalhes->set_capacidade_carga_kg(dados.value("capacidade_carga_kg", 0.0));
                else if(dados["capacidade_carga_kg"].is_string()) detalhes->set_capacidade_carga_kg(std::stod(dados.value("capacidade_carga_kg", "0.0")));
            }
            if(dados.contains("tipo_carga")) detalhes->set_tipo_carga(dados.value("tipo_carga", ""));
            if(dados.contains("qtde_eixos")) {
                if(dados["qtde_eixos"].is_number()) detalhes->set_qtde_eixos(dados.value("qtde_eixos", 0));
                else if(dados["qtde_eixos"].is_string()) detalhes->set_qtde_eixos(std::stoi(dados.value("qtde_eixos", "0")));
            }
            if(dados.contains("max_passageiros")) {
                if(dados["max_passageiros"].is_number()) detalhes->set_max_passageiros(dados.value("max_passageiros", 0));
                else if(dados["max_passageiros"].is_string()) detalhes->set_max_passageiros(std::stoi(dados.value("max_passageiros", "0")));
            }
        } else if (tipo_str == "MOTOCICLETA" || tipo_int == 3) {
            requisicao_proto.set_tipo_veiculo(frota::TIPO_VEICULO_MOTOCICLETA);
            auto detalhes = requisicao_proto.mutable_motocicleta();
            if(dados.contains("tipo_tracao")) detalhes->set_tipo_tracao(dados.value("tipo_tracao", ""));
            if(dados.contains("abs")) detalhes->set_abs(dados.value("abs", false));
            if(dados.contains("partida_eletrica")) detalhes->set_partida_eletrica(dados.value("partida_eletrica", false));
            if(dados.contains("modos_pilotagem")) detalhes->set_modos_pilotagem(dados.value("modos_pilotagem", ""));
        }

        frota::Veiculo resposta_proto;
        grpc::ClientContext contexto_rede;
        grpc::Status status_execucao = stub_veiculos_->AtualizarVeiculo(&contexto_rede, requisicao_proto, &resposta_proto);
        
        ResultadoAtualizacaoVeiculo resultado;
        if (status_execucao.ok()) {
            resultado.sucesso = true;
            resultado.veiculo["id_veiculo"] = resposta_proto.id_veiculo();
            resultado.veiculo["placa"] = resposta_proto.placa();
        } else {
            resultado.sucesso = false;
            resultado.mensagem_erro = status_execucao.error_message();
        }
        return resultado;
    }
};

#endif
