import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  useForm,
  type UseFormRegister,
  type FieldErrors,
} from "react-hook-form";
import {
  Mail,
  Lock,
  User,
  FileText,
  Truck,
  Phone,
  MapPin,
  Loader2,
  AlertCircle,
  Briefcase,
} from "lucide-react";
import { authApi } from "../../services/api";

import imgCadastro from "../../assets/cadastro-bg.png";
import logoBlue from "../../assets/logo-blue.png";

interface InputFieldProps {
  label: string;
  name: string;
  icon: any;
  placeholder: string;
  type?: string;
  required?: boolean;
  pattern?: any;
  width?: string;
  register: UseFormRegister<any>;
  errors: FieldErrors;
}

const InputField = ({
  label,
  name,
  icon: Icon,
  placeholder,
  type = "text",
  required = true,
  pattern,
  width = "w-full",
  register,
  errors,
}: InputFieldProps) => (
  <div className={width}>
    <label className="block text-xs font-bold text-gray-700 mb-1">
      {label}
    </label>
    <div className="relative">
      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
        <Icon size={16} />
      </div>
      <input
        {...register(name, {
          required: required && "Obrigatório",
          pattern: pattern,
        })}
        type={type}
        className={`block w-full pl-9 px-3 py-2 border rounded-lg outline-none text-sm transition-all ${
          errors[name]
            ? "border-red-500 focus:ring-red-200 focus:border-red-500"
            : "border-gray-300 focus:ring-blue-500 focus:border-blue-500"
        }`}
        placeholder={placeholder}
      />
    </div>
    {errors[name] && (
      <p className="text-[10px] text-red-500 mt-1 flex items-center gap-1">
        <AlertCircle size={10} /> {String(errors[name]?.message || "Inválido")}
      </p>
    )}
  </div>
);

