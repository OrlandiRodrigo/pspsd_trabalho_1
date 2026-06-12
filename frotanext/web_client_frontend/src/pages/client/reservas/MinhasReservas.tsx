import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Loader2, Calendar, MapPin, AlertCircle, Edit } from "lucide-react";
import { NavbarInternal } from "../../../components/layout/NavbarInternal";
import { CancelModal } from "../../../components/ui/CancelModal";
import { ModifyModal } from "../../../components/ui/ModifyModal";
import { DetailsModal } from "../../../components/ui/DetailsModal";
import {
  reservaService,
  type UpdateReservaData,
} from "../../../services/reservaService";
import type { Reserva } from "../../../types/reserva";
import imgPlaceholder from "../../../assets/card-frota.png";
import { Footer } from "../../../components/layout/Footer";

export function MinhasReservas() {
  const [reservas, setReservas] = useState<Reserva[]>([]);
  const [loading, setLoading] = useState(true);
  const [filtroStatus, setFiltroStatus] = useState<string>("todas");
  const [cancelModalOpen, setCancelModalOpen] = useState(false);
  const [modifyModalOpen, setModifyModalOpen] = useState(false);
  const [detailsModalOpen, setDetailsModalOpen] = useState(false);
  const [reservaParaDetalhes, setReservaParaDetalhes] =
    useState<Reserva | null>(null);

  const [reservaSelecionada, setReservaSelecionada] = useState<Reserva | null>(
    null
  );
  const [loadingAction, setLoadingAction] = useState(false);

  useEffect(() => {
    carregarReservas();
  }, []);

  const carregarReservas = async () => {
    try {
      const dados = await reservaService.listarMinhas();
      setReservas(dados);
    } catch (error) {
      console.error("Erro ao buscar reservas:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleClickCancelar = (reserva: Reserva) => {
    setReservaSelecionada(reserva);
    setCancelModalOpen(true);
  };

  const confirmarCancelamento = async () => {
    if (!reservaSelecionada) return;
    setLoadingAction(true);
    try {
      await reservaService.cancelar(reservaSelecionada.id_reserva);
      await carregarReservas();
      setCancelModalOpen(false);
      setReservaSelecionada(null);
    } catch (error) {
      console.error(error);
      alert("Erro ao cancelar reserva.");
    } finally {
      setLoadingAction(false);
    }
  };

  const handleClickDetalhes = (reserva: Reserva) => {
    setReservaParaDetalhes(reserva);
    setDetailsModalOpen(true);
  };

  const handleClickModificar = (reserva: Reserva) => {
    setReservaSelecionada(reserva);
    setModifyModalOpen(true);
  };

  const confirmarModificacao = async (id: number, dados: UpdateReservaData) => {
    setLoadingAction(true);
    try {
      await reservaService.atualizar(id, dados);
      await carregarReservas();
      setModifyModalOpen(false);
      setReservaSelecionada(null);
      alert("Reserva atualizada com sucesso!");
    } catch (error) {
      console.error(error);
      alert("Erro ao modificar reserva. Verifique se as datas são válidas.");
    } finally {
      setLoadingAction(false);
    }
  };

  const formatarData = (isoString: string) => {
    const data = new Date(isoString);
    return data.toLocaleString("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const reservasFiltradas = reservas.filter((r) => {
    if (filtroStatus === "todas") return true;
    if (filtroStatus === "ativas")
      return ["confirmada", "em_andamento"].includes(r.status);
    if (filtroStatus === "finalizadas") return r.status === "finalizada";
    if (filtroStatus === "canceladas") return r.status === "cancelada";
    return true;
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case "confirmada":
        return "bg-green-100 text-green-700 border-green-200";
      case "em_andamento":
        return "bg-blue-100 text-blue-700 border-blue-200";
      case "finalizada":
        return "bg-gray-200 text-gray-600 border-gray-300";
      case "cancelada":
        return "bg-red-100 text-red-600 border-red-200";
      default:
        return "bg-gray-100 text-gray-600";
    }
  };

  const getStatusLabel = (status: string) => {
    const labels: any = {
      confirmada: "Confirmado",
      em_andamento: "Em Andamento",
      finalizada: "Finalizado",
      cancelada: "Cancelado",
      pendente: "Pendente",
    };
    return labels[status] || status;
  };

  return (
    <div className="min-h-screen bg-gray-100 font-sans text-slate-900 pb-20">
      <NavbarInternal />

      <CancelModal
        isOpen={cancelModalOpen}
        isLoading={loadingAction}
        onClose={() => setCancelModalOpen(false)}
        onConfirm={confirmarCancelamento}
        title="Cancelar Reserva?"
        description="Você tem certeza que deseja cancelar este agendamento?"
      />

      <ModifyModal
        isOpen={modifyModalOpen}
        isLoading={loadingAction}
        onClose={() => setModifyModalOpen(false)}
        onConfirm={confirmarModificacao}
        reservaAtual={reservaSelecionada}
      />

      <DetailsModal
        isOpen={detailsModalOpen}
        onClose={() => setDetailsModalOpen(false)}
        reserva={reservaParaDetalhes}
      />

      <div className="max-w-5xl mx-auto px-4 mt-8">
        <h1 className="text-2xl font-bold text-slate-800 mb-6 font-futuristic">
          Meus Agendamentos e Histórico
        </h1>
        <div className="flex flex-wrap gap-2 mb-8">
          <button
            onClick={() => setFiltroStatus("todas")}
            className={`px-6 py-2 rounded-full text-sm font-bold shadow-sm transition-all ${
              filtroStatus === "todas"
                ? "bg-[#007bff] text-white shadow-md"
                : "bg-white text-gray-600 hover:bg-gray-100 border border-gray-200"
            }`}
          >
            Todas
          </button>
          <button
            onClick={() => setFiltroStatus("ativas")}
            className={`px-6 py-2 rounded-full text-sm font-bold shadow-sm transition-all ${
              filtroStatus === "ativas"
                ? "bg-[#007bff] text-white shadow-md"
                : "bg-white text-gray-600 hover:bg-gray-100 border border-gray-200"
            }`}
          >
            Próximas/Ativas
          </button>
          <button
            onClick={() => setFiltroStatus("finalizadas")}
            className={`px-6 py-2 rounded-full text-sm font-bold shadow-sm transition-all ${
              filtroStatus === "finalizadas"
                ? "bg-[#007bff] text-white shadow-md"
                : "bg-white text-gray-600 hover:bg-gray-100 border border-gray-200"
            }`}
          >
            Finalizadas
          </button>
          <button
            onClick={() => setFiltroStatus("canceladas")}
            className={`px-6 py-2 rounded-full text-sm font-bold shadow-sm transition-all ${
              filtroStatus === "canceladas"
                ? "bg-[#007bff] text-white shadow-md"
                : "bg-white text-gray-600 hover:bg-gray-100 border border-gray-200"
            }`}
          >
            Canceladas
          </button>
        </div>
            
        <div className="space-y-6">
          {loading ? (
            <div className="flex justify-center py-20">
              <Loader2 size={48} className="animate-spin text-blue-600" />
            </div>
          ) : reservasFiltradas.length === 0 ? (
            <div className="text-center py-16 bg-white rounded-2xl border border-dashed border-gray-300">
              <p className="text-gray-500 text-lg mb-4">
                Nenhuma reserva encontrada.
              </p>
              <Link
                to="/reservas/nova"
                className="text-blue-600 font-bold hover:underline"
              >
                Fazer uma nova reserva
              </Link>
            </div>
          ) : (
            reservasFiltradas.map((reserva) => (
              <div
                key={reserva.id_reserva}
                className={`bg-white rounded-xl shadow-sm border border-gray-200 p-6 flex flex-col md:flex-row items-center gap-6 transition-all hover:shadow-md ${
                  reserva.status === "cancelada" ||
                  reserva.status === "finalizada"
                    ? "opacity-80 grayscale-[0.5]"
                    : ""
                }`}
              >
                <div className="w-full md:w-1/3">
                  <img
                    src={reserva.veiculo.imagem_url || imgPlaceholder}
                    alt={reserva.veiculo.modelo}
                    className="w-full h-32 object-contain"
                  />
                </div>

                <div className="flex-1 space-y-2 w-full text-center md:text-left">
                  <div className="flex flex-col md:flex-row md:items-center gap-2 mb-2">
                    <h3 className="text-xl font-bold text-slate-900">
                      {reserva.veiculo.modelo}{" "}
                      <span className="text-sm font-normal text-gray-500">
                        - {reserva.veiculo.tipo_veiculo}
                      </span>
                    </h3>
                    <span
                      className={`inline-block text-[10px] uppercase font-bold px-2 py-1 rounded border ${getStatusColor(
                        reserva.status
                      )} w-fit mx-auto md:mx-0`}
                    >
                      {getStatusLabel(reserva.status)}
                    </span>
                  </div>
                  <div className="flex gap-2 mb-3">
                    {reserva.seguro_pessoal && (
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-indigo-100 text-indigo-700 border border-indigo-200 flex items-center gap-1">
                        🛡️ Pessoal
                      </span>
                    )}
                    {reserva.seguro_terceiros && (
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-purple-100 text-purple-700 border border-purple-200 flex items-center gap-1">
                        🚗 Terceiros
                      </span>
                    )}
                  </div>

                  <div className="text-sm text-gray-600 mt-2 space-y-1 bg-gray-50 p-3 rounded-lg border border-gray-100">
                    <p className="flex items-center gap-2 justify-center md:justify-start">
                      <Calendar size={14} className="text-blue-500" />
                      <strong>Retirada:</strong>{" "}
                      {formatarData(reserva.data_retirada)}
                    </p>
                    <p className="flex items-center gap-2 justify-center md:justify-start">
                      <Calendar size={14} className="text-orange-500" />
                      <strong>Devolução:</strong>{" "}
                      {formatarData(reserva.data_devolucao)}
                    </p>
                    <p className="flex items-center gap-2 justify-center md:justify-start text-xs text-gray-400">
                      <MapPin size={12} /> Local: Agência Central (Aeroporto)
                    </p>
                  </div>
                </div>

                <div className="w-full md:w-auto flex flex-col gap-3 min-w-[160px]">
                  <button
                    onClick={() => handleClickDetalhes(reserva)}
                    className="bg-[#007bff] hover:bg-[#0056b3] text-white font-bold py-2 px-4 rounded-lg shadow transition-colors text-sm"
                  >
                    Ver Detalhes
                  </button>

                  {/* Ações de Modificar/Cancelar */}
                  {["confirmada", "pendente"].includes(reserva.status) && (
                    <>
                      <button
                        onClick={() => handleClickModificar(reserva)}
                        className="text-gray-500 text-xs hover:text-blue-600 underline decoration-gray-300 transition-colors flex items-center justify-center gap-1"
                      >
                        <Edit size={12} /> Modificar Reserva
                      </button>
                      <button
                        onClick={() => handleClickCancelar(reserva)}
                        className="text-red-400 text-xs hover:text-red-600 underline decoration-red-200 transition-colors flex items-center justify-center gap-1"
                      >
                        <AlertCircle size={12} /> Cancelar
                      </button>
                    </>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    {/* FOOTER */}
      <Footer />
    </div>
  );
}
