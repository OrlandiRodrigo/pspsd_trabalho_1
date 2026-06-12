import { authApi } from './api';
import type { LoginResponse } from '../types/auth';

export const authService = {
  login: async (email: string, senha: string) => {
    const response = await authApi.post<LoginResponse>('/auth/login', {
      email: email,
      senha: senha
    });
    return response.data;
  },

  loginCliente: async (email: string, senha: string) => {
    const response = await authApi.post<LoginResponse>('/auth/login-cliente', {
      email: email,
      senha: senha
    });
    return response.data;
  },
 
  registrarFuncionario: async (email: string, nomeCompleto: string, senha: string) => {
    const response = await authApi.post('/auth/registar-funcionario', {
      email: email,
      nome_completo: nomeCompleto,
      senha: senha
    });
    return response.data;
  }
};