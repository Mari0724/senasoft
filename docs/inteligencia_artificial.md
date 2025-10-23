# 🤖 Uso de Inteligencia Artificial

La solución **CivIA** aplica distintas técnicas de **Inteligencia Artificial y Procesamiento de Lenguaje Natural (NLP)** para transformar datos textuales y sociales en conocimiento útil para la toma de decisiones.

---

## 🧠 Clasificación y resumen temático

Se empleó el modelo preentrenado **`all-MiniLM-L6-v2`** de *Sentence-Transformers* para generar **embeddings semánticos** a partir de los comentarios ciudadanos.  
Estos vectores permiten representar el significado de los textos y medir su similitud, agrupándolos en temas sin necesidad de etiquetas previas.

El agrupamiento se realizó mediante **K-Means**, generando **seis clústeres principales** que representan las problemáticas más comunes detectadas en las comunidades (salud, educación, medio ambiente, seguridad, entre otras).

---

## ⚙️ Procesos implementados

1. **Limpieza y normalización del texto** (eliminación de signos, acentos y stopwords) con NLTK.  
2. **Generación de embeddings** utilizando el modelo **MiniLM (sentence-transformers)**.  
3. **Agrupamiento automático** de reportes mediante **K-Means**, basado en similitud semántica.  
4. **Extracción de palabras clave** con **TF-IDF**, para identificar los términos más representativos de cada tema.  
5. **Análisis de sentimientos** con el modelo en español **BETO (pysentimiento/robertuito-sentiment-analysis)**, clasificando cada comentario como *positivo*, *negativo* o *neutro*.  
6. **Cruce de resultados** con variables sociales (ruralidad, internet, atención del gobierno) para generar un panorama integral.  
7. **Generación de explicaciones automáticas** con **OpenAI (ChatGPT)**, que interpreta los datos finales y ofrece recomendaciones empáticas a la ONG.

---

## 🧩 Modelos utilizados

| Tipo de análisis | Modelo / técnica | Descripción |
|------------------|------------------|--------------|
| Análisis semántico | **MiniLM (all-MiniLM-L6-v2)** | Genera embeddings vectoriales que representan el significado de los comentarios. |
| Agrupamiento temático | **K-Means** | Clasifica los comentarios en grupos de temas similares. |
| Análisis emocional | **BETO (pysentimiento)** | Detecta el tono emocional de los comentarios (positivo, neutro o negativo). |
| Asistencia generativa | **OpenAI (ChatGPT)** | Explica los resultados del dashboard y propone recomendaciones prácticas. |

---

## 📈 Métricas y explicabilidad

- **Métricas aplicadas:** se evaluó la coherencia temática y la distribución de los clústeres usando *Silhouette Score*, *Davies–Bouldin* y *Calinski–Harabasz*.  
- **Explicabilidad:** cada tema se documentó con sus **palabras clave** y una breve descripción generada por IA, mostrando cómo el modelo agrupa los textos y qué conceptos predominan en cada grupo.  
- **Validación cualitativa:** se compararon manualmente los resultados del análisis semántico con los patrones sociales identificados, confirmando la coherencia entre texto y contexto.

---

> 💬 En conjunto, los modelos **MiniLM, K-Means, BETO y OpenAI** conforman un flujo integral de análisis que combina interpretación semántica, detección emocional, contexto social y generación automática de conocimiento.
