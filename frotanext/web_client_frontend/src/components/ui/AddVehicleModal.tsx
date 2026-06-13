import { useForm } from "react-hook-form";
import { X, Plus, Loader2, Car, Truck, Bike } from "lucide-react";
import type { TipoVeiculo } from "../../types/veiculo";

interface AddVehicleModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: (tipo: TipoVeiculo, dados: any) => void;
  isLoading: boolean;
}

export function AddVehicleModal({
  isOpen,
  onClose,
  onConfirm,
  isLoading,
}: AddVehicleModalProps) {
  const { register, handleSubmit, watch } = useForm();

  const tipoSelecionado = watch("tipo_veiculo", "passeio");

  const onSubmit = (data: any) => {
    const payload = {
      ...data,
      ano_fabricacao: Number(data.ano_fabricacao),
      ano_modelo: Number(data.ano_modelo),
      valor_diaria: Number(data.valor_diaria),
      capacidade_tanque: Number(data.capacidade_tanque),
      qtde_portas: data.qtde_portas ? Number(data.qtde_portas) : undefined,
      cilindrada: data.cilindrada ? Number(data.cilindrada) : undefined,
      capacidade_carga_kg: data.capacidade_carga_kg
        ? Number(data.capacidade_carga_kg)
        : undefined,
      qtde_eixos: data.qtde_eixos ? Number(data.qtde_eixos) : undefined,
      max_passageiros: data.max_passageiros
        ? Number(data.max_passageiros)
        : undefined,
    };

    Object.keys(payload).forEach(
      (key) => payload[key] === undefined && delete payload[key]
    );

    onConfirm(data.tipo_veiculo, payload);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-fade-in">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-3xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="bg-blue-600 p-6 flex justify-between items-center shrink-0">
          <h3 className="text-xl font-bold text-white font-futuristic flex items-center gap-2">
            <Plus size={24} /> Adicionar Novo Veículo
          </h3>
          <button
            onClick={onClose}
            className="text-blue-100 hover:text-white bg-white/10 p-2 rounded-full hover:bg-white/20 transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        <form
          onSubmit={handleSubmit(onSubmit)}
          className="p-8 overflow-y-auto custom-scrollbar"
        >
          {/* SELEÇÃO DE TIPO */}
          <div className="mb-8">
            <label className="block text-sm font-bold text-gray-700 mb-2">
              Categoria do Veículo
            </label>
            <div className="grid grid-cols-3 gap-4">
              <label
                className={`cursor-pointer border-2 rounded-xl p-4 flex flex-col items-center gap-2 transition-all ${
                  tipoSelecionado === "passeio"
                    ? "border-blue-600 bg-blue-50 text-blue-700"
                    : "border-gray-200 hover:border-gray-300 text-gray-500"
                }`}
              >
                <input
                  type="radio"
                  value="passeio"
                  {...register("tipo_veiculo")}
                  className="hidden"
                  defaultChecked
                />
                <Car size={24} />{" "}
                <span className="font-bold text-sm">Passeio</span>
              </label>
              <label
                className={`cursor-pointer border-2 rounded-xl p-4 flex flex-col items-center gap-2 transition-all ${
                  tipoSelecionado === "motocicleta"
                    ? "border-blue-600 bg-blue-50 text-blue-700"
                    : "border-gray-200 hover:border-gray-300 text-gray-500"
                }`}
              >
                <input
                  type="radio"
                  value="motocicleta"
                  {...register("tipo_veiculo")}
                  className="hidden"
                />
                <Bike size={24} />{" "}
                <span className="font-bold text-sm">Moto</span>
              </label>
              <label
                className={`cursor-pointer border-2 rounded-xl p-4 flex flex-col items-center gap-2 transition-all ${
                  tipoSelecionado === "utilitario"
                    ? "border-blue-600 bg-blue-50 text-blue-700"
                    : "border-gray-200 hover:border-gray-300 text-gray-500"
                }`}
              >
                <input
                  type="radio"
                  value="utilitario"
                  {...register("tipo_veiculo")}
                  className="hidden"
                />
                <Truck size={24} />{" "}
                <span className="font-bold text-sm">Utilitário</span>
              </label>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* DADOS GERAIS */}
            <div className="col-span-2 border-b border-gray-100 pb-2 mb-2 font-bold text-gray-400 text-xs uppercase">
              Dados Básicos
            </div>

            <div className="col-span-2">
              <label className="block text-xs font-bold text-gray-500 mb-1">
                Status Inicial
              </label>
              <select
                {...register("status")}
                className="w-full p-3 border rounded-lg bg-white"
              >
                <option value="disponível">Disponível (Padrão)</option>
                <option value="em manutenção">
                  Em Manutenção (Chegou da oficina)
                </option>
                <option value="indisponível">Indisponível</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-gray-500 mb-1">
                Placa
              </label>
              <input
                {...register("placa", { required: true })}
                className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none uppercase"
                placeholder="ABC-1234"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-gray-500 mb-1">
                Chassi
              </label>
              <input
                {...register("chassi", { required: true })}
                className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none uppercase"
                placeholder="123456789"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-gray-500 mb-1">
                Marca
              </label>
              <input
                {...register("marca", { required: true })}
                className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                placeholder="Fiat"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-gray-500 mb-1">
                Modelo
              </label>
              <input
                {...register("modelo", { required: true })}
                className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                placeholder="Argo 1.0"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-gray-500 mb-1">
                Cor
              </label>
              <select
                {...register("cor")}
                className="w-full p-3 border rounded-lg bg-white"
              >
                <option value="Branco">Branco</option>
                <option value="Preto">Preto</option>
                <option value="Prata">Prata</option>
                <option value="Cinza">Cinza</option>
                <option value="Vermelho">Vermelho</option>
                <option value="Azul">Azul</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-bold text-gray-500 mb-1">
                Valor Diária (R$)
              </label>
              <input
                type="number"
                step="0.01"
                {...register("valor_diaria", { required: true })}
                className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                placeholder="150.00"
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-bold text-gray-500 mb-1">
                  Ano Fab.
                </label>
                <input
                  type="number"
                  {...register("ano_fabricacao", { required: true })}
                  className="w-full p-3 border rounded-lg"
                  placeholder="2023"
                />
              </div>
              <div>
                <label className="block text-xs font-bold text-gray-500 mb-1">
                  Ano Mod.
                </label>
                <input
                  type="number"
                  {...register("ano_modelo", { required: true })}
                  className="w-full p-3 border rounded-lg"
                  placeholder="2024"
                />
              </div>
            </div>
            <div>
              <label className="block text-xs font-bold text-gray-500 mb-1">
                Tanque (L)
              </label>
              <input
                type="number"
                {...register("capacidade_tanque", { required: true })}
                className="w-full p-3 border rounded-lg"
                placeholder="50"
              />
            </div>

            <div className="col-span-2 flex gap-6 py-2">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  {...register("cambio_automatico")}
                  className="w-5 h-5 text-blue-600"
                />
                <span className="text-sm font-medium">Câmbio Automático</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  {...register("ar_condicionado")}
                  className="w-5 h-5 text-blue-600"
                />
                <span className="text-sm font-medium">Ar Condicionado</span>
              </label>
            </div>

            {/* CAMPOS ESPECÍFICOS */}
            <div className="col-span-2 border-b border-gray-100 pb-2 mt-4 mb-2 font-bold text-gray-400 text-xs uppercase">
              Detalhes Específicos ({tipoSelecionado})
            </div>

            {tipoSelecionado === "passeio" && (
              <>
                <div>
                  <label className="block text-xs font-bold text-gray-500 mb-1">
                    Portas
                  </label>
                  <input
                    type="number"
                    {...register("qtde_portas", { value: 4 })}
                    className="w-full p-3 border rounded-lg"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-gray-500 mb-1">
                    Carroceria
                  </label>
                  <input
                    {...register("tipo_carroceria")}
                    className="w-full p-3 border rounded-lg"
                    placeholder="Sedan, Hatch..."
                  />
                </div>
              </>
            )}

            {tipoSelecionado === "motocicleta" && (
              <>
                <div>
                  <label className="block text-xs font-bold text-gray-500 mb-1">
                    Cilindrada (cc)
                  </label>
                  <input
                    type="number"
                    {...register("cilindrada")}
                    className="w-full p-3 border rounded-lg"
                    placeholder="160"
                  />
                </div>
                <div className="flex items-center gap-2 mt-6">
                  <input
                    type="checkbox"
                    {...register("partida_eletrica")}
                    defaultChecked
                    className="w-5 h-5"
                  />
                  <span className="text-sm">Partida Elétrica</span>
                </div>
              </>
            )}

            {tipoSelecionado === "utilitario" && (
              <>
                <div>
                  <label className="block text-xs font-bold text-gray-500 mb-1">
                    Tipo (Furgão/Van)
                  </label>
                  <input
                    {...register("tipo_utilitario")}
                    className="w-full p-3 border rounded-lg"
                    placeholder="Furgão"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-gray-500 mb-1">
                    Carga (kg)
                  </label>
                  <input
                    type="number"
                    {...register("capacidade_carga_kg")}
                    className="w-full p-3 border rounded-lg"
                    placeholder="1000"
                  />
                </div>
              </>
            )}

            {/* Campo URL da Imagem */}
            <div className="col-span-2">
              <label className="block text-xs font-bold text-gray-500 mb-1">
                URL da Foto (Opcional)
              </label>
              <input
                {...register("imagem_url")}
                className="w-full p-3 border rounded-lg text-sm"
                placeholder="https://..."
              />
            </div>
          </div>

          {/* Ações */}
          <div className="mt-8 flex justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              className="px-6 py-3 rounded-xl text-gray-600 font-bold hover:bg-gray-100 transition-colors"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="px-8 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold shadow-lg flex items-center gap-2 disabled:opacity-50 font-futuristic"
            >
              {isLoading ? (
                <Loader2 className="animate-spin" />
              ) : (
                "Cadastrar Veículo"
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
