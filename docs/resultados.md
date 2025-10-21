# Resultados

- `themes.csv` con los temas y palabras clave más frecuentes.
- `social_results.csv` con correlaciones sociales.
- `final_results.csv` integrando ambos análisis.
- API `/impact` para consulta final del índice social.
- Dashboard con visualización de resultados.

**Visualización final:**
```python
themes = pd.read_csv('data/themes.csv')
social = pd.read_csv('data/original.csv')
merged = social.merge(themes, on='Ciudad', how='left')
