import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { X, Save, Loader2, Car, AlertTriangle } from 'lucide-react'; 
import type { Veiculo } from '../../types/veiculo';

interface VehicleEditModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (id: number, tipo: any, data: any) => void;
  isLoading: boolean;
  veiculo: Veiculo | null;
}

export function VehicleEditModal({ isOpen, onClose, onSave, isLoading, veiculo }: VehicleEditModalProps) {
  const { register, handleSubmit, reset } = useForm();

  const isBloqueadoPorReserva = veiculo?.status === 'reservado' || veiculo?.status === 'alugado';

  useEffect(() => {
    if (veiculo) {
      reset({
        placa: veiculo.placa,
        marca: veiculo.marca,
        modelo: veiculo.modelo,
        cor: veiculo.cor,
        valor_diaria: veiculo.valor_diaria,
        ano_modelo: veiculo.ano_modelo,
        status: veiculo.status,
      });
    }
  }, [veiculo, reset]);

  const onSubmit = (data: any) => {
    if (veiculo) {
      if (isBloqueadoPorReserva) {
          delete data.status;
      }
      onSave(veiculo.id_veiculo, veiculo.tipo_veiculo, data);
    }
  };

  if (!isOpen || !veiculo) return null;

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-fade-in">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl overflow-hidden flex flex-col max-h-[90vh]">
        
        <div className="bg-slate-900 p-6 border-b border-slate-800 flex justify-between items-center shrink-0">
          <div className="flex items-center gap-3">
            <div className="bg-blue-600 p-2 rounded-lg text-white">
               <Car size={20} />
            </div>
            <div>
                <h3 className="text-lg font-bold text-white font-futuristic">Editar Veículo</h3>
                <p className="text-xs text-gray-400 uppercase">{veiculo.modelo} - {veiculo.placa}</p>
            </div>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-white transition-colors">
            <X size={24} />
          </button>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="p-8 overflow-y-auto custom-scrollbar">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                
                <div className="col-span-2">
                    <label className="block text-xs font-bold text-gray-500 mb-1 uppercase">Status Operacional</label>
                    <div className="relative">
                        <select 
                            {...register('status')} 
                            disabled={isBloqueadoPorReserva}
                            className={`w-full p-3 border rounded-lg outline-none appearance-none font-bold ${
                                isBloqueadoPorReserva 
                                ? 'bg-gray-100 text-gray-400 border-gray-200 cursor-not-allowed' 
                                : 'bg-white border-gray-300 focus:ring-2 focus:ring-blue-500 text-slate-800'
                            }`}
                        >
                            <option value="disponível">🟢 Disponível</option>
                            <option value="em manutenção">🟠 Em Manutenção</option>
                            <option value="indisponível">🔴 Indisponível (Inativo)</option>
                            <option value="reservado" disabled>🟣 Reservado</option>
                            <option value="alugado" disabled>🔵 Alugado</option>
                        </select>
                        
                        {isBloqueadoPorReserva && (
                            <div className="flex items-center gap-2 mt-2 text-xs text-orange-600 bg-orange-50 p-2 rounded border border-orange-100">
                                <AlertTriangle size={14} />
                                <span>Este veículo possui uma reserva ativa. O status deve ser alterado via Gerenciamento de Reservas.</span>
                            </div>
                        )}
                    </div>
                </div>

                <div>
                    <label className="block text-xs font-bold text-gray-500 mb-1 uppercase">Marca</label>
                    <input {...register('marca')} disabled className="w-full p-3 bg-gray-100 border border-gray-200 rounded-lg text-gray-500 cursor-not-allowed" />
                </div>

                <div>
                    <label className="block text-xs font-bold text-gray-500 mb-1 uppercase">Modelo</label>
                    <input {...register('modelo')} disabled className="w-full p-3 bg-gray-100 border border-gray-200 rounded-lg text-gray-500 cursor-not-allowed" />
                </div>

                <div>
                    <label className="block text-xs font-bold text-gray-500 mb-1 uppercase">Placa</label>
                    <input {...register('placa')} className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none font-mono uppercase" />
                </div>

                <div>
                    <label className="block text-xs font-bold text-gray-500 mb-1 uppercase">Valor da Diária (R$)</label>
                    <input type="number" step="0.01" {...register('valor_diaria', { valueAsNumber: true })} className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-blue-700 font-bold" />
                </div>

                <div>
                    <label className="block text-xs font-bold text-gray-500 mb-1 uppercase">Cor</label>
                    <select {...register('cor')} className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none bg-white">
                        <option value="Preto">Preto</option>
                        <option value="Branco">Branco</option>
                        <option value="Prata">Prata</option>
                        <option value="Cinza">Cinza</option>
                        <option value="Vermelho">Vermelho</option>
                        <option value="Azul">Azul</option>
                    </select>
                </div>

                <div>
                    <label className="block text-xs font-bold text-gray-500 mb-1 uppercase">Ano Modelo</label>
                    <input type="number" {...register('ano_modelo', { valueAsNumber: true })} className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" />
                </div>

            </div>

            <div className="mt-8 pt-6 border-t border-gray-100 flex justify-end gap-3">
                <button type="button" onClick={onClose} className="px-6 py-3 rounded-xl text-sm font-bold text-gray-600 hover:bg-gray-100 transition-colors">Cancelar</button>
                <button type="submit" disabled={isLoading} className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-xl shadow-lg transition-all flex items-center gap-2 disabled:opacity-50 font-futuristic">
                    {isLoading ? <Loader2 className="animate-spin" /> : <><Save size={18} /> Salvar Alterações</>}
                </button>
            </div>
        </form>

      </div>
    </div>
  );
}