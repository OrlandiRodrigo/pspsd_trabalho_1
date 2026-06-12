import { CheckCircle, X, Loader2 } from 'lucide-react';
import type { Reserva } from '../../types/reserva';

interface FinalizeModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: (id: number) => void;
  isLoading: boolean;
  reserva: Reserva | null;
}

export function FinalizeModal({ isOpen, onClose, onConfirm, isLoading, reserva }: FinalizeModalProps) {
  if (!isOpen || !reserva) return null;

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-fade-in">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden transform transition-all">
        
        <div className="bg-green-50 p-6 border-b border-green-100 flex items-start gap-4">
          <div className="bg-green-100 p-2 rounded-full shrink-0">
            <CheckCircle className="text-green-600 w-6 h-6" />
          </div>
          <div className="flex-1">
            <h3 className="text-lg font-bold text-green-900 font-futuristic">Registrar Devolução?</h3>
            <p className="text-sm text-green-700 mt-1">Finalizar reserva #{reserva.id_reserva}</p>
          </div>
          <button onClick={onClose} className="text-green-400 hover:text-green-700 transition-colors">
            <X size={20} />
          </button>
        </div>

        <div className="p-6 bg-white">
          <p className="text-sm text-gray-600 mb-4">
            Confirma que o veículo <strong>{reserva.veiculo.modelo}</strong> foi devolvido e vistoriado?
          </p>
          
          <div className="bg-gray-50 p-3 rounded-lg border border-gray-200 text-xs text-gray-500 mb-6">
            <p>⚠️ Ao confirmar, o status mudará para <strong>Finalizada</strong> e o veículo ficará <strong>Disponível</strong> novamente na frota.</p>
            <p className="mt-2">Se houver atraso na entrega, a multa será calculada automaticamente pelo sistema.</p>
          </div>

          <div className="flex gap-3 justify-end">
            <button onClick={onClose} disabled={isLoading} className="px-4 py-2 rounded-lg text-sm font-bold text-gray-600 hover:bg-gray-100 border border-gray-200 transition-colors">
              Cancelar
            </button>
            <button onClick={() => onConfirm(reserva.id_reserva)} disabled={isLoading} className="px-6 py-2 rounded-lg text-sm font-bold text-white bg-green-600 hover:bg-green-700 shadow-lg flex items-center gap-2 disabled:opacity-50">
              {isLoading ? <Loader2 className="animate-spin w-4 h-4" /> : "Confirmar Devolução"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}