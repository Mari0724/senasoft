import pandas as pd
import re
import string
import nltk
import torch
import numpy as np
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from app.application.helpers import evaluar_y_graficar, mostrar_resumen

nltk.download("stopwords")

# ============================================================
#  1️⃣ CARGAR Y PREPARAR DATOS LIMPIOS
# ============================================================
def cargar_y_preparar_datos(path: str) -> pd.DataFrame:
    print("📂 Cargando dataset limpio...")
    df = pd.read_csv(path, sep=";", encoding="utf-8")
    df.columns = [c.strip().lower() for c in df.columns]

    if "comentario" not in df.columns:
        raise ValueError(f"No se encontró la columna 'comentario'. Columnas: {df.columns.tolist()}")

    stop_words = set(stopwords.words("spanish"))

    def limpiar_texto(texto):
        if pd.isna(texto):
            return ""
        texto = texto.lower()
        texto = re.sub(r"\d+", "", texto)
        texto = texto.translate(str.maketrans("", "", string.punctuation))
        palabras = [p for p in texto.split() if p not in stop_words]
        return " ".join(palabras)

    df["comentario_limpio"] = df["comentario"].apply(limpiar_texto)
    print(f"✅ Limpieza completada. Total de filas: {len(df)}")
    return df


# ============================================================
#  2️⃣ GENERAR EMBEDDINGS SEMÁNTICOS
# ============================================================
def generar_embeddings(df: pd.DataFrame):
    print("🔍 Generando embeddings semánticos (modelo MiniLM)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(df["comentario_limpio"].tolist(), show_progress_bar=True)
    print("✅ Embeddings generados correctamente.")
    return embeddings


# ============================================================
#  3️⃣ AGRUPAR TEMAS Y EXTRAER PALABRAS CLAVE
# ============================================================
def agrupar_y_extraer_temas(df: pd.DataFrame, embeddings, n_clusters: int = 6) -> pd.DataFrame:
    print(f"🧠 Agrupando en {n_clusters} temas...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["tema"] = kmeans.fit_predict(embeddings)

    print("🗝️ Extrayendo palabras clave por tema...")
    temas = sorted(df["tema"].unique())
    resultados = []

    for tema in temas:
        textos = df[df["tema"] == tema]["comentario_limpio"].dropna().tolist()
        textos_filtrados = [t for t in textos if len(t.split()) > 1]
        if len(textos_filtrados) < 2:
            resultados.append({"tema": tema, "palabras_clave": "(sin datos suficientes)"})
            continue

        vectorizer = TfidfVectorizer(max_features=5)
        X = vectorizer.fit_transform(textos_filtrados)
        keywords = vectorizer.get_feature_names_out()
        resultados.append({"tema": tema, "palabras_clave": ", ".join(keywords)})

    df = df.merge(pd.DataFrame(resultados), on="tema", how="left")
    print("✅ Temas y palabras clave generadas correctamente.")
    return df


# ============================================================
#  4️⃣ ANÁLISIS DE SENTIMIENTOS (Modelo Español BETO)
# ============================================================
def analizar_sentimientos(df: pd.DataFrame):
    print("💬 Analizando sentimientos con modelo español (BETO)...")
    model_name = "pysentimiento/robertuito-sentiment-analysis"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    model.eval()

    textos = df["comentario"].fillna("").astype(str).tolist()
    batch_size = 64
    preds, probas = [], []
    labels = {0: "negativo", 1: "neutro", 2: "positivo"}

    for i in range(0, len(textos), batch_size):
        batch = textos[i : i + batch_size]
        with torch.no_grad():
            inputs = tokenizer(batch, padding=True, truncation=True, max_length=256, return_tensors="pt")
            outputs = model(**inputs)
            soft = torch.nn.functional.softmax(outputs.logits, dim=1).cpu().numpy()
        probas.append(soft)
        preds.extend(soft.argmax(axis=1))

    probas = np.vstack(probas)
    df["sentimiento"] = [labels[p] for p in preds]
    df["sent_neg"] = probas[:, 0]
    df["sent_neu"] = probas[:, 1]
    df["sent_pos"] = probas[:, 2]

    # ✅ Sanity check (3 frases rápidas)
    print("\n🧪 Sanity check:")
    ejemplos = ["Excelente atención", "Muy mala gestión", "Regular el servicio"]
    with torch.no_grad():
        t = tokenizer(ejemplos, padding=True, truncation=True, return_tensors="pt")
        o = model(**t)
        s = torch.nn.functional.softmax(o.logits, dim=1).cpu().numpy()
    for txt, prob in zip(ejemplos, s):
        print(f"  '{txt}': NEG={prob[0]:.2f} NEU={prob[1]:.2f} POS={prob[2]:.2f}")

    print("✅ Análisis de sentimientos completado.")
    return df


# ============================================================
#  5️⃣ PIPELINE COMPLETO
# ============================================================
def ejecutar_nlp_pipeline():
    df = cargar_y_preparar_datos("data/clean_data.csv")
    embeddings = generar_embeddings(df)
    df = agrupar_y_extraer_temas(df, embeddings, n_clusters=6)
    df = analizar_sentimientos(df)

    # Guardar resultados combinados
    df.to_csv("data/themes_nlp.csv", sep=";", encoding="utf-8", index=False)
    print("📁 Resultados guardados en data/themes_nlp.csv")

    # Mostrar y evaluar
    mostrar_resumen(df)
    evaluar_y_graficar(df, embeddings)

    print("\n🎯 Proceso NLP completado exitosamente.")


# ============================================================
#  6️⃣ EJECUCIÓN DIRECTA
# ============================================================
if __name__ == "__main__":
    ejecutar_nlp_pipeline()
