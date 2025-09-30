# Aplicación de técnicas de Machine Learning para la detección de incidentes de ciberseguridad en un SIEM basado en Elastic

Proyecto de investigación (Maestría en IA – UNI) para desarrollar un modelo de machine learning que, a partir de los logs recolectados por los agentes desplegados en un SIEM de Elastic, permita detectar y clasificar incidentes de ciberseguridad, mejorando la capacidad de identificación temprana de amenazas y reduciendo los falsos positivos.

---

# Estructura del repositorio

```text
data/
  ├─ raw/         # Logs originales
  └─ processed/   # Datos procesados y features
notebooks/
  ├─ Preprocessing2.ipynb
  ├─ Modelo2.ipynb
  └─ prediccion_ataques2.ipynb
src/              # Código Python (scripts ejecutables)
  ├─ preprocess.py
  ├─ train.py
  ├─ predict.py
  └─ run_pipeline.py
docs/
  ├─ DATASET.md          # Documentación del dataset
logs/
requirements.txt
.env.example
```

---

# Instrucciones rápidas

1. # Configurar entorno
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate    # Windows
   pip install -U pip
   pip install -r requirements.txt
   cp .env.example .env
   ```

2. # Agregar notebooks
   Copiar los notebooks reales dentro de `notebooks/` con estos nombres exactos:
   - `Preprocessing2.ipynb`
   - `Modelo2.ipynb`
   - `prediccion_ataques2.ipynb`

3. # Colocar datos
   Copiar los datos crudos en `data/raw/`.

4. # Ejecutar pipeline completo
   ```bash
   python -m src.run_pipeline
   ```
   o paso a paso con:
   ```bash
   make ingest
   make preprocess
   make train
   make predict
   ```

---

## Documentación del dataset

- Toda la información sobre la procedencia, variables y control de integridad de los datos debe registrarse en `docs/DATASET.md`.  
- Para calcular el hash del directorio `data/raw/` ejecutar:
  ```bash
  make hash
  ```
  y copiar el valor SHA256 al documento.

---

## Roadmap

En `docs/ROADMAP_SPRINT1.md` se encuentra el plan de trabajo para esta entrega de Track A:
- Subir notebooks finales a `notebooks/`
- Completar `docs/DATASET.md`
- Ejecutar el pipeline de inicio a fin
- Generar artefactos y logs
- Documentar el hash del dataset

---

## Reproducibilidad garantizada

- Dependencias declaradas en `requirements.txt`
- Ejecución de notebooks mediante `papermill`
- Logs centralizados en `logs/pipeline.log`
- Dataset con hash de integridad
