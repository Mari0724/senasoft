# 🧩 Arquitectura del Sistema

La aplicación se estructura bajo una **arquitectura modular inspirada en el modelo hexagonal (Ports and Adapters)**, donde cada capa cumple una responsabilidad específica y puede evolucionar de forma independiente.

---

## 📁 Estructura general del proyecto

```
SENASOFT/
├── app/
│   ├── api/
│   │   └── routes.py                 ← Endpoints principales de FastAPI
│   │
│   ├── application/                  ← Lógica de negocio y servicios de IA
│   │   └── openai_gateway.py         ← Conexión con la API de OpenAI (asistente explicativo)
│   │
│   ├── core/                         ← Servicios internos y utilidades generales
│   │
│   └── infrastructure/               ← Capa de infraestructura (salida y persistencia)
│       └── visuals/                  ← Generación y almacenamiento de gráficas
│
├── data/
│   ├── reports/                      ← Archivos de reportes generados
│   ├── visuals/                      ← Visualizaciones exportadas automáticamente
│   ├── original.csv                  ← Dataset original entregado por la ONG
│   ├── clean_data.csv                ← Datos limpios tras el proceso ETL
│   ├── themes_nlp.csv                ← Resultados del módulo semántico (MiniLM + BETO)
│   ├── impact_social.csv             ← Resultados del análisis social y priorización
│   └── final_results.csv             ← Unión final de análisis semántico y social
│
├── docs/                             ← Documentación técnica (MkDocs)
│   ├── problematica.md
│   ├── proceso_solucion.md
│   ├── conclusiones.md
│   └── FORMATO_ANALITICA_DE_DATOS_SENASOFT_v4.pdf
│
├── frontend/                         ← Carpeta destinada al prototipo visual del dashboard (React/TypeScript)
│
├── visuals/                          ← Imágenes generadas durante las pruebas
│
├── main.py                           ← Punto de entrada principal de la aplicación FastAPI
├── run.py                            ← Script de ejecución local
├── mkdocs.yml                        ← Configuración de la documentación en MkDocs
├── requirements.txt                  ← Dependencias del entorno virtual
├── .gitignore                        ← Archivos y carpetas excluidos del control de versiones
└── .env                              ← Variables de entorno locales

```

---

## ⚙️ Componentes principales

### 🧠 Capa de Aplicación (`app/application/`)
Contiene la lógica principal del sistema:
- Procesamiento **semántico y emocional** mediante *MiniLM* y *BETO*.
- Cálculo del **índice de impacto social** a partir de vulnerabilidad, urgencia y condiciones estructurales.
- Conexión con **OpenAI (ChatGPT)** para generar explicaciones automáticas del dashboard.

---

### 🌐 Capa de API (`app/api/`)
Define los endpoints REST implementados con **FastAPI**:
- `/analyze` → ejecuta el pipeline de análisis semántico.  
- `/impact` → calcula el índice de impacto social y genera visualizaciones.  

Esta capa actúa como **puerto de entrada** dentro del modelo hexagonal.

---

### 🏗️ Capa de Infraestructura (`app/infrastructure/`)
Incluye los **adaptadores de salida** del sistema:
- Generación de gráficos y reportes en la carpeta `visuals/`.
- Preparada para integrar almacenamiento externo o servicios adicionales en el futuro.

---

### 📊 Capa de Datos (`/data`)
Centraliza todos los archivos del flujo analítico:
- Desde `original.csv` (datos crudos) hasta `final_results.csv` (resultado fusionado).  
- Permite reproducir todo el pipeline sin conexión a internet.

---

### 🧾 Capa de Documentación (`/docs`)
Contiene toda la documentación técnica y de proceso elaborada en **Markdown** y publicada con **MkDocs** en GitHub Pages:  
[https://mari0724.github.io/senasoft/](https://mari0724.github.io/senasoft/)  
Incluye tanto la descripción técnica como el **formato oficial del SENA**.

---

## 🧱 Principios de diseño

- **Separación de responsabilidades:** cada módulo cumple una función clara y aislada.  
- **Arquitectura extensible:** se pueden agregar nuevos modelos o endpoints sin alterar la base.  
- **Ejecución modular en local:** cada componente puede probarse por separado.  
- **Escalabilidad futura:** lista para migrar a un despliegue en la nube si se requiere.  

---

> 💡 *Esta estructura modular permitió mantener orden, trazabilidad y escalabilidad en la solución CivIA, siguiendo los principios del diseño hexagonal adaptados al contexto del reto SENASoft 2025.*
```