import { useState, useEffect } from 'react';
import { X, Loader2, Calendar, Shield, Save } from 'lucide-react';
import type { Reserva } from '../../types/reserva';
import type { UpdateReservaData } from '../../services/reservaService';

interface ModifyModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: (id: number, data: UpdateReservaData) => void;
  isLoading: boolean;
  reservaAtual: Reserva | null;
}

export function ModifyModal({ 
  isOpen, 
  onClose, 
  onConfirm, 
  isLoading, 
  reservaAtual 
}: ModifyModalProps) {
  
  const [dataRetirada, setDataRetirada] = useState('');
  const [dataDevolucao, setDataDevolucao] = useState('');
  const [seguroPessoal, setSeguroPessoal] = useState(false);
  const [seguroTerceiros, setSeguroTerceiros] = useState(false);

  const formatToInput = (isoString: string) => {
    if (!isoString) return '';
    return isoString.substring(0, 16); 
  };

  useEffect(() => {
    if (reservaAtual) {
      setDataRetirada(formatToInput(reservaAtual.data_retirada));
      setDataDevolucao(formatToInput(reservaAtual.data_devolucao));
      setSeguroPessoal(reservaAtual.seguro_pessoal); 
      setSeguroTerceiros(reservaAtual.seguro_terceiros);
    }
  }, [reservaAtual]);

  const handleSubmit = () => {
    if (!reservaAtual) return;

    const dadosAtualizados: UpdateReservaData = {
        data_retirada: dataRetirada,
        data_devolucao: dataDevolucao,
        seguro_pessoal: seguroPessoal,
        seguro_terceiros: seguroTerceiros
    };

    onConfirm(reservaAtual.id_reserva, dadosAtualizados);
  };

  if (!isOpen || !reservaAtual) return null;

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-fade-in">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden transform transition-all scale-100">
        
        {/* Cabeçalho */}
        <div className="bg-blue-50 p-6 border-b border-blue-100 flex items-center justify-between">
          <div>
            <h3 className="text-lg font-bold text-blue-900 font-futuristic">Modificar Reserva</h3>
            <p className="text-xs text-blue-700 mt-1">Veículo: {reservaAtual.veiculo.modelo}</p>
          </div>
          <button onClick={onClose} className="text-blue-400 hover:text-blue-700 transition-colors">
            <X size={24} />
          </button>
        </div>

        {/* Formulário */}
        <div className="p-6 bg-white space-y-6">
            
            {/* Datas */}
            <div>
                <h4 className="flex items-center gap-2 font-bold text-gray-700 mb-3 text-sm uppercase tracking-wider">
                    <Calendar size={16} className="text-blue-500" /> Novas Datas
                </h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                        <label className="block text-xs font-bold text-gray-500 mb-1">Retirada</label>
                        <input 
                            type="datetime-local" 
                            className="w-full border border-gray-300 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                            value={dataRetirada}
                            onChange={(e) => setDataRetirada(e.target.value)}
                        />
                    </div>
                    <div>
                        <label className="block text-xs font-bold text-gray-500 mb-1">Devolução</label>
                        <input 
                            type="datetime-local" 
                            className="w-full border border-gray-300 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                            value={dataDevolucao}
                            onChange={(e) => setDataDevolucao(e.target.value)}
                        />
                    </div>
                </div>
            </div>

            {/* Seguros */}
            <div>
                <h4 className="flex items-center gap-2 font-bold text-gray-700 mb-3 text-sm uppercase tracking-wider">
                    <Shield size={16} className="text-blue-500" /> Ajustar Seguros
                </h4>
                <div className="space-y-3">
                    <label className="flex items-center p-3 border border-gray-200 rounded-xl cursor-pointer hover:bg-blue-50 transition-colors">
                        <input 
                            type="checkbox" 
                            className="w-4 h-4 text-blue-600" 
                            checked={seguroPessoal} 
                            onChange={(e) => setSeguroPessoal(e.target.checked)} 
                        />
                        <div className="ml-3">
                            <span className="block font-bold text-sm text-gray-800">Seguro Pessoal</span>
                            <span className="block text-[10px] text-gray-500">Cobertura médica para ocupantes</span>
                        </div>
                    </label>
                    <label className="flex items-center p-3 border border-gray-200 rounded-xl cursor-pointer hover:bg-blue-50 transition-colors">
                        <input 
                            type="checkbox" 
                            className="w-4 h-4 text-blue-600" 
                            checked={seguroTerceiros} 
                            onChange={(e) => setSeguroTerceiros(e.target.checked)} 
                        />
                        <div className="ml-3">
                            <span className="block font-bold text-sm text-gray-800">Seguro contra Terceiros</span>
                            <span className="block text-[10px] text-gray-500">Cobertura de danos a outros veículos</span>
                        </div>
                    </label>
                </div>
            </div>

            <div className="bg-yellow-50 p-3 rounded-lg border border-yellow-100">
                <p className="text-xs text-yellow-700 text-center">
                    <strong>Atenção:</strong> A alteração de datas ou seguros resultará em um novo cálculo do valor total.
                </p>
            </div>

        </div>

        {/* Rodapé */}
        <div className="p-4 bg-gray-50 flex justify-end gap-3 border-t border-gray-100">
            <button 
              onClick={onClose}
              disabled={isLoading}
              className="px-4 py-2 rounded-lg text-sm font-bold text-gray-600 hover:bg-white border border-transparent hover:border-gray-300 transition-all"
            >
              Cancelar
            </button>
            
            <button 
              onClick={handleSubmit}
              disabled={isLoading}
              className="px-6 py-2 rounded-lg text-sm font-bold text-white bg-blue-600 hover:bg-blue-700 shadow-lg transition-all flex items-center gap-2 disabled:opacity-50"
            >
              {isLoading ? <Loader2 className="animate-spin w-4 h-4" /> : <><Save size={16} /> Salvar Alterações</>}
            </button>
        </div>

      </div>
    </div>
  );
}