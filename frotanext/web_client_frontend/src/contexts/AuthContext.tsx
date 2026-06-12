import { createContext, useState, useEffect, type ReactNode } from 'react';
import { jwtDecode } from 'jwt-decode';
import type { DecodedToken, User } from '../types/auth';

interface AuthContextType {
  user: User | null;
  login: (token: string) => void;
  logout: () => void;
  loading: boolean;
  isAdmin: boolean;
  isCompany: boolean;
}

// eslint-disable-next-line react-refresh/only-export-components
export const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const logout = () => {
    localStorage.removeItem('frota_token');
    setUser(null);
  };

  const processarToken = (token: string) => {
    try {
      const decoded = jwtDecode<DecodedToken>(token);
      
      let tipoUsuario: User['tipo'] = 'admin';
      
      if (decoded.tipo === 'pessoa_fisica') tipoUsuario = 'cliente_pf';
      if (decoded.tipo === 'pessoa_juridica') tipoUsuario = 'cliente_pj';
  
      setUser({
        id: decoded.sub,
        email: decoded.email || decoded.sub,
        tipo: tipoUsuario,
        isAuthenticated: true,
      });
    } catch (error) {
      console.error("Erro ao processar token:", error);
      logout();
    }
  };

  const login = (token: string) => {
    localStorage.setItem('frota_token', token);
    processarToken(token);
  };

  useEffect(() => {
    const token = localStorage.getItem('frota_token');
    if (token) {
      processarToken(token);
    }
    setLoading(false);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); 

  return (
    <AuthContext.Provider 
      value={{ 
        user, 
        login, 
        logout, 
        loading,
        isAdmin: user?.tipo === 'admin',
        isCompany: user?.tipo === 'cliente_pj'
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}