import { Link, useLocation } from "react-router-dom";
import { User as UserIcon, LogOut, PlusCircle, History } from "lucide-react";
import { useAuth } from "../../hooks/useAuth";
import hexBg from "../../assets/hex-bg.png";
import logoFn from "../../assets/logo-fn.png";

export function NavbarInternal() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const isNovaReservaPage = location.pathname === "/reservas/nova";

  return (
    <header className="relative w-full h-28 bg-slate-900 shadow-md z-50">
      <div className="absolute inset-0 overflow-hidden">
        <img
          src={hexBg}
          alt="Background"
          className="w-full h-full object-cover opacity-100"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-black/60 via-black/20 to-black/60" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 h-full flex items-center justify-between">
        {/* ESQUERDA */}
        <Link
          to="/dashboard"
          className="flex items-center hover:opacity-80 transition-opacity"
        >
          <img
            src={logoFn}
            alt="FrotaNext"
            className="h-20 w-auto object-contain drop-shadow-md"
          />
        </Link>

        {/* CENTRO */}
        <Link
          to="/perfil"
          className="hidden md:flex items-center gap-3 hover:bg-white/5 p-2 rounded-xl transition-colors group"
        >
          <div className="text-right">
            <p className="text-xs text-gray-300 uppercase tracking-wider font-bold shadow-black drop-shadow-sm group-hover:text-blue-200">
              Painel do Cliente
            </p>
            <p className="text-lg text-white font-bold font-futuristic drop-shadow-md group-hover:underline decoration-blue-500 underline-offset-4">
              Olá, {user?.email?.split("@")[0] || "Cliente"}
            </p>
          </div>
          <div className="h-12 w-12 rounded-full bg-blue-600 flex items-center justify-center border-2 border-white/50 shadow-lg group-hover:border-white transition-colors">
            <UserIcon className="text-white h-6 w-6" />
          </div>
        </Link>

        {/* DIREITA */}
        <div className="flex items-center gap-3">
          {isNovaReservaPage ? (
            <Link
              to="/reservas/minhas"
              className="hidden sm:flex items-center gap-2 bg-[#0047ab] hover:bg-[#003380] text-white text-sm font-bold py-3 px-6 rounded-xl transition-all shadow-lg border border-blue-400/30 hover:-translate-y-0.5"
            >
              <History size={18} />
              Minhas Reservas
            </Link>
          ) : (
            <Link
              to="/reservas/nova"
              className="hidden sm:flex items-center gap-2 bg-[#0047ab] hover:bg-[#003380] text-white text-sm font-bold py-3 px-6 rounded-xl transition-all shadow-lg border border-blue-400/30 hover:-translate-y-0.5"
            >
              <PlusCircle size={18} />
              Nova Reserva
            </Link>
          )}

          <button
            onClick={logout}
            className="bg-black/40 hover:bg-red-600/90 hover:text-white text-gray-100 text-sm font-bold py-3 px-6 rounded-xl border border-white/20 transition-all flex items-center gap-2 backdrop-blur-md"
          >
            Sair <LogOut size={16} />
          </button>
        </div>
      </div>
    </header>
  );
}
