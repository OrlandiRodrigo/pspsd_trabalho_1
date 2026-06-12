import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Search, Loader2, Car, Bike, Truck } from 'lucide-react';
import { AdminLayout } from '../../../components/layout/AdminLayout';
import { veiculoService } from '../../../services/veiculoService';
import type { Veiculo, TipoVeiculo } from '../../../types/veiculo';

// Modais
import { ConfirmModal } from '../../../components/ui/ConfirmModal';
import { StatusModal } from '../../../components/ui/StatusModal';
import { VehicleEditModal } from '../../../components/ui/VehicleEditModal';
import { AddVehicleModal } from '../../../components/ui/AddVehicleModal';
import { VehicleDetailsModal } from '../../../components/ui/VehicleDetailsModal';

export function AdminFrota() {
  // --- ESTADOS ---
  const [veiculos, setVeiculos] = useState<Veiculo[]>([]);
  const [loading, setLoading] = useState(true);
  const [termoBusca, setTermoBusca] = useState('');

  // Estados de Modais
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [editModalOpen, setEditModalOpen] = useState(false);
  const [addModalOpen, setAddModalOpen] = useState(false);
  const [detailsModalOpen, setDetailsModalOpen] = useState(false);

  const [veiculoSelecionado, setVeiculoSelecionado] = useState<Veiculo | null>(null);
  const [loadingAction, setLoadingAction] = useState(false);

  const [statusModal, setStatusModal] = useState<{ open: boolean; type: 'success' | 'error'; title: string; msg: string }>({
    open: false, type: 'success', title: '', msg: ''
  });

  // --- CARREGAR DADOS ---
  const carregarDados = async () => {
    setLoading(true);
    try {
      const dados = await veiculoService.listarTodosAdmin();
      setVeiculos(dados);
    } catch (error) {
      console.error("Erro ao carregar frota", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    carregarDados();
  }, []);

  // --- HANDLERS (Ações) ---

  // 1. Adicionar
  const handleAddVeiculo = async (tipo: TipoVeiculo, dados: any) => {
      setLoadingAction(true);
      try {
          await veiculoService.criar(tipo, dados);
          setAddModalOpen(false);
          setStatusModal({ open: true, type: 'success', title: 'Veículo Cadastrado', msg: 'Novo veículo adicionado à frota.' });
          await carregarDados();
      } catch (error: any) {
          const msg = error.response?.data?.detail || "Erro ao criar veículo.";
          setStatusModal({ open: true, type: 'error', title: 'Erro', msg: msg });
      } finally {
          setLoadingAction(false);
      }
  };

  // 2. Detalhes
  const openDetails = (v: Veiculo) => {
      setVeiculoSelecionado(v);
      setDetailsModalOpen(true);
  };

  // 3. Editar (Abrir modal)
  const handleEditClick = (veiculo: Veiculo) => {
    setVeiculoSelecionado(veiculo);
    setEditModalOpen(true);
  };

  // 4. Editar (Confirmar)
  const confirmEdit = async (id: number, tipo: TipoVeiculo, data: any) => {
       setLoadingAction(true);
       try {
           await veiculoService.atualizar(id, tipo, data);
           setEditModalOpen(false);
           setStatusModal({ open: true, type: 'success', title: 'Veículo Atualizado', msg: 'As informações foram salvas com sucesso.' });
           await carregarDados();
       } catch(err) {
           setStatusModal({ open: true, type: 'error', title: 'Erro', msg: 'Erro ao atualizar veículo.' });
       } finally {
           setLoadingAction(false);
       }
  };

  // 5. Excluir (Abrir modal)
  const handleDeleteClick = (veiculo: Veiculo) => {
    setVeiculoSelecionado(veiculo);
    setDeleteModalOpen(true);
  };

  // 6. Excluir (Confirmar)
  const confirmDelete = async () => {
      if(!veiculoSelecionado) return;
      setLoadingAction(true);
      try {
          await veiculoService.deletar(veiculoSelecionado.id_veiculo);
          setDeleteModalOpen(false);
          setStatusModal({ open: true, type: 'success', title: 'Veículo Excluído', msg: 'O veículo foi removido com sucesso.' });
          await carregarDados();
      } catch(err) {
          setDeleteModalOpen(false); 
          setStatusModal({ open: true, type: 'error', title: 'Erro ao Excluir', msg: 'Não foi possível remover. Verifique se não há reservas associadas.' });
      } finally {
          setLoadingAction(false);
      }
  };

  // --- HELPERS VISUAIS ---
  const getStatusBadge = (status: string) => {
    const styles: any = {
      'disponível': 'bg-green-100 text-green-700 border-green-200',
      'alugado': 'bg-blue-100 text-blue-700 border-blue-200',
      'em manutenção': 'bg-yellow-100 text-yellow-700 border-yellow-200',
      'reservado': 'bg-purple-100 text-purple-700 border-purple-200',
      'indisponível': 'bg-red-100 text-red-700 border-red-200'
    };
    return styles[status] || 'bg-gray-100 text-gray-700';
  };

  const getIconeTipo = (tipo: string) => {
    if (tipo === 'motocicleta') return <Bike size={18} />;
    if (tipo === 'utilitario') return <Truck size={18} />;
    return <Car size={18} />;
  };

  // Filtragem
  const veiculosFiltrados = veiculos.filter(v => 
    v.modelo.toLowerCase().includes(termoBusca.toLowerCase()) || 
    v.placa.toLowerCase().includes(termoBusca.toLowerCase())
  );

  return (
    <AdminLayout title="Veículos / Frota" subtitle="Gerenciamento completo da frota de veículos.">
      
      {/* --- MODAIS --- */}
      <AddVehicleModal 
        isOpen={addModalOpen}
        onClose={() => setAddModalOpen(false)}
        onConfirm={handleAddVeiculo}
        isLoading={loadingAction}
      />

      <VehicleDetailsModal 
        isOpen={detailsModalOpen}
        onClose={() => setDetailsModalOpen(false)}
        veiculo={veiculoSelecionado}
      />

      <ConfirmModal 
        isOpen={deleteModalOpen}
        isLoading={loadingAction}
        onClose={() => setDeleteModalOpen(false)}
        onConfirm={confirmDelete}
        title="Remover Veículo?"
        description={`Tem certeza que deseja excluir o ${veiculoSelecionado?.modelo} (${veiculoSelecionado?.placa})? Esta ação é irreversível.`}
      />

      <VehicleEditModal 
        isOpen={editModalOpen}
        isLoading={loadingAction}
        onClose={() => setEditModalOpen(false)}
        onSave={confirmEdit}
        veiculo={veiculoSelecionado}
      />

      <StatusModal 
        isOpen={statusModal.open} 
        onClose={() => setStatusModal({...statusModal, open: false})} 
        type={statusModal.type} 
        title={statusModal.title} 
        message={statusModal.msg} 
      />

      {/* --- BARRA DE AÇÕES --- */}
      <div className="flex flex-col md:flex-row justify-between items-center gap-4 mb-6 bg-white p-4 rounded-xl shadow-sm border border-gray-200">
         <div className="relative w-full md:w-96">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search size={18} className="text-gray-400" />
            </div>
            <input 
                type="text"
                placeholder="Buscar por modelo ou placa..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
                value={termoBusca}
                onChange={(e) => setTermoBusca(e.target.value)}
            />
         </div>

         <button 
            onClick={() => setAddModalOpen(true)} 
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg flex items-center gap-2 transition-colors shadow-md w-full md:w-auto justify-center font-futuristic"
         >
            <Plus size={20} /> Adicionar Novo Veículo
         </button>
      </div>

      {/* --- TABELA --- */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
         {loading ? (
            <div className="p-12 flex justify-center"><Loader2 className="animate-spin text-blue-600" size={32} /></div>
         ) : (
            <div className="overflow-x-auto">
                <table className="w-full text-sm text-left">
                    <thead className="bg-gray-50 text-gray-600 uppercase text-xs font-bold border-b border-gray-200">
                        <tr>
                            <th className="px-6 py-4">Modelo</th>
                            <th className="px-6 py-4">Placa</th>
                            <th className="px-6 py-4">Categoria</th>
                            <th className="px-6 py-4">Status</th>
                            <th className="px-6 py-4">Diária</th>
                            <th className="px-6 py-4 text-right">Ações</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                        {veiculosFiltrados.map((veiculo) => (
                            <tr key={veiculo.id_veiculo} className="hover:bg-gray-50 transition-colors group">
                                <td className="px-6 py-4">
                                    <button 
                                        onClick={() => openDetails(veiculo)}
                                        className="font-bold text-slate-900 hover:text-blue-600 hover:underline text-left"
                                    >
                                        {veiculo.modelo}
                                    </button>
                                    <span className="block text-xs text-gray-400 font-normal">{veiculo.marca}</span>
                                </td>
                                <td className="px-6 py-4 font-mono text-slate-600">{veiculo.placa}</td>
                                <td className="px-6 py-4">
                                    <div className="flex items-center gap-2 text-gray-600 capitalize">
                                        {getIconeTipo(veiculo.tipo_veiculo)} {veiculo.tipo_veiculo}
                                    </div>
                                </td>
                                <td className="px-6 py-4">
                                    <span className={`px-2 py-1 rounded-full text-[10px] font-bold border uppercase ${getStatusBadge(veiculo.status)}`}>
                                        {veiculo.status}
                                    </span>
                                </td>
                                <td className="px-6 py-4 font-bold text-slate-700">R$ {veiculo.valor_diaria.toFixed(2)}</td>
                                <td className="px-6 py-4 text-right flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                    <button 
                                        onClick={() => handleEditClick(veiculo)}
                                        className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                                        title="Editar"
                                    >
                                        <Edit size={18} />
                                    </button>
                                    <button 
                                        onClick={() => handleDeleteClick(veiculo)}
                                        className="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                                        title="Excluir"
                                    >
                                        <Trash2 size={18} />
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                {veiculosFiltrados.length === 0 && (
                    <div className="p-8 text-center text-gray-400">Nenhum veículo encontrado.</div>
                )}
            </div>
         )}
      </div>

    </AdminLayout>
  );
}