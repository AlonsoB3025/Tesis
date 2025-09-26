# Backlog – Sprint de Inteligencia Artificial
## Proyecto de Tesis:
**Modelo Inteligente para Apoyo en la Correlación de Eventos en SIEM usando Machine Learning**

---

### Objetivo General del Sprint
Desarrollar un modelo base de clasificación que permita identificar, correlacionar y priorizar eventos registrados en un sistema SIEM, reduciendo falsos positivos y facilitando la detección de amenazas reales en entornos de red corporativos.

---

### Historias de usuario y backlog técnico

| N.º | Historia / Tarea                                                                 | Prioridad | Sprint Día |
|-----|-----------------------------------------------------------------------------------|-----------|------------|
| 1   | Como investigador, deseo definir claramente el objetivo del modelo               | Alta      | 1          |
| 2   | Como analista, necesito obtener logs de eventos realistas para entrenamiento     | Alta      | 2          |
| 3   | Como desarrollador, deseo construir un pipeline de carga y limpieza de datos     | Alta      | 3          |
| 4   | Como analista, deseo realizar un análisis exploratorio visual de los eventos     | Alta      | 4          |
| 5   | Como ingeniero, necesito entrenar un modelo de clasificación base                | Alta      | 5          |
| 6   | Como investigador, deseo evaluar y registrar métricas de desempeño del modelo    | Alta      | 6          |
| 7   | Como científico de datos, deseo registrar y versionar los resultados obtenidos   | Media     | 6          |

---

### Resultado Esperado del Sprint 

- Dataset cargado, procesado y versionado.
- Visualizaciones que revelen la distribución de tipos de eventos y anomalías.
- Entrenamiento y validación de un modelo base (`Random Forest`, `Decision Tree`, `Logistic Regression`).
- Registro de métricas clave: accuracy, precision, recall, F1-score.
- Carpeta `models/` con el modelo serializado.
- `results/` con gráficos, métricas y análisis.

---

### Tecnologías y herramientas previstas

- `Python 3.10+`
- `Pandas`, `Scikit-learn`, `Seaborn`, `Matplotlib`
- `Jupyter Notebook`
- Entorno de trabajo en VS Code
- Dataset: a determinar (logs reales o CICIDS/UNSW)

---

### Dataset Utilizado: Logs Antivirus Etiquetados

- **Nombre del archivo:** `Logs-antivirus_etiquetado.csv`  
- **Ubicación:** `data/raw/Logs-antivirus_etiquetado.csv`  
- **Descripción:** Contiene registros generados por un sistema antivirus, con eventos etiquetados como “virus” o “benigno”. Las columnas incluyen marca temporal, dirección IP origen/destino, tipo de evento, severidad y una etiqueta que indica la presencia de amenaza.  
- **Uso en el proyecto:** Este dataset es la base de la sección supervisada del modelo híbrido. Será empleado para entrenar clasificadores que identifiquen patrones asociados a ataques confirmados.  
- **Origen:** Recolectado y etiquetado internamente a partir de registros reales o simulados de un sistema SIEM.  
- **Fecha de inclusión:** 30/06/2025  
- **Tamaño aproximado:** [indicar número de registros y columnas si lo deseas]

---

### Notas adicionales

- Se recomienda registrar todos los pasos en un `notebook` nombrado según el sprint (`Sprint_IA_Modelo_Base_Comentado.ipynb`).
- El modelo desarrollado servirá como línea base para comparación con el modelo híbrido final.
