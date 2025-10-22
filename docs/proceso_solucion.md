# 🔍 Proceso de construcción de la solución

## 1. Análisis inicial y comprensión del reto

Durante las primeras horas del reto **SENASoft 2025 – Categoría Inteligencia Artificial**, analizamos cuidadosamente la descripción del problema:  
una **organización sin ánimo de lucro (ONG)** necesitaba comprender las principales problemáticas de distintas comunidades colombianas, basándose en reportes ciudadanos y datos sociales.

El conjunto de datos incluía **comentarios en texto libre** (reportes ciudadanos) junto con variables sociales como:
- Acceso a internet  
- Atención previa del gobierno  
- Zona rural o urbana  
- Nivel de urgencia del problema  

Desde el inicio entendimos que el desafío no consistía en clasificar por sector (salud, educación, etc.), sino en **descubrir patrones y relaciones entre diferentes problemáticas sociales** que permitieran a la ONG **priorizar sus recursos y esfuerzos**.

> 💡 **Conclusión de esta etapa:**  
> El objetivo no era “saber cuál sector tiene más casos”, sino **encontrar dónde y por qué los problemas se repiten o agravan**.

---

## 2. Exploración y validación del dataset (ETL y análisis estructural)

Antes de aplicar cualquier modelo, realizamos un proceso completo de **ETL (Extracción, Transformación y Carga)** para garantizar la calidad de los datos.  

El ETL incluyó:
1. **Limpieza de texto:** eliminación de caracteres especiales, acentos y tildes.  
2. **Normalización de columnas:** nombres en formato `snake_case`, sin espacios ni símbolos.  
3. **Estandarización de valores vacíos:** uso de `NaN` en columnas numéricas y categóricas.  
4. **Conversión de tipos de datos:** por ejemplo, `edad` transformada a número entero.  
5. **Validación final:** revisión de filas incompletas, duplicados y rangos inválidos.

El resultado fue un dataset **totalmente limpio y listo para análisis**, guardado como `clean_data.csv`.

> ⚙️ Este paso nos permitió eliminar ambigüedades y asegurar que los resultados de la IA fueran confiables.  
> Desde este punto, no fue necesario volver a realizar limpieza ni reexploración.

---

## 3. Identificación de patrones e hipótesis de trabajo

Con el dataset limpio, comenzamos un análisis exploratorio sobre el contenido de los reportes ciudadanos.  
Detectamos tres hallazgos importantes:

- Los reportes **no estaban concentrados en un solo sector**, sino dispersos entre salud, educación, medio ambiente y seguridad.  
- Los **comentarios describían problemas similares con distintas palabras**, lo que hacía imposible analizarlos con métodos tradicionales.  
- Variables sociales como *acceso a internet* y *atención previa del gobierno* parecían influir en el **nivel de urgencia**.

A partir de esto formulamos la hipótesis central:

> 🧠 *“Podemos usar técnicas de Procesamiento del Lenguaje Natural (NLP) para agrupar los comentarios por similitud semántica y descubrir patrones de necesidad social relacionados con las condiciones de cada comunidad.”*

---

## 4. Construcción técnica de la solución

La solución se diseñó en **tres módulos principales**, integrados bajo una arquitectura limpia con **FastAPI**.

### 🧩 a. Módulo de IA semántica (texto)

- Se generaron **embeddings** vectoriales a partir de los comentarios.  
- Se aplicaron algoritmos de **clustering (KMeans o BERTopic)** para agrupar los reportes similares.  
- Cada grupo produjo **palabras clave representativas**, que permitieron interpretar los temas principales detectados por la IA.

### 🌍 b. Módulo de análisis social

- Los resultados del análisis semántico se cruzaron con variables sociales como:
  - `acceso_a_internet`
  - `atencion_previa_del_gobierno`
  - `zona_rural`
- Esto permitió descubrir correlaciones, por ejemplo:  
  > zonas rurales con bajo acceso a internet → mayores niveles de urgencia en salud o educación.

### ⚖️ c. Módulo de priorización (Índice de Impacto Social)

- Se construyó un **índice compuesto** que combina:
  - Frecuencia del tema en los reportes.  
  - Nivel promedio de urgencia.  
  - Condiciones sociales de la zona (falta de internet, ruralidad, etc.).  
- Este índice permite **clasificar automáticamente las regiones o problemáticas que requieren mayor atención** por parte de la ONG.

---

## 5. Validación de resultados

Para comprobar la coherencia del modelo, se realizaron validaciones cualitativas y cuantitativas:

- **Validación semántica:** revisión de los grupos creados por la IA para confirmar que los comentarios fueran similares en contexto.  
- **Verificación social:** comparación entre los temas detectados y las condiciones sociales de las comunidades.  
- **Consistencia del índice:** comprobación de que los puntajes altos coincidieran con situaciones reales de mayor urgencia.

> ✅ Los resultados demostraron que la IA era capaz de identificar patrones transversales (por ejemplo, contaminación, inseguridad, educación rural) de manera más eficiente que el análisis manual.

---

## 6. Preparación para el despliegue y demostración

Para la entrega del reto, se priorizó la **funcionalidad local y modular**, de modo que el proyecto pudiera ejecutarse sin conexión a internet ni dependencias externas pesadas.

Se implementó una API con **FastAPI**, que incluye:
- `/analyze` → analiza el dataset y devuelve los temas detectados.  
- `/impact` → calcula y muestra el índice de impacto social.

Además:
- Se documentó todo el flujo con **MkDocs**, permitiendo reproducir el proceso completo.  
- La estructura modular permite un despliegue futuro en **Render, Railway o Azure App Service** sin cambios en el código.

> 💬 “Actualmente la solución se ejecuta en local por razones de tiempo,  
> pero su arquitectura está lista para desplegarse en cualquier servicio web.”

---

## 7. Decisiones clave del proceso

| Etapa | Decisión tomada | Justificación |
|--------|----------------|----------------|
| Exploración | Mantener un enfoque multisectorial | La problemática social no está limitada a un solo campo. |
| Preparación de datos | Implementar ETL completo | Asegurar consistencia y calidad del dataset. |
| IA semántica | Usar embeddings + clustering | Detectar patrones sin etiquetas predefinidas. |
| Integración social | Cruzar con variables de conectividad y ruralidad | Contextualizar los hallazgos de la IA. |
| Despliegue | Ejecutar en local con FastAPI modular | Asegurar funcionalidad y rapidez para el reto. |

---

## 8. Cómo defender el proceso ante expertos

Si algún jurado o experto solicita justificación de decisiones, se puede responder con:

> “Ya realizamos la exploración y limpieza completa del dataset.  
> La elección del enfoque semántico se debe a que los comentarios son texto no estructurado.  
> Aplicamos IA para descubrir patrones y los cruzamos con variables sociales,  
> logrando priorizar zonas de alto impacto de forma objetiva y reproducible.”

Y si preguntan sobre despliegue:

> “Por tiempos del reto trabajamos en entorno local,  
> pero el backend con FastAPI y la estructura modular nos permiten desplegar en la nube fácilmente si el proyecto avanza a producción.”

---

## 9. Conclusión general

El proceso de construcción de la solución fue **iterativo, razonado y validado**.  
Pasamos de un dataset crudo y disperso a una herramienta de análisis social inteligente, capaz de transformar texto ciudadano en conocimiento accionable.

> En síntesis, **ComuniMind** usa IA para unir lo que la comunidad dice con los factores sociales que explican sus necesidades,  
> ayudando a la ONG a tomar decisiones basadas en datos reales y con impacto humano.

---
