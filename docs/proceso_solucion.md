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

La solución se diseñó en **cuatro módulos principales**, integrados bajo una arquitectura limpia con **FastAPI**.

---

### 🧩 a. Módulo de IA semántica (texto)

- Se generaron **embeddings vectoriales** a partir de los comentarios limpios utilizando el modelo **SentenceTransformer “all-MiniLM-L6-v2”**, especializado en análisis semántico.  
- Se aplicó el algoritmo **K-Means** para **agrupar los reportes según similitud temática**, obteniendo **seis clústeres principales**.  
- A cada grupo se le extrajeron sus **palabras clave representativas** mediante **TF-IDF**, lo que permitió identificar los temas sociales más mencionados por las comunidades.  
- Además, se integró un análisis de **sentimientos con el modelo en español BETO** (*pysentimiento/robertuito-sentiment-analysis*), clasificando los comentarios en **positivo, negativo o neutro**, junto con sus probabilidades.

---

### 🌍 b. Módulo de análisis social

- Se diseñó un proceso de **normalización y evaluación social** para medir la vulnerabilidad estructural de las comunidades, considerando los factores:  
  - `acceso_a_internet`  
  - `atencion_previa_del_gobierno`  
  - `zona_rural`  
  - `nivel_de_urgencia`  
- Cada variable se transformó a un rango **[0–1]**, garantizando comparabilidad entre distintos indicadores.  
- El **índice de vulnerabilidad** se calculó mediante una combinación ponderada de factores estructurales, definida así:  
  - **Falta de acceso a internet (40 %)**: se le otorgó mayor peso porque representa una barrera transversal que limita el acceso a educación, salud y participación ciudadana, impactando directamente en el desarrollo social.  
  - **Ausencia de atención previa del gobierno (30 %)**: refleja la falta de intervención institucional y, por tanto, el nivel de abandono o rezago histórico de la comunidad.  
  - **Condición rural (30 %)**: se asoció con menor acceso a infraestructura y servicios, además de mayor dispersión poblacional, lo cual incrementa la vulnerabilidad estructural.  
- Con estos factores, se identificaron patrones territoriales a partir de cuantiles estadísticos dinámicos (percentil 65 o mediana según el tamaño del conjunto).  
- De este modo, las ciudades se clasificaron en cuatro **patrones sociales**:  
  - **Zona crítica** → alta vulnerabilidad y alta urgencia.  
  - **Zona invisible** → alta vulnerabilidad pero urgencia baja (riesgo latente).  
  - **Zona puntual** → baja vulnerabilidad pero urgencia alta (evento no estructural).  
  - **Estable** → condiciones equilibradas y sostenibles.  
- Este enfoque permitió representar cuantitativamente la realidad social de cada ciudad y **priorizar regiones donde las brechas estructurales son más profundas**.

---

### ⚖️ c. Módulo de priorización (Índice de Impacto Social)

- A partir de los resultados anteriores, se construyó un **índice compuesto de impacto social**, integrando en un solo valor los factores de vulnerabilidad, urgencia y acceso.  
- Cada componente se ponderó según su **capacidad de incidir en la calidad de vida y en la necesidad de intervención institucional**, de la siguiente forma:  
  - **Vulnerabilidad estructural (35 %)**: concentra los elementos sociales más difíciles de revertir a corto plazo, por lo tanto, es el factor más determinante.  
  - **Nivel de urgencia (25 %)**: refleja la presión inmediata que vive la comunidad y orienta la prioridad de atención.  
  - **Acceso a internet (20 %)**: un factor clave para el desarrollo educativo, laboral y social; su ausencia agrava el impacto.  
  - **Atención previa del gobierno (10 %)**: indica la continuidad o abandono en la respuesta institucional.  
  - **Ruralidad (10 %)**: mantiene un peso relevante por las dificultades logísticas y estructurales de intervención.  
- El resultado final genera un **valor entre 0 y 1** por ciudad, donde 1 representa el mayor nivel de impacto social.  
- Este índice permitió **jerarquizar automáticamente las regiones más vulnerables** y se visualizó en un gráfico de barras horizontal, donde los colores comunican el tipo de patrón social:  
  - 🔴 *Zona crítica* → `#E63946`  
  - 🟡 *Zona invisible* → `#F4D35E`  
  - 🟠 *Zona puntual* → `#F29E38`  
  - 🟢 *Estable* → `#35DBB8`  
- La gráfica se exporta automáticamente como `data/visuals/impact_chart.png`, integrándose dentro del dashboard principal como un resumen visual del impacto social total.
- Los porcentajes asignados fueron determinados mediante una combinación de análisis exploratorio, criterio social y validación empírica.
En particular, las variables ruralidad y atención previa del gobierno recibieron un peso del 10 % tras observar su alta correlación con otros factores estructurales, lo que evitó duplicar su influencia en el índice.
Este valor se mantuvo tras varias pruebas, al comprobar que ofrecía una distribución equilibrada de impacto social entre las ciudades y una mejor interpretación visual del ranking.

---

### 💬 d. Módulo de asistencia con IA (OpenAI)

- Se desarrolló un componente de **asistencia inteligente** que conecta la aplicación con la **API de OpenAI (ChatGPT)**, a través de un *gateway* propio.  
- Este módulo integra la información proveniente de los dos análisis previos:  
  - El archivo **`impact_social.csv`**, que contiene los resultados del índice de vulnerabilidad, urgencia y clasificación por patrones sociales.  
  - El archivo **`themes_nlp.csv`**, que almacena los resultados semánticos y de sentimientos generados por el modelo BETO.  
