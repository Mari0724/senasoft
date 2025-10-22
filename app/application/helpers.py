import os
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score,
)

# ============================================================
#  RESUMEN EN CONSOLA (temas top)
# ============================================================
def mostrar_resumen(df, top_n=5):
    print("\nResumen de temas detectados (TOP):")
    resumen = (
        df.groupby(["tema", "palabras_clave"])
          .size()
          .reset_index(name="frecuencia")
          .sort_values("frecuencia", ascending=False)
          .head(top_n)
    )
    for _, row in resumen.iterrows():
        print(f"  • Tema {row['tema']:>2} → {row['palabras_clave']}  | {row['frecuencia']} reportes")
    print("   (ver imágenes en data/visuals/ y CSVs generados para detalle)")

# ============================================================
#  EVALUACIÓN + GRÁFICOS (CLUSTERING + SENTIMIENTO)
# ============================================================
def evaluar_y_graficar(df, embeddings, k_min=3, k_max=10):
    """
    - Calcula métricas de clustering (Silhouette, Davies-Bouldin, Calinski-Harabasz)
    - Genera curvas de selección de K (elbow e índice Silhouette por K)
    - Grafica distribución por tema, sentimientos por tema, pastel global de sentimientos
    - Grafica histograma de confianza POS/NEG del clasificador de sentimiento
    - Exporta métricas y tablas a CSV/JSON
    """
    print("\nEvaluando modelo y generando gráficos...")
    os.makedirs("data/visuals", exist_ok=True)

    # --------- MÉTRICAS DE CLUSTERING (con el K actual) ---------
    try:
        sil = silhouette_score(embeddings, df["tema"])
        db = davies_bouldin_score(embeddings, df["tema"])
        ch = calinski_harabasz_score(embeddings, df["tema"])
        print(f"Silhouette: {sil:.3f} | 🔻 Davies-Bouldin: {db:.3f} | 🔺 Calinski-Harabasz: {ch:.0f}")
    except Exception as e:
        sil = db = ch = None
        print(f"No se pudieron calcular métricas del clustering: {e}")

    # Guardar métricas en JSON
    with open("data/visuals/cluster_metrics.json", "w", encoding="utf-8") as f:
        json.dump({"silhouette": sil, "davies_bouldin": db, "calinski_harabasz": ch}, f, ensure_ascii=False, indent=2)

    # --------- CURVAS PARA ELEGIR K (opcional pero útil en demo) ---------
    # Reentrenamos KMeans para varios K y graficamos Inertia (Elbow) y Silhouette.
    try:
        ks = list(range(k_min, k_max + 1))
        inertias, silhouettes = [], []
        for k in ks:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = km.fit_predict(embeddings)
            inertias.append(km.inertia_)
            # Silhouette solo si k > 1 y hay muestras suficientes
            if len(set(labels)) > 1:
                silhouettes.append(silhouette_score(embeddings, labels))
            else:
                silhouettes.append(np.nan)

        # Elbow (Inertia)
        plt.figure(figsize=(8, 5))
        plt.plot(ks, inertias, marker="o")
        plt.title("Curva del codo (Inertia vs K)")
        plt.xlabel("K (número de clusters)")
        plt.ylabel("Inertia (↓ mejor codo)")
        plt.xticks(ks)
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig("data/visuals/elbow_k.png", dpi=300, bbox_inches="tight")
        plt.close()
        print("Guardado: data/visuals/elbow_k.png")

        # Silhouette por K
        plt.figure(figsize=(8, 5))
        plt.plot(ks, silhouettes, marker="o")
        plt.title("Índice Silhouette por K (↑ mejor)")
        plt.xlabel("K (número de clusters)")
        plt.ylabel("Silhouette")
        plt.xticks(ks)
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig("data/visuals/silhouette_k.png", dpi=300, bbox_inches="tight")
        plt.close()
        print("Guardado: data/visuals/silhouette_k.png")
    except Exception as e:
        print(f"No se pudieron generar curvas de K: {e}")

    # --------- ETIQUETAS LEGIBLES PARA LOS TEMAS ---------
    etiquetas_temas = (
        df.groupby("tema")["palabras_clave"]
          .first()
          .fillna("(sin datos)")
          .apply(lambda x: x[:40] + "..." if len(x) > 40 else x)
          .to_dict()
    )

    # --------- GRAF. 1: DISTRIBUCIÓN DE COMENTARIOS POR TEMA ---------
    tema_counts = df["tema"].value_counts().sort_index()
    temas_legibles = [etiquetas_temas.get(t, str(t)) for t in tema_counts.index]

    plt.figure(figsize=(10, 5))
    plt.bar(temas_legibles, tema_counts.values)
    plt.title("Distribución de comentarios por tema")
    plt.xlabel("Tema detectado (palabras clave)")
    plt.ylabel("Cantidad de comentarios")
    plt.xticks(rotation=25, ha="right", fontsize=9)
    if sil is not None:
        plt.figtext(0.5, -0.02, f"Silhouette: {sil:.3f} | Davies-Bouldin: {db:.3f} | Calinski-Harabasz: {ch:.0f}",
                    ha="center", fontsize=9)
    plt.tight_layout()
    plt.savefig("data/visuals/distribucion_temas.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("Guardado: data/visuals/distribucion_temas.png")

    # Exportar tamaños de cluster
    tema_counts.rename_axis("tema").reset_index(name="cantidad") \
        .to_csv("data/visuals/cluster_sizes.csv", index=False)

    # --------- GRAF. 2: SENTIMIENTOS POR TEMA ---------
    pivot = df.groupby(["tema", "sentimiento"]).size().unstack(fill_value=0)
    pivot.index = [etiquetas_temas.get(t, str(t)) for t in pivot.index]

    ax = pivot.plot(kind="bar", figsize=(10, 5))
    ax.set_title("Sentimientos por tema detectado")
    ax.set_xlabel("Tema detectado (palabras clave)")
    ax.set_ylabel("Cantidad de comentarios")
    plt.xticks(rotation=25, ha="right", fontsize=9)
    plt.tight_layout()
    plt.savefig("data/visuals/sentimientos_por_tema.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("Guardado: data/visuals/sentimientos_por_tema.png")

    # --------- GRAF. 3: PASTEL GLOBAL DE SENTIMIENTOS + CSV ---------
    conteo = df["sentimiento"].value_counts()
    conteo.rename_axis("clase").reset_index(name="cantidad") \
        .assign(porcentaje=lambda d: (d["cantidad"] / d["cantidad"].sum() * 100).round(2)) \
        .to_csv("data/visuals/sentimientos_globales.csv", index=False)

    etiquetas = conteo.index.tolist()
    valores = conteo.values.tolist()
    plt.figure(figsize=(6, 6))
    plt.pie(valores,
            labels=[f"{e} ({v})" for e, v in zip(etiquetas, valores)],
            autopct="%1.1f%%",
            startangle=140)
    plt.title("Distribución global de sentimientos")
    plt.tight_layout()
    plt.savefig("data/visuals/sentimientos_globales.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("Guardado: data/visuals/sentimientos_globales.png")

    # --------- GRAF. 4: HISTOGRAMA DE CONFIANZA DEL CLASIFICADOR ---------
    # Estas columnas las crea nlp_service. Si no están, se omite.
    if {"sent_pos", "sent_neg"}.issubset(df.columns):
        plt.figure(figsize=(8, 5))
        plt.hist(df["sent_pos"], bins=20, alpha=0.6, label="POS")
        plt.hist(df["sent_neg"], bins=20, alpha=0.6, label="NEG")
        plt.title("Confianza del modelo de sentimiento (POS vs NEG)")
        plt.xlabel("Probabilidad")
        plt.ylabel("Frecuencia")
        plt.legend()
        plt.tight_layout()
        plt.savefig("data/visuals/confianza_sentimiento.png", dpi=300, bbox_inches="tight")
        plt.close()
        print("Guardado: data/visuals/confianza_sentimiento.png")
    else:
        print("Columnas de confianza de sentimiento no disponibles (sent_pos/sent_neg).")

    print("Evaluación y gráficos generados.")
