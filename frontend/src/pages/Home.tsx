import { useState } from "react";
import { Brain, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();
  const [showQR, setShowQR] = useState(false);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-gray-50 to-gray-100 text-center px-12">
      {/* 🔹 Contenedor principal más ancho y balanceado */}
      <div className="max-w-7xl w-full grid grid-cols-2 gap-20 items-center">
        {/* 🔸 Columna izquierda — Logo y autores */}
        <div className="flex flex-col items-center justify-center space-y-10">
          {/* Logo institucional */}
          <div className="flex flex-col items-center gap-4">
            <div className="flex items-center gap-4">
              <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-[#B40000] shadow-lg">
                <Brain className="h-10 w-10 text-white" />
              </div>
              <div className="text-left">
                <h1 className="text-6xl font-extrabold text-gray-900">
                  Civ<span className="text-[#B40000]">IA</span>
                </h1>
                <p className="text-lg text-gray-600 -mt-1">SENA/Soft 2025</p>
              </div>
            </div>

            <p className="text-gray-500 text-base mt-3">
              Sistema de Análisis Inteligente SENA
            </p>
          </div>

          {/* Autoras */}
          <div className="text-gray-800 font-medium text-base mt-2">
            <p className="uppercase text-[#B40000] font-semibold text-xs mb-1 tracking-widest">
              Desarrollado por
            </p>
            <p>Emilia Gallo Alzate</p>
            <p>María Ximena Marín Delgado</p>
          </div>

          {/* Botón de acceso */}
          <Button
            onClick={() => navigate("/dashboard")}
            size="lg"
            className="mt-6 bg-[#B40000] hover:bg-red-700 text-white text-lg font-semibold px-10 py-7 rounded-full flex items-center gap-3 shadow-lg transition-transform hover:scale-105"
          >
            Entrar a la Plataforma <ArrowRight className="w-5 h-5" />
          </Button>
        </div>

        {/* 🔸 Columna derecha — QR y descripción */}
        <Card className="bg-white/95 backdrop-blur-md shadow-xl border border-gray-200 rounded-3xl h-[480px] flex flex-col justify-center">
          <CardHeader className="pb-3">
            <CardTitle className="text-[#B40000] text-lg font-semibold tracking-wider uppercase">
              Documentación del Proyecto
            </CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col items-center justify-center space-y-6">
            {/* Interacción para mostrar QR */}
            <div className="flex flex-col items-center justify-center mt-2 space-y-3">
              {!showQR ? (
                <>
                  <p className="text-base text-gray-600">
                    Escanea el código de documentación
                  </p>
                  <Button
                    variant="outline"
                    onClick={() => setShowQR(true)}
                    className="border-[#B40000] text-[#B40000] hover:bg-[#B40000] hover:text-white transition-all text-base px-6 py-3"
                  >
                    Mostrar QR
                  </Button>
                </>
              ) : (
                <div className="bg-gray-100 border border-dashed border-gray-400 rounded-2xl w-48 h-48 flex items-center justify-center shadow-sm">
                  <img
                    src="/CivIA.png"
                    alt="QR de documentación"
                    className="w-40 h-40 object-contain opacity-90"
                  />
                </div>
              )}
            </div>
            {/* Descripción */}
            <p className="text-gray-700 text-base leading-relaxed max-w-md text-center">
              <strong>CivIA</strong> es una herramienta que analiza información social y emocional
              proveniente de comunidades locales. Utiliza inteligencia artificial para detectar
              patrones, medir el impacto social y ofrecer recomendaciones automatizadas a
              organizaciones del sector público y social.
            </p>
          </CardContent>
        </Card>
      </div>

      {/* 🔹 Footer */}
      <footer className="absolute bottom-5 text-sm text-gray-500">
        © 2025 CivIA — Proyecto desarrollado en el marco de SENASOFT
      </footer>
    </div>
  );
}
