# src/run_pipeline.py
import os, papermill as pm
from src.utils import setup_logging

NB_DIR = "notebooks"
ORDER = ["Preprocessing2", "Modelado2", "prediccion_ataques2"]

PARAMS = {
    "RAW_DIR": "data/raw",
    "PROCESSED_DIR": "data/processed",
    "RANDOM_STATE": 42
}

def run_notebook(name):
    infile  = os.path.join(NB_DIR, f"{name}.ipynb")
    outfile = os.path.join(NB_DIR, f"{name}.executed.ipynb")
    pm.execute_notebook(infile, outfile, parameters=PARAMS)

def main():
    log = setup_logging()
    log.info("=== PIPELINE (notebooks) INICIADO ===")
    for nb in ORDER:
        path = os.path.join(NB_DIR, f"{nb}.ipynb")
        if os.path.exists(path):
            log.info("Ejecutando: %s", path)
            run_notebook(nb)
        else:
            log.warning("No encontrado: %s (saltando)", path)
    log.info("=== PIPELINE (notebooks) FINALIZADO ===")

if __name__ == "__main__":
    main()