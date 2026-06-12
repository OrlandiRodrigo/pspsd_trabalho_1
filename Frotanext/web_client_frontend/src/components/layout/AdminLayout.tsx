import type { ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Car, CalendarRange, Users } from 'lucide-react';
import { NavbarAdmin } from './NavbarAdmin';

interface AdminLayoutProps {
  children: ReactNode;
  title: string;
  subtitle?: string;
}

export function AdminLayout({ children, title, subtitle }: AdminLayoutProps) {
  const location = useLocation();

  const isActive = (path: string) => location.pathname.startsWith(path) 
    ? 'bg-blue-600 shadow-lg font-bold text-white' 
    : 'text-blue-100 hover:bg-white/10 transition-all';

  return (
    <div className="min-h-screen bg-gray-100 font-sans flex flex-col">
      <NavbarAdmin />

      <div className="flex flex-1 h-[calc(100vh-80px)] overflow-hidden">
        
        {/* SIDEBAR */}
        <aside className="w-64 bg-[#003366] text-white hidden md:flex flex-col py-8 shadow-inner shrink-0">
            <nav className="space-y-2 px-4">
                <Link to="/admin/dashboard" className={`flex items-center gap-3 px-4 py-3 rounded-xl ${isActive('/admin/dashboard')}`}>
                    <LayoutDashboard size={20} /> Visão Geral
                </Link>
                <Link to="/admin/veiculos" className={`flex items-center gap-3 px-4 py-3 rounded-xl ${isActive('/admin/veiculos')}`}>
                    <Car size={20} /> Veículos / Frota
                </Link>
                <Link to="/admin/reservas" className={`flex items-center gap-3 px-4 py-3 rounded-xl ${isActive('/admin/reservas')}`}>
                    <CalendarRange size={20} /> Reservas
                </Link>
                <Link to="/admin/clientes" className={`flex items-center gap-3 px-4 py-3 rounded-xl ${isActive('/admin/clientes')}`}>
                    <Users size={20} /> Clientes
                </Link>
            </nav>
            <div className="mt-auto px-6 pb-4">
                <p className="text-xs text-blue-300 opacity-50">FrotaNext Admin</p>
            </div>
        </aside>

        <main className="flex-1 p-8 overflow-y-auto bg-gray-50 w-full">
            <div className="mb-8">
                <h2 className="text-3xl font-bold text-slate-800 font-futuristic">{title}</h2>
                {subtitle && <p className="text-gray-500 mt-1">{subtitle}</p>}
            </div>
            
            {children}
        </main>
      </div>
    </div>
  );
}