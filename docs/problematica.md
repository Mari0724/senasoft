# 🌍 Contexto y Justificación

## Contexto general

Durante el reto **SENASoft 2025 – Categoría Inteligencia Artificial**, se nos planteó desarrollar una solución con IA que ayudara a una **organización sin ánimo de lucro (ONG)** a comprender las problemáticas más relevantes de distintas comunidades en Colombia.  
El conjunto de datos proporcionado contenía información **diversa**, con reportes de necesidades en los sectores de **salud, educación, medio ambiente y seguridad**, junto con variables sociales como **acceso a internet**, **atención previa del gobierno** y **ubicación (rural o urbana)**.

---

## Detección de la problemática

Al analizar el dataset, identificamos que **la mayoría de los registros no estaban concentrados en un único sector**, sino distribuidos entre múltiples categorías y regiones.  
En lugar de reducir el alcance a un solo campo (por ejemplo, salud o educación), decidimos **abordar el reto desde una perspectiva integral**, para **no desperdiciar información valiosa ni ignorar patrones cruzados** entre diferentes problemáticas.

> 💡 Esto nos llevó a entender que el verdadero problema no era “qué sector tiene más casos”, sino **cómo la ONG puede identificar en qué lugares y temas enfocar sus esfuerzos y recursos**, considerando además los factores sociales y emocionales asociados.

---

## Justificación de la solución

La solución propuesta permite a la ONG **analizar miles de comentarios y reportes ciudadanos de manera automatizada**, utilizando modelos de Inteligencia Artificial que combinan varias capas de análisis:

- **Análisis semántico (MiniLM + K-Means)** para agrupar los comentarios en temas o patrones comunes sin necesidad de etiquetas previas.  
- **Análisis emocional (modelo BETO)** para detectar el tono general de los mensajes (positivo, negativo o neutro), permitiendo identificar la percepción ciudadana frente a cada situación.  
- **Análisis social estructural** para cruzar los hallazgos de la IA con variables como conectividad, atención gubernamental y ruralidad.  
- **Asistencia con IA generativa (OpenAI)** para explicar los resultados del dashboard y ofrecer recomendaciones automáticas a la ONG de forma empática y comprensible.

De este modo, la herramienta ayuda a **priorizar las zonas y temáticas donde la intervención tendría mayor impacto social**, optimizando la toma de decisiones de la organización con base en evidencia y datos reales.

---

## Enfoque multisectorial

En lugar de limitar el análisis a un solo campo, nuestra propuesta **trabaja con todas las categorías del dataset (salud, educación, medio ambiente y seguridad)**, utilizando técnicas de clasificación, resumen y correlación para **agrupar los problemas más frecuentes en cada comunidad**.

Esto ofrece una **visión completa del panorama social**, facilitando que la ONG:
- Dirija recursos de forma más estratégica.  
- Compare tendencias entre sectores.  
- Detecte correlaciones entre factores, por ejemplo:  
  > baja conectividad + alta urgencia + sentimiento negativo = prioridad de intervención.

Este enfoque integral permite comprender las causas y no solo los síntomas de los problemas sociales.

---

## Impacto esperado

La solución aporta valor directo a la ONG al:
- Reducir el tiempo necesario para analizar información textual extensa.  
- Priorizar acciones con base en datos reales y verificados.  
- Incorporar el análisis emocional y contextual para mejorar la interpretación de los hallazgos.  
- Promover una **gestión social inteligente**, apoyada en IA, datos abiertos y ética tecnológica.

Además, genera un **impacto indirecto en la comunidad**, al permitir que los esfuerzos de ayuda lleguen más rápido a los lugares donde realmente se necesitan, con estrategias basadas en evidencia y sensibilidad social.

---

> En síntesis, **nuestra solución no se enfoca en un solo sector porque la problemática social no lo está**.  
> **CivIA** convierte los datos dispersos de la comunidad en conocimiento útil y humano, utilizando IA para conectar la voz ciudadana con las condiciones sociales que explican sus necesidades.  

📘 *Una explicación detallada de los modelos, módulos y procesos técnicos se encuentra en el archivo* [`proceso_solucion.md`](proceso_solucion.md), *donde se documenta paso a paso el desarrollo completo de la solución.*

---
