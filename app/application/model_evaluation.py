import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from app.application.social_module import load_dataset, normalize_data, compute_social_index

DATA_PATH = "data/clean_data.csv"

def evaluate_social_model():
    """Evalúa qué aprendió el modelo social a través de correlaciones y distribuciones."""
    df = load_dataset(DATA_PATH)
    df = normalize_data(df)

    # Calculamos el índice social completo
    summary = compute_social_index(df)

    # === 1 Distribución de vulnerabilidad vs urgencia ===
    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        data=summary,
        x="vulnerabilidad",
        y="nivel_de_urgencia",
        hue="patron_social",
        palette={
            "Zona crítica": "#d73027",
            "Zona invisible": "#fc8d59",
            "Zona puntual": "#fee08b",
            "Estable": "#1a9850"
        },
        s=100
    )
    plt.title("\n Relación entre Vulnerabilidad y Urgencia por Patrón Social")
    plt.xlabel("Vulnerabilidad (0–1)")
    plt.ylabel("Urgencia (0–1)")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig("data/visuals/model_learning_scatter.png", bbox_inches="tight")
    plt.close()

    # === 2 Correlación entre variables ===
    corr = df[["nivel_de_urgencia", "acceso_a_internet", "atencion_previa_del_gobierno", "zona_rural"]].corr()

    plt.figure(figsize=(6, 5))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlaciones aprendidas entre variables sociales")
    plt.tight_layout()
    plt.savefig("data/visuals/model_correlation_heatmap.png", bbox_inches="tight")
    plt.close()

    print("✅ Evaluación del modelo completada.")
    print("Gráficos generados:")
    print(" - data/model_learning_scatter.png (relación entre variables)")
    print(" - data/model_correlation_heatmap.png (correlaciones)")

if __name__ == "__main__":
    evaluate_social_model()
