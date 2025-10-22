import os
import shutil
import pandas as pd
from app.application.data_service import run_etl
from app.application.nlp_service import ejecutar_nlp_pipeline
from app.application.social_module import load_dataset, compute_social_index
from app.application.visual_service import generar_todos_los_graficos

# ==============================
# RUTAS BASE
# ==============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
INFRA_VISUALS = os.path.join(BASE_DIR, "app", "infrastructure", "visuals")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(INFRA_VISUALS, exist_ok=True)

# ==============================
# PIPELINE COMPLETO
# ==============================
def run_pipeline():
    print("🔄 Iniciando pipeline completo de ComuniMind...\n")

    # -------------------------------------------------
    # 1 ETL: limpieza y normalización de datos
    # -------------------------------------------------
    print("Paso 1: Ejecutando limpieza de datos (ETL)...")
    run_etl()

    # -------------------------------------------------
    # 2 Análisis de temas y sentimientos (NLP)
    # -------------------------------------------------
    print("\nPaso 2: Analizando temas y sentimientos...")
    ejecutar_nlp_pipeline()

    # -------------------------------------------------
    # 3 Análisis de vulnerabilidad e impacto social
    # -------------------------------------------------
    print("\nPaso 3: Calculando vulnerabilidad e impacto social...")
    df = load_dataset(os.path.join(DATA_DIR, "clean_data.csv"))
    social_df = compute_social_index(df)
    impact_path = os.path.join(DATA_DIR, "impact_social.csv")
    social_df.to_csv(impact_path, sep=";", encoding="utf-8", index=False)
    print(f"Archivo guardado: {impact_path}")

    # -------------------------------------------------
    # 4 Integrar resultados NLP + Social
    # -------------------------------------------------
    print("\n Paso 4: Integrando resultados finales...")
    nlp_df = pd.read_csv(os.path.join(DATA_DIR, "themes_nlp.csv"), sep=";")

    merged = pd.merge(social_df, nlp_df, on="ciudad", how="left")
    merged_path = os.path.join(DATA_DIR, "final_results.csv")
    merged.to_csv(merged_path, sep=";", encoding="utf-8", index=False)
    print(f" Archivo unificado generado: {merged_path}")

    # -------------------------------------------------
    # 5 Generar visualizaciones finales
    # -------------------------------------------------
    print("\n Paso 5: Generando visualizaciones sociales...")
    output_visuals = os.path.join(BASE_DIR, "app", "infrastructure", "visuals")
    rutas = generar_todos_los_graficos(output_visuals)
    print(" Gráficos generados:", rutas)
    # -------------------------------------------------
    # 6 Copiar visualizaciones a carpeta del dashboard
    # -------------------------------------------------
    print("\n Paso 6: Actualizando dashboard...")
    rutas = generar_todos_los_graficos(INFRA_VISUALS)
    # -------------------------------------------------
    # 7 Confirmar finalización
    # -------------------------------------------------
    print("\nPipeline completado exitosamente.")
    print(f"Resultados disponibles en: {DATA_DIR}")
    print(f"Visualizaciones listas en: {INFRA_VISUALS}\n")


if __name__ == "__main__":
    run_pipeline()
