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

class ClienteFrota {
private:
    std::unique_ptr<frota::ServicoGestaoVeiculos::Stub> stub_veiculos_;

public:
    explicit ClienteFrota(std::shared_ptr<grpc::Channel> canal_comunicacao)
        : stub_veiculos_(frota::ServicoGestaoVeiculos::NewStub(canal_comunicacao)) {}

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
};

#endif 