# src/preprocess.py
import os, pandas as pd
from glob import glob
from src.utils import setup_logging, stamp_dir

RAW, PROC = "data/raw", "data/processed"

def main():
    log = setup_logging()
    log.info("Preprocesamiento iniciado")
    os.makedirs(PROC, exist_ok=True)

    # Ejemplo: unir algunas columnas comunes si existen
    sample_files = glob(os.path.join(RAW, "*.csv"))
    if not sample_files:
        log.warning("No se hallaron CSV en data/raw")
    else:
        # Cargar un CSV grande a modo de demo (ajusta a tu realidad)
        df = pd.read_csv(sample_files[0], low_memory=False)
        log.info("Archivo base: %s | filas=%s, cols=%s", os.path.basename(sample_files[0]), len(df), len(df.columns))

        # Normaliza timestamp si existe
        if "@timestamp" in df.columns:
            df["@timestamp"] = pd.to_datetime(df["@timestamp"], errors="coerce")

        # Guarda features mínimas (ajústalo a tu notebook)
        out = os.path.join(PROC, "features.parquet")
        df.to_parquet(out, index=False)
        log.info("Features guardadas en %s", out)

    stamp_dir(os.path.join(PROC, "_preprocessed"))
    log.info("Preprocesamiento finalizado OK")

if __name__ == "__main__":
    main()