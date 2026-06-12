import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  Car,
  CalendarRange,
  TrendingUp,
  ArrowUpRight,
  ArrowDownLeft,
  Plus,
  List,
  CheckCircle,
  AlertTriangle,
  Clock,
  Loader2,
} from "lucide-react";
import { AdminLayout } from "../../components/layout/AdminLayout";
import { veiculoService } from "../../services/veiculoService";
import { reservaService } from "../../services/reservaService";

export function AdminDashboard() {
  const [loading, setLoading] = useState(true);

  const [stats, setStats] = useState({
    frota: { total: 0, disponiveis: 0, ocupados: 0 },
    reservas: { ativas: 0, valor: 0 },
    agenda: { acoes: 0, retiradas: 0, devolucoes: 0 },
  });

  useEffect(() => {
    carregarDadosDashboard();
  }, []);

  const carregarDadosDashboard = async () => {
    try {
      const [veiculos, reservas] = await Promise.all([
        veiculoService.listarTodosAdmin(),
        reservaService.listarTodas(),
      ]);

      const totalVeiculos = veiculos.length;
      const disponiveis = veiculos.filter(
        (v) => v.status === "disponível"
      ).length;
      const ocupados = veiculos.filter((v) =>
        ["alugado", "em manutenção", "indisponível", "reservado"].includes(
          v.status
        )
      ).length;

      const reservasAndamento = reservas.filter(
        (r) => r.status === "em_andamento"
      );
      const totalValorAtivo = reservasAndamento.reduce(
        (acc, r) => acc + r.valor_total_estimado,
        0
      );

      const hoje = new Date().toISOString().split("T")[0];

      const retiradasHoje = reservas.filter(
        (r) => r.data_retirada.startsWith(hoje) && r.status === "confirmada"
      ).length;

      const devolucoesHoje = reservas.filter(
        (r) => r.data_devolucao.startsWith(hoje) && r.status === "em_andamento"
      ).length;

      setStats({
        frota: { total: totalVeiculos, disponiveis, ocupados },
        reservas: { ativas: reservasAndamento.length, valor: totalValorAtivo },
        agenda: {
          acoes: retiradasHoje + devolucoesHoje,
          retiradas: retiradasHoje,
          devolucoes: devolucoesHoje,
        },
      });
    } catch (error) {
      console.error("Erro ao carregar dashboard", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <AdminLayout title="Dashboard" subtitle="Carregando indicadores...">
        <div className="flex h-96 items-center justify-center">
          <Loader2 className="animate-spin text-blue-600 w-12 h-12" />
        </div>
      </AdminLayout>
    );
  }

  return (
    <AdminLayout
      title="Visão Geral da Operação"
      subtitle="Acompanhe os indicadores em tempo real."
    >
      {/* GRID DE CARDS (KPIs) */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10 animate-fade-in">
        {/* CARD 1: STATUS DA FROTA */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 relative overflow-hidden group hover:shadow-md transition-all">
          <div className="flex justify-between items-start mb-4">
            <h3 className="font-bold text-slate-700 text-lg">
              Status da Frota
            </h3>
            <div className="bg-blue-50 p-2 rounded-lg text-blue-600">
              <Car size={24} />
            </div>
          </div>

          <div className="flex items-baseline gap-2 mb-6">
            <span className="text-5xl font-bold text-slate-900 font-futuristic">
              {stats.frota.total}
            </span>
            <span className="text-sm text-gray-500 font-medium">Total</span>
          </div>

          <div className="space-y-3 text-sm">
            <div className="flex items-center gap-2 text-green-700 bg-green-50 px-3 py-2 rounded-lg w-full">
              <CheckCircle size={16} />
              <span className="font-bold">
                {stats.frota.disponiveis} Disponíveis agora
              </span>
            </div>
            <div className="flex items-center gap-2 text-orange-700 bg-orange-50 px-3 py-2 rounded-lg w-full">
              <AlertTriangle size={16} />
              <span className="font-bold">
                {stats.frota.ocupados} Ocupados/Manutenção
              </span>
            </div>
          </div>
        </div>

        {/* CARD 2: RESERVAS ATIVAS */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 relative overflow-hidden group hover:shadow-md transition-all">
          <div className="flex justify-between items-start mb-4">
            <h3 className="font-bold text-slate-700 text-lg">
              Reservas Ativas
            </h3>
            <div className="bg-indigo-50 p-2 rounded-lg text-indigo-600">
              <Clock size={24} />
            </div>
          </div>

          <div className="flex items-baseline gap-2 mb-6">
            <span className="text-5xl font-bold text-slate-900 font-futuristic">
              {stats.reservas.ativas}
            </span>
            <span className="text-sm text-gray-500 font-medium">
              Em andamento
            </span>
          </div>

          <div className="mt-auto pt-4 border-t border-gray-100 flex items-center gap-3 text-slate-700">
            <div className="bg-gray-100 p-2 rounded-full">
              <TrendingUp size={20} className="text-green-600" />
            </div>
            <div>
              <p className="text-[10px] uppercase font-bold text-gray-400">
                Faturamento Estimado
              </p>
              <p className="font-bold text-lg text-slate-800">
                {stats.reservas.valor.toLocaleString("pt-BR", {
                  style: "currency",
                  currency: "BRL",
                })}
              </p>
            </div>
          </div>
        </div>

        {/* CARD 3: AGENDA DE HOJE */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 relative overflow-hidden group hover:shadow-md transition-all">
          <div className="flex justify-between items-start mb-4">
            <h3 className="font-bold text-slate-700 text-lg">Agenda de Hoje</h3>
            <div className="bg-purple-50 p-2 rounded-lg text-purple-600">
              <CalendarRange size={24} />
            </div>
          </div>

          <div className="flex items-baseline gap-2 mb-6">
            <span className="text-5xl font-bold text-slate-900 font-futuristic">
              {stats.agenda.acoes}
            </span>
            <span className="text-sm text-gray-500 font-medium">
              Ações Previstas
            </span>
          </div>

          <div className="space-y-2 text-sm">
            <div className="flex items-center justify-between p-2 hover:bg-gray-50 rounded transition-colors border border-transparent hover:border-gray-100">
              <div className="flex items-center gap-2 text-gray-600">
                <ArrowUpRight size={18} className="text-blue-500" /> Retiradas
              </div>
              <span className="font-bold text-slate-900 bg-blue-100 text-blue-700 px-2 py-0.5 rounded">
                {stats.agenda.retiradas}
              </span>
            </div>
            <div className="flex items-center justify-between p-2 hover:bg-gray-50 rounded transition-colors border border-transparent hover:border-gray-100">
              <div className="flex items-center gap-2 text-gray-600">
                <ArrowDownLeft size={18} className="text-green-500" />{" "}
                Devoluções
              </div>
              <span className="font-bold text-slate-900 bg-green-100 text-green-700 px-2 py-0.5 rounded">
                {stats.agenda.devolucoes}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* ATALHOS RÁPIDOS */}
      <h3 className="text-xl font-bold text-slate-700 mb-6 font-futuristic">
        Atalhos Rápidos
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Botão Adicionar Veículo */}
        <Link
          to="/admin/veiculos"
          className="bg-[#007bff] hover:bg-[#0056b3] text-white p-6 rounded-xl shadow-lg flex items-center justify-center gap-3 transition-all transform hover:-translate-y-1 group"
        >
          <div className="bg-white/20 p-3 rounded-full group-hover:scale-110 transition-transform">
            <Plus size={24} />
          </div>
          <span className="font-bold text-lg">Gerenciar Frota</span>
        </Link>

        {/* Botão Ver Reservas */}
        <Link
          to="/admin/reservas"
          className="bg-white hover:bg-gray-50 text-slate-700 border-2 border-gray-200 p-6 rounded-xl shadow-sm flex items-center justify-center gap-3 transition-all transform hover:-translate-y-1 group"
        >
          <div className="bg-gray-100 p-3 rounded-full group-hover:bg-gray-200 transition-colors text-slate-600">
            <List size={24} />
          </div>
          <span className="font-bold text-lg">Ver Todas as Reservas</span>
        </Link>
      </div>
    </AdminLayout>
  );
}
