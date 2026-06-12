import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useForm, type SubmitHandler } from "react-hook-form";
import { Mail, Lock, Loader2 } from "lucide-react";
import { useAuth } from "../../hooks/useAuth";
import { authService } from "../../services/authService"; 

import imgLoginSide from "../../assets/login-bg.png";
import logoBlue from "../../assets/logo-blue.png";

interface LoginInputs {
  email: string;
  password: string;
}

export function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginInputs>();

  const onSubmit: SubmitHandler<LoginInputs> = async (data) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await authService.loginCliente(data.email, data.password);

      login(response.access_token);
      navigate("/dashboard");
      
    } catch (err: any) {
      console.error(err);
      
      if (err.response && err.response.data && err.response.data.mensagem) {
         setError(err.response.data.mensagem);
      } else {
         setError("Acesso negado. Verifique as suas credenciais.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex bg-white font-sans h-screen overflow-hidden">
      
      {/* LADO ESQUERDO: IMAGEM */}
      <div className="hidden lg:block lg:w-6/12 relative h-full">
        <img
          src={imgLoginSide}
          alt="Login Background"
          className="absolute inset-0 w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black/30" />
      </div>

      {/* LADO DIREITO: FORMULÁRIO */}
      <div className="w-full lg:w-6/12 flex flex-col justify-center items-center p-8 md:p-20 bg-slate-50 h-full">
        <div className="w-full max-w-md space-y-8">
          
          <div className="flex flex-col items-center">
            <Link to="/">
              <img src={logoBlue} alt="FrotaNext" className="h-44 w-auto object-contain mb-6" />
            </Link>
            <h2 className="text-3xl font-extrabold text-slate-800 font-futuristic tracking-wide">
              Bem-vindo de volta
            </h2>
            <p className="mt-2 text-sm text-slate-500">
              Faça login para gerir as suas reservas.
            </p>
          </div>

          {error && (
            <div className="p-4 bg-red-50 border-l-4 border-red-500 text-red-700 text-sm rounded">
              <p className="font-bold">Erro</p>
              <p>{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div>
              <label className="block text-sm font-bold text-slate-700 mb-1">E-mail</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  {...register("email", { required: "E-mail obrigatório" })}
                  type="email"
                  className="block w-full pl-10 px-4 py-3 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-slate-900 placeholder-gray-400"
                  placeholder="seu@email.com"
                />
              </div>
              {errors.email && <p className="mt-1 text-sm text-red-500">{errors.email.message}</p>}
            </div>

            <div>
              <label className="block text-sm font-bold text-slate-700 mb-1">Senha</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  {...register("password", { required: "Senha obrigatória" })}
                  type="password"
                  className="block w-full pl-10 px-4 py-3 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-slate-900 placeholder-gray-400"
                  placeholder="••••••••"
                />
              </div>
              <div className="flex justify-end mt-1">
                <a href="#" className="text-xs text-blue-600 hover:text-blue-800 font-semibold hover:underline">
                  Esqueci minha senha
                </a>
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg shadow-md text-lg font-bold text-white bg-[#007bff] hover:bg-[#0056b3] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all transform hover:-translate-y-0.5 disabled:opacity-50 font-futuristic uppercase tracking-wide"
            >
              {isLoading ? (
                <><Loader2 className="animate-spin mr-2" /> Entrando...</>
              ) : ("ENTRAR")}
            </button>
          </form>

          <div className="mt-6 text-center text-sm">
            <span className="text-gray-600">Não tem uma conta? </span>
            <Link to="/cadastro" className="font-bold text-[#007bff] hover:text-[#0056b3] hover:underline">
              Cadastre-se
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}