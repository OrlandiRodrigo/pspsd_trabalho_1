import { Link } from 'react-router-dom';
import hexBg from '../../assets/hex-bg.png'; 
import logoFn from '../../assets/logo-fn.png'; 

export function Navbar() {
  return (
    <header className="relative w-full h-[500px] bg-slate-900 overflow-hidden shadow-2xl">
      
      {/* 1. FUNDO HEXAGONAL */}
      <div className="absolute inset-0">
        <img 
          src={hexBg} 
          alt="Background" 
          className="w-full h-full object-cover opacity-80" 
        />
        <div className="absolute inset-0 bg-gradient-to-r from-black/80 via-black/40 to-black/80" />
      </div>

      {/* 2. NAV SUPERIOR */}
      <nav className="relative z-20 max-w-7xl mx-auto px-6 py-6 flex justify-end items-start">
        <Link 
          to="/login" 
          className="font-futuristic bg-[#0047ab] hover:bg-[#003380] text-white text-sm font-bold py-2 px-8 rounded-full shadow-lg border border-blue-400/50 transition-all hover:shadow-blue-500/50"
        >
          Fazer Login
        </Link>
      </nav>

      {/* 3. CONTEÚDO CENTRAL */}
      <div className="relative z-10 h-full flex flex-col md:flex-row items-center justify-start -mt-24 px-4 max-w-full mx-auto overflow-hidden">
        
        {/* LOGO GIGANTE */}
        <div className="flex-shrink-0 transform transition hover:scale-105 duration-500 -ml-20 md:-ml-32">
            <img 
              src={logoFn} 
              alt="FrotaNext Logo" 
              style={{ width: '750px', height: 'auto', filter: 'drop-shadow(0 0 25px rgba(255,255,255,0.15))' }} 
            />
        </div>

        {/* TEXTO E BOTÃO */}
        <div className="flex flex-col items-center text-center md:ml-10 mt-8 md:mt-0 text-white w-full md:w-auto">
            
            <h1 className="font-futuristic text-3xl md:text-5xl text-white mb-4 leading-tight drop-shadow-2xl">
              Bem-vindo(a) a <br />
              <span className="text-blue-400 text-6xl">FrotaNext!</span>
            </h1>
            
            <div className="mt-6">
              <Link 
                to="/cadastro" 
                className="font-futuristic bg-[#003366] hover:bg-[#002244] text-white text-2xl py-4 px-12 rounded-xl shadow-2xl border-2 border-blue-500/50 inline-block hover:shadow-blue-500/40 transition-all transform hover:-translate-y-1"
              >
                Crie Sua Conta!
              </Link>
            </div>
        </div>

      </div>
    </header>
  );
}