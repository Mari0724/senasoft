import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowRight } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-gray-50 to-gray-100 text-center px-6">
      {/* 🔹 Contenedor general (centrado en pantalla) */}
      <div className="max-w-5xl w-full grid grid-cols-2 gap-12 items-center">
        {/* 🔸 Columna izquierda - Logo y texto */}
        <div className="flex flex-col items-center justify-center space-y-5">
          <img
            src="/logo.png"
            alt="Logo CivIA"
            className="w-28 h-28 mb-2 drop-shadow-md"
          />
          <h1 className="text-5xl font-extrabold tracking-tight text-gray-900">
            Civ<span className="text-[#B40000]">IA</span>
          </h1>
          <p className="text-gray-600 text-lg font-medium -mt-2">
            Sistema de Análisis Inteligente SENA
          </p>

          <div className="text-gray-800 font-medium text-sm">
            <p className="uppercase text-[#B40000] font-semibold text-xs mb-1 tracking-widest">
              Desarrollado por
            </p>
            <p>Emilia Gallo Alzate</p>
            <p>María Ximena Marín Delgado</p>
          </div>

          <Button
            onClick={() => navigate("/dashboard")}
            size="lg"
            className="mt-4 bg-[#B40000] hover:bg-red-700 text-white font-semibold text-base px-8 py-6 rounded-full flex items-center gap-2 shadow-md"
          >
            🚀 Entrar a la Plataforma <ArrowRight className="w-4 h-4" />
          </Button>
        </div>

        {/* 🔸 Columna derecha - QR y descripción */}
        <Card className="bg-white/90 backdrop-blur-sm shadow-md border border-gray-200 rounded-2xl h-[430px] flex flex-col justify-center">
          <CardHeader className="pb-3">
            <CardTitle className="text-[#B40000] text-sm font-semibold tracking-wider uppercase">
              Documentación del Proyecto
            </CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col items-center justify-center space-y-4">
            {/* QR */}
            <div className="bg-gray-100 border border-dashed border-gray-400 rounded-xl w-40 h-40 flex items-center justify-center">
              <img
                src="/qr-docu.png"
                alt="QR de documentación"
                className="w-32 h-32 object-contain opacity-90"
              />
            </div>
            {/* Descripción */}
            <p className="text-gray-700 text-sm leading-relaxed max-w-sm">
              <strong>CivIA</strong> es una herramienta que analiza información social y emocional 
              proveniente de comunidades locales. Usa inteligencia artificial para detectar patrones, 
              medir impacto social y ofrecer recomendaciones automatizadas a organizaciones sociales 
              y del sector público.
            </p>
          </CardContent>
        </Card>
      </div>

      {/* 🔹 Footer discreto */}
      <footer className="absolute bottom-4 text-xs text-gray-500">
        © 2025 CivIA — Proyecto desarrollado en el marco de SENASOFT
      </footer>
    </div>
  );
}
