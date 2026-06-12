import { Link } from 'react-router-dom';
import { LogOut, ShieldCheck } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';
import hexBg from '../../assets/hex-bg.png'; 
import logoFn from '../../assets/logo-fn.png'; 

export function NavbarAdmin() {
  const { logout } = useAuth();

  return (
    <header className="relative w-full h-20 bg-slate-900 shadow-md z-50">
      
      {/* 1. FUNDO */}
      <div className="absolute inset-0 overflow-hidden">
        <img 
          src={hexBg} 
          alt="Background" 
          className="w-full h-full object-cover opacity-100" 
        />
        <div className="absolute inset-0 bg-gradient-to-r from-slate-900/90 via-slate-900/80 to-slate-900/90" />
      </div>

      {/* 2. CONTEÚDO */}
      <div className="relative z-10 w-full px-6 h-full flex items-center justify-between">
        
        {/* ESQUERDA */}
        <Link to="/admin/dashboard" className="flex items-center hover:opacity-80 transition-opacity">
            <img 
              src={logoFn} 
              alt="FrotaNext Admin" 
              className="h-12 w-auto object-contain" 
            />
        </Link>

        {/* CENTRO */}
        <div className="hidden md:flex items-center gap-3">
            <ShieldCheck className="text-blue-500 w-6 h-6" />
            <h1 className="text-2xl text-white font-bold font-futuristic tracking-wider drop-shadow-md">
                PORTAL ADMINISTRATIVO
            </h1>
        </div>

        {/* DIREITA */}
        <button 
            onClick={logout}
            className="bg-red-600/20 hover:bg-red-600 hover:text-white text-red-200 text-xs font-bold py-2 px-6 rounded-lg border border-red-500/30 transition-all flex items-center gap-2 backdrop-blur-md"
        >
            Sair <LogOut size={14} /> 
        </button>

      </div>
    </header>
  );
}