import { Link } from "react-router-dom";
import { User as UserIcon, LogOut } from "lucide-react";
import { useAuth } from "../../hooks/useAuth";
import hexBg from "../../assets/hex-bg.png";
import logoFn from "../../assets/logo-fn.png";

export function NavbarLogin() {
  const { user, logout } = useAuth();

  return (
    <header className="relative w-full h-[500px] bg-slate-900 overflow-hidden shadow-2xl">
      {/* FUNDO */}
      <div className="absolute inset-0">
        <img
          src={hexBg}
          alt="Background"
          className="w-full h-full object-cover opacity-80"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-black/80 via-black/40 to-black/80" />
      </div>

      {/* NAV SUPERIOR */}
      <nav className="relative z-20 max-w-7xl mx-auto px-6 py-6 flex justify-end items-start">
        <button
          onClick={logout}
          className="font-futuristic bg-white/10 hover:bg-red-600 hover:border-red-600 text-white text-xs font-bold py-2 px-6 rounded-full border border-white/20 transition-all flex items-center gap-2 backdrop-blur-sm hover:shadow-lg cursor-pointer"
        >
          <LogOut size={14} /> Sair
        </button>
      </nav>

      {/* CONTEÚDO CENTRAL */}
      <div className="relative z-10 h-full flex flex-col md:flex-row items-center justify-start -mt-24 px-4 max-w-full mx-auto overflow-hidden">
        {/* LOGO À ESQUERDA */}
        <div className="flex-shrink-0 transform transition hover:scale-105 duration-500 -ml-20 md:-ml-32">
          <Link to="/dashboard" className="block cursor-pointer">
            <img
              src={logoFn}
              alt="FrotaNext Logo"
              style={{
                width: "750px",
                height: "auto",
                filter: "drop-shadow(0 0 25px rgba(255,255,255,0.15))",
              }}
            />
          </Link>
        </div>

        {/* TEXTO E BOTÃO */}
        <div className="flex flex-col items-center text-center md:ml-10 mt-8 md:mt-0 text-white w-full md:w-auto">
          <h1 className="font-futuristic text-3xl md:text-5xl mb-2 leading-tight drop-shadow-2xl">
            Painel do <span className="text-blue-400">Cliente</span>
          </h1>

          {/* Bloco de Saudação */}
          <Link
            to="/perfil"
            className="flex items-center gap-4 mt-4 mb-8 bg-black/30 px-6 py-3 rounded-2xl backdrop-blur-sm border border-white/10 shadow-inner hover:bg-black/50 hover:border-blue-400/50 transition-all group cursor-pointer"
          >
            <div className="h-12 w-12 rounded-full bg-blue-600 flex items-center justify-center border-2 border-white shadow-lg shrink-0 group-hover:scale-110 transition-transform">
              <UserIcon className="text-white h-6 w-6" />
            </div>
            <div className="text-left">
              <p className="text-[10px] text-gray-300 font-bold uppercase tracking-widest mb-0.5 group-hover:text-blue-200">
                BEM-VINDO DE VOLTA,
              </p>
              <p className="text-xl font-bold text-white font-futuristic leading-none underline decoration-transparent group-hover:decoration-blue-400 transition-all underline-offset-4">
                {user?.email?.split("@")[0] || "Cliente"}
              </p>
            </div>
          </Link>

          {/* Botão Minhas Reservas */}
          <Link
            to="/reservas/minhas"
            className="font-futuristic bg-[#003366] hover:bg-[#002244] text-white text-xl py-3 px-12 rounded-xl shadow-2xl border-2 border-blue-500/50 inline-block hover:shadow-blue-500/40 transition-all transform hover:-translate-y-1"
          >
            Minhas Reservas
          </Link>
        </div>
      </div>
    </header>
  );
}
