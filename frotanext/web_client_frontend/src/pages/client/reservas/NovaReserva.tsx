import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { NavbarInternal } from '../../../components/layout/NavbarInternal';
import { Footer } from '../../../components/layout/Footer';
import { veiculoService } from '../../../services/veiculoService';
import { reservaService, type SimulacaoRequest, type SimulacaoResponse } from '../../../services/reservaService';
import { clienteService } from '../../../services/clienteService';
import { useAuth } from '../../../hooks/useAuth'; 
import type { Veiculo, TipoVeiculo } from '../../../types/veiculo';
import { Check, Loader2, Calendar, Shield, ArrowRight, ArrowLeft, User } from 'lucide-react';

import imgPlaceholder from '../../../assets/card-frota.png'; 

export function NovaReserva() {
  const navigate = useNavigate();
  const { isCompany } = useAuth(); 
  
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  
  const [veiculos, setVeiculos] = useState<Veiculo[]>([]);
  const [filtroAtual, setFiltroAtual] = useState<TipoVeiculo | 'todos'>('todos');
  const [veiculoSelecionado, setVeiculoSelecionado] = useState<Veiculo | null>(null);

  const [dataRetirada, setDataRetirada] = useState('');
  const [dataDevolucao, setDataDevolucao] = useState('');
  const [seguroPessoal, setSeguroPessoal] = useState(false);
  const [seguroTerceiros, setSeguroTerceiros] = useState(false);
  const [simulacao, setSimulacao] = useState<SimulacaoResponse | null>(null);
  const [erroSimulacao, setErroSimulacao] = useState('');

  const [listaMotoristas, setListaMotoristas] = useState<any[]>([]);
  const [motoristaId, setMotoristaId] = useState<number | null>(null);

  useEffect(() => {
    const carregarVeiculos = async () => {
      setLoading(true);
      try {
        const categoria = filtroAtual === 'todos' ? undefined : filtroAtual;
        const dados = await veiculoService.listar(categoria);
        setVeiculos(dados);
      } catch (error) {
        console.error("Erro ao buscar veículos", error);
      } finally {
        setLoading(false);
      }
    };
    if (step === 1) carregarVeiculos();
  }, [filtroAtual, step]);

  useEffect(() => {
    const carregarMotoristas = async () => {
        if (step === 2 && isCompany) {
            try {
                const dadosEmpresa: any = await clienteService.meusDados('cliente_pj');
                setListaMotoristas(dadosEmpresa.motoristas || []);
            } catch (err) {
                console.error("Erro ao carregar motoristas", err);
            }
        }
    };
    carregarMotoristas();
  }, [step, isCompany]);


  const handleSelecionarVeiculo = (v: Veiculo) => {
    setVeiculoSelecionado(v);
    setStep(2);
    window.scrollTo(0,0);
  };

  const handleSimular = async () => {
    if (isCompany && !motoristaId) {
        setErroSimulacao("Selecione o motorista responsável.");
        return;
    }

    if (!veiculoSelecionado || !dataRetirada || !dataDevolucao) {
        setErroSimulacao("Selecione as datas de retirada e devolução.");
        return;
    }
    setLoading(true);
    setErroSimulacao('');
    
    try {
        const payload: SimulacaoRequest = {
            veiculo_id: veiculoSelecionado.id_veiculo,
            data_retirada: dataRetirada,
            data_devolucao: dataDevolucao,
            seguro_pessoal: seguroPessoal,
            seguro_terceiros: seguroTerceiros
        };
        const resultado = await reservaService.simular(payload);
        setSimulacao(resultado);
        setStep(3);
    } catch (err: any) {
        setErroSimulacao(err.response?.data?.detail || "Erro ao simular valores.");
    } finally {
        setLoading(false);
    }
  };

  const handleConfirmarReserva = async () => {
    if (!veiculoSelecionado || !simulacao) return;
    setLoading(true);
    try {
        const formatarData = (d: string) => d.length === 16 ? `${d}:00` : d;
        const payload: any = { 
            veiculo_id: veiculoSelecionado.id_veiculo,
            data_retirada: formatarData(dataRetirada),
            data_devolucao: formatarData(dataDevolucao),
            seguro_pessoal: seguroPessoal,
            seguro_terceiros: seguroTerceiros,
        };
        
        if (isCompany && motoristaId) {
            payload.motorista_id = motoristaId;
        }

        await reservaService.criar(payload);
        navigate('/reservas/minhas');
    } catch (err: any) {
        console.error(err);
        const mensagemErro = err.response?.data?.detail || "Erro desconhecido ao confirmar.";
        if (Array.isArray(mensagemErro)) {
            alert(`Erro de validação: ${mensagemErro[0].msg}`);
        } else {
            alert(`Erro: ${mensagemErro}`);
        }
    } finally {
        setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 font-sans text-slate-900 flex flex-col">
      <NavbarInternal />

      <div className="max-w-7xl mx-auto px-4 py-10 w-full flex-grow">
        
        {/* BARRA DE PROGRESSO */}
        <div className="w-full max-w-3xl mx-auto mb-12">
           
           <div className="relative w-full h-3 bg-gray-200 rounded-full overflow-hidden mb-3">
              <div 
                  className="absolute top-0 left-0 h-full bg-blue-600 transition-all duration-700 ease-in-out shadow-[0_0_10px_rgba(37,99,235,0.5)]"
                  style={{ width: step === 1 ? '33%' : step === 2 ? '66%' : '100%' }}
              >
                  <div className="absolute top-0 right-0 bottom-0 w-20 bg-gradient-to-r from-transparent to-white/30 skew-x-12"></div>
              </div>
           </div>

           <div className="flex justify-between text-xs font-bold uppercase tracking-widest px-1">
              <span className={`${step >= 1 ? 'text-blue-700' : 'text-gray-400'} transition-colors duration-300`}>
                1. Veículo
              </span>
              <span className={`${step >= 2 ? 'text-blue-700' : 'text-gray-400'} transition-colors duration-300`}>
                2. Dados
              </span>
              <span className={`${step >= 3 ? 'text-blue-700' : 'text-gray-400'} transition-colors duration-300`}>
                3. Confirmar
              </span>
           </div>

        </div>

        {/* PASSO 1  */}
        {step === 1 && (
          <div className="animate-fade-in">
            <h2 className="text-3xl font-bold font-futuristic text-slate-800 mb-8 text-center md:text-left">Escolha seu Veículo</h2>
            <div className="flex flex-wrap gap-2 mb-8 justify-center md:justify-start">
                {/* Filtros */}
                <button onClick={() => setFiltroAtual('todos')} className={`px-4 py-2 rounded-full text-sm font-bold border ${filtroAtual === 'todos' ? 'bg-slate-900 text-white border-slate-900' : 'bg-white text-gray-600 border-gray-200'}`}>Todos</button>
                <button onClick={() => setFiltroAtual('passeio')} className={`px-4 py-2 rounded-full text-sm font-bold border ${filtroAtual === 'passeio' ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-gray-600 border-gray-200'}`}>Passeio</button>
                <button onClick={() => setFiltroAtual('motocicleta')} className={`px-4 py-2 rounded-full text-sm font-bold border ${filtroAtual === 'motocicleta' ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-gray-600 border-gray-200'}`}>Motos</button>
                <button onClick={() => setFiltroAtual('utilitario')} className={`px-4 py-2 rounded-full text-sm font-bold border ${filtroAtual === 'utilitario' ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-gray-600 border-gray-200'}`}>Utilitários</button>
            </div>

            {loading ? (
              <div className="flex justify-center py-20"><Loader2 size={48} className="animate-spin text-blue-600" /></div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {veiculos.map((veiculo) => (
                  <div key={veiculo.id_veiculo} className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-xl transition-all group">
                    <div className="h-48 bg-gray-100 relative">
                      <img src={veiculo.imagem_url || imgPlaceholder} alt={veiculo.modelo} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"/>
                      <div className="absolute top-3 right-3 bg-white/90 backdrop-blur px-2 py-1 rounded text-[10px] font-bold uppercase tracking-wider text-slate-700">
                        {veiculo.tipo_veiculo}
                      </div>
                    </div>
                    <div className="p-6">
                      <h3 className="text-lg font-bold text-slate-900">{veiculo.modelo}</h3>
                      <p className="text-xs text-gray-500 mb-4">{veiculo.marca} • {veiculo.ano_modelo}</p>
                      <div className="flex justify-between items-end">
                        <div>
                            <p className="text-xs text-gray-400">Diária</p>
                            <p className="text-xl font-bold text-blue-600">R$ {veiculo.valor_diaria.toFixed(2)}</p>
                        </div>
                        <button onClick={() => handleSelecionarVeiculo(veiculo)} className="bg-slate-900 hover:bg-blue-600 text-white text-sm font-bold py-2 px-4 rounded-lg transition-colors">
                            Escolher
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* PASSO 2: DATAS E SEGUROS + MOTORISTA (PJ) */}
        {step === 2 && veiculoSelecionado && (
             <div className="max-w-3xl mx-auto animate-fade-in">
                <div className="bg-white rounded-3xl shadow-lg border border-gray-100 overflow-hidden">
                    
                    {/* Header Veículo */}
                    <div className="bg-slate-50 p-6 border-b border-gray-100 flex items-center gap-4">
                        <img src={veiculoSelecionado.imagem_url || imgPlaceholder} className="w-24 h-16 object-cover rounded-lg shadow-sm" alt="" />
                        <div>
                            <h3 className="font-bold text-xl">{veiculoSelecionado.modelo}</h3>
                            <p className="text-sm text-gray-500">Diária: <span className="text-blue-600 font-bold">R$ {veiculoSelecionado.valor_diaria.toFixed(2)}</span></p>
                        </div>
                    </div>

                    <div className="p-8 space-y-8">
                        
                        {/* --- SELEÇÃO DE MOTORISTA (APENAS PJ) --- */}
                        {isCompany && (
                            <div className="p-4 bg-blue-50 rounded-xl border border-blue-100">
                                <h4 className="flex items-center gap-2 font-bold text-blue-900 mb-3">
                                    <User className="text-blue-600" /> Quem irá retirar o veículo?
                                </h4>
                                <div className="relative">
                                    <select 
                                        className="w-full p-3 border border-blue-200 rounded-lg appearance-none focus:ring-2 focus:ring-blue-500 outline-none bg-white"
                                        onChange={(e) => setMotoristaId(Number(e.target.value))}
                                        defaultValue=""
                                    >
                                        <option value="" disabled>Selecione um motorista da lista...</option>
                                        {listaMotoristas.map((motorista) => (
                                            <option key={motorista.id_pessoa} value={motorista.id_pessoa}>
                                                {motorista.nome_completo} (CPF: {motorista.cpf})
                                            </option>
                                        ))}
                                    </select>
                                    {listaMotoristas.length === 0 && (
                                        <p className="text-xs text-red-500 mt-2">
                                            Você não tem motoristas cadastrados. Vá em "Gestão de Motoristas" primeiro.
                                        </p>
                                    )}
                                </div>
                            </div>
                        )}
                        {/* Datas */}
                        <div>
                            <h4 className="flex items-center gap-2 font-bold text-gray-700 mb-4">
                                <Calendar className="text-blue-500" /> Período da Reserva
                            </h4>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-xs font-bold text-gray-500 mb-1">Retirada</label>
                                    <input type="datetime-local" className="w-full border border-gray-300 rounded-lg p-3 text-sm focus:ring-2 focus:ring-blue-500 outline-none" onChange={(e) => setDataRetirada(e.target.value)} />
                                </div>
                                <div>
                                    <label className="block text-xs font-bold text-gray-500 mb-1">Devolução</label>
                                    <input type="datetime-local" className="w-full border border-gray-300 rounded-lg p-3 text-sm focus:ring-2 focus:ring-blue-500 outline-none" onChange={(e) => setDataDevolucao(e.target.value)} />
                                </div>
                            </div>
                        </div>

                        {/* Seguros */}
                        <div>
                            <h4 className="flex items-center gap-2 font-bold text-gray-700 mb-4">
                                <Shield className="text-blue-500" /> Proteção e Seguros
                            </h4>
                            <div className="space-y-3">
                                <label className="flex items-center p-4 border border-gray-200 rounded-xl cursor-pointer hover:bg-blue-50 transition-colors">
                                    <input type="checkbox" className="w-5 h-5 text-blue-600" onChange={(e) => setSeguroPessoal(e.target.checked)} />
                                    <div className="ml-3"><span className="block font-bold text-sm text-gray-800">Seguro Pessoal (+R$ 25,00/dia)</span></div>
                                </label>
                                <label className="flex items-center p-4 border border-gray-200 rounded-xl cursor-pointer hover:bg-blue-50 transition-colors">
                                    <input type="checkbox" className="w-5 h-5 text-blue-600" onChange={(e) => setSeguroTerceiros(e.target.checked)} />
                                    <div className="ml-3"><span className="block font-bold text-sm text-gray-800">Seguro contra Terceiros (+R$ 35,00/dia)</span></div>
                                </label>
                            </div>
                        </div>

                        {erroSimulacao && <div className="text-red-500 text-sm bg-red-50 p-3 rounded-lg text-center font-bold">{erroSimulacao}</div>}
                        
                        <div className="flex gap-4 pt-4">
                            <button onClick={() => setStep(1)} className="px-6 py-3 rounded-xl text-gray-600 font-bold hover:bg-gray-100 transition-colors">Voltar</button>
                            <button onClick={handleSimular} disabled={loading} className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-xl transition-all shadow-lg flex justify-center items-center gap-2 disabled:opacity-50">
                                {loading ? <Loader2 className="animate-spin" /> : <>Simular e Continuar <ArrowRight size={18} /></>}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        )}

        {/* PASSO 3: CONFIRMAÇÃO  */}
        {step === 3 && simulacao && veiculoSelecionado && (
             <div className="max-w-2xl mx-auto animate-fade-in">
                <div className="bg-white rounded-3xl shadow-xl border border-blue-100 overflow-hidden">
                    <div className="bg-slate-900 p-6 text-center"><h2 className="text-2xl font-bold text-white font-futuristic">Resumo da Reserva</h2></div>
                    <div className="p-8">
                        <div className="space-y-3 text-sm text-gray-700 mb-8">
                             <div className="flex justify-between"><span>Período</span><span className="font-bold">{new Date(dataRetirada).toLocaleDateString()} até {new Date(dataDevolucao).toLocaleDateString()}</span></div>
                             <div className="flex justify-between text-xl font-bold text-blue-700 pt-4 border-t border-gray-100 mt-2"><span>Total Estimado</span><span>R$ {simulacao.valor_total_estimado.toFixed(2)}</span></div>
                        </div>
                        <div className="flex gap-4">
                            <button onClick={() => setStep(2)} className="px-6 py-3 rounded-xl text-gray-600 font-bold hover:bg-gray-100 transition-colors flex items-center gap-2"><ArrowLeft size={18} /> Corrigir</button>
                            <button onClick={handleConfirmarReserva} disabled={loading} className="flex-1 bg-green-600 hover:bg-green-700 text-white font-bold py-3 rounded-xl transition-all shadow-lg flex justify-center items-center gap-2 disabled:opacity-50">
                                {loading ? <Loader2 className="animate-spin" /> : <>CONFIRMAR RESERVA <Check size={18} /></>}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        )}

      </div>
      
      <Footer />
    </div>
  );
}
