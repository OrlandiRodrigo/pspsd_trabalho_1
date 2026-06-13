import imgFooter from '../../assets/footer-bg.png'; 
import logoFn from '../../assets/logo-fn.png'; 

export function Footer() {
  return (
    <footer className="w-full mt-12 relative h-64 overflow-hidden">
      
      {/* Imagem de Fundo */}
      <img 
        src={imgFooter} 
        className="w-full h-full object-cover opacity-90" 
        alt="Estrada ao pôr do sol" 
      />
      
      {/* Overlay Escuro + Logo Centralizado */}
      <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
        
        {/* LOGO */}
        <img 
            src={logoFn} 
            alt="Logo FrotaNext" 
            className="h-32 w-auto object-contain opacity-90 hover:opacity-100 transition-opacity drop-shadow-lg" 
        />

      </div>
      
      {/* Copyright */}
      <div className="absolute bottom-2 w-full text-center">
         <p className="text-[10px] text-white/50">© 2025 FrotaNext. Todos os direitos reservados.</p>
      </div>

    </footer>
  );
}