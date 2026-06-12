export type TipoVeiculo = 'passeio' | 'utilitario' | 'motocicleta';
export type StatusVeiculo = 'disponível' | 'reservado' | 'alugado' | 'em manutenção' | 'indisponível';

export interface Veiculo {
  id_veiculo: number;
  marca: string;
  modelo: string;
  ano_fabricacao: number;
  ano_modelo: number;
  cor: string;
  placa: string;
  valor_diaria: number;
  imagem_url?: string;
  status: StatusVeiculo;
  tipo_veiculo: TipoVeiculo;
  
  chassi: string;
  capacidade_tanque: number;
  
  tipo_carroceria?: string;
  qtde_portas?: number;
  qtde_passageiros?: number;
  cambio_automatico?: boolean;
  ar_condicionado?: boolean;
  
  cilindrada?: number;
  tipo_tracao?: string;
  abs?: boolean;
  partida_eletrica?: boolean;
  modos_pilotagem?: string;
  
  tipo_utilitario?: string;
  capacidade_carga_kg?: number;
  capacidade_carga_m3?: number;
  tipo_carga?: string;
  qtde_eixos?: number;
  max_passageiros?: number;
  
  motor?: string;
}