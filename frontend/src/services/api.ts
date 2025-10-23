// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export interface TrainResponse {
  status: string;
  message: string;
}

export interface MetricsResponse {
  accuracy?: number;
  precision?: number;
  recall?: number;
  f1_score?: number;
  [key: string]: any;
}

export interface ExplainResponse {
  explanation?: string;
  message?: string;
}

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  async runPipeline(): Promise<TrainResponse> {
    const response = await fetch(`${this.baseUrl}/api/run_pipeline`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Error al entrenar: ${response.statusText}`);
    }

    return response.json();
  }

  async getMetrics(): Promise<MetricsResponse> {
    const response = await fetch(`${this.baseUrl}/api/metrics`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Error al obtener métricas: ${response.statusText}`);
    }

    return response.json();
  }

  async explainDashboard(): Promise<ExplainResponse> {
    const response = await fetch(`${this.baseUrl}/api/explain`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Error al obtener explicación: ${response.statusText}`);
    }

    return response.json();
  }

  getChartUrl(chartName: string): string {
    return `${this.baseUrl}/static/${chartName}`;
  }
}

export const apiService = new ApiService();
