import { X, User, MapPin, Phone, Mail, Shield, Truck, Users } from 'lucide-react';
import type { DadosCliente } from '../../services/clienteService';

interface ClientDetailsModalProps {
  isOpen: boolean;
  onClose: () => void;
  cliente: DadosCliente | null;
}

export function ClientDetailsModal({ isOpen, onClose, cliente }: ClientDetailsModalProps) {
  if (!isOpen || !cliente) return null;

  const isPJ = cliente.tipo_cliente === 'PJ';
  const nomePrincipal = isPJ ? cliente.razao_social : cliente.nome_completo;
  const docPrincipal = isPJ ? cliente.cnpj : cliente.cpf;

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-fade-in">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl overflow-hidden flex flex-col max-h-[90vh]">
        
        {/* Header */}
        <div className="bg-slate-900 p-6 border-b border-slate-800 flex justify-between items-center shrink-0">
          <div className="flex items-center gap-3">
            <div className="bg-blue-600 p-2 rounded-lg text-white">
               {isPJ ? <BriefcaseIcon /> : <User size={20} />}
            </div>
            <div>
                <p className="text-xs text-blue-400 font-bold uppercase tracking-wider">
                    {isPJ ? 'Pessoa Jurídica' : 'Pessoa Física'}
                </p>
                <h3 className="text-xl font-bold text-white font-futuristic">{nomePrincipal}</h3>
            </div>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-white transition-colors bg-white/10 p-2 rounded-full">
            <X size={20} />
          </button>
        </div>

        {/* Corpo */}
        <div className="p-8 overflow-y-auto custom-scrollbar space-y-8">
            
            {/* Status */}
            <div className={`p-3 rounded-lg border flex items-center gap-2 ${cliente.e_ativo ? 'bg-green-50 border-green-200 text-green-800' : 'bg-red-50 border-red-200 text-red-800'}`}>
                <Shield size={18} />
                <span className="font-bold text-sm">Status da Conta: {cliente.e_ativo ? 'ATIVA' : 'BLOQUEADA'}</span>
            </div>

            {/* Dados Pessoais */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <h4 className="text-xs font-bold text-gray-400 uppercase mb-1">Documento</h4>
                    <p className="font-mono text-slate-700 font-bold">{docPrincipal}</p>
                </div>
                <div>
                    <h4 className="text-xs font-bold text-gray-400 uppercase mb-1">E-mail</h4>
                    <p className="text-slate-700 flex items-center gap-2"><Mail size={14}/> {cliente.email}</p>
                </div>
                <div>
                    <h4 className="text-xs font-bold text-gray-400 uppercase mb-1">Telefone</h4>
                    <p className="text-slate-700 flex items-center gap-2"><Phone size={14}/> {cliente.telefone}</p>
                </div>
                {!isPJ && (
                    <div>
                        <h4 className="text-xs font-bold text-gray-400 uppercase mb-1">CNH</h4>
                        <p className="text-slate-700 flex items-center gap-2"><Truck size={14}/> {cliente.cnh}</p>
                    </div>
                )}
                <div>
                    <h4 className="text-xs font-bold text-gray-400 uppercase mb-1">Data Cadastro</h4>
                    <p className="text-slate-700">{new Date(cliente.data_criacao).toLocaleDateString('pt-BR')}</p>
                </div>
            </div>

            {/* Endereço */}
            <div className="bg-gray-50 p-4 rounded-xl border border-gray-100">
                <h4 className="font-bold text-gray-700 flex items-center gap-2 mb-3 border-b pb-2 border-gray-200">
                    <MapPin size={16} className="text-blue-500"/> Endereço
                </h4>
                <p className="text-sm text-gray-600">
                    {cliente.endereco.rua}, {cliente.endereco.numero} {cliente.endereco.complemento && `- ${cliente.endereco.complemento}`}
                    <br />
                    {cliente.endereco.bairro} - {cliente.endereco.cidade}/{cliente.endereco.estado}
                    <br />
                    CEP: {cliente.endereco.cep}
                </p>
            </div>

            {/* Motoristas (Apenas PJ) */}
            {isPJ && cliente.motoristas && (
                <div>
                    <h4 className="font-bold text-gray-700 flex items-center gap-2 mb-4">
                        <Users size={20} className="text-blue-500"/> Motoristas Vinculados ({cliente.motoristas.length})
                    </h4>
                    {cliente.motoristas.length > 0 ? (
                        <div className="grid gap-2">
                            {cliente.motoristas.map((mot: any) => (
                                <div key={mot.id_pessoa} className="flex items-center justify-between p-3 bg-white border rounded-lg shadow-sm">
                                    <div className="flex items-center gap-3">
                                        <div className="bg-blue-100 p-2 rounded-full text-blue-600"><User size={16}/></div>
                                        <div>
                                            <p className="text-sm font-bold">{mot.nome_completo}</p>
                                            <p className="text-xs text-gray-500">CPF: {mot.cpf}</p>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <p className="text-sm text-gray-400 italic">Nenhum motorista vinculado.</p>
                    )}
                </div>
            )}

        </div>
      </div>
    </div>
  );
}

// Ícone auxiliar
function BriefcaseIcon() {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="20" height="14" x="2" y="7" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
    )
}