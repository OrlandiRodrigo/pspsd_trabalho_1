import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { Navbar } from "../../components/layout/Navbar";
import { NavbarLogin } from "../../components/layout/NavbarLogin";
import { Footer } from "../../components/layout/Footer";
import { veiculoService } from "../../services/veiculoService";
import type { Veiculo, TipoVeiculo } from "../../types/veiculo";
import { Car, Bike, Truck, Loader2, Filter, Info } from "lucide-react";
import { VehicleDetailsModal } from "../../components/ui/VehicleDetailsModal";
import { useAuth } from "../../hooks/useAuth";

import imgPlaceholder from "../../assets/card-frota.png";

export function Frota() {
  const { user } = useAuth();
  const [searchParams] = useSearchParams();

  const tipoInicial =
    (searchParams.get("tipo") as TipoVeiculo | "todos") || "todos";

  const [veiculos, setVeiculos] = useState<Veiculo[]>([]);
  const [loading, setLoading] = useState(true);
  const [filtroAtual, setFiltroAtual] = useState<TipoVeiculo | "todos">(
    tipoInicial
  );

  const [modalOpen, setModalOpen] = useState(false);
  const [veiculoSelecionado, setVeiculoSelecionado] = useState<Veiculo | null>(
    null
  );

  useEffect(() => {
    const carregarVeiculos = async () => {
      setLoading(true);
      try {
        const categoria = filtroAtual === "todos" ? undefined : filtroAtual;
        const dados = await veiculoService.listar(categoria);
        setVeiculos(dados);
      } catch (error) {
        console.error("Erro ao buscar frota:", error);
      } finally {
        setLoading(false);
      }
    };
    carregarVeiculos();
  }, [filtroAtual]);

  const abrirDetalhes = (veiculo: Veiculo) => {
    setVeiculoSelecionado(veiculo);
    setModalOpen(true);
  };

  return (
    <div className="min-h-screen bg-gray-50 font-sans text-slate-900 flex flex-col">
      {user ? <NavbarLogin /> : <Navbar />}

      <VehicleDetailsModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        veiculo={veiculoSelecionado}
      />

      <div className="bg-slate-900 text-white py-16 text-center">
        <h1 className="text-4xl font-bold font-futuristic mb-4">
          Conheça Nossa Frota
        </h1>
        <p className="text-gray-300 max-w-2xl mx-auto px-4">
          Veículos modernos, revisados e prontos para te levar aonde você
          precisa.
        </p>
      </div>

      <div className="max-w-7xl mx-auto px-4 -mt-8 relative z-10 pb-20 flex-grow">
        {/* BARRA DE FILTROS */}
        <div className="bg-white p-2 rounded-xl shadow-lg flex flex-wrap justify-center gap-2 mb-12 border border-gray-100 w-fit mx-auto">
          <button
            onClick={() => setFiltroAtual("todos")}
            className={`px-6 py-3 rounded-lg text-sm font-bold transition-all flex items-center gap-2 ${
              filtroAtual === "todos"
                ? "bg-blue-600 text-white shadow-md"
                : "text-gray-600 hover:bg-gray-50"
            }`}
          >
            <Filter size={18} /> Todos
          </button>
          <button
            onClick={() => setFiltroAtual("passeio")}
            className={`px-6 py-3 rounded-lg text-sm font-bold transition-all flex items-center gap-2 ${
              filtroAtual === "passeio"
                ? "bg-blue-600 text-white shadow-md"
                : "text-gray-600 hover:bg-gray-50"
            }`}
          >
            <Car size={18} /> Carros
          </button>
          <button
            onClick={() => setFiltroAtual("motocicleta")}
            className={`px-6 py-3 rounded-lg text-sm font-bold transition-all flex items-center gap-2 ${
              filtroAtual === "motocicleta"
                ? "bg-blue-600 text-white shadow-md"
                : "text-gray-600 hover:bg-gray-50"
            }`}
          >
            <Bike size={18} /> Motos
          </button>
          <button
            onClick={() => setFiltroAtual("utilitario")}
            className={`px-6 py-3 rounded-lg text-sm font-bold transition-all flex items-center gap-2 ${
              filtroAtual === "utilitario"
                ? "bg-blue-600 text-white shadow-md"
                : "text-gray-600 hover:bg-gray-50"
            }`}
          >
            <Truck size={18} /> Utilitários
          </button>
        </div>

        {/* GRID DE VEÍCULOS */}
        {loading ? (
          <div className="flex justify-center py-20">
            <Loader2 size={48} className="animate-spin text-blue-600" />
          </div>
        ) : veiculos.length === 0 ? (
          <div className="text-center py-20 opacity-60">
            <p className="text-xl font-bold text-gray-400">
              Nenhum veículo encontrado.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {veiculos.map((veiculo) => (
              <div
                key={veiculo.id_veiculo}
                className="bg-white rounded-3xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-2xl transition-all group flex flex-col h-full transform hover:-translate-y-1"
              >
                <div className="h-56 bg-gray-50 relative flex items-center justify-center p-6">
                  <img
                    src={veiculo.imagem_url || imgPlaceholder}
                    alt={veiculo.modelo}
                    className="w-full h-full object-contain drop-shadow-lg group-hover:scale-110 transition-transform duration-500"
                  />
                  <div className="absolute top-4 right-4 bg-white/90 backdrop-blur text-slate-700 px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider shadow-sm border border-gray-100">
                    {veiculo.tipo_veiculo}
                  </div>
                </div>

                <div className="p-6 flex-1 flex flex-col">
                  <div className="mb-4">
                    <h3 className="text-2xl font-bold text-slate-900 mb-1 font-futuristic">
                      {veiculo.modelo}
                    </h3>
                    <p className="text-sm text-gray-500 font-medium">
                      {veiculo.marca} • {veiculo.ano_modelo}
                    </p>
                  </div>

                  <div className="grid grid-cols-2 gap-2 mb-6 text-xs text-gray-600">
                    <span className="bg-gray-50 px-2 py-1 rounded border border-gray-100 text-center font-medium text-slate-700">
                      {veiculo.cambio_automatico ? "Automático" : "Manual"}
                    </span>
                    {veiculo.ar_condicionado && (
                      <span className="bg-gray-50 px-2 py-1 rounded border border-gray-100 text-center font-medium text-slate-700">
                        Ar Condicionado
                      </span>
                    )}
                    <span className="bg-gray-50 px-2 py-1 rounded border border-gray-100 text-center col-span-2 font-medium text-slate-700">
                      Cor: {veiculo.cor}
                    </span>
                  </div>

                  {/* AQUI: Adicionei gap-6 para separar o valor do botão */}
                  <div className="mt-auto pt-6 border-t border-gray-100 flex items-center justify-between gap-6">
                    <div>
                      <p className="text-[10px] text-gray-400 font-bold uppercase">
                        Diária a partir de
                      </p>
                      <p className="text-2xl font-bold text-blue-600 font-futuristic">
                        R$ {veiculo.valor_diaria.toFixed(2)}
                      </p>
                    </div>

                    <button
                      onClick={() => abrirDetalhes(veiculo)}
                      className="bg-white hover:bg-gray-50 text-slate-900 border-2 border-slate-900 font-bold py-2 px-4 rounded-xl transition-colors flex items-center gap-2 text-sm whitespace-nowrap"
                    >
                      Ver Detalhes <Info size={16} />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
}
