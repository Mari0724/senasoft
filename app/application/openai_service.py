import os
import pandas as pd
from app.infrastructure.openai_gateway import OpenAIGateway

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")

def generar_explicacion_desde_csv() -> str:
    """
    Carga los resultados del dashboard (social + NLP) y genera una explicación completa usando OpenAI.
    """

    # 1 Leer datasets
    try:
        df_impacto = pd.read_csv(os.path.join(DATA_DIR, "impact_social.csv"), sep=";")
        df_sent = pd.read_csv(os.path.join(DATA_DIR, "themes_nlp.csv"), sep=";")
        print("Datos cargados correctamente.")
    except Exception as e:
        raise FileNotFoundError(f"No se pudieron cargar los CSV: {e}")

    # 2 Extraer indicadores sociales
    top_ciudades = df_impacto.sort_values("impacto_social", ascending=False)["ciudad"].head(3).tolist()

    zonas_criticas = df_impacto[df_impacto["patron_social"] == "Zona crítica"]["ciudad"].tolist()
    zonas_invisibles = df_impacto[df_impacto["patron_social"] == "Zona invisible"]["ciudad"].tolist()
    zonas_puntuales = df_impacto[df_impacto["patron_social"] == "Zona puntual"]["ciudad"].tolist()

    vulnerabilidad_prom = round(df_impacto["vulnerabilidad"].mean(), 2)
    urgencia_prom = round(df_impacto["nivel_de_urgencia"].mean(), 2)

    # 3 Extraer información NLP
    if "categoria_del_problema" in df_sent.columns:
        top_categorias = df_sent["categoria_del_problema"].value_counts().head(3).index.tolist()
    else:
        top_categorias = []

    if all(c in df_sent.columns for c in ["sent_pos", "sent_neg"]):
        avg_pos = df_sent["sent_pos"].mean()
        avg_neg = df_sent["sent_neg"].mean()
        sentimiento_general = (
            "Predominantemente positivo" if avg_pos > avg_neg else "Predominantemente negativo"
        )
    else:
        sentimiento_general = "Sin datos de sentimiento"

    # 4 Construir prompt (más completo)
    prompt = f"""
    Eres un asesor social de una ONG que analiza información de comunidades locales
    usando modelos de IA. Explica los resultados obtenidos y da recomendaciones concretas.

    🔹 **Indicadores generales:**
    - Promedio de vulnerabilidad estructural: {vulnerabilidad_prom}
    - Promedio de nivel de urgencia: {urgencia_prom}
    - Balance emocional general: {sentimiento_general}

    🔹 **Zonas críticas:** {', '.join(zonas_criticas) or 'Ninguna detectada'}
    🔹 **Zonas invisibles:** {', '.join(zonas_invisibles) or 'Ninguna detectada'}
    🔹 **Zonas puntuales:** {', '.join(zonas_puntuales) or 'Ninguna detectada'}

    🔹 **Ciudades con mayor impacto social:** {', '.join(top_ciudades) or 'Sin datos'}
    🔹 **Categorías más urgentes:** {', '.join(top_categorias) or 'Sin datos'}

    Instrucciones:
    1. Resume la situación social detectada con claridad.
    2. Explica brevemente qué significan las zonas críticas e invisibles.
    3. Termina con un párrafo que empiece con:
       "Por esto te recomendamos..." e incluye una acción y una zona específica.

    Sé empático y usa un lenguaje accesible para una ONG.
    Responde en un máximo de 300 palabras.
    """

    # 5 Llamar a OpenAI
    gateway = OpenAIGateway()
    respuesta = gateway.generar_respuesta(prompt)
    return respuesta
