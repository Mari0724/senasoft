# Arquitectura del Sistema

La aplicación se divide en módulos independientes que se integran al final del desarrollo.

app/
├── application/
│ ├── nlp_module/ ← Procesamiento de texto (IA Temática)
│ ├── social_module/ ← Análisis social (IA Social)
│ └── insight_service.py ← Integración final de resultados
├── api/
│ ├── routes.py ← Endpoints de FastAPI
│ └── templates/ ← Interfaz o visualización de resultados
├── data/
│ ├── original.csv ← Dataset original con información de comunidades
│ ├── themes.csv ← Resultados del módulo NLP
│ ├── social_results.csv ← Resultados del análisis social
│ └── final_results.csv ← Fusión final de ambos análisis

### Herramientas principales
- **FastAPI** para servicios REST.
- **Pandas / Scikit-learn** para análisis de datos.
- **Sentence-Transformers / BERTopic** para embeddings y clustering.
- **Matplotlib** para visualización.
- **MkDocs** para documentación profesional.
