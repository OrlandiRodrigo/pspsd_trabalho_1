import { api } from './api';

export interface DadosCliente {
  id_pessoa: number;
  email: string;
  telefone: string;
  endereco: {
    rua: string;
    numero: string;
    complemento?: string;
    bairro: string;
    cidade: string;
    estado: string;
    cep: string;
  };
  e_ativo: boolean;
  
  data_criacao: string; 
  
  nome_completo?: string;
  cpf?: string;
  cnh?: string;
  
  razao_social?: string;
  cnpj?: string;
  motoristas?: any[];

  tipo_cliente: 'PF' | 'PJ'; 
}

export const clienteService = {
  meusDados: async (tipo: 'cliente_pf' | 'cliente_pj') => {
    const endpoint = tipo === 'cliente_pj' 
      ? `/clientes/pessoas-juridicas/me` 
      : `/clientes/pessoas-fisicas/me`;
      
    const response = await api.get<DadosCliente>(endpoint);
    return response.data;
  },

  buscarPorId: async (id: string, tipo: 'cliente_pf' | 'cliente_pj' | 'admin') => {
    const endpoint = tipo === 'cliente_pj' 
      ? `/clientes/pessoas-juridicas/${id}` 
      : `/clientes/pessoas-fisicas/${id}`;
      
    const response = await api.get<DadosCliente>(endpoint);
    return response.data;
  },

  atualizarMeusDados: async (tipo: 'cliente_pf' | 'cliente_pj', dados: Partial<DadosCliente>) => {
    const endpoint = tipo === 'cliente_pj' 
      ? `/clientes/pessoas-juridicas/me` 
      : `/clientes/pessoas-fisicas/me`;

    const response = await api.put(endpoint, dados);
    return response.data;
  },

  listarTodos: async () => {
    const [pfs, pjs] = await Promise.all([
      api.get<DadosCliente[]>('/clientes/pessoas-fisicas/'),
      api.get<DadosCliente[]>('/clientes/pessoas-juridicas/')
    ]);

    const listaPF = pfs.data.map(c => ({ ...c, tipo_cliente: 'PF' as const }));
    const listaPJ = pjs.data.map(c => ({ ...c, tipo_cliente: 'PJ' as const }));

    return [...listaPF, ...listaPJ];
  },

  alterarStatus: async (id: number, tipo: 'PF' | 'PJ', novoStatus: 'ativo' | 'bloqueado') => {
    const endpoint = tipo === 'PJ' 
      ? `/clientes/pessoas-juridicas/${id}/status` 
      : `/clientes/pessoas-fisicas/${id}/status`;
    
    const response = await api.patch(endpoint, { novo_status: novoStatus });
    return response.data;
  },

  deletar: async (id: number, tipo: 'PF' | 'PJ') => {
    const endpoint = tipo === 'PJ' 
      ? `/clientes/pessoas-juridicas/${id}` 
      : `/clientes/pessoas-fisicas/${id}`;
      
    await api.delete(endpoint);
  }
};