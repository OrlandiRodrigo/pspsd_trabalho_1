import { api } from './api';
import type { Veiculo, TipoVeiculo } from '../types/veiculo';

export const veiculoService = {
  listar: async (categoria?: TipoVeiculo) => {
    const params = new URLSearchParams();
    if (categoria) params.append('categoria', categoria);
    
    const response = await api.get<Veiculo[]>(`/frota/veiculos?${params.toString()}`);
    return response.data;
  },
  
  listarTodosAdmin: async () => {
      const response = await api.get<Veiculo[]>('/frota/veiculos?apenas_disponiveis=false');
      return response.data;
  },

  deletar: async (id: number) => {
    await api.delete(`/veiculos/${id}`);
  },

  atualizar: async (id: number, tipo: TipoVeiculo, dados: Partial<Veiculo>) => {
    const response = await api.put(`/veiculos/${tipo}/${id}`, dados);
    return response.data;
  },

  criar: async (tipo: TipoVeiculo, dados: any) => {
    const response = await api.post(`/veiculos/${tipo}`, dados);
    return response.data;
  }
};
