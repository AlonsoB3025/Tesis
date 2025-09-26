# Track A — Elastic SIEM + Machine Learning (Tesis)

Este repositorio contiene la estructura mínima reproducible para la parte Track A de la tesis. 
Integra los cuadernos Jupyter ya desarrollados con un pipeline automatizado y documentación del dataset.

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
