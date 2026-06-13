import { useState, useEffect } from 'react';
import { User, Trash2, Plus, Loader2, AlertCircle, ShieldCheck } from 'lucide-react';
import { NavbarInternal } from '../../../components/layout/NavbarInternal';
import { Footer } from '../../../components/layout/Footer';
import { ConfirmModal } from '../../../components/ui/ConfirmModal';
import { StatusModal } from '../../../components/ui/StatusModal';
import { clienteService } from '../../../services/clienteService';
import { empresaService } from '../../../services/empresaService';

interface Motorista {
  id_pessoa: number;
  nome_completo: string;
  cpf: string;
  email: string;
}

export function GestaoMotoristas() {
  const [motoristas, setMotoristas] = useState<Motorista[]>([]);
  const [loading, setLoading] = useState(true);
  
  const [novoCpf, setNovoCpf] = useState('');
  const [adicionando, setAdicionando] = useState(false);
  
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [motoristaParaRemover, setMotoristaParaRemover] = useState<Motorista | null>(null);
  const [statusModal, setStatusModal] = useState<{ open: boolean; type: 'success' | 'error'; title: string; msg: string }>({
    open: false, type: 'success', title: '', msg: ''
  });

  const carregarMotoristas = async () => {
    try {
      const dadosEmpresa: any = await clienteService.meusDados('cliente_pj');
      setMotoristas(dadosEmpresa.motoristas || []);
    } catch (error) {
      console.error("Erro ao carregar motoristas:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    carregarMotoristas();
  }, []);

  // --- ADICIONAR MOTORISTA ---
  const handleAdicionar = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!novoCpf) return;
    
    setAdicionando(true);
    try {
      await empresaService.adicionarMotorista(novoCpf);
      setNovoCpf(''); 
      await carregarMotoristas(); 
      setStatusModal({
        open: true, type: 'success', title: 'Motorista Vinculado!', msg: 'O motorista foi adicionado à sua frota com sucesso.'
      });
    } catch (err: any) {
      const msg = err.response?.data?.detail || "Erro ao adicionar. Verifique se o CPF está correto e se o motorista possui cadastro.";
      setStatusModal({
        open: true, type: 'error', title: 'Falha ao Adicionar', msg: msg
      });
    } finally {
      setAdicionando(false);
    }
  };

  // --- REMOVER MOTORISTA ---
  const requestRemover = (motorista: Motorista) => {
    setMotoristaParaRemover(motorista);
    setConfirmOpen(true);
  };

  const confirmRemover = async () => {
    if (!motoristaParaRemover) return;
    
    try {
      await empresaService.removerMotorista(motoristaParaRemover.id_pessoa);
      setConfirmOpen(false);
      await carregarMotoristas();
      setStatusModal({
        open: true, type: 'success', title: 'Acesso Removido', msg: 'O motorista foi desvinculado da sua empresa.'
      });
    } catch (error) {
      setConfirmOpen(false);
      setStatusModal({
        open: true, type: 'error', title: 'Erro', msg: 'Não foi possível remover o motorista.'
      });
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 font-sans text-slate-900 flex flex-col">
      <NavbarInternal />

      {/* MODAIS */}
      <ConfirmModal 
        isOpen={confirmOpen}
        isLoading={false}
        onClose={() => setConfirmOpen(false)}
        onConfirm={confirmRemover}
        title="Desvincular Motorista?"
        description={`Tem certeza que deseja remover ${motoristaParaRemover?.nome_completo}? Ele não poderá mais receber reservas pela empresa.`}
      />

      <StatusModal 
        isOpen={statusModal.open}
        onClose={() => setStatusModal({ ...statusModal, open: false })}
        type={statusModal.type}
        title={statusModal.title}
        message={statusModal.msg}
      />

      <div className="max-w-4xl mx-auto px-4 mt-8 w-full flex-grow pb-12">
        
        <div className="flex items-center gap-4 mb-8">
            <div className="bg-slate-900 p-3 rounded-full text-white shadow-lg">
                <ShieldCheck size={32} />
            </div>
            <div>
                <h1 className="text-3xl font-bold text-slate-800 font-futuristic">Gestão de Motoristas</h1>
                <p className="text-gray-500">Adicione condutores autorizados a utilizar a frota da sua empresa.</p>
            </div>
        </div>

        {/* CARD DE ADICIONAR */}
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-200 mb-10 animate-fade-in">
          <h3 className="font-bold text-lg mb-4 flex items-center gap-2 text-slate-700">
            <Plus size={20} className="text-blue-600" /> Vincular Novo Condutor
          </h3>
          
          <form onSubmit={handleAdicionar} className="flex flex-col sm:flex-row gap-4 items-start sm:items-center">
            <div className="flex-grow w-full">
              <input 
                type="text" 
                placeholder="Digite o CPF do motorista (apenas números)" 
                className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none text-lg"
                value={novoCpf}
                onChange={(e) => setNovoCpf(e.target.value)}
              />
            </div>
            <button 
              type="submit"
              disabled={adicionando || !novoCpf}
              className="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-8 rounded-xl transition-all shadow-lg flex justify-center items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed font-futuristic"
            >
              {adicionando ? <Loader2 className="animate-spin" /> : "ADICIONAR"}
            </button>
          </form>
          <div className="mt-4 flex items-start gap-2 text-xs text-gray-400 bg-gray-50 p-3 rounded-lg border border-gray-100">
            <AlertCircle size={14} className="mt-0.5 shrink-0" />
            <p>O motorista precisa ter um cadastro pessoal (Pessoa Física) ativo na FrotaNext antes de ser vinculado.</p>
          </div>
        </div>

        {/* LISTA DE MOTORISTAS */}
        <div className="flex items-center justify-between mb-6">
            <h3 className="font-bold text-xl text-slate-800 font-futuristic">Equipe Autorizada</h3>
            <span className="bg-blue-100 text-blue-800 text-xs font-bold px-3 py-1 rounded-full">{motoristas.length} condutores</span>
        </div>
        
        {loading ? (
           <div className="flex justify-center py-10"><Loader2 className="animate-spin text-blue-600" size={40} /></div>
        ) : motoristas.length === 0 ? (
           <div className="text-center py-16 bg-white rounded-2xl border border-dashed border-gray-300 text-gray-500 flex flex-col items-center">
              <User size={48} className="text-gray-300 mb-4" />
              <p>Nenhum motorista vinculado ainda.</p>
           </div>
        ) : (
           <div className="grid gap-4 animate-fade-in">
              {motoristas.map((m) => (
                <div key={m.id_pessoa} className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col sm:flex-row items-center justify-between gap-4 hover:shadow-md transition-shadow">
                   
                   <div className="flex items-center gap-4 w-full sm:w-auto">
                      <div className="bg-blue-50 p-4 rounded-full text-blue-600 shrink-0">
                         <User size={24} />
                      </div>
                      <div>
                         <h4 className="font-bold text-lg text-slate-800">{m.nome_completo}</h4>
                         <p className="text-sm text-gray-500 font-mono">CPF: {m.cpf}</p>
                         <p className="text-xs text-gray-400">{m.email}</p>
                      </div>
                   </div>

                   <button 
                      onClick={() => requestRemover(m)}
                      className="w-full sm:w-auto text-red-500 hover:text-white hover:bg-red-500 border border-red-200 hover:border-red-500 px-4 py-2 rounded-lg transition-all flex items-center justify-center gap-2 text-sm font-bold"
                   >
                      <Trash2 size={18} /> Desvincular
                   </button>
                </div>
              ))}
           </div>
        )}

      </div>

      <Footer />
    </div>
  );
}