import { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Car, Clock, Truck, Bike } from "lucide-react";
import { Footer } from "../../components/layout/Footer";
import { useAuth } from "../../hooks/useAuth";

import imgFrota from "../../assets/card-frota.png";
import imgEmpresa from "../../assets/card-empresa.png";
import imgApp from "../../assets/card-app.png";

export function Home() {
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      navigate("/dashboard");
    }
  }, [user, navigate]);

  if (user) return null;

  return (
    <div className="min-h-screen bg-white font-sans text-slate-900 flex flex-col">
      {/* 1. TEXTO INICIAL */}
      <div className="w-full bg-white pt-12 pb-8 text-center px-4">
        <h1 className="text-3xl md:text-5xl font-bold text-slate-900 font-futuristic mb-2">
          Sua jornada começa <span className="text-[#003366]">aqui.</span>
        </h1>
        <p className="text-gray-500">
          A melhor experiência em locação de veículos.
        </p>
      </div>

      {/* 2. COMO FUNCIONA (Substituindo os ícones antigos) */}
<section className="bg-slate-900 text-white py-20">
  <div className="max-w-6xl mx-auto px-4">
    <div className="text-center mb-12">
        <h2 className="text-2xl font-bold font-futuristic text-blue-400 mb-2">Como Funciona</h2>
        <p className="text-gray-400">Alugar seu carro nunca foi tão simples.</p>
    </div>

    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
      <div className="hidden md:block absolute top-12 left-[16%] right-[16%] h-0.5 bg-blue-800/50 -z-0"></div>

      {/* Passo 1 */}
      <div className="flex flex-col items-center relative z-10">
        <div className="w-24 h-24 bg-slate-800 rounded-full flex items-center justify-center border-4 border-slate-900 shadow-lg mb-6 group hover:bg-blue-900 transition-colors">
           <Car size={40} className="text-blue-400 group-hover:text-white transition-colors" />
        </div>
        <h3 className="font-bold text-xl mb-2">1. Escolha</h3>
        <p className="text-sm text-gray-400 text-center max-w-[200px]">Navegue pela nossa frota e encontre o veículo ideal para sua necessidade.</p>
      </div>

      {/* Passo 2 */}
      <div className="flex flex-col items-center relative z-10">
        <div className="w-24 h-24 bg-slate-800 rounded-full flex items-center justify-center border-4 border-slate-900 shadow-lg mb-6 group hover:bg-blue-900 transition-colors">
           <Clock size={40} className="text-blue-400 group-hover:text-white transition-colors" />
        </div>
        <h3 className="font-bold text-xl mb-2">2. Reserve</h3>
        <p className="text-sm text-gray-400 text-center max-w-[200px]">Faça seu cadastro em segundos e reserve 100% online, sem burocracia.</p>
      </div>

      {/* Passo 3 */}
      <div className="flex flex-col items-center relative z-10">
        <div className="w-24 h-24 bg-slate-800 rounded-full flex items-center justify-center border-4 border-slate-900 shadow-lg mb-6 group hover:bg-blue-900 transition-colors">
           <Truck size={40} className="text-blue-400 group-hover:text-white transition-colors" />
        </div>
        <h3 className="font-bold text-xl mb-2">3. Dirija</h3>
        <p className="text-sm text-gray-400 text-center max-w-[200px]">Retire o veículo na agência e aproveite!</p>
      </div>

    </div>
  </div>
</section>

      {/* 3. CATEGORIAS */}
      <section className="py-24 max-w-6xl mx-auto px-4">
        <h2 className="text-2xl font-bold mb-16 text-gray-900 font-futuristic uppercase tracking-wider">
          Explore Nossas Categorias
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-16 justify-items-center">
          <Link
            to="/frota?tipo=passeio"
            className="flex flex-col items-center group w-full relative pt-4"
          >
            <span className="absolute top-0 bg-gray-100 px-3 py-1 rounded-md text-[10px] text-gray-500 shadow-sm border border-gray-200">
              Detalhes
            </span>
            <Car
              size={90}
              strokeWidth={1.5}
              className="mb-4 mt-4 text-black group-hover:text-blue-800 transition-colors"
            />
            <span className="font-bold text-lg font-futuristic">
              Carros de Passeio
            </span>
          </Link>
          <Link
            to="/frota?tipo=motocicleta"
            className="flex flex-col items-center group w-full relative pt-4"
          >
            <span className="absolute top-0 bg-gray-100 px-3 py-1 rounded-md text-[10px] text-gray-500 shadow-sm border border-gray-200">
              Detalhes
            </span>
            <Bike
              size={90}
              strokeWidth={1.5}
              className="mb-4 mt-4 text-black group-hover:text-blue-800 transition-colors"
            />
            <span className="font-bold text-lg font-futuristic">
              Motocicletas
            </span>
          </Link>
          <Link
            to="/frota?tipo=utilitario"
            className="flex flex-col items-center group w-full relative pt-4"
          >
            <span className="absolute top-0 bg-gray-100 px-3 py-1 rounded-md text-[10px] text-gray-500 shadow-sm border border-gray-200">
              Detalhes
            </span>
            <Truck
              size={90}
              strokeWidth={1.5}
              className="mb-4 mt-4 text-black group-hover:text-blue-800 transition-colors"
            />
            <span className="font-bold text-lg font-futuristic">
              Utilitários
            </span>
          </Link>
        </div>
      </section>

      {/* 4. CARDS */}
      <section className="py-16 max-w-7xl mx-auto px-4 mb-12">
        <h2 className="text-2xl font-bold mb-10 text-gray-900 font-futuristic">
          Por que escolher a FrotaNext?
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="group">
            <div className="rounded-3xl overflow-hidden mb-4 shadow-lg border border-gray-100">
              <img
                src={imgFrota}
                alt="Frota"
                style={{ height: "250px", width: "100%", objectFit: "cover" }}
                className="hover:scale-105 transition-transform duration-500"
              />
            </div>
            <h3 className="font-bold text-xl mb-1 font-futuristic">
              Frota Completa
            </h3>
            <p className="text-sm text-gray-600">
              Carros, motos e utilitários.
            </p>
          </div>
          <div className="group">
            <div className="rounded-3xl overflow-hidden mb-4 shadow-lg border border-gray-100">
              <img
                src={imgEmpresa}
                alt="Empresa"
                style={{ height: "250px", width: "100%", objectFit: "cover" }}
                className="hover:scale-105 transition-transform duration-500"
              />
            </div>
            <h3 className="font-bold text-xl mb-1 font-futuristic">
              Para Você e Sua Empresa
            </h3>
            <p className="text-sm text-gray-600">
              Planos flexíveis e gestão facilitada.
            </p>
          </div>
          <div className="group">
            <div className="rounded-3xl overflow-hidden mb-4 shadow-lg border border-gray-100">
              <img
                src={imgApp}
                alt="App"
                style={{
                  height: "250px",
                  width: "100%",
                  objectFit: "cover",
                  objectPosition: "top",
                }}
                className="hover:scale-105 transition-transform duration-500"
              />
            </div>
            <h3 className="font-bold text-xl mb-1 font-futuristic">
              Reserva Rápida
            </h3>
            <p className="text-sm text-gray-600">
              Alugue 100% online em 3 minutos.
            </p>
          </div>
        </div>
      </section>

      {/* 5. FOOTER */}
      <Footer />
    </div>
  );
}
