import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { PlusCircle, History, User, Car, Bike, Truck, Users, Calendar, MapPin, AlertCircle, Loader2, Edit } from 'lucide-react';
import { NavbarLogin } from '../../components/layout/NavbarLogin';
import { Footer } from '../../components/layout/Footer'; 
import { useAuth } from '../../hooks/useAuth';

import { reservaService, type UpdateReservaData } from '../../services/reservaService';
import type { Reserva } from '../../types/reserva';

import { CancelModal } from '../../components/ui/CancelModal';
import { ModifyModal } from '../../components/ui/ModifyModal';
import { DetailsModal } from '../../components/ui/DetailsModal';

import imgPlaceholder from '../../assets/card-frota.png'; 

export function Dashboard() {
  const { isCompany } = useAuth();
  
  const [proximaReserva, setProximaReserva] = useState<Reserva | null>(null);
  const [loading, setLoading] = useState(true);

  const [detailsModalOpen, setDetailsModalOpen] = useState(false);
  const [cancelModalOpen, setCancelModalOpen] = useState(false);
  const [modifyModalOpen, setModifyModalOpen] = useState(false);
  const [loadingAction, setLoadingAction] = useState(false);

  useEffect(() => {
    carregarProximaReserva();
  }, []);

  const carregarProximaReserva = async () => {
    try {
      const todasReservas = await reservaService.listarMinhas();
      
      const ativas = todasReservas
        .filter(r => ['confirmada', 'pendente', 'em_andamento'].includes(r.status))
        .sort((a, b) => new Date(a.data_retirada).getTime() - new Date(b.data_retirada).getTime());

      if (ativas.length > 0) {
        setProximaReserva(ativas[0]); 
      } else {
        setProximaReserva(null);
      }
    } catch (error) {
      console.error("Erro ao carregar dashboard:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleCancelar = async () => {
    if (!proximaReserva) return;
    setLoadingAction(true);
    try {
      await reservaService.cancelar(proximaReserva.id_reserva);
      setCancelModalOpen(false);
      await carregarProximaReserva(); 
    } catch (error) {
      alert("Erro ao cancelar reserva.");
    } finally {
      setLoadingAction(false);
    }
  };

  const handleModificar = async (id: number, dados: UpdateReservaData) => {
    setLoadingAction(true);
    try {
        await reservaService.atualizar(id, dados);
        setModifyModalOpen(false);
        await carregarProximaReserva();
        alert("Reserva atualizada com sucesso!");
    } catch (error) {
        alert("Erro ao modificar reserva.");
    } finally {
        setLoadingAction(false);
    }
  };

  const formatarData = (isoString: string) => {
    const data = new Date(isoString);
    return data.toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="min-h-screen bg-gray-50 font-sans text-slate-900 flex flex-col">
      
      <NavbarLogin />

      {/* MODAIS INVISÍVEIS */}
      <DetailsModal 
        isOpen={detailsModalOpen} 
        onClose={() => setDetailsModalOpen(false)} 
        reserva={proximaReserva} 
      />
      
      <CancelModal 
        isOpen={cancelModalOpen}
        isLoading={loadingAction}
        onClose={() => setCancelModalOpen(false)}
        onConfirm={handleCancelar}
        title="Cancelar Próxima Viagem?"
        description="Tem certeza? O veículo ficará disponível para outros clientes."
      />

      <ModifyModal 
        isOpen={modifyModalOpen}
        isLoading={loadingAction}
        onClose={() => setModifyModalOpen(false)}
        onConfirm={handleModificar}
        reservaAtual={proximaReserva}
      />


      <div className="max-w-7xl mx-auto px-4 -mt-10 relative z-20 pb-20 flex-grow w-full">
        
        {/* 1. AÇÕES RÁPIDAS */}
        <div className={`grid grid-cols-1 gap-6 mb-16 ${isCompany ? 'md:grid-cols-4' : 'md:grid-cols-3'}`}>
          
          <Link to="/reservas/nova" className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all flex flex-col items-center gap-4 group border border-gray-100 transform hover:-translate-y-1">
            <div className="bg-black text-white p-4 rounded-full group-hover:bg-blue-600 transition-colors shadow-md">
              <PlusCircle size={40} />
            </div>
            <span className="font-bold text-xl font-futuristic text-gray-800 text-center">Nova Reserva</span>
          </Link>
          
          <Link to="/reservas/minhas" className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all flex flex-col items-center gap-4 group border border-gray-100 transform hover:-translate-y-1">
             <div className="bg-black text-white p-4 rounded-full group-hover:bg-blue-600 transition-colors shadow-md">
              <History size={40} />
            </div>
            <span className="font-bold text-xl font-futuristic text-gray-800 text-center">Histórico de Reservas</span>
          </Link>

          {isCompany && (
            <Link to="/empresa/motoristas" className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all flex flex-col items-center gap-4 group border border-gray-100 transform hover:-translate-y-1">
              <div className="bg-black text-white p-4 rounded-full group-hover:bg-blue-600 transition-colors shadow-md">
                <Users size={40} />
              </div>
              <span className="font-bold text-xl font-futuristic text-gray-800 text-center">Gestão de Motoristas</span>
            </Link>
          )}

          <Link to="/perfil" className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all flex flex-col items-center gap-4 group border border-gray-100 transform hover:-translate-y-1">
             <div className="bg-black text-white p-4 rounded-full group-hover:bg-blue-600 transition-colors shadow-md">
              <User size={40} />
            </div>
            <span className="font-bold text-xl font-futuristic text-gray-800 text-center">Meu Perfil</span>
          </Link>
        </div>

        {/* 2. EXPLORE CATEGORIAS */}
        <div className="mb-16">
          <h2 className="text-2xl font-bold mb-12 text-gray-800 font-futuristic uppercase tracking-wide">Explore Nossas Categorias</h2>
          <div className="flex flex-wrap justify-center gap-16 md:gap-28">
            <Link to="/frota?tipo=passeio" className="flex flex-col items-center group relative pt-4 cursor-pointer">
              <span className="absolute -top-2 bg-gray-100 px-3 py-1 rounded-md text-[10px] text-gray-500 shadow-sm border border-gray-200 opacity-0 group-hover:opacity-100 transition-opacity">Detalhes</span>
              <Car size={90} strokeWidth={1.5} className="mb-4 mt-2 text-black group-hover:text-blue-600 transition-transform duration-300 group-hover:scale-110" />
              <span className="font-bold text-lg font-futuristic text-gray-800">Carros de Passeio</span>
            </Link>
            <Link to="/frota?tipo=motocicleta" className="flex flex-col items-center group relative pt-4 cursor-pointer">
               <span className="absolute -top-2 bg-gray-100 px-3 py-1 rounded-md text-[10px] text-gray-500 shadow-sm border border-gray-200 opacity-0 group-hover:opacity-100 transition-opacity">Detalhes</span>
              <Bike size={90} strokeWidth={1.5} className="mb-4 mt-2 text-black group-hover:text-blue-600 transition-transform duration-300 group-hover:scale-110" />
              <span className="font-bold text-lg font-futuristic text-gray-800">Motocicletas</span>
            </Link>
            <Link to="/frota?tipo=utilitario" className="flex flex-col items-center group relative pt-4 cursor-pointer">
               <span className="absolute -top-2 bg-gray-100 px-3 py-1 rounded-md text-[10px] text-gray-500 shadow-sm border border-gray-200 opacity-0 group-hover:opacity-100 transition-opacity">Detalhes</span>
              <Truck size={90} strokeWidth={1.5} className="mb-4 mt-2 text-black group-hover:text-blue-600 transition-transform duration-300 group-hover:scale-110" />
              <span className="font-bold text-lg font-futuristic text-gray-800">Utilitários</span>
            </Link>
          </div>
        </div>

        {/* 3. SUA PRÓXIMA VIAGEM */}
        <div className="mb-16 animate-fade-in">
          <h2 className="text-2xl font-bold mb-6 text-gray-900 font-futuristic">Sua Próxima Viagem</h2>
          
          {loading ? (
            <div className="flex justify-center py-12"><Loader2 className="animate-spin text-blue-600" size={40} /></div>
          ) : proximaReserva ? (
            // --- CARD QUANDO EXISTE RESERVA ---
            <div className="bg-white rounded-3xl shadow-xl border border-gray-100 p-8 flex flex-col md:flex-row items-center gap-8 transition-all hover:shadow-2xl">
              
              <div className="md:w-1/3 relative">
                <img 
                    src={proximaReserva.veiculo.imagem_url || imgPlaceholder} 
                    alt="Veículo" 
                    className="w-full h-48 object-cover rounded-xl shadow-sm" 
                />
                <span className="absolute top-2 left-2 bg-green-500 text-white text-[10px] font-bold px-2 py-1 rounded shadow">
                    CONFIRMADO
                </span>
              </div>

              <div className="md:w-1/3 flex flex-col gap-3 w-full text-center md:text-left">
                <h3 className="text-3xl font-bold text-slate-900 font-futuristic">{proximaReserva.veiculo.modelo}</h3>
                
                <div className="text-gray-600 text-sm space-y-2 bg-gray-50 p-4 rounded-xl border border-gray-100">
                  <p className="flex items-center justify-center md:justify-start gap-2">
                     <Calendar size={16} className="text-blue-600"/> 
                     <span><strong>Retirada:</strong> {formatarData(proximaReserva.data_retirada)}</span>
                  </p>
                  <p className="flex items-center justify-center md:justify-start gap-2">
                     <Calendar size={16} className="text-orange-500"/> 
                     <span><strong>Devolução:</strong> {formatarData(proximaReserva.data_devolucao)}</span>
                  </p>
                  <p className="flex items-center justify-center md:justify-start gap-2 text-gray-400 text-xs">
                     <MapPin size={14} /> Agência Central
                  </p>
                </div>
              </div>

              <div className="md:w-1/3 flex flex-col items-center gap-4 w-full">
                <button 
                    onClick={() => setDetailsModalOpen(true)}
                    className="w-full bg-[#007bff] hover:bg-[#0056b3] text-white font-bold py-4 rounded-xl shadow-lg transition-all hover:shadow-blue-500/30 text-lg font-futuristic transform hover:-translate-y-0.5"
                >
                  Ver Detalhes da Reserva
                </button>
                
                <div className="flex gap-6">
                  <button 
                    onClick={() => setModifyModalOpen(true)}
                    className="text-gray-500 hover:text-blue-600 text-sm font-medium hover:underline flex items-center gap-1"
                  >
                      <Edit size={14} /> Modificar
                  </button>
                  <button 
                    onClick={() => setCancelModalOpen(true)}
                    className="text-red-400 hover:text-red-600 text-sm font-medium hover:underline flex items-center gap-1"
                  >
                      <AlertCircle size={14} /> Cancelar
                  </button>
                </div>
              </div>
            </div>
          ) : (
            // --- CARD QUANDO NÃO TEM RESERVA ---
            <div className="bg-white rounded-3xl shadow-md border border-gray-200 p-12 text-center flex flex-col items-center">
                <div className="bg-gray-100 p-4 rounded-full mb-4">
                    <Car size={48} className="text-gray-400" />
                </div>
                <h3 className="text-xl font-bold text-gray-700 mb-2">Você não tem viagens agendadas</h3>
                <p className="text-gray-500 mb-6 max-w-md">Que tal planejar sua próxima aventura ou viagem de negócios agora mesmo?</p>
                <Link 
                    to="/reservas/nova" 
                    className="bg-slate-900 hover:bg-blue-600 text-white font-bold py-3 px-8 rounded-xl transition-all shadow-lg hover:shadow-blue-500/30"
                >
                    Fazer uma Reserva Agora
                </Link>
            </div>
          )}
        </div>

      </div>

      <Footer />

    </div>
  );
}
