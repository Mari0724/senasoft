# Metodología Ágil

## Marco de trabajo: Scrum Adaptado

Dado que el equipo estuvo conformado por **dos integrantes**, se implementó una versión reducida de la metodología **Scrum**, conservando sus principios esenciales: trabajo colaborativo, iteraciones cortas (*sprints*) y mejora continua.

El desarrollo se realizó en **dos sprints principales de un día cada uno** y un **mini-sprint adicional** para la integración final con OpenAI y la validación de resultados.

---

## Roles del equipo

| Rol | Integrante | Responsabilidad |
|------|-------------|----------------|
| Scrum Master & Product Owner | **Emilia Gallo Alzate** & **María Ximena Marín Delgado** | Gestión del tiempo, definición de objetivos diarios, seguimiento de tareas y documentación. |
| **María Ximena Marín Delgado** | Integrante 1 | Desarrollo del módulo de **IA Temática (procesamiento de texto y sentimientos)**. |
| **Emilia Gallo Alzate** | Integrante 2 | Desarrollo del módulo de **IA Social**, cálculo del **índice de impacto** y creación de la **API con FastAPI**. |

> ⚙️ Ambas participaron en la planificación, documentación, pruebas y presentación final, garantizando una visión unificada del producto.

---

## Plan de Sprints

| Día / Sprint | María Ximena Marín Delgado (IA Texto) | Emilia Gallo Alzate (IA Social + API) |
|---------------|---------------------------------------|--------------------------------------|
| **Sprint 1 – Día 1 AM** | Limpieza de datos, normalización y generación de embeddings con MiniLM. | Exploración inicial del dataset y definición de endpoints base en FastAPI. |
| **Sprint 1 – Día 1 PM** | Agrupamiento de temas con K-Means y extracción de palabras clave con TF-IDF. | Cálculo de correlaciones sociales (internet, ruralidad, atención) y primeras visualizaciones. |
| **Sprint 2 – Día 2 AM** | Integración del modelo BETO para análisis de sentimientos. | Cálculo del índice de impacto social y clasificación por patrones sociales. |
| **Sprint 2 – Día 2 PM** | Exportación de `themes_nlp.csv` y validación de resultados. | Pruebas del endpoint `/impact` y generación del dashboard visual. |
| **Mini-Sprint – Integración final** | Revisión conjunta de outputs y redacción de la documentación técnica. | Implementación del módulo **OpenAI (asistente explicativo)** conectado al dashboard y validación final. |

---

## Beneficios del enfoque ágil

- Permitió **avanzar en paralelo** sin bloqueos entre los módulos de texto y social.  
- Fomentó la **autoorganización** y la toma de decisiones rápidas en cada iteración.  
- Facilitó la **integración progresiva** de todos los componentes (ETL, IA, API, dashboard y OpenAI).  
- Garantizó una **entrega funcional, documentada y validada** dentro del tiempo del reto.  
- El **mini-sprint de integración** permitió añadir valor extra al producto sin comprometer la estabilidad general.

---

> 💡 *Este enfoque ágil permitió mantener la velocidad de desarrollo sin perder la calidad técnica ni la coherencia entre módulos, dejando una base sólida para futuras ampliaciones o despliegues.*
