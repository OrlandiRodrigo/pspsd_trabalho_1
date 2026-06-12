export interface DecodedToken {
  sub: string;       
  email?: string;    
  tipo?: 'pessoa_fisica' | 'pessoa_juridica';
  exp: number;       
}

export interface User {
  id: string;
  email: string;
  tipo: 'admin' | 'cliente_pf' | 'cliente_pj';
  isAuthenticated: boolean;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}