# Uso de Inteligencia Artificial

### Clasificación y resumen
Se emplean modelos preentrenados (como `all-MiniLM-L6-v2` o IBM Granite) para analizar los comentarios ciudadanos y agruparlos por temas.

### Procesos implementados
1. Limpieza y tokenización (NLTK o spaCy)
2. Generación de embeddings con `sentence-transformers`
3. Agrupamiento con KMeans o BERTopic
4. Cálculo de frecuencia y urgencia promedio por tema
5. Exportación a `themes.csv`

### Modelos
- **Modelo base:** Transformers
- **Métricas:** Precisión, F1, Recall
- **Explicabilidad:** Se documenta cómo el modelo toma decisiones sobre cada tema o resumen.
