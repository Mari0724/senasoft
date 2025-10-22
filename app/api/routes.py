from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import os

# ==============================
# 📦 Importar módulos de aplicación
# ==============================
from app.application.social_module import (
    load_dataset, analyze_social_patterns, compute_social_index
)
from app.application.pipeline import run_pipeline

# ==============================
# ⚙️ Configuración base del router
# ==============================
router = APIRouter(prefix="/api", tags=["Análisis Social"])
DATA_PATH = "data/clean_data.csv"

# Ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Directorio de las plantillas (HTML)
TEMPLATES_DIR = os.path.join(BASE_DIR, "app", "api", "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# ==============================
# 🌍 Endpoints analíticos
# ==============================
@router.get("/patterns")
def get_social_patterns():
    """Obtiene patrones sociales por ciudad."""
    df = load_dataset(DATA_PATH)
    results = analyze_social_patterns(df)
    return results.to_dict(orient="records")


@router.get("/impact")
def get_social_index():
    """Calcula el índice social consolidado."""
    df = load_dataset(DATA_PATH)
    summary = compute_social_index(df)
    return summary.to_dict(orient="records")


# ==============================
# 🚀 Ejecutar pipeline completo
# ==============================
@router.post("/run_pipeline")
def trigger_pipeline():
    """
    Ejecuta todo el flujo de ComuniMind:
    - Limpieza de datos (ETL)
    - Análisis de temas y sentimientos (NLP)
    - Cálculo de impacto social
    - Generación de visualizaciones
    """
    try:
        print("🚀 Ejecutando pipeline completo desde API...")
        run_pipeline()

        response = {
            "status": "success",
            "message": "Pipeline ejecutado correctamente.",
            "results": {
                "data_folder": "data/",
                "dashboard_images": "app/infrastructure/visuals/"
            }
        }
        return JSONResponse(content=response, status_code=200)

    except Exception as e:
        response = {
            "status": "error",
            "message": f"Ocurrió un error durante la ejecución del pipeline: {str(e)}"
        }
        return JSONResponse(content=response, status_code=500)


# ==============================
# 🖥️ Dashboard visual
# ==============================
@router.get("/dashboard", response_class=HTMLResponse)
def show_dashboard(request: Request):
    """Renderiza el dashboard visual de ComuniMind."""
    return templates.TemplateResponse("dashboard.html", {"request": request})
