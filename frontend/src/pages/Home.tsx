import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowRight } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 flex flex-col items-center justify-center text-center px-6 py-12">
      {/* 🔹 Logo + Nombre */}
      <div className="mb-10">
        <img
          src="/logo.png"
          alt="Logo CivIA"
          className="w-24 h-24 mx-auto mb-3 drop-shadow-md"
        />
        <h1 className="text-4xl font-extrabold tracking-tight text-gray-900">
          Civ<span className="text-[#B40000]">IA</span>
        </h1>
        <p className="text-gray-600 text-lg mt-1">
          Sistema de Análisis Inteligente SENA
        </p>
      </div>

      {/* 🔹 Tarjeta central con información */}
      <Card className="max-w-xl w-full bg-white/90 backdrop-blur-sm shadow-lg border border-gray-200 rounded-2xl mb-10">
        <CardHeader>
          <CardTitle className="text-[#B40000] uppercase text-sm tracking-wider">
            Desarrollado por
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Autoras */}
          <div className="text-gray-800 font-medium">
            <p>Emilia Gallo Alzate</p>
            <p>María Ximena Marín Delgado</p>
          </div>

          {/* QR */}
          <div className="flex flex-col items-center justify-center mt-6">
            <p className="text-sm text-gray-600 mb-2">
              📎 Escanea este código para acceder a la documentación
            </p>
            <div className="bg-gray-100 border border-dashed border-gray-400 rounded-xl w-40 h-40 flex items-center justify-center">
              <img
                src="/qr-docu.png"
                alt="QR de documentación"
                className="w-32 h-32 object-contain opacity-90"
              />
            </div>
          </div>

          {/* Descripción */}
          <div className="mt-6 text-sm text-gray-700 leading-relaxed">
            <p>
              <strong>CivIA</strong> es una herramienta que analiza información
              social y emocional proveniente de comunidades locales. Usa
              inteligencia artificial para detectar patrones, medir impacto
              social y ofrecer recomendaciones a organizaciones sociales y del
              sector público.
            </p>
          </div>
        </CardContent>
      </Card>

      {/* 🔹 Botón de acceso */}
      <Button
        onClick={() => navigate("/dashboard")}
        size="lg"
        className="bg-[#B40000] hover:bg-red-700 text-white font-semibold text-base px-8 py-6 rounded-full flex items-center gap-2 shadow-md"
      >
        🚀 Entrar a la Plataforma <ArrowRight className="w-4 h-4" />
      </Button>

      {/* 🔹 Footer */}
      <footer className="mt-12 text-xs text-gray-500">
        © 2025 CivIA | Proyecto desarrollado en el marco de SENASOFT
      </footer>
    </div>
  );
}
