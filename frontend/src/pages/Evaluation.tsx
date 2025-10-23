import { useState, useEffect } from "react";
import { LineChart, TrendingUp, Target, Zap } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { apiService, MetricsResponse } from "@/services/api";
import { Loader } from "@/components/Loader";
import { toast } from "sonner";

export default function Evaluation() {
  const [metrics, setMetrics] = useState<MetricsResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const loadMetrics = async () => {
    setIsLoading(true);
    try {
      const data = await apiService.getMetrics();
      setMetrics(data);
      toast.success("Métricas actualizadas");
    } catch (error) {
      toast.error("Error al cargar métricas", {
        description: error instanceof Error ? error.message : "Ocurrió un error desconocido",
      });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadMetrics();
  }, []);

  const formatPercentage = (value: number | undefined) => {
    if (value === undefined) return "N/A";
    return `${(value * 100).toFixed(2)}%`;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Evaluación del Modelo</h1>
          <p className="text-muted-foreground mt-2">
            Métricas de rendimiento y precisión del modelo de IA
          </p>
        </div>

        <Button onClick={loadMetrics} disabled={isLoading}>
          <TrendingUp className="mr-2 h-4 w-4" />
          Actualizar Métricas
        </Button>
      </div>

      {/* Metrics Cards */}
      {isLoading ? (
        <Card className="glass-card">
          <CardContent className="py-12">
            <Loader text="Cargando métricas..." size="lg" />
          </CardContent>
        </Card>
      ) : metrics ? (
        <>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Card className="glass-card">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">Precisión</CardTitle>
                <Target className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-primary">
                  {formatPercentage(metrics.accuracy)}
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  Accuracy del modelo
                </p>
              </CardContent>
            </Card>

            <Card className="glass-card">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">Precisión</CardTitle>
                <Zap className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-primary">
                  {formatPercentage(metrics.precision)}
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  Precision score
                </p>
              </CardContent>
            </Card>

            <Card className="glass-card">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">Recall</CardTitle>
                <LineChart className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-primary">
                  {formatPercentage(metrics.recall)}
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  Recall score
                </p>
              </CardContent>
            </Card>

            <Card className="glass-card">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">F1-Score</CardTitle>
                <TrendingUp className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-primary">
                  {formatPercentage(metrics.f1_score)}
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  F1 score
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Detailed Metrics */}
          <Card className="glass-card">
            <CardHeader>
              <CardTitle>Métricas Detalladas</CardTitle>
              <CardDescription>
                Información completa sobre el rendimiento del modelo
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {Object.entries(metrics).map(([key, value]) => (
                  <div key={key} className="flex items-center justify-between border-b border-border pb-2 last:border-0 last:pb-0">
                    <span className="text-sm font-medium capitalize">
                      {key.replace(/_/g, " ")}
                    </span>
                    <span className="text-sm text-muted-foreground">
                      {typeof value === "number" ? formatPercentage(value) : String(value)}
                    </span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Performance Info */}
          <Card className="glass-card border-primary/20">
            <CardHeader>
              <CardTitle className="text-base">Interpretación de Métricas</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div>
                <h4 className="font-medium text-sm mb-1">Accuracy (Precisión)</h4>
                <p className="text-sm text-muted-foreground">
                  Porcentaje de predicciones correctas sobre el total de predicciones.
                </p>
              </div>
              <div>
                <h4 className="font-medium text-sm mb-1">Precision</h4>
                <p className="text-sm text-muted-foreground">
                  De las predicciones positivas, cuántas fueron correctas.
                </p>
              </div>
              <div>
                <h4 className="font-medium text-sm mb-1">Recall (Sensibilidad)</h4>
                <p className="text-sm text-muted-foreground">
                  De todos los casos positivos reales, cuántos fueron identificados.
                </p>
              </div>
              <div>
                <h4 className="font-medium text-sm mb-1">F1-Score</h4>
                <p className="text-sm text-muted-foreground">
                  Media armónica entre Precision y Recall, balance global del modelo.
                </p>
              </div>
            </CardContent>
          </Card>
        </>
      ) : (
        <Card className="glass-card">
          <CardContent className="py-12 text-center">
            <p className="text-muted-foreground">
              No hay métricas disponibles. Ejecuta el entrenamiento primero.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
