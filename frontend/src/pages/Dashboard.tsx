import { useState, useEffect } from "react";
import { MessageSquare } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { apiService } from "@/services/api";
import { Loader } from "@/components/Loader";
import { toast } from "sonner";

const charts = [
  { name: "impacto_por_ciudad.png", title: "Impacto Social por Ciudad" },
  { name: "categorias_urgentes.png", title: "Categorías Urgentes" },
  { name: "internet_vs_urgencia.png", title: "Internet vs Urgencia" },
  { name: "sentimiento_promedio.png", title: "Sentimiento Promedio" },
  { name: "temas_detectados.png", title: "Temas Detectados" },
  { name: "categorias_impacto.png", title: "Categorías de Mayor Impacto" },
  { name: "reportes_por_genero.png", title: "Reportes por Género" },
];

export default function Dashboard() {
  const [explanation, setExplanation] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);
  const [kpis, setKpis] = useState({
    total_registros: 0,
    sentimiento_positivo: 0,
    categorias_activas: 0,
    temas_identificados: 0,
  });

  // 🔹 Cargar KPIs automáticamente al abrir el dashboard
  useEffect(() => {
    const fetchKpis = async () => {
      try {
        const data = await apiService.getKpis();
        setKpis(data);
      } catch (error) {
        console.error("Error cargando KPIs:", error);
        toast.error("No se pudieron cargar los indicadores principales");
      }
    };
    fetchKpis();
  }, []);

  // 💬 Explicación IA
  const handleExplain = async () => {
    setIsLoading(true);
    try {
      const response = await apiService.explainDashboard();
      setExplanation(response.explanation || response.message);
      toast.success("Explicación generada", {
        description: "La IA ha analizado el dashboard exitosamente",
      });
    } catch (error) {
      toast.error("Error al obtener explicación", {
        description: error instanceof Error ? error.message : "Ocurrió un error desconocido",
      });
    } finally {
      setIsLoading(false);
    }
  };

  // =======================
  // 🧠 Render del Dashboard
  // =======================
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
          <p className="text-muted-foreground mt-2">
            Visualización de análisis de sentimientos e impacto social
          </p>
        </div>

        <Button onClick={handleExplain} size="lg" disabled={isLoading} className="gap-2">
          <MessageSquare className="h-5 w-5" />
          {isLoading ? "Analizando..." : "💬 IA, Explícame este panel"}
        </Button>
      </div>

      {/* Charts Grid */}
      <div className="grid gap-6 md:grid-cols-2">
        {charts.map((chart) => (
          <Card key={chart.name} className="glass-card overflow-hidden">
            <CardHeader>
              <CardTitle className="text-base">{chart.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="relative aspect-video w-full bg-muted rounded-lg overflow-hidden">
                <img
                  src={apiService.getChartUrl(chart.name)}
                  alt={chart.title}
                  className="w-full h-full object-contain"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement;
                    target.style.display = "none";
                    const parent = target.parentElement;
                    if (parent) {
                      parent.innerHTML = `
                        <div class="flex items-center justify-center h-full text-muted-foreground">
                          <div class="text-center">
                            <p class="text-sm">Gráfico no disponible</p>
                            <p class="text-xs mt-1">Ejecuta el entrenamiento para generar visualizaciones</p>
                          </div>
                        </div>
                      `;
                    }
                  }}
                />
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* AI Explanation Section */}
      {(explanation || isLoading) && (
        <Card className="glass-card border-primary/20">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <MessageSquare className="h-5 w-5 text-primary" />
              Explicación de la IA
            </CardTitle>
            <CardDescription>
              Análisis generado automáticamente de los datos del dashboard
            </CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <Loader text="Generando explicación..." />
            ) : (
              <div className="prose prose-sm max-w-none">
                <p className="text-foreground whitespace-pre-wrap">{explanation}</p>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Stats Overview (KPIs dinámicos) */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">Total Registros</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold text-primary">
              {kpis.total_registros.toLocaleString()}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">Sentimiento Positivo</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold text-green-600">
              {kpis.sentimiento_positivo.toFixed(1)}%
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">Categorías Activas</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold text-primary">{kpis.categorias_activas}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">Temas Identificados</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold text-primary">{kpis.temas_identificados}</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
