# 📊 Resultados

El proyecto **CivIA** generó resultados tangibles que integran los análisis **semántico**, **social**, **emocional** y **generativo**, permitiendo comprender de manera integral las problemáticas de las comunidades.

---

## 📁 Archivos generados

- **`themes_nlp.csv`** → Contiene los **temas detectados**, sus **palabras clave** y los **sentimientos asociados** (positivo, neutro, negativo) extraídos con los modelos **MiniLM** y **BETO**.  
- **`impact_social.csv`** → Resume los **indicadores sociales por ciudad**, calculando vulnerabilidad, urgencia y el patrón social correspondiente (Zona crítica, invisible, puntual o estable).  
- **`final_results.csv`** → Combina los resultados semánticos y sociales, generando el **Índice de Impacto Social** final para priorizar las zonas de atención.  
- **`clean_data.csv`** → Conjunto de datos procesados y normalizados tras el ETL inicial.  
- **`visuals/impact_chart.png`** → Gráfico de barras que muestra el ranking de impacto social por ciudad.

---

## 🌐 API funcional

Se implementó una **API desarrollada en FastAPI**, que permite ejecutar los análisis y acceder a los resultados mediante endpoints locales:

| Endpoint | Descripción |
|-----------|--------------|
| **`/analyze`** | Ejecuta el pipeline completo de análisis de texto (embeddings + clustering + sentimientos). |
| **`/impact`** | Calcula el índice de impacto social y genera visualizaciones actualizadas en `data/visuals/`. |

> 💡 La API se ejecuta completamente en entorno local, garantizando independencia y reproducibilidad sin conexión a internet.

---

## 📊 Dashboard y asistencia IA

- Se integró un **dashboard visual** en HTML (prototipo local) donde se presentan los gráficos, indicadores y tablas de resultados.  
- Desde el dashboard, el usuario puede activar el botón **“IA Explícame”**, que conecta con el **módulo OpenAI** (`openai_gateway.py`) y genera una explicación automática de los resultados combinados.  
- Este asistente resume la situación general, explica las zonas críticas y finaliza con una recomendación práctica del tipo:  
  > “Por esto te recomendamos intervenir prioritariamente en la Zona Crítica de Bucaramanga, donde la falta de internet y la baja atención institucional coinciden con un sentimiento negativo generalizado.”

---

## 📈 Visualización final

El proceso de integración de resultados se realizó a través de **Pandas**, uniendo los datos temáticos y sociales en un único conjunto final:

```python
import pandas as pd

themes = pd.read_csv('data/themes_nlp.csv', sep=';')
social = pd.read_csv('data/impact_social.csv', sep=';')

final_results = social.merge(themes, how='left', left_on='ciudad', right_on='ciudad')
final_results.to_csv('data/final_results.csv', sep=';', index=False)
```

La visualización generada muestra las ciudades priorizadas según su impacto social total, con colores que representan los patrones detectados:

- 🔴 Zona crítica

- 🟡 Zona invisible
-
- 🟠 Zona puntual
 
- 🟢 Estable

>📘 Los resultados completos, gráficas y archivos CSV se encuentran disponibles en la carpeta data/ del proyecto.
Para más detalles sobre el proceso de obtención de estos resultados, consultar el documento proceso_solucion.md
.