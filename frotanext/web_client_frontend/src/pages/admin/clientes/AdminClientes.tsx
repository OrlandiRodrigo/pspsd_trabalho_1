import { useState, useEffect } from "react";
import {
  Search,
  Loader2,
  Info,
  Trash2,
  Lock,
  Unlock,
  Filter,
  User,
  Briefcase,
} from "lucide-react";
import { AdminLayout } from "../../../components/layout/AdminLayout";
import {
  clienteService,
  type DadosCliente,
} from "../../../services/clienteService";

import { ClientDetailsModal } from "../../../components/ui/ClientDetailsModal";
import { ConfirmModal } from "../../../components/ui/ConfirmModal";
import { StatusModal } from "../../../components/ui/StatusModal";

export function AdminClientes() {
  const [clientes, setClientes] = useState<DadosCliente[]>([]);
  const [loading, setLoading] = useState(true);
  const [termoBusca, setTermoBusca] = useState("");
  const [filtroTipo, setFiltroTipo] = useState<"todos" | "PF" | "PJ">("todos");

  const [clienteSelecionado, setClienteSelecionado] =
    useState<DadosCliente | null>(null);
  const [detailsOpen, setDetailsOpen] = useState(false);
  const [blockOpen, setBlockOpen] = useState(false);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [loadingAction, setLoadingAction] = useState(false);

  const [statusModal, setStatusModal] = useState<{
    open: boolean;
    type: "success" | "error";
    title: string;
    message: string;
  }>({
    open: false,
    type: "success",
    title: "",
    message: "",
  });

  const carregarDados = async () => {
    setLoading(true);
    try {
      const dados = await clienteService.listarTodos();
      setClientes(dados);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    carregarDados();
  }, []);

  // --- HANDLERS ---

  const handleToggleBlock = async () => {
    if (!clienteSelecionado) return;
    setLoadingAction(true);

    const novoStatus = clienteSelecionado.e_ativo ? "bloqueado" : "ativo";
    const acao = clienteSelecionado.e_ativo ? "Bloqueado" : "Desbloqueado";

    try {
      await clienteService.alterarStatus(
        clienteSelecionado.id_pessoa,
        clienteSelecionado.tipo_cliente,
        novoStatus
      );
      setBlockOpen(false);
      setStatusModal({
        open: true,
        type: "success",
        title: `Cliente ${acao}`,
        message: `O acesso do cliente foi atualizado com sucesso.`,
      });
      await carregarDados();
    } catch (err) {
      setStatusModal({
        open: true,
        type: "error",
        title: "Erro",
        message: "Não foi possível alterar o status.",
      });
    } finally {
      setLoadingAction(false);
    }
  };

  const handleDelete = async () => {
    if (!clienteSelecionado) return;
    setLoadingAction(true);
    try {
      await clienteService.deletar(
        clienteSelecionado.id_pessoa,
        clienteSelecionado.tipo_cliente
      );
      setDeleteOpen(false);
      setStatusModal({
        open: true,
        type: "success",
        title: "Cliente Excluído",
        message: "O registro foi removido permanentemente.",
      });
      await carregarDados();
    } catch (err) {
      setDeleteOpen(false);
      setStatusModal({
        open: true,
        type: "error",
        title: "Não pode excluir",
        message: "Este cliente possui histórico ou reservas ativas. Tente bloqueá-lo em vez de excluir.",
      });
    } finally {
      setLoadingAction(false);
    }
  };

  const clientesFiltrados = clientes.filter((c) => {
    const texto = termoBusca.toLowerCase();
    const nome = c.tipo_cliente === "PJ" ? c.razao_social : c.nome_completo;
    const doc = c.tipo_cliente === "PJ" ? c.cnpj : c.cpf;

    const matchBusca =
      nome?.toLowerCase().includes(texto) ||
      doc?.includes(texto) ||
      c.email.toLowerCase().includes(texto);

    const matchTipo = filtroTipo === "todos" || c.tipo_cliente === filtroTipo;

    return matchBusca && matchTipo;
  });

  return (
    <AdminLayout
      title="Gerenciamento de Clientes"
      subtitle="Controle de usuários PF e PJ."
    >
      {/* MODAIS */}
      <ClientDetailsModal
        isOpen={detailsOpen}
        onClose={() => setDetailsOpen(false)}
        cliente={clienteSelecionado}
      />

      <ConfirmModal
        isOpen={blockOpen}
        isLoading={loadingAction}
        onClose={() => setBlockOpen(false)}
        onConfirm={handleToggleBlock}
        title={
          clienteSelecionado?.e_ativo ? "Bloquear Acesso?" : "Restaurar Acesso?"
        }
        description={
          clienteSelecionado?.e_ativo
            ? "O usuário não poderá mais fazer login ou criar reservas."
            : "O usuário poderá voltar a utilizar a plataforma normalmente."
        }
      />

      <ConfirmModal
        isOpen={deleteOpen}
        isLoading={loadingAction}
        onClose={() => setDeleteOpen(false)}
        onConfirm={handleDelete}
        title="Excluir Conta?"
        description="Esta ação é irreversível. Só é permitida se o cliente não tiver reservas pendentes."
      />

      <StatusModal
        isOpen={statusModal.open}
        onClose={() => setStatusModal({ ...statusModal, open: false })}
        {...statusModal}
      />

      {/* BARRA DE AÇÕES */}
      <div className="flex flex-col md:flex-row justify-between items-center gap-4 mb-6 bg-white p-4 rounded-xl shadow-sm border border-gray-200">
        <div className="relative w-full md:w-80">
          <Search
            size={18}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
          />
          <input
            type="text"
            placeholder="Buscar por Nome, CPF/CNPJ ou Email..."
            className="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
            value={termoBusca}
            onChange={(e) => setTermoBusca(e.target.value)}
          />
        </div>
        <div className="flex items-center gap-2">
          <Filter size={18} className="text-gray-400 mr-2" />
          {["todos", "PF", "PJ"].map((t) => (
            <button
              key={t}
              onClick={() => setFiltroTipo(t as any)}
              className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-all ${
                filtroTipo === t
                  ? "bg-slate-800 text-white"
                  : "bg-gray-100 text-gray-600"
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      {/* TABELA */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        {loading ? (
          <div className="p-12 flex justify-center">
            <Loader2 className="animate-spin text-blue-600" size={32} />
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="bg-gray-50 text-gray-600 uppercase text-xs font-bold border-b border-gray-200">
                <tr>
                  <th className="px-6 py-4">Nome / Razão Social</th>
                  <th className="px-6 py-4">Tipo</th>
                  <th className="px-6 py-4">Documento</th>
                  <th className="px-6 py-4">Status</th>
                  <th className="px-6 py-4 text-right">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {clientesFiltrados.map((cliente) => (
                  <tr
                    key={`${cliente.tipo_cliente}-${cliente.id_pessoa}`}
                    className={`hover:bg-gray-50 transition-colors ${
                      !cliente.e_ativo ? "bg-red-50/50" : ""
                    }`}
                  >
                    <td className="px-6 py-4">
                      <div className="font-bold text-slate-900">
                        {cliente.tipo_cliente === "PJ"
                          ? cliente.razao_social
                          : cliente.nome_completo}
                      </div>
                      <div className="text-xs text-gray-400">
                        {cliente.email}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2 text-gray-600">
                        {cliente.tipo_cliente === "PJ" ? (
                          <Briefcase size={16} />
                        ) : (
                          <User size={16} />
                        )}
                        {cliente.tipo_cliente}
                      </div>
                    </td>
                    <td className="px-6 py-4 font-mono text-xs text-slate-600">
                      {cliente.tipo_cliente === "PJ"
                        ? cliente.cnpj
                        : cliente.cpf}
                    </td>
                    <td className="px-6 py-4">
                      {cliente.e_ativo ? (
                        <span className="px-2 py-1 rounded-full text-[10px] font-bold bg-green-100 text-green-700 border border-green-200">
                          ATIVO
                        </span>
                      ) : (
                        <span className="px-2 py-1 rounded-full text-[10px] font-bold bg-red-100 text-red-700 border border-red-200">
                          BLOQUEADO
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4 text-right flex justify-end gap-2">
                      <button
                        onClick={() => {
                          setClienteSelecionado(cliente);
                          setDetailsOpen(true);
                        }}
                        className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                        title="Detalhes"
                      >
                        <Info size={18} />
                      </button>

                      <button
                        onClick={() => {
                          setClienteSelecionado(cliente);
                          setBlockOpen(true);
                        }}
                        className={`p-2 rounded-lg transition-colors ${
                          cliente.e_ativo
                            ? "text-orange-500 hover:bg-orange-50"
                            : "text-green-600 hover:bg-green-50"
                        }`}
                        title={cliente.e_ativo ? "Bloquear" : "Desbloquear"}
                      >
                        {cliente.e_ativo ? (
                          <Lock size={18} />
                        ) : (
                          <Unlock size={18} />
                        )}
                      </button>

                      <button
                        onClick={() => {
                          setClienteSelecionado(cliente);
                          setDeleteOpen(true);
                        }}
                        className="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                        title="Excluir Conta"
                      >
                        <Trash2 size={18} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {clientesFiltrados.length === 0 && (
              <div className="p-8 text-center text-gray-400">
                Nenhum cliente encontrado.
              </div>
            )}
          </div>
        )}
      </div>
    </AdminLayout>
  );
}
