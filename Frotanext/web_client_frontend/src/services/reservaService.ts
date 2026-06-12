import type { Reserva } from '../types/reserva';
import { api } from './api';

export interface SimulacaoRequest {
  veiculo_id: number;
  data_retirada: string; 
  data_devolucao: string; 
  seguro_pessoal: boolean;
  seguro_terceiros: boolean;
}

export interface SimulacaoResponse {
  quantidade_diarias: number;
  valor_diarias: number;
  valor_seguros: number;
  valor_total_estimado: number;
}

export interface UpdateReservaData {
  data_retirada?: string;
  data_devolucao?: string;
  seguro_pessoal?: boolean;
  seguro_terceiros?: boolean;
}

export const reservaService = {
  simular: async (dados: SimulacaoRequest) => {
    const response = await api.post<SimulacaoResponse>('/reservas/simulacao', dados);
    return response.data;
  },

  criar: async (dados: SimulacaoRequest) => {
    const response = await api.post('/reservas/', dados);
    return response.data;
  },
  
  listarMinhas: async () => {
    const response = await api.get<Reserva[]>('/reservas/minhas');
    return response.data;
  },
  
  cancelar: async (id: number) => {
    const response = await api.put(`/reservas/${id}/cancelar`);
    return response.data;
  },

  atualizar: async (id: number, dados: UpdateReservaData) => {
    const response = await api.put(`/reservas/${id}`, dados);
    return response.data;
  },

  listarTodas: async (status?: string) => {
    const url = status ? `/reservas/?status=${status}` : '/reservas/';
    const response = await api.get<Reserva[]>(url);
    return response.data;
  },

  finalizar: async (id: number) => {
    const response = await api.put(`/reservas/${id}/finalizar`);
    return response.data;
  },

  confirmar: async (id: number) => {
    const response = await api.put(`/reservas/${id}/confirmar`);
    return response.data;
  },

  retirar: async (id: number) => {
    const response = await api.put(`/reservas/${id}/retirar`);
    return response.data;
  }

};
