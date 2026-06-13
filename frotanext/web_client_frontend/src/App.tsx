import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Navbar } from './components/layout/Navbar';

// --- PÁGINAS PÚBLICAS ---
import { Home } from './pages/public/Home';
import { Login } from './pages/public/Login';
import { Cadastro } from './pages/public/Cadastro';
import { Frota } from './pages/public/Frota';

// --- PÁGINAS DO CLIENTE ---
import { Dashboard } from './pages/client/Dashboard';
import { NovaReserva } from './pages/client/reservas/NovaReserva';
import { MinhasReservas } from './pages/client/reservas/MinhasReservas';
import { Perfil } from './pages/client/Perfil';
import { GestaoMotoristas } from './pages/client/empresa/GestaoMotoristas';

// --- PÁGINAS DO ADMIN ---
import { LoginAdmin } from './pages/admin/LoginAdmin';
import { AdminDashboard } from './pages/admin/AdminDashboard';
import { AdminFrota } from './pages/admin/frota/AdminFrota';
import { AdminReservas } from './pages/admin/reservas/AdminReservas';
import { AdminClientes } from './pages/admin/clientes/AdminClientes';

import { useAuth } from './hooks/useAuth';
import type { JSX } from 'react/jsx-dev-runtime';

function PrivateRoute({ children }: { children: JSX.Element }) {
  const { user, loading } = useAuth();
  
  if (loading) return <div className="flex h-screen items-center justify-center">Carregando...</div>;
  
  if (!user) {
    return <Navigate to="/login" />;
  }
  
  return children;
}

function PrivateAdminRoute({ children }: { children: JSX.Element }) {
  const { user, loading, isAdmin } = useAuth();
  
  if (loading) return <div className="flex h-screen items-center justify-center">Carregando...</div>;
  
  if (!user || !isAdmin) {
    return <Navigate to="/admin/login" />;
  }
  
  return children;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* --- ROTAS PÚBLICAS --- */}
        <Route path="/" element={<><Navbar /><Home /></>} />
        <Route path="/login" element={<Login />} />
        <Route path="/cadastro" element={<Cadastro />} />
        <Route path="/frota" element={<Frota />} />
        <Route path="/admin/login" element={<LoginAdmin />} />
        
        {/* --- ROTAS PROTEGIDAS (CLIENTE) --- */}
        <Route path="/dashboard" element={
          <PrivateRoute>
            <Dashboard />
          </PrivateRoute>
        } />
        
        <Route path="/reservas/nova" element={
            <PrivateRoute>
                <NovaReserva />
            </PrivateRoute>
        } />

        <Route path="/reservas/minhas" element={
            <PrivateRoute>
                <MinhasReservas />
            </PrivateRoute>
        } />

        <Route path="/perfil" element={
            <PrivateRoute>
                <Perfil />
            </PrivateRoute>
        } />

        <Route path="/empresa/motoristas" element={
            <PrivateRoute>
                <GestaoMotoristas />
            </PrivateRoute>
        } />

        {/* --- ROTAS PROTEGIDAS (ADMIN) --- */}
        <Route path="/admin/dashboard" element={
          <PrivateAdminRoute>
            <AdminDashboard />
          </PrivateAdminRoute>
        } />

        <Route path="/admin/veiculos" element={
          <PrivateAdminRoute>
            <AdminFrota />
          </PrivateAdminRoute>
        } />

        <Route path="/admin/reservas" element={
          <PrivateAdminRoute>
            <AdminReservas />
          </PrivateAdminRoute>
        } />

        <Route path="/admin/clientes" element={
          <PrivateAdminRoute>
            <AdminClientes />
          </PrivateAdminRoute>
        } />

      </Routes>
    </BrowserRouter>
  );
}

export default App;