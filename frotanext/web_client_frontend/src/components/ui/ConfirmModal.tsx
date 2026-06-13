import { Save, X, Loader2 } from 'lucide-react';

interface ConfirmModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  isLoading: boolean;
  title?: string;
  description?: string;
}

export function ConfirmModal({ 
  isOpen, 
  onClose, 
  onConfirm, 
  isLoading, 
  title = "Salvar Alterações?", 
  description = "As novas informações substituirão as antigas." 
}: ConfirmModalProps) {
  
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-fade-in">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden transform transition-all scale-100">
        
        {/* Cabeçalho */}
        <div className="bg-blue-50 p-6 border-b border-blue-100 flex items-start gap-4">
          <div className="bg-blue-100 p-2 rounded-full shrink-0">
            <Save className="text-blue-600 w-6 h-6" />
          </div>
          <div className="flex-1">
            <h3 className="text-lg font-bold text-blue-900 font-futuristic">{title}</h3>
            <p className="text-sm text-blue-700 mt-1">{description}</p>
          </div>
          <button onClick={onClose} className="text-blue-400 hover:text-blue-700 transition-colors">
            <X size={20} />
          </button>
        </div>

        {/* Ações */}
        <div className="p-6 bg-white flex gap-3 justify-end">
          <button 
            onClick={onClose}
            disabled={isLoading}
            className="px-4 py-2 rounded-lg text-sm font-bold text-gray-600 hover:bg-gray-100 border border-gray-200 transition-colors"
          >
            Cancelar
          </button>
          
          <button 
            onClick={onConfirm}
            disabled={isLoading}
            className="px-6 py-2 rounded-lg text-sm font-bold text-white bg-blue-600 hover:bg-blue-700 shadow-lg transition-all flex items-center gap-2 disabled:opacity-50"
          >
            {isLoading ? <Loader2 className="animate-spin w-4 h-4" /> : "Confirmar e Salvar"}
          </button>
        </div>

      </div>
    </div>
  );
}