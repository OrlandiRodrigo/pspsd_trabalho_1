import { X, Calendar, Shield, DollarSign, User } from 'lucide-react'; 
import type { Reserva } from '../../types/reserva';
import imgPlaceholder from '../../assets/card-frota.png'; 

interface DetailsModalProps {
  isOpen: boolean;
  onClose: () => void;
  reserva: Reserva | null;
}

export function DetailsModal({ isOpen, onClose, reserva }: DetailsModalProps) {
  
  if (!isOpen || !reserva) return null;

  const formatMoeda = (valor: number) => 
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor);

  const formatDate = (isoString: string) => {
    return new Date(isoString).toLocaleString('pt-BR', {
      day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit'
    });
  };

  const dataInicio = new Date(reserva.data_retirada);
  const dataFim = new Date(reserva.data_devolucao);
  const diffTime = Math.abs(dataFim.getTime() - dataInicio.getTime());
  const dias = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) || 1;
  
  const totalDiarias = dias * reserva.veiculo.valor_diaria;
  const custoSeguros = reserva.valor_total_estimado - totalDiarias;

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-fade-in">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl overflow-hidden transform transition-all scale-100 flex flex-col max-h-[90vh]">
        
        <div className="bg-slate-900 p-6 flex justify-between items-center shrink-0">
          <div>
            <p className="text-blue-400 text-xs font-bold uppercase tracking-wider mb-1">Reserva #{reserva.id_reserva}</p>
            <h3 className="text-xl font-bold text-white font-futuristic">Detalhes da Reserva</h3>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-white transition-colors bg-white/10 p-2 rounded-full hover:bg-white/20">
            <X size={20} />
          </button>
        </div>

        <div className="p-0 overflow-y-auto custom-scrollbar">
          
          <div className="relative h-48 bg-gray-100">
            <img 
              src={reserva.veiculo.imagem_url || imgPlaceholder} 
              alt={reserva.veiculo.modelo} 
              className="w-full h-full object-contain p-4"
            />
            <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4 pt-12">
               <h2 className="text-2xl font-bold text-white">{reserva.veiculo.modelo}</h2>
               <p className="text-gray-300 text-sm">{reserva.veiculo.marca} • {reserva.veiculo.cor} • {reserva.veiculo.ano_modelo}</p>
            </div>
          </div>

          <div className="p-8 space-y-8">
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  
                  <div className="space-y-6">
                      {/* Seção Datas */}
                      <div>
                          <h4 className="font-bold text-gray-800 flex items-center gap-2 border-b pb-2 mb-3">
                            <Calendar size={18} className="text-blue-600"/> Cronograma
                          </h4>
                          <div className="pl-2 space-y-2">
                              <div>
                                  <p className="text-xs text-gray-500 font-bold uppercase">Retirada</p>
                                  <p className="text-sm font-medium text-slate-700">{formatDate(reserva.data_retirada)}</p>
                              </div>
                              <div>
                                  <p className="text-xs text-gray-500 font-bold uppercase">Devolução</p>
                                  <p className="text-sm font-medium text-slate-700">{formatDate(reserva.data_devolucao)}</p>
                              </div>
                          </div>
                      </div>

                      {/* Motorista */}
                      {reserva.motorista && (
                        <div>
                            <h4 className="font-bold text-gray-800 flex items-center gap-2 border-b pb-2 mb-3">
                                <User size={18} className="text-blue-600"/> Condutor
                            </h4>
                            <div className="pl-2">
                                <p className="text-sm font-bold text-slate-800">{reserva.motorista.nome_completo}</p>
                                <p className="text-xs text-gray-500">CPF: {reserva.motorista.cpf}</p>
                            </div>
                        </div>
                      )}
                  </div>

                  {/* Seguros */}
                  <div className="space-y-4">
                      <h4 className="font-bold text-gray-800 flex items-center gap-2 border-b pb-2">
                        <Shield size={18} className="text-blue-600"/> Proteção
                      </h4>
                      <div className="pl-2 space-y-2">
                          <div className={`flex items-center gap-2 p-2 rounded-lg ${reserva.seguro_pessoal ? 'bg-green-50 border border-green-100' : 'bg-gray-50 border border-gray-100 opacity-50'}`}>
                              <div className={`w-2 h-2 rounded-full ${reserva.seguro_pessoal ? 'bg-green-500' : 'bg-gray-400'}`} />
                              <span className="text-sm font-medium text-gray-700">Seguro Pessoal</span>
                          </div>
                          <div className={`flex items-center gap-2 p-2 rounded-lg ${reserva.seguro_terceiros ? 'bg-green-50 border border-green-100' : 'bg-gray-50 border border-gray-100 opacity-50'}`}>
                              <div className={`w-2 h-2 rounded-full ${reserva.seguro_terceiros ? 'bg-green-500' : 'bg-gray-400'}`} />
                              <span className="text-sm font-medium text-gray-700">Seguro Terceiros</span>
                          </div>
                      </div>
                  </div>

              </div>

              <div className="bg-slate-50 rounded-xl p-6 border border-slate-100">
                  <h4 className="font-bold text-gray-800 flex items-center gap-2 mb-4">
                    <DollarSign size={18} className="text-blue-600"/> Resumo Financeiro
                  </h4>
                  
                  <div className="space-y-2 text-sm text-gray-600 border-b border-gray-200 pb-4 mb-4">
                      <div className="flex justify-between">
                          <span>Diárias ({dias}x {formatMoeda(reserva.veiculo.valor_diaria)})</span>
                          <span>{formatMoeda(totalDiarias)}</span>
                      </div>
                      <div className="flex justify-between">
                          <span>Taxas de Seguro e Serviços</span>
                          <span>{formatMoeda(custoSeguros)}</span>
                      </div>
                  </div>

                  <div className="flex justify-between items-center">
                      <span className="font-bold text-gray-800 text-lg">Total Estimado</span>
                      <span className="font-bold text-2xl text-blue-700">{formatMoeda(reserva.valor_total_estimado)}</span>
                  </div>
              </div>

          </div>
        </div>

        <div className="p-4 bg-white border-t border-gray-100 flex justify-end shrink-0">
            <button 
              onClick={onClose}
              className="bg-slate-900 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-xl transition-colors w-full sm:w-auto"
            >
              Fechar
            </button>
        </div>

      </div>
    </div>
  );
}