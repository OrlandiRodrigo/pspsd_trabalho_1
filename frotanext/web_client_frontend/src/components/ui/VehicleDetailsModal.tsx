import { Link } from "react-router-dom";
import { X, Check, Info, Fuel, Settings, Wind, Users } from "lucide-react";
import type { Veiculo } from "../../types/veiculo";
import { useAuth } from "../../hooks/useAuth";
import imgPlaceholder from "../../assets/card-frota.png";

interface VehicleDetailsModalProps {
  isOpen: boolean;
  onClose: () => void;
  veiculo: Veiculo | null;
}

export function VehicleDetailsModal({
  isOpen,
  onClose,
  veiculo,
}: VehicleDetailsModalProps) {
  const { isAdmin } = useAuth();

  if (!isOpen || !veiculo) return null;

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/70 backdrop-blur-sm p-4 animate-fade-in">
      <div className="bg-white rounded-3xl shadow-2xl w-full max-w-4xl overflow-hidden transform transition-all scale-100 flex flex-col md:flex-row max-h-[90vh]">
        {/* LADO ESQUERDO: FOTO */}
        <div className="md:w-1/2 bg-gray-100 relative flex items-center justify-center p-8">
          <img
            src={veiculo.imagem_url || imgPlaceholder}
            alt={veiculo.modelo}
            className="w-full h-auto object-contain max-h-[300px] drop-shadow-xl"
          />
          <div className="absolute top-4 left-4 bg-white/90 backdrop-blur px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider shadow-sm">
            {veiculo.tipo_veiculo}
          </div>
        </div>

        {/* LADO DIREITO: INFORMAÇÕES */}
        <div className="md:w-1/2 p-8 flex flex-col overflow-y-auto custom-scrollbar">
          <div className="flex justify-between items-start mb-2">
            <div>
              <h2 className="text-3xl font-bold text-slate-900 font-futuristic">
                {veiculo.modelo}
              </h2>
              <p className="text-gray-500 font-medium">
                {veiculo.marca} • {veiculo.ano_modelo}
              </p>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-slate-900 transition-colors p-2 hover:bg-gray-100 rounded-full"
            >
              <X size={24} />
            </button>
          </div>

          <div className="mb-8 mt-4">
            <p className="text-xs text-gray-400 font-bold uppercase mb-1">
              Valor da Diária
            </p>
            <p className="text-4xl font-bold text-blue-600">
              R$ {veiculo.valor_diaria.toFixed(2)}
            </p>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-8">
            <div className="bg-gray-50 p-3 rounded-xl border border-gray-100 flex items-center gap-3">
              <div className="bg-white p-2 rounded-lg shadow-sm text-blue-500">
                <Settings size={18} />
              </div>
              <div>
                <p className="text-[10px] text-gray-400 font-bold uppercase">
                  Câmbio
                </p>
                <p className="text-sm font-semibold text-gray-700">
                  {veiculo.cambio_automatico ? "Automático" : "Manual"}
                </p>
              </div>
            </div>

            <div className="bg-gray-50 p-3 rounded-xl border border-gray-100 flex items-center gap-3">
              <div className="bg-white p-2 rounded-lg shadow-sm text-blue-500">
                <Wind size={18} />
              </div>
              <div>
                <p className="text-[10px] text-gray-400 font-bold uppercase">
                  Climatização
                </p>
                <p className="text-sm font-semibold text-gray-700">
                  {veiculo.ar_condicionado ? "Ar Condicionado" : "Sem Ar"}
                </p>
              </div>
            </div>

            <div className="bg-gray-50 p-3 rounded-xl border border-gray-100 flex items-center gap-3">
              <div className="bg-white p-2 rounded-lg shadow-sm text-blue-500">
                <Fuel size={18} />
              </div>
              <div>
                <p className="text-[10px] text-gray-400 font-bold uppercase">
                  Tanque
                </p>
                <p className="text-sm font-semibold text-gray-700">
                  {veiculo.capacidade_tanque} Litros
                </p>
              </div>
            </div>

            {veiculo.qtde_passageiros && (
              <div className="bg-gray-50 p-3 rounded-xl border border-gray-100 flex items-center gap-3">
                <div className="bg-white p-2 rounded-lg shadow-sm text-blue-500">
                  <Users size={18} />
                </div>
                <div>
                  <p className="text-[10px] text-gray-400 font-bold uppercase">
                    Passageiros
                  </p>
                  <p className="text-sm font-semibold text-gray-700">
                    {veiculo.qtde_passageiros} Pessoas
                  </p>
                </div>
              </div>
            )}
          </div>

          <div className="mb-8 bg-blue-50 p-4 rounded-xl border border-blue-100">
            <h4 className="font-bold text-blue-800 text-sm mb-2 flex items-center gap-2">
              <Info size={16} /> Ficha Técnica
            </h4>
            <ul className="text-xs text-blue-700 space-y-1 list-disc pl-4">
              <li>Cor: {veiculo.cor}</li>
              <li>Ano Fabricação: {veiculo.ano_fabricacao}</li>
              <li>Chassi: {veiculo.chassi}</li>
              {veiculo.tipo_carroceria && (
                <li>Carroceria: {veiculo.tipo_carroceria}</li>
              )}
              {veiculo.cilindrada && (
                <li>Cilindrada: {veiculo.cilindrada}cc</li>
              )}
              {veiculo.capacidade_carga_kg && (
                <li>Carga: {veiculo.capacidade_carga_kg}kg</li>
              )}
            </ul>
          </div>

          {!isAdmin && (
            <div className="mt-auto">
              <Link
                to="/reservas/nova"
                className="w-full bg-slate-900 hover:bg-blue-600 text-white font-bold py-4 rounded-xl transition-all shadow-lg hover:shadow-blue-500/30 flex justify-center items-center gap-2 text-lg font-futuristic group"
              >
                RESERVAR AGORA{" "}
                <Check className="group-hover:scale-125 transition-transform" />
              </Link>
              <p className="text-center text-xs text-gray-400 mt-3">
                Você será redirecionado para a área de login ou reserva.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