- A partir de estos datos, el sistema construye un **prompt contextual dinámico**, que resume los indicadores principales (vulnerabilidad, urgencia, zonas críticas, sentimientos, categorías dominantes, etc.) y los envía al modelo de OpenAI.  
- La IA genera una **explicación automática y empática** que cumple tres funciones principales:
  1. **Interpretar** la situación general detectada en los datos (por ejemplo, explicar por qué una ciudad aparece como zona crítica).  
  2. **Traducir resultados técnicos a lenguaje social accesible**, permitiendo que los usuarios de una ONG comprendan los hallazgos sin conocimientos de IA.  
  3. **Ofrecer recomendaciones concretas** de acción social, finalizando siempre con un párrafo iniciando con:  
     > “Por esto te recomendamos…”  
     que sugiere una medida prioritaria basada en los datos.  
- Este módulo se activa desde el dashboard mediante el botón **“IA Explícame”**, que ejecuta la función `generar_explicacion_desde_csv()`.  
- La función combina automáticamente los indicadores sociales y semánticos, genera el resumen y devuelve el texto listo para mostrar en la interfaz, proporcionando una **interacción conversacional entre la IA y el usuario humano**.

---

## 5. Validación de resultados

Para comprobar la coherencia del modelo, se realizaron validaciones cualitativas y cuantitativas:

- **Validación semántica:** revisión de los grupos creados por la IA para confirmar que los comentarios fueran similares en contexto.  
- **Verificación social:** comparación entre los temas detectados y las condiciones sociales de las comunidades.  
- **Consistencia del índice:** comprobación de que los puntajes altos coincidieran con situaciones reales de mayor urgencia.

> ✅ Los resultados demostraron que la IA era capaz de identificar patrones transversales (por ejemplo, contaminación, inseguridad, educación rural) de manera más eficiente que el análisis manual.

---

---

## 6. Preparación para el despliegue y demostración

Para la entrega del reto se priorizó la **funcionalidad local y la estabilidad del sistema**, de modo que toda la solución pudiera ejecutarse sin conexión a internet y sin depender de servicios externos.

Se implementó una API con **FastAPI**, que permite ejecutar los procesos de análisis directamente en el entorno local.  
Las rutas principales fueron:  
- `/analyze` → analiza el dataset y devuelve los temas detectados por el modelo semántico.  
- `/impact` → calcula el índice de impacto social y genera las visualizaciones correspondientes.

Además:
- La **documentación completa del proyecto** se elaboró con **MkDocs** y fue **desplegada en GitHub Pages** como soporte técnico del trabajo:  
  👉 [https://mari0724.github.io/senasoft/](https://mari0724.github.io/senasoft/)  
- El resto de componentes (API, análisis de datos, modelo semántico, análisis social y módulo OpenAI) se ejecutan **totalmente en local**, manteniendo una estructura modular que facilita su comprensión y posible despliegue futuro.  
- Por razones de tiempo y del alcance del reto, **no se realizó despliegue en la nube**, aunque la arquitectura del proyecto quedó organizada para permitirlo si fuera necesario más adelante.

> 💬 “Actualmente la solución se ejecuta en local,  
> pero la documentación técnica fue publicada en GitHub Pages como evidencia del proceso completo.”

---

## 7. Decisiones clave del proceso

| Etapa | Decisión tomada | Justificación |
|--------|-----------------|----------------|
| Exploración | Mantener un enfoque multisectorial (educación, salud, medio ambiente, seguridad) | La información de la ONG abarcaba distintos temas y limitar el modelo a un solo sector hubiera reducido su utilidad. |
| Preparación de datos | Implementar un proceso ETL completo (limpieza, normalización y carga) | Aseguró la consistencia del dataset y permitió combinar fuentes sociales y textuales sin errores. |
| IA semántica | Usar embeddings con **MiniLM** y clustering con **K-Means** | Detectar patrones temáticos en los comentarios sin etiquetas predefinidas, aprovechando relaciones semánticas. |
| Análisis emocional | Integrar el modelo **BETO (pysentimiento)** | Identificar el tono emocional de los reportes y agregar una dimensión cualitativa a los temas detectados. |
| Integración social | Cruzar los resultados de la IA con variables de conectividad, ruralidad y atención institucional | Contextualizar los hallazgos temáticos con condiciones reales de las comunidades. |
| Priorización | Diseñar un **índice de impacto social ponderado** | Jerarquizar las zonas según vulnerabilidad, urgencia y condiciones estructurales. |
| Asistencia IA | Conectar con **OpenAI (ChatGPT)** mediante un gateway | Generar explicaciones automáticas y recomendaciones empáticas basadas en los resultados del dashboard. |
| Documentación | Desplegar la documentación en **GitHub Pages con MkDocs** | Dejar evidencia accesible del proceso técnico sin requerir despliegue completo del sistema. |
| Despliegue | Ejecutar todo el sistema en entorno **local con FastAPI modular** | Asegurar estabilidad, compatibilidad y rapidez dentro del tiempo del reto. |

---

## 8. Conclusión general

El desarrollo de la solución fue un proceso **iterativo, razonado y validado**, donde cada módulo se diseñó con un propósito claro y complementario.  
A partir de un dataset inicial crudo y heterogéneo, se logró construir una herramienta de **analítica social inteligente**, capaz de integrar modelos semánticos, análisis emocional y factores estructurales de vulnerabilidad.

**CivIA** representa una aplicación práctica y ética de la Inteligencia Artificial: transforma los comentarios de las comunidades en **conocimiento útil y accionable**, revelando no solo *qué* problemas existen, sino también *por qué* y *dónde* deben atenderse primero.  

> En síntesis, la solución conecta la voz ciudadana con los indicadores sociales que la explican,  
> ayudando a las ONG a **tomar decisiones basadas en datos reales, comprensión emocional y evidencia territorial**,  
> siempre con enfoque humano y de impacto positivo.

---
