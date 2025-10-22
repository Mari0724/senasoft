import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ==============================
#  RUTAS BASE
# ==============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")

# ==============================
#  FUNCIONES DE VISUALIZACIÓN
# ==============================

def grafico_impacto_por_ciudad(output_dir):
    """ Promedio de impacto social por ciudad."""
    df = pd.read_csv(os.path.join(DATA_DIR, "impact_social.csv"), sep=";")
    plt.figure(figsize=(8, 5))
    df = df.sort_values("impacto_social", ascending=True)
    colores = df["patron_social"].map({
        "Zona crítica": "#E63946",
        "Zona invisible": "#F4D35E",
        "Zona puntual": "#F29E38",
        "Estable": "#35DBB8"
    }).fillna("#999")

    plt.barh(df["ciudad"], df["impacto_social"], color=colores)
    plt.title("Impacto social promedio por ciudad")
    plt.xlabel("Índice de impacto social (0–1)")
    plt.tight_layout()
    path = os.path.join(output_dir, "impacto_por_ciudad.png")
    plt.savefig(path)
    plt.close()
    return path

def grafico_categorias_impacto(output_dir):
    """Categorías con mayor impacto social según IA."""
    df = pd.read_csv(os.path.join(DATA_DIR, "final_results.csv"), sep=";")
    if "categoria_del_problema" not in df.columns:
        return None
    top = df.groupby("categoria_del_problema")["impacto_social"].mean().sort_values(ascending=False).head(8)
    plt.figure(figsize=(9, 5))
    top.plot(kind="bar", color="#b40000")
    plt.title("Categorías con mayor impacto social (IA + Social)")
    plt.ylabel("Promedio de impacto social")
    plt.xlabel("Categoría del problema")
    plt.tight_layout()
    path = os.path.join(output_dir, "categorias_impacto.png")
    plt.savefig(path)
    plt.close()
    return path


def grafico_internet_vs_urgencia(output_dir):
    """ Acceso a internet vs nivel de urgencia."""
    df = pd.read_csv(os.path.join(DATA_DIR, "clean_data.csv"), sep=";")
    df["nivel_de_urgencia"] = df["nivel_de_urgencia"].str.lower()
    grouped = df.groupby("acceso_a_internet")["nivel_de_urgencia"].value_counts().unstack().fillna(0)
    grouped.plot(kind="bar", stacked=True, color=["#b40000", "#ccc"])
    plt.title("Acceso a internet vs nivel de urgencia")
    plt.xlabel("Acceso a internet (0 = No, 1 = Sí)")
    plt.ylabel("Cantidad de reportes")
    plt.tight_layout()
    path = os.path.join(output_dir, "internet_vs_urgencia.png")
    plt.savefig(path)
    plt.close()
    return path


def grafico_reportes_por_genero(output_dir):
    """ Distribución de reportes por género."""
    df = pd.read_csv(os.path.join(DATA_DIR, "clean_data.csv"), sep=";")
    generos = df["genero"].value_counts()
    colores = ["#b40000", "#F4D35E", "#35DBB8"]
    plt.figure(figsize=(5, 5))
    generos.plot(kind="pie", autopct="%1.1f%%", colors=colores)
    plt.title("Distribución de reportes por género")
    plt.ylabel("")
    plt.tight_layout()
    path = os.path.join(output_dir, "reportes_por_genero.png")
    plt.savefig(path)
    plt.close()
    return path

"""
    NLP- Sentimientos y capas ocultas en la urgencia y comentarios
"""

def grafico_sentimiento_promedio(output_dir):
    """Distribución de sentimientos (positivo, neutro, negativo) por ciudad."""
    df = pd.read_csv(os.path.join(DATA_DIR, "themes_nlp.csv"), sep=";")

    # Agrupar promedios por ciudad
    resumen = df.groupby("ciudad")[["sent_pos", "sent_neu", "sent_neg"]].mean().dropna()

    # Normalizar para que las tres columnas sumen 1 por ciudad (proporción)
    resumen = resumen.div(resumen.sum(axis=1), axis=0)

    # Ordenar por ciudades con más positividad
    resumen = resumen.sort_values("sent_pos", ascending=False).head(10)

    # Colores institucionales
    colores = ["#2ECC71", "#F4D35E", "#E74C3C"]

    # Crear gráfico apilado horizontal
    resumen.plot(kind="barh", stacked=True, color=colores, figsize=(9, 5))
    plt.title("Distribución de sentimientos promedio por ciudad")
    plt.xlabel("Proporción de comentarios (%)")
    plt.ylabel("Ciudad")
    plt.legend(["Positivo", "Neutro", "Negativo"], loc="lower right")
    plt.tight_layout()

    path = os.path.join(output_dir, "sentimiento_promedio.png")
    plt.savefig(path)
    plt.close()
    return path


def grafico_temas_detectados(output_dir):
    """Temas detectados por IA (NLP clustering)."""
    df = pd.read_csv(os.path.join(DATA_DIR, "themes_nlp.csv"), sep=";")
    top = df["palabras_clave"].value_counts().head(10)
    plt.figure(figsize=(9, 5))
    top.plot(kind="barh", color="#b40000")
    plt.title("Temas detectados por IA")
    plt.xlabel("Cantidad de comentarios agrupados")
    plt.tight_layout()
    path = os.path.join(output_dir, "temas_detectados.png")
    plt.savefig(path)
    plt.close()
    return path


# ==============================
#  FUNCIÓN PRINCIPAL
# ==============================
def generar_todos_los_graficos(output_dir):
    """Genera los 5 gráficos finales del dashboard."""
    os.makedirs(output_dir, exist_ok=True)
    print(f"Generando visualizaciones en {output_dir} ...")

    rutas = {
        "impacto_por_ciudad": grafico_impacto_por_ciudad(output_dir),
        "categorias_impacto": grafico_categorias_impacto(output_dir),
        "internet_vs_urgencia": grafico_internet_vs_urgencia(output_dir),
        "reportes_por_genero": grafico_reportes_por_genero(output_dir),
        "sentimiento_promedio": grafico_sentimiento_promedio(output_dir),
        "temas_detectados": grafico_temas_detectados(output_dir),
    }


    print("✅ Gráficos generados correctamente.")
    return rutas


if __name__ == "__main__":
    output_default = os.path.join(BASE_DIR, "app", "infrastructure", "visuals")
    generar_todos_los_graficos(output_default)
