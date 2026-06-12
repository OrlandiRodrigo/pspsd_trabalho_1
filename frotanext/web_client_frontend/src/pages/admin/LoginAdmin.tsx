import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useForm, type SubmitHandler } from 'react-hook-form';
import { Mail, Lock, Loader2, ShieldAlert } from 'lucide-react';
import { authService } from '../../services/authService';
import { useAuth } from '../../hooks/useAuth';

import imgAdminSide from '../../assets/login-admin-bg.png'; 
import logoBlue from '../../assets/logo-fn.png';

interface LoginInputs {
  email: string;
  password: string;
}

export function LoginAdmin() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm<LoginInputs>();

  const onSubmit: SubmitHandler<LoginInputs> = async (data) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await authService.login(data.email, data.password);

      login(response.access_token);
      
      navigate('/admin/dashboard');
    } catch (err) {
      console.error(err);
      setError('Acesso negado. Verifique as suas credenciais.');
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="min-h-screen flex bg-slate-900 font-sans h-screen overflow-hidden">
      
      {/* LADO ESQUERDO: IMAGEM */}
      <div className="hidden lg:block lg:w-7/12 relative h-full">
        <img
          src={imgAdminSide}
          alt="Admin Background"
          className="absolute inset-0 w-full h-full object-cover brightness-110"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-slate-900/90 via-transparent to-transparent" />
        
        <div className="absolute bottom-12 left-12 text-white max-w-md">
           <h2 className="text-4xl font-bold font-futuristic mb-2 text-blue-100">Portal Administrativo</h2>
        </div>
      </div>

      {/* LADO DIREITO: FORMULÁRIO */}
      <div className="w-full lg:w-5/12 flex flex-col justify-center items-center p-8 md:p-20 bg-slate-900 h-full border-l border-slate-800 shadow-2xl relative z-10">
        <div className="w-full max-w-sm space-y-8">
          
          <div className="flex flex-col items-center">
            <Link to="/">
              <img 
                src={logoBlue} 
                alt="FrotaNext" 
                className="h-40 w-auto object-contain mb-8 drop-shadow-[0_0_15px_rgba(59,130,246,0.5)]" 
              />
            </Link>
            <h2 className="text-2xl font-bold text-white font-futuristic tracking-wider flex items-center gap-2">
               <ShieldAlert className="text-blue-500" /> Acesso Restrito
            </h2>
          </div>

          {error && (
            <div className="p-4 bg-red-900/30 border-l-4 border-red-500 text-red-200 text-sm rounded">
              <p className="font-bold">Falha na Autenticação</p>
              <p>{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div>
              <label className="block text-xs font-bold text-slate-400 mb-1 uppercase">E-mail Corporativo</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail className="h-5 w-5 text-slate-500" />
                </div>
                <input
                  {...register("email", { required: "E-mail obrigatório" })}
                  type="email"
                  className="block w-full pl-10 px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-white placeholder-slate-500 outline-none transition-all"
                  placeholder="admin@frotanext.com"
                />
              </div>
              {errors.email && <p className="mt-1 text-xs text-red-400">{errors.email.message}</p>}
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-400 mb-1 uppercase">Senha</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-slate-500" />
                </div>
                <input
                  {...register("password", { required: "Senha obrigatória" })}
                  type="password"
                  className="block w-full pl-10 px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-white placeholder-slate-500 outline-none transition-all"
                  placeholder="••••••••"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg shadow-lg text-sm font-bold text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all disabled:opacity-50 font-futuristic uppercase tracking-widest"
            >
              {isLoading ? <Loader2 className="animate-spin mr-2" /> : "ACESSAR SISTEMA"}
            </button>
          </form>

          <div className="text-center">
            <Link to="/login" className="text-xs text-slate-500 hover:text-white transition-colors">
              Voltar para Login de Cliente
            </Link>
          </div>

        </div>
      </div>
    </div>
  );
}