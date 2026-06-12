import type { Veiculo } from './veiculo';

export type StatusReserva = 'pendente' | 'confirmada' | 'em_andamento' | 'finalizada' | 'cancelada';

interface MotoristaResumo {
  id_pessoa: number;
  nome_completo: string;
  cpf: string;
  email: string;
}

export interface Reserva {
  id_reserva: number;
  data_retirada: string;
  data_devolucao: string;
  valor_total_estimado: number;
  status: StatusReserva;
  
  seguro_pessoal: boolean;
  seguro_terceiros: boolean;
  
  veiculo: Veiculo;
  
  // NOVO CAMPO
  motorista?: MotoristaResumo;
}