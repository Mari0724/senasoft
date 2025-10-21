import pandas as pd
import re
import os
import unicodedata
import chardet
import numpy as np

# ==============================
# 📂 RUTAS
# ==============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, "data", "original.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "clean_data.csv")

# ==============================
# 🧠 FUNCIONES AUXILIARES
# ==============================
def normalize_text(text: str) -> str:
    """Convierte texto a minúsculas, sin acentos ni símbolos raros."""
    if not isinstance(text, str):
        text = str(text)
    text = text.lower()
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def normalize_columns(columns):
    """Normaliza nombres de columnas: sin tildes, en minúsculas, con _."""
    normalized = []
    for col in columns:
        col = unicodedata.normalize("NFKD", col).encode("ascii", "ignore").decode("utf-8")
        col = col.strip().lower()
        col = re.sub(r"[^a-z0-9]+", "_", col)
        col = col.strip("_")
        normalized.append(col)
    return normalized

# ==============================
# 🚀 ETL COMPLETO
# ==============================
def run_etl():
    print("🚀 Iniciando ETL completo con normalización numérica y textual...")

    # 1️⃣ Detectar codificación
    with open(DATA_PATH, "rb") as f:
        raw = f.read()
        detected = chardet.detect(raw)
        encoding_used = detected["encoding"]
    print(f"🔍 Codificación detectada: {encoding_used}")

    # 2️⃣ Leer CSV
    df = pd.read_csv(DATA_PATH, sep=",", encoding=encoding_used, on_bad_lines="skip")
    print(f"📥 Datos cargados: {df.shape[0]} filas, {df.shape[1]} columnas")

    # 3️⃣ Normalizar nombres de columnas
    df.columns = normalize_columns(df.columns)

    # 4️⃣ Limpiar texto en columnas tipo string
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).apply(normalize_text)

    # 5️⃣ Procesar la columna edad
    if "edad" in df.columns:
        # Convertir a numérico (coerce convierte errores en NaN)
        df["edad"] = pd.to_numeric(df["edad"], errors="coerce")

        # Eliminar edades fuera de rango (menores de 0 o >120)
        df.loc[(df["edad"] < 0) | (df["edad"] > 120), "edad"] = np.nan

        # Convertir floats válidos a enteros y NaN a vacío
        df["edad"] = df["edad"].apply(lambda x: "" if pd.isna(x) else int(x))

    # 6️⃣ Reemplazar espacios vacíos o 'nan' string por NaN visual
    df = df.replace(r"^\s*$", "", regex=True)

    # 7️⃣ Guardar archivo final limpio
    df.to_csv(OUTPUT_PATH, sep=";", encoding="utf-8", index=False)
    print(f"✅ Archivo final limpio guardado en: {OUTPUT_PATH}")
    print("🎯 Codificación: UTF-8 | Edades enteras | Vacíos reales (sin 23.0 ni NaN)\n")


if __name__ == "__main__":
    run_etl()
