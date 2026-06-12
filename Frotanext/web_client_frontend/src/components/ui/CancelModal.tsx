import { AlertTriangle, X, Loader2 } from 'lucide-react';

interface CancelModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  isLoading: boolean;
  title?: string;
  description?: string;
}

export function CancelModal({ 
  isOpen, 
  onClose, 
  onConfirm, 
  isLoading, 
  title = "Cancelar Reserva", 
  description = "Tem certeza que deseja cancelar? Essa ação não pode ser desfeita." 
}: CancelModalProps) {
  
  if (!isOpen) return null;

  return (
    // Overlay Escuro (Fundo)
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 transition-all animate-fade-in">
      
      {/* Caixa do Modal */}
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden transform transition-all scale-100">
        
        {/* Cabeçalho */}
        <div className="bg-red-50 p-6 border-b border-red-100 flex items-start gap-4">
          <div className="bg-red-100 p-2 rounded-full shrink-0">
            <AlertTriangle className="text-red-600 w-6 h-6" />
          </div>
          <div className="flex-1">
            <h3 className="text-lg font-bold text-red-900 font-futuristic">{title}</h3>
            <p className="text-sm text-red-700 mt-1">{description}</p>
          </div>
          <button onClick={onClose} className="text-red-400 hover:text-red-700 transition-colors">
            <X size={20} />
          </button>
        </div>

        {/* Corpo/Ações */}
        <div className="p-6 bg-white">
          <p className="text-sm text-gray-500 mb-6">
            Ao confirmar, o veículo ficará disponível para outros clientes e o status da sua reserva mudará para <strong>Cancelada</strong>.
          </p>

          <div className="flex gap-3 justify-end">
            <button 
              onClick={onClose}
              disabled={isLoading}
              className="px-4 py-2 rounded-lg text-sm font-bold text-gray-600 hover:bg-gray-100 border border-gray-200 transition-colors"
            >
              Voltar / Manter
            </button>
            
            <button 
              onClick={onConfirm}
              disabled={isLoading}
              className="px-6 py-2 rounded-lg text-sm font-bold text-white bg-red-600 hover:bg-red-700 shadow-lg hover:shadow-red-500/30 transition-all flex items-center gap-2 disabled:opacity-50"
            >
              {isLoading ? <Loader2 className="animate-spin w-4 h-4" /> : "Sim, Cancelar Reserva"}
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}