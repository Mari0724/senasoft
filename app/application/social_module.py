import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# =========================================
# 1️⃣ CARGA Y NORMALIZACIÓN DE DATOS
# =========================================
def load_dataset(path: str) -> pd.DataFrame:
    """Carga el dataset, detecta separador y normaliza columnas."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró el archivo: {os.path.abspath(path)}")

    with open(path, "r", encoding="utf-8-sig") as f:
        sample = f.readline()
        sep = ";" if ";" in sample else ","

    df = pd.read_csv(path, encoding="utf-8-sig", sep=sep)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df


def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza columnas: limpia texto y convierte variables binarias a 0/1."""

    # --- Normalizar nombres de columnas (por si acaso) ---
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # --- Normalizar nivel de urgencia ---
    if "nivel_de_urgencia" in df.columns:
        if df["nivel_de_urgencia"].dtype == "object":
            # Si son textos tipo “urgente” o “no urgente”
            df["nivel_de_urgencia"] = (
                df["nivel_de_urgencia"]
                .astype(str)
                .str.lower()
                .str.strip()
                .replace({
                    "urgente": 1,
                    "no urgente": 0,
                    "no_urgente": 0
                })
            )
        else:
            # Si ya es numérica (0 o 1), aseguramos el rango
            df["nivel_de_urgencia"] = df["nivel_de_urgencia"].clip(0, 1)

    # --- Convertir columnas binarias a enteros ---
    for col in ["acceso_a_internet", "atencion_previa_del_gobierno", "zona_rural"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    return df

# =========================================
# 2️⃣ ÍNDICE DE VULNERABILIDAD SOCIAL
# =========================================
def analyze_social_patterns(df: pd.DataFrame) -> pd.DataFrame:
    """Combina factores sociales y urgencia y clasifica con umbrales dinámicos."""
    df = normalize_data(df)

    # Vulnerabilidad estructural (0–1). Ponderaciones ajustables.
    df["vulnerabilidad"] = (
        (1 - df["acceso_a_internet"]) * 0.4 +
        (1 - df["atencion_previa_del_gobierno"]) * 0.3 +
        df["zona_rural"] * 0.3
    )

    # Agrupar por ciudad
    summary = df.groupby("ciudad", dropna=True).agg(
        vulnerabilidad=("vulnerabilidad", "mean"),
        nivel_de_urgencia=("nivel_de_urgencia", "mean"),
        n_reportes=("id", "count")
    ).reset_index()

    # --- UMBRALES DINÁMICOS (cuantiles) ---
    # Si tienes pocas ciudades, usa mediana (0.5). Con más ciudades, 0.65 da mejor contraste.
    q_v = 0.65 if summary.shape[0] >= 8 else 0.5
    q_u = 0.65 if summary.shape[0] >= 8 else 0.5

    v_hi = float(summary["vulnerabilidad"].quantile(q_v))
    u_hi = float(summary["nivel_de_urgencia"].quantile(q_u))

    # Clasificación relativa (alto vs bajo) según cuantiles
    v_alta = summary["vulnerabilidad"] >= v_hi
    u_alta = summary["nivel_de_urgencia"] >= u_hi

    # Etiquetas:
    # - Crítica: alta vulnerabilidad y alta urgencia
    # - Invisible: alta vulnerabilidad pero urgencia baja (riesgo latente)
    # - Puntual: baja vulnerabilidad pero urgencia alta (evento no estructural)
    # - Estable: lo demás
    conditions = [
        v_alta & u_alta,
        v_alta & ~u_alta,
        ~v_alta & u_alta
    ]
    labels = ["Zona crítica", "Zona invisible", "Zona puntual"]
    summary["patron_social"] = np.select(conditions, labels, default="Estable")

    # Si por distribución siguen saliendo todas iguales, forzamos separación por ranking:
    if summary["patron_social"].nunique() == 1:
        # Top 30% vulnerabilidad -> 'Zona crítica'
        cutoff = max(1, int(np.ceil(0.3 * len(summary))))
        top_idx = summary["vulnerabilidad"].rank(method="first", ascending=False) <= cutoff
        summary.loc[top_idx, "patron_social"] = "Zona crítica"

    # Redondeo amigable
    summary["vulnerabilidad"] = summary["vulnerabilidad"].round(2)
    summary["nivel_de_urgencia"] = summary["nivel_de_urgencia"].round(2)

    return summary[["ciudad", "vulnerabilidad", "nivel_de_urgencia", "patron_social", "n_reportes"]]

def compute_social_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula el índice de impacto social combinando factores estructurales (vulnerabilidad),
    de acceso y contexto (internet, atención, ruralidad) y urgencia.
    """
    summary = analyze_social_patterns(df)

    # Unir datos base para tener acceso_a_internet, etc.
    base_cols = ["ciudad", "acceso_a_internet", "atencion_previa_del_gobierno", "zona_rural"]
    base_info = df[base_cols].groupby("ciudad", as_index=False).mean()

    summary = summary.merge(base_info, on="ciudad", how="left")

    # Normalizar de 0 a 1 para evitar sesgos
    for col in ["vulnerabilidad", "nivel_de_urgencia", "acceso_a_internet", "atencion_previa_del_gobierno", "zona_rural"]:
        summary[col] = (summary[col] - summary[col].min()) / (summary[col].max() - summary[col].min() + 1e-9)

    # Cálculo ponderado más realista
    summary["impacto_social"] = (
        (summary["vulnerabilidad"] * 0.35) +
        (summary["nivel_de_urgencia"] * 0.25) +
        ((1 - summary["acceso_a_internet"]) * 0.2) +
        ((1 - summary["atencion_previa_del_gobierno"]) * 0.1) +
        (summary["zona_rural"] * 0.1)
    )

    # Redondeo solo al final
    summary["impacto_social"] = summary["impacto_social"].round(3)

    # Generar gráfico
    try:
        generate_impact_chart(summary)
    except Exception as e:
        print("⚠️ No se pudo generar el gráfico:", e)

    # Ordenar por impacto descendente
    return summary[[
        "ciudad", "vulnerabilidad", "nivel_de_urgencia",
        "patron_social", "impacto_social", "n_reportes"
    ]].sort_values("impacto_social", ascending=False).reset_index(drop=True)


def generate_impact_chart(summary: pd.DataFrame, output_path="data/visuals/impact_chart.png"):
    """Genera un gráfico de barras del impacto social."""
    import matplotlib.pyplot as plt

    if "impacto_social" not in summary.columns:
        print("⚠️ No se encontró la columna 'impacto_social'. Se omite el gráfico.")
        return

    plt.figure(figsize=(8,5))
    colors = {
        "Zona crítica": "#E63946",
        "Zona invisible": "#F4D35E",
        "Zona puntual": "#F29E38",  
        "Estable": "#35DBB8"
    }


    plt.barh(
        summary["ciudad"],
        summary["impacto_social"],
        color=[colors.get(z, "#cccccc") for z in summary["patron_social"]]
    )
    plt.xlabel("Impacto social (0–1)")
    plt.title("Ranking de impacto social por ciudad")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"Gráfico guardado en {output_path}")