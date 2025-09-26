# Makefile — Tesis_SIEM_ML
# Atajos para entorno y pipeline

# Configuración
VENV_DIR := .venv
PYTHON   := $(VENV_DIR)/bin/python
PIP      := $(VENV_DIR)/bin/pip

# Lista de notebooks (sin extensión)
NOTEBOOKS := Preprocessing2 Modelo2 prediccion_ataques2

.PHONY: help setup ensure-dirs kernel run ingest preprocess train predict dataset-doc hash freeze clean veryclean

## help: muestra esta ayuda
help:ß
	@echo "Comandos disponibles:"
	@echo "  make setup         -> crea venv e instala requirements"
	@echo "  make ensure-dirs   -> crea carpetas base (data/raw, processed, logs, ...)"
	@echo "  make kernel        -> registra el kernel Jupyter del venv"
	@echo "  make run           -> ejecuta el pipeline de notebooks con papermill"
	@echo "  make ingest        -> ejecuta src.ingest"
	@echo "  make preprocess    -> ejecuta src.preprocess"
	@echo "  make train         -> ejecuta src.train"
	@echo "  make predict       -> ejecuta src.predict"
	@echo "  make dataset-doc   -> genera docs/DATASET.md"
	@echo "  make hash          -> imprime SHA256 de data/raw"
	@echo "  make freeze        -> guarda versions exactas en requirements.lock.txt"
	@echo "  make clean         -> limpia outputs (processed, logs, executed nbs)"

## setup: crea venv e instala requirements
setup:
	python3 -m venv $(VENV_DIR)
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -r requirements.txt

## ensure-dirs: crea carpetas base
ensure-dirs:
	mkdir -p data/raw data/processed logs notebooks docs

## kernel: registra el kernel Jupyter del venv
kernel:
	$(PYTHON) -m ipykernel install --user --name tesis-venv --display-name "Python (tesis-venv)"

## run: ejecuta los 3 notebooks con papermill (ver src/run_pipeline.py)
run:
	$(PYTHON) -m src.run_pipeline

## ingest: corre la etapa de ingesta
ingest:
	$(PYTHON) -m src.ingest

## preprocess: corre la etapa de preprocesamiento
preprocess:
	$(PYTHON) -m src.preprocess

## train: corre la etapa de entrenamiento
train:
	$(PYTHON) -m src.train

## predict: corre la etapa de predicción
predict:
	$(PYTHON) -m src.predict

## dataset-doc: genera/actualiza docs/DATASET.md (requiere tools/generate_dataset_md.py)
dataset-doc:
	$(PYTHON) tools/generate_dataset_md.py

## hash: imprime SHA256 del directorio data/raw (control de integridad)
hash:
	$(PYTHON) - <<'PY'
from pathlib import Path
import os, hashlib
def sha256_dir(d):
    h=hashlib.sha256()
    d=Path(d)
    if d.exists():
        for root,_,files in os.walk(d):
            for f in sorted(files):
                with open(Path(root)/f,'rb') as fh:
                    for chunk in iter(lambda: fh.read(8192), b""): h.update(chunk)
    print("SHA256(data/raw) =", h.hexdigest())
sha256_dir("data/raw")
PY

## freeze: congela versiones exactas (para reproducibilidad total)
freeze:
	$(PIP) freeze > requirements.lock.txt

## clean: borra artefactos generados
clean:
	rm -rf data/processed/* logs/* notebooks/*.executed.ipynb

## veryclean: borra también la venv ( volverás a instalar dependencias)
veryclean: clean
	rm -rf $(VENV_DIR)
