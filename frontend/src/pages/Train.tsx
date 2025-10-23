import { useState } from "react";
import { Brain, Play, CheckCircle2, AlertCircle, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { apiService } from "@/services/api";
import { Loader } from "@/components/Loader";
import { toast } from "sonner";

export default function Train() {
  const [isTraining, setIsTraining] = useState(false);
  const [trainStatus, setTrainStatus] = useState<"idle" | "success" | "error">("idle");
  const [kpis, setKpis] = useState({
    total_registros: 0,
    sentimiento_positivo: 0,
    categorias_activas: 0,
    temas_identificados: 0,
  });

  // 🔹 Ejecuta el pipeline y luego actualiza los KPIs
  const handleTrain = async () => {
    setIsTraining(true);
    setTrainStatus("idle");

    try {
      const response = await apiService.runPipeline();
      setTrainStatus("success");

      toast.success("Entrenamiento completado", {
        description: response.message || "El modelo se ha entrenado exitosamente",
      });

      // ✅ Al finalizar, obtener KPIs actualizados
      const kpiData = await apiService.getKpis();
      setKpis(kpiData);

    } catch (error) {
      setTrainStatus("error");
      toast.error("Error en el entrenamiento", {
        description: error instanceof Error ? error.message : "Ocurrió un error desconocido",
      });
    } finally {
      setIsTraining(false);
    }
  };

  // 🔁 Permitir refrescar métricas manualmente
  const handleRefreshKpis = async () => {
    try {
      const data = await apiService.getKpis();
      setKpis(data);
      toast.success("Indicadores actualizados");
    } catch {
      toast.error("No se pudieron actualizar los indicadores");
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-foreground">Entrenar IA</h1>
        <p className="text-muted-foreground mt-2">
          Ejecuta el pipeline de entrenamiento del modelo de análisis de sentimientos
        </p>
      </div>

      {/* Training Card */}
      <Card className="glass-card">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Brain className="h-5 w-5 text-primary" />
            Pipeline de Entrenamiento
          </CardTitle>
          <CardDescription>
            Este proceso entrena el modelo con los datos más recientes y actualiza las predicciones
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Status indicator */}
          {trainStatus === "success" && (
            <div className="flex items-center gap-2 rounded-lg bg-green-50 p-4 text-green-800 border border-green-200">
              <CheckCircle2 className="h-5 w-5" />
              <span className="font-medium">Entrenamiento completado exitosamente</span>
            </div>
          )}

          {trainStatus === "error" && (
            <div className="flex items-center gap-2 rounded-lg bg-red-50 p-4 text-red-800 border border-red-200">
              <AlertCircle className="h-5 w-5" />
              <span className="font-medium">Error durante el entrenamiento</span>
            </div>
          )}

          {/* Action button */}
          {isTraining ? (
            <Loader text="Entrenando modelo..." size="lg" />
          ) : (
            <Button
              onClick={handleTrain}
              size="lg"
              className="w-full"
              disabled={isTraining}
            >
              <Play className="mr-2 h-5 w-5" />
              Iniciar Entrenamiento
            </Button>
          )}

          {/* Info */}
          <div className="rounded-lg bg-muted p-4 space-y-2">
            <h4 className="font-medium text-sm">Proceso de entrenamiento:</h4>
            <ul className="text-sm text-muted-foreground space-y-1 list-disc list-inside">
              <li>Carga y preprocesamiento de datos</li>
              <li>Entrenamiento del modelo de IA</li>
              <li>Validación y evaluación de métricas</li>
              <li>Generación de gráficos y visualizaciones disponible en la pestaña dashboard</li>
            </ul>
          </div>
        </CardContent>
      </Card>

      {/* KPI Cards */}
      <div className="flex items-center justify-between mt-8">
        <h2 className="text-xl font-semibold">Indicadores del modelo</h2>
        <Button
          onClick={handleRefreshKpis}
          size="sm"
          className="gap-2 text-sm"
          variant="outline"
        >
          <RefreshCw className="h-4 w-4" /> Actualizar
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium">Datos procesados</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold text-primary">{kpis.total_registros.toLocaleString()}</p>
            <p className="text-xs text-muted-foreground">registros analizados</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium">Sentimiento Positivo</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold text-green-600">{kpis.sentimiento_positivo.toFixed(1)}%</p>
            <p className="text-xs text-muted-foreground">promedio detectado</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium">Categorías Activas</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold text-primary">{kpis.categorias_activas}</p>
            <p className="text-xs text-muted-foreground">problemas detectados</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium">Temas Identificados</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold text-primary">{kpis.temas_identificados}</p>
            <p className="text-xs text-muted-foreground">en análisis NLP</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