export function Cadastro() {
  const navigate = useNavigate();
  const [tipoConta, setTipoConta] = useState<"PF" | "PJ">("PF");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm({
    mode: "onChange",
  });

  const handleTrocarAba = (tipo: "PF" | "PJ") => {
    setTipoConta(tipo);
    reset();
  };

  const onSubmit = async (data: any) => {
    setIsLoading(true);
    setError(null);

    try {
      const payload =
        tipoConta === "PF"
          ? {
              nome_completo: data.nome,
              email: data.email,
              cpf: data.documento,
              cnh: data.cnh || "N/A",
              telefone: data.telefone,
              senha_texto_puro: data.senha,
              endereco: {
                cep: data.cep,
                rua: data.rua,
                numero: data.numero,
                bairro: data.bairro,
                cidade: data.cidade,
                estado: data.estado,
                complemento: data.complemento || "",
              },
            }
          : {
              razao_social: data.nome,
              nome_fantasia: data.nome,
              email: data.email,
              cnpj: data.documento,
              telefone: data.telefone,
              senha_texto_puro: data.senha,
              endereco: {
                cep: data.cep,
                rua: data.rua,
                numero: data.numero,
                bairro: data.bairro,
                cidade: data.cidade,
                estado: data.estado,
                complemento: data.complemento || "",
              },
            };

      const endpoint =
        tipoConta === "PF"
          ? "/clientes/pessoas-fisicas"
          : "/clientes/pessoas-juridicas";

      await authApi.post(endpoint, payload);
      navigate("/login");
    } catch (err: any) {
      console.error(err);
      const msg = err.response?.data?.detail || "Erro ao criar conta.";
      setError(Array.isArray(msg) ? msg[0].msg : msg);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex bg-white font-sans h-screen overflow-hidden">
      {/* ESQUERDA: IMAGEM */}
      <div className="hidden lg:block lg:w-5/12 relative h-full">
        <img
          src={imgCadastro}
          alt="Background"
          className="absolute inset-0 w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-blue-900/20" />
      </div>

      {/* DIREITA: FORMULÁRIO */}
      <div className="w-full lg:w-7/12 flex flex-col items-center bg-white h-full overflow-y-auto py-10">
        <div className="w-full max-w-xl px-8">
          <div className="flex flex-col items-center mb-6">
            <Link to="/">
              <img
                src={logoBlue}
                alt="FrotaNext"
                className="h-16 w-auto object-contain mb-2"
              />
            </Link>
            <h2 className="text-2xl font-bold text-[#003366] font-futuristic">
              Crie sua Conta
            </h2>
          </div>

          {/* TABS */}
          <div className="flex p-1 bg-gray-100 rounded-lg mb-6">
            <button
              onClick={() => handleTrocarAba("PF")}
              className={`flex-1 py-2 text-sm font-bold rounded-md transition-all ${
                tipoConta === "PF"
                  ? "bg-[#007bff] text-white shadow"
                  : "text-gray-500 hover:bg-gray-200"
              }`}
            >
              Pessoa Física
            </button>
            <button
              onClick={() => handleTrocarAba("PJ")}
              className={`flex-1 py-2 text-sm font-bold rounded-md transition-all ${
                tipoConta === "PJ"
                  ? "bg-[#007bff] text-white shadow"
                  : "text-gray-500 hover:bg-gray-200"
              }`}
            >
              Pessoa Jurídica
            </button>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border-l-4 border-red-500 text-red-700 text-xs rounded font-medium">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            {/* SEÇÃO 1: DADOS DE ACESSO */}
            <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider border-b pb-1">
              Dados de Acesso
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <InputField
                register={register}
                errors={errors}
                label={tipoConta === "PF" ? "Nome Completo" : "Razão Social"}
                name="nome"
                icon={tipoConta === "PF" ? User : Briefcase}
                placeholder="Nome"
              />
              <InputField
                register={register}
                errors={errors}
                label={tipoConta === "PF" ? "CPF" : "CNPJ"}
                name="documento"
                icon={FileText}
                placeholder="Apenas números"
              />

              <InputField
                register={register}
                errors={errors}
                label="E-mail"
                name="email"
                icon={Mail}
                placeholder="seu@email.com"
                type="email"
                pattern={{ value: /^\S+@\S+$/i, message: "E-mail inválido" }}
              />

              <InputField
                register={register}
                errors={errors}
                label="Senha"
                name="senha"
                icon={Lock}
                placeholder="Mínimo 8 caracteres"
                type="password"
                pattern={{ value: /^.{8,}$/, message: "Mínimo 8 caracteres" }}
              />

              <InputField
                register={register}
                errors={errors}
                label="Telefone"
                name="telefone"
                icon={Phone}
                placeholder="(00) 00000-0000"
              />

              {tipoConta === "PF" && (
                <InputField
                  register={register}
                  errors={errors}
                  label="CNH"
                  name="cnh"
                  icon={Truck}
                  placeholder="Nº da CNH"
                />
              )}
            </div>

            {/* SEÇÃO 2: ENDEREÇO */}
            <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider border-b pb-1 mt-4">
              Endereço
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="md:col-span-1">
                <InputField
                  register={register}
                  errors={errors}
                  label="CEP"
                  name="cep"
                  icon={MapPin}
                  placeholder="00000-000"
                />
              </div>
              <div className="md:col-span-2">
                <InputField
                  register={register}
                  errors={errors}
                  label="Rua"
                  name="rua"
                  icon={MapPin}
                  placeholder="Nome da Rua"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="col-span-1">
                <InputField
                  register={register}
                  errors={errors}
                  label="Número"
                  name="numero"
                  icon={MapPin}
                  placeholder="123"
                />
              </div>
              <div className="col-span-1">
                <InputField
                  register={register}
                  errors={errors}
                  label="Comp."
                  name="complemento"
                  icon={MapPin}
                  placeholder="Apto"
                  required={false}
                />
              </div>
              <div className="col-span-2 md:col-span-2">
                <InputField
                  register={register}
                  errors={errors}
                  label="Bairro"
                  name="bairro"
                  icon={MapPin}
                  placeholder="Bairro"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <InputField
                register={register}
                errors={errors}
                label="Cidade"
                name="cidade"
                icon={MapPin}
                placeholder="Cidade"
              />
              <InputField
                register={register}
                errors={errors}
                label="Estado (UF)"
                name="estado"
                icon={MapPin}
                placeholder="UF"
                pattern={{ value: /^[A-Za-z]{2}$/, message: "2 letras" }}
              />
            </div>

            {/* BOTÃO CADASTRAR */}
            <div className="mt-6">
              <button
                type="submit"
                disabled={isLoading}
                className={`w-full py-3 rounded-lg shadow-lg text-white font-bold font-futuristic transition-all transform hover:-translate-y-0.5 ${
                  isLoading
                    ? "bg-gray-300 cursor-not-allowed"
                    : "bg-[#007bff] hover:bg-[#0056b3]"
                }`}
              >
                {isLoading ? (
                  <Loader2 className="animate-spin mx-auto" />
                ) : (
                  "CADASTRAR"
                )}
              </button>
            </div>
          </form>

          <div className="mt-6 text-center text-sm pb-8">
            <span className="text-gray-600">Já tem uma conta? </span>
            <Link
              to="/login"
              className="font-bold text-[#007bff] hover:underline"
            >
              Faça Login
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
