import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import {
  User,
  Mail,
  Phone,
  MapPin,
  FileText,
  Briefcase,
  Save,
  Loader2,
  Truck,
  AlertCircle,
} from "lucide-react";
import { NavbarInternal } from "../../components/layout/NavbarInternal";
import { Footer } from "../../components/layout/Footer";
import { ConfirmModal } from "../../components/ui/ConfirmModal";
import { StatusModal } from "../../components/ui/StatusModal";
import { useAuth } from "../../hooks/useAuth";
import {
  clienteService,
  type DadosCliente,
} from "../../services/clienteService";

export function Perfil() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [confirmOpen, setConfirmOpen] = useState(false);
  const [statusModal, setStatusModal] = useState<{
    open: boolean;
    type: "success" | "error";
    title: string;
    msg: string;
  }>({
    open: false,
    type: "success",
    title: "",
    msg: "",
  });
  const [dadosParaSalvar, setDadosParaSalvar] = useState<DadosCliente | null>(
    null
  );

  const {
    register,
    handleSubmit,
    reset, // <--- IMPORTANTE: Usar reset em vez de setValue
    formState: { errors, isValid },
  } = useForm<DadosCliente>({
    mode: "onChange",
  });

  useEffect(() => {
    if (user?.id) {
      carregarDados();
    }
  }, [user]);

  const carregarDados = async () => {
    try {
      if (user?.tipo === "admin") return;
      const dados = await clienteService.meusDados(
        user!.tipo as "cliente_pf" | "cliente_pj"
      );

      // CORREÇÃO PRINCIPAL:
      // O reset preenche tudo de uma vez e recalcula a validade do formulário.
      reset(dados);
    } catch (error) {
      console.error("Erro ao carregar perfil:", error);
    } finally {
      setLoading(false);
    }
  };

  const onSubmit = (data: DadosCliente) => {
    setDadosParaSalvar(data);
    setConfirmOpen(true);
  };

  const handleConfirmSave = async () => {
    if (!dadosParaSalvar) return;
    setSaving(true);
    try {
      await clienteService.atualizarMeusDados(
        user!.tipo as any,
        dadosParaSalvar
      );
      setConfirmOpen(false);
      setStatusModal({
        open: true,
        type: "success",
        title: "Perfil Atualizado!",
        msg: "Suas informações foram salvas com sucesso.",
      });
      await carregarDados();
    } catch (error) {
      setConfirmOpen(false);
      setStatusModal({
        open: true,
        type: "error",
        title: "Erro ao Salvar",
        msg: "Não foi possível atualizar seus dados.",
      });
    } finally {
      setSaving(false);
    }
  };

  const isPJ = user?.tipo === "cliente_pj";

  return (
    <div className="min-h-screen bg-gray-50 font-sans text-slate-900 flex flex-col">
      <NavbarInternal />

      <ConfirmModal
        isOpen={confirmOpen}
        isLoading={saving}
        onClose={() => setConfirmOpen(false)}
        onConfirm={handleConfirmSave}
        title="Salvar Alterações no Perfil?"
        description="Tem certeza que deseja atualizar seus dados cadastrais?"
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
          <div className="bg-blue-600 p-4 rounded-full shadow-lg text-white">
            <User size={32} />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-slate-800 font-futuristic">
              Meu Perfil
            </h1>
            <p className="text-gray-500">
              Gerencie suas informações pessoais e de contato.
            </p>
          </div>
        </div>

        {loading ? (
          <div className="flex justify-center py-20">
            <Loader2 size={48} className="animate-spin text-blue-600" />
          </div>
        ) : (
          <form
            onSubmit={handleSubmit(onSubmit)}
            className="space-y-8 animate-fade-in"
          >
            {/* CARD 1: IDENTIFICAÇÃO */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
              <h2 className="text-lg font-bold text-slate-700 mb-6 flex items-center gap-2 border-b pb-2">
                <FileText size={20} className="text-blue-600" /> Identificação
              </h2>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-xs font-bold text-gray-500 mb-1 uppercase">
                    {isPJ ? "Razão Social" : "Nome Completo"}
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                      {isPJ ? <Briefcase size={18} /> : <User size={18} />}
                    </div>
                    <input
                      {...register(isPJ ? "razao_social" : "nome_completo")}
                      disabled
                      className="w-full pl-10 p-3 bg-gray-50 border border-gray-200 rounded-lg text-gray-500 cursor-not-allowed font-medium"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold text-gray-500 mb-1 uppercase">
                    {isPJ ? "CNPJ" : "CPF"}
                  </label>
                  <input
                    {...register(isPJ ? "cnpj" : "cpf")}
                    disabled
                    className="w-full p-3 bg-gray-50 border border-gray-200 rounded-lg text-gray-500 cursor-not-allowed font-medium"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-gray-500 mb-1 uppercase">
                    E-mail
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                      <Mail size={18} />
                    </div>
                    <input
                      {...register("email", {
                        required: "E-mail é obrigatório",
                        pattern: {
                          value: /^\S+@\S+$/i,
                          message: "E-mail inválido",
                        },
                      })}
                      className={`w-full pl-10 p-3 border rounded-lg focus:ring-2 outline-none ${
                        errors.email
                          ? "border-red-500 focus:ring-red-200"
                          : "border-gray-300 focus:ring-blue-500"
                      }`}
                    />
                  </div>
                  {errors.email && (
                    <p className="text-xs text-red-500 mt-1 flex items-center gap-1">
                      <AlertCircle size={12} /> {errors.email.message}
                    </p>
                  )}
                </div>

                {!isPJ && (
                  <div>
                    <label className="block text-xs font-bold text-gray-500 mb-1 uppercase">
                      CNH
                    </label>
                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                        <Truck size={18} />
                      </div>
                      <input
                        {...register("cnh", { required: "CNH é obrigatória" })}
                        className={`w-full pl-10 p-3 border rounded-lg focus:ring-2 outline-none ${
                          errors.cnh
                            ? "border-red-500 focus:ring-red-200"
                            : "border-gray-300 focus:ring-blue-500"
                        }`}
                      />
                    </div>
                    {errors.cnh && (
                      <p className="text-xs text-red-500 mt-1 flex items-center gap-1">
                        <AlertCircle size={12} /> {errors.cnh.message}
                      </p>
                    )}
                  </div>
                )}

                <div>
                  <label className="block text-xs font-bold text-gray-500 mb-1 uppercase">
                    Telefone
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                      <Phone size={18} />
                    </div>
                    <input
                      {...register("telefone", {
                        required: "Telefone é obrigatório",
                      })}
                      className={`w-full pl-10 p-3 border rounded-lg focus:ring-2 outline-none ${
                        errors.telefone
                          ? "border-red-500 focus:ring-red-200"
                          : "border-gray-300 focus:ring-blue-500"
                      }`}
                    />
                  </div>
                  {errors.telefone && (
                    <p className="text-xs text-red-500 mt-1 flex items-center gap-1">
                      <AlertCircle size={12} /> {errors.telefone.message}
                    </p>
                  )}
                </div>
              </div>
            </div>

            {/* CARD 2: ENDEREÇO */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
              <h2 className="text-lg font-bold text-slate-700 mb-6 flex items-center gap-2 border-b pb-2">
                <MapPin size={20} className="text-blue-600" /> Endereço
              </h2>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="md:col-span-1">
                  <label className="block text-xs font-bold text-gray-500 mb-1">
                    CEP
                  </label>
                  <input
                    {...register("endereco.cep", { required: true })}
                    className={`w-full p-3 border rounded-lg outline-none ${
                      errors.endereco?.cep
                        ? "border-red-500"
                        : "border-gray-300 focus:ring-2 focus:ring-blue-500"
                    }`}
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-xs font-bold text-gray-500 mb-1">
                    Rua
                  </label>
                  <input
                    {...register("endereco.rua", { required: true })}
                    className={`w-full p-3 border rounded-lg outline-none ${
                      errors.endereco?.rua
                        ? "border-red-500"
                        : "border-gray-300 focus:ring-2 focus:ring-blue-500"
                    }`}
                  />
                </div>
                <div className="md:col-span-1">
                  <label className="block text-xs font-bold text-gray-500 mb-1">
                    Número
                  </label>
                  <input
                    {...register("endereco.numero", { required: true })}
                    className={`w-full p-3 border rounded-lg outline-none ${
                      errors.endereco?.numero
                        ? "border-red-500"
                        : "border-gray-300 focus:ring-2 focus:ring-blue-500"
                    }`}
                  />
                </div>
                <div className="md:col-span-1">
                  <label className="block text-xs font-bold text-gray-500 mb-1">
                    Bairro
                  </label>
                  <input
                    {...register("endereco.bairro", { required: true })}
                    className={`w-full p-3 border rounded-lg outline-none ${
                      errors.endereco?.bairro
                        ? "border-red-500"
                        : "border-gray-300 focus:ring-2 focus:ring-blue-500"
                    }`}
                  />
                </div>
                <div className="md:col-span-1">
                  <label className="block text-xs font-bold text-gray-500 mb-1">
                    Complemento
                  </label>
                  <input
                    {...register("endereco.complemento")}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-xs font-bold text-gray-500 mb-1">
                    Cidade
                  </label>
                  <input
                    {...register("endereco.cidade", { required: true })}
                    className={`w-full p-3 border rounded-lg outline-none ${
                      errors.endereco?.cidade
                        ? "border-red-500"
                        : "border-gray-300 focus:ring-2 focus:ring-blue-500"
                    }`}
                  />
                </div>
                <div className="md:col-span-1">
                  <label className="block text-xs font-bold text-gray-500 mb-1">
                    Estado (UF)
                  </label>
                  <input
                    {...register("endereco.estado", {
                      required: true,
                      maxLength: 2,
                    })}
                    className={`w-full p-3 border rounded-lg outline-none ${
                      errors.endereco?.estado
                        ? "border-red-500"
                        : "border-gray-300 focus:ring-2 focus:ring-blue-500"
                    }`}
                    maxLength={2}
                  />
                </div>
              </div>
            </div>

            <div className="flex justify-end items-center gap-4">
              {!isValid && (
                <p className="text-red-500 text-xs font-bold animate-pulse">
                  Existem campos obrigatórios vazios ou inválidos.
                </p>
              )}

              <button
                type="submit"
                disabled={saving}
                className={`font-bold py-4 px-8 rounded-xl shadow-lg flex items-center gap-2 transition-all font-futuristic ${
                  saving
                    ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                    : "bg-green-600 hover:bg-green-700 text-white hover:scale-105 transform"
                }`}
              >
                {saving ? (
                  <Loader2 className="animate-spin" />
                ) : (
                  <>
                    <Save size={20} /> SALVAR ALTERAÇÕES
                  </>
                )}
              </button>
            </div>
          </form>
        )}
      </div>

      <Footer />
    </div>
  );
}
