import { api } from './api';

export const empresaService = {
  adicionarMotorista: async (cpf: string) => {
    const response = await api.post('/minha-empresa/motoristas', { cpf_motorista: cpf });
    return response.data;
  },

  removerMotorista: async (id: number) => {
    const response = await api.delete(`/minha-empresa/motoristas/${id}`);
    return response.data;
  }
};