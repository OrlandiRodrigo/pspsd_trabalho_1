import { CheckCircle, AlertCircle } from 'lucide-react';

interface StatusModalProps {
  isOpen: boolean;
  onClose: () => void;
  type: 'success' | 'error';
  title: string;
  message: string;
}

export function StatusModal({ isOpen, onClose, type, title, message }: StatusModalProps) {
  if (!isOpen) return null;

  const isSuccess = type === 'success';

  return (
    <div className="fixed inset-0 z-[70] flex items-center justify-center bg-black/40 backdrop-blur-sm p-4 animate-fade-in">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-sm overflow-hidden text-center p-6 transform transition-all">
        
        <div className={`mx-auto w-16 h-16 rounded-full flex items-center justify-center mb-4 ${isSuccess ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'}`}>
          {isSuccess ? <CheckCircle size={32} /> : <AlertCircle size={32} />}
        </div>

        <h3 className={`text-xl font-bold mb-2 font-futuristic ${isSuccess ? 'text-green-800' : 'text-red-800'}`}>
          {title}
        </h3>
        
        <p className="text-gray-600 mb-6 text-sm">
          {message}
        </p>

        <button 
          onClick={onClose}
          className={`w-full py-3 rounded-xl font-bold text-white transition-all shadow-lg ${isSuccess ? 'bg-green-600 hover:bg-green-700' : 'bg-red-600 hover:bg-red-700'}`}
        >
          OK, Entendi
        </button>

      </div>
    </div>
  );
}