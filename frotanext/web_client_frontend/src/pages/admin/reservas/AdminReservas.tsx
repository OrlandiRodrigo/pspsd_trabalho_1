import { useState, useEffect } from 'react';
import { Search, Loader2, Edit, Trash2, CheckCircle, Info, Filter, Key } from 'lucide-react';
import { AdminLayout } from '../../../components/layout/AdminLayout';
import { reservaService, type UpdateReservaData } from '../../../services/reservaService';
import type { Reserva } from '../../../types/reserva';

import { DetailsModal } from '../../../components/ui/DetailsModal';
import { CancelModal } from '../../../components/ui/CancelModal';
import { ModifyModal } from '../../../components/ui/ModifyModal';
import { StatusModal } from '../../../components/ui/StatusModal';
import { FinalizeModal } from '../../../components/ui/FinalizeModal';

export function AdminReservas() {
  // --- ESTADOS ---
  const [reservas, setReservas] = useState<Reserva[]>([]);
  const [loading, setLoading] = useState(true);
  const [termoBusca, setTermoBusca] = useState('');
  const [filtroStatus, setFiltroStatus] = useState('todas');

  const [reservaSelecionada, setReservaSelecionada] = useState<Reserva | null>(null);
  const [loadingAction, setLoadingAction] = useState(false);

  const [detailsOpen, setDetailsOpen] = useState(false);
  const [editOpen, setEditOpen] = useState(false);
  const [cancelOpen, setCancelOpen] = useState(false);
  const [finalizeOpen, setFinalizeOpen] = useState(false);
  
  const [statusModal, setStatusModal] = useState<{ open: boolean; type: 'success' | 'error'; title: string; msg: string }>({
    open: false, type: 'success', title: '', msg: ''
  });

  const carregarDados = async () => {
    setLoading(true);
    try {
      const dados = await reservaService.listarTodas();
      setReservas(dados);
    } catch (error) {
      console.error("Erro ao carregar reservas:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    carregarDados();
  }, []);

  // --- HANDLERS ---

  const handleConfirmar = async (id: number) => {
    setLoadingAction(true);
    try {
      await reservaService.confirmar(id);
      setStatusModal({ open: true, type: 'success', title: 'Reserva Confirmada', msg: 'O veículo foi reservado com sucesso.' });
      await carregarDados();
    } catch (err) {
      setStatusModal({ open: true, type: 'error', title: 'Erro', msg: 'Falha ao confirmar reserva.' });
    } finally {
      setLoadingAction(false);
    }
  };

  const handleRetirar = async (id: number) => {
    setLoadingAction(true);
    try {
      await reservaService.retirar(id);
      setStatusModal({ open: true, type: 'success', title: 'Retirada Registrada', msg: 'Locação iniciada. Veículo marcado como ALUGADO.' });
      await carregarDados();
    } catch (err) {
      setStatusModal({ open: true, type: 'error', title: 'Erro', msg: 'Falha ao registrar retirada.' });
    } finally {
      setLoadingAction(false);
    }
  };

  const handleCancel = async () => {
    if (!reservaSelecionada) return;
    setLoadingAction(true);
    try {
      await reservaService.cancelar(reservaSelecionada.id_reserva);
      setCancelOpen(false);
      setStatusModal({ open: true, type: 'success', title: 'Reserva Cancelada', msg: 'O status foi atualizado e o veículo liberado.' });
      await carregarDados();
    } catch (err) {
      setCancelOpen(false);
      setStatusModal({ open: true, type: 'error', title: 'Erro', msg: 'Não foi possível cancelar a reserva.' });
    } finally {
      setLoadingAction(false);
    }
  };

  const handleEdit = async (id: number, dados: UpdateReservaData) => {
    setLoadingAction(true);
    try {
      await reservaService.atualizar(id, dados);
      setEditOpen(false);
      setStatusModal({ open: true, type: 'success', title: 'Reserva Atualizada', msg: 'As alterações foram salvas com sucesso.' });
      await carregarDados();
    } catch (err) {
      setEditOpen(false);
      setStatusModal({ open: true, type: 'error', title: 'Erro', msg: 'Falha ao atualizar os dados da reserva.' });
    } finally {
      setLoadingAction(false);
    }
  };

  const handleFinalize = async (id: number) => {
    setLoadingAction(true);
    try {
      await reservaService.finalizar(id);
      setFinalizeOpen(false);
      setStatusModal({ open: true, type: 'success', title: 'Devolução Concluída', msg: 'Reserva finalizada, valores calculados e veículo disponível.' });
      await carregarDados();
    } catch (err) {
      setFinalizeOpen(false);
      setStatusModal({ open: true, type: 'error', title: 'Erro', msg: 'Falha ao registrar a devolução.' });
    } finally {
      setLoadingAction(false);
    }
  };

  // --- HELPERS VISUAIS ---
  const getStatusBadge = (status: string) => {
    const map: Record<string, string> = {
      'confirmada': 'bg-green-100 text-green-700 border-green-200',
      'em_andamento': 'bg-blue-100 text-blue-700 border-blue-200',
      'finalizada': 'bg-gray-100 text-gray-600 border-gray-200',
      'cancelada': 'bg-red-100 text-red-600 border-red-200',
      'pendente': 'bg-yellow-100 text-yellow-700 border-yellow-200'
    };
    return map[status] || 'bg-gray-100';
  };

  const formatData = (iso: string) => new Date(iso).toLocaleDateString('pt-BR');

  const reservasFiltradas = reservas.filter(r => {
    const termo = termoBusca.toLowerCase();
    const matchBusca = 
        r.id_reserva.toString().includes(termo) ||
        r.veiculo.modelo.toLowerCase().includes(termo) ||
        r.veiculo.placa.toLowerCase().includes(termo);
    
    const matchStatus = filtroStatus === 'todas' || r.status === filtroStatus;

    return matchBusca && matchStatus;
  });

  return (
    <AdminLayout title="Gerenciamento de Reservas" subtitle="Controle total de locações e devoluções.">
      
      {/* MODAIS */}
      <DetailsModal 
        isOpen={detailsOpen} 
        onClose={() => setDetailsOpen(false)} 
        reserva={reservaSelecionada} 
      />
      
      <CancelModal 
        isOpen={cancelOpen} 
        isLoading={loadingAction} 
        onClose={() => setCancelOpen(false)} 
        onConfirm={handleCancel} 
        title="Cancelar Reserva?" 
        description="Esta ação é irreversível e liberará o veículo imediatamente."
      />
      
      <ModifyModal 
        isOpen={editOpen} 
        isLoading={loadingAction} 
        onClose={() => setEditOpen(false)} 
        onConfirm={handleEdit} 
        reservaAtual={reservaSelecionada} 
      />

      <FinalizeModal 
        isOpen={finalizeOpen} 
        isLoading={loadingAction} 
        onClose={() => setFinalizeOpen(false)} 
        onConfirm={handleFinalize} 
        reserva={reservaSelecionada} 
      />

      <StatusModal 
        isOpen={statusModal.open} 
        onClose={() => setStatusModal({...statusModal, open: false})} 
        type={statusModal.type} 
        title={statusModal.title} 
        message={statusModal.msg} 
      />


      {/* --- BARRA DE FERRAMENTAS --- */}
      <div className="flex flex-col md:flex-row justify-between items-center gap-4 mb-6 bg-white p-4 rounded-xl shadow-sm border border-gray-200">
         
         {/* Campo de Busca */}
         <div className="relative w-full md:w-80">
            <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input 
                type="text" 
                placeholder="Buscar por ID, Placa ou Modelo..." 
                className="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
                value={termoBusca}
                onChange={e => setTermoBusca(e.target.value)}
            />
         </div>

         {/* Filtros de Status */}
         <div className="flex items-center gap-2 overflow-x-auto w-full md:w-auto pb-2 md:pb-0">
             <Filter size={18} className="text-gray-400 hidden md:block shrink-0" />
             {['todas', 'pendente', 'confirmada', 'em_andamento', 'finalizada', 'cancelada'].map(st => (
                 <button
                    key={st}
                    onClick={() => setFiltroStatus(st)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-bold uppercase transition-all whitespace-nowrap ${
                        filtroStatus === st 
                        ? 'bg-slate-800 text-white shadow-md' 
                        : 'bg-gray-100 text-gray-500 hover:bg-gray-200 border border-gray-200'
                    }`}
                 >
                    {st.replace('_', ' ')}
                 </button>
             ))}
         </div>
      </div>

      {/* --- TABELA DE RESERVAS --- */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
         {loading ? (
            <div className="p-12 flex justify-center"><Loader2 className="animate-spin text-blue-600" size={32} /></div>
         ) : (
            <div className="overflow-x-auto">
                <table className="w-full text-sm text-left">
                    <thead className="bg-gray-50 text-gray-600 uppercase text-xs font-bold border-b border-gray-200">
                        <tr>
                            <th className="px-6 py-4">ID</th>
                            <th className="px-6 py-4">Veículo</th>
                            <th className="px-6 py-4">Período</th>
                            <th className="px-6 py-4">Valor Est.</th>
                            <th className="px-6 py-4">Status</th>
                            <th className="px-6 py-4 text-right">Ações</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                        {reservasFiltradas.map((reserva) => (
                            <tr key={reserva.id_reserva} className="hover:bg-gray-50 transition-colors group">
                                <td className="px-6 py-4 font-mono text-gray-500">#{reserva.id_reserva}</td>
                                
                                <td className="px-6 py-4">
                                    <div className="font-bold text-slate-800">{reserva.veiculo.modelo}</div>
                                    <div className="text-xs text-gray-400 font-mono">{reserva.veiculo.placa}</div>
                                </td>
                                
                                <td className="px-6 py-4 text-gray-600 text-xs">
                                    <div><span className="font-bold">Ret:</span> {formatData(reserva.data_retirada)}</div>
                                    <div><span className="font-bold">Dev:</span> {formatData(reserva.data_devolucao)}</div>
                                </td>
                                
                                <td className="px-6 py-4 font-mono text-blue-600 font-bold">
                                    R$ {reserva.valor_total_estimado.toFixed(2)}
                                </td>
                                
                                <td className="px-6 py-4">
                                    <span className={`px-2 py-1 rounded-full text-[10px] font-bold border uppercase ${getStatusBadge(reserva.status)}`}>
                                        {reserva.status.replace('_', ' ')}
                                    </span>
                                </td>
                                
                                <td className="px-6 py-4 text-right flex justify-end gap-2 items-center">
                                    
                                    {/* 1. INFO */}
                                    <button 
                                        onClick={() => { setReservaSelecionada(reserva); setDetailsOpen(true); }} 
                                        className="p-2 text-gray-500 hover:bg-gray-100 rounded-lg transition-colors" 
                                        title="Ver Detalhes"
                                    >
                                        <Info size={18} />
                                    </button>

                                    {/* 2. CONFIRMAR  */}
                                    {reserva.status === 'pendente' && (
                                        <button 
                                            onClick={() => handleConfirmar(reserva.id_reserva)} 
                                            className="p-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors" 
                                            title="Aprovar Reserva"
                                        >
                                            <CheckCircle size={18} />
                                        </button>
                                    )}

                                    {/* 3. RETIRAR  */}
                                    {reserva.status === 'confirmada' && (
                                        <button 
                                            onClick={() => handleRetirar(reserva.id_reserva)} 
                                            className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors" 
                                            title="Registrar Retirada (Entregar Chaves)"
                                        >
                                            <Key size={18} />
                                        </button>
                                    )}

                                    {/* 4. EDITAR */}
                                    {['pendente', 'confirmada', 'em_andamento'].includes(reserva.status) && (
                                        <button 
                                            onClick={() => { setReservaSelecionada(reserva); setEditOpen(true); }} 
                                            className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors" 
                                            title="Editar Reserva"
                                        >
                                            <Edit size={18} />
                                        </button>
                                    )}

                                    {/* 5. FINALIZAR  */}
                                    {reserva.status === 'em_andamento' && (
                                        <button 
                                            onClick={() => { setReservaSelecionada(reserva); setFinalizeOpen(true); }} 
                                            className="p-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors" 
                                            title="Registrar Devolução"
                                        >
                                            <CheckCircle size={18} />
                                        </button>
                                    )}

                                    {/* 6. CANCELAR  */}
                                    {['pendente', 'confirmada'].includes(reserva.status) && (
                                        <button 
                                            onClick={() => { setReservaSelecionada(reserva); setCancelOpen(true); }} 
                                            className="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors" 
                                            title="Cancelar Reserva"
                                        >
                                            <Trash2 size={18} />
                                        </button>
                                    )}

                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                
                {/* Estado Vazio */}
                {!loading && reservasFiltradas.length === 0 && (
                    <div className="p-12 text-center text-gray-400 bg-gray-50">
                        <p>Nenhuma reserva encontrada com os filtros atuais.</p>
                    </div>
                )}
            </div>
         )}
      </div>
    </AdminLayout>
  );
}