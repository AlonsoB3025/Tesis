# src/ingest.py
import os
from src.utils import setup_logging, stamp_dir

RAW = "data/raw"

def main():
    log = setup_logging()
    log.info("Ingesta iniciada")
    files = [f for f in os.listdir(RAW) if not f.startswith(".")]
    log.info("Archivos encontrados en data/raw: %d", len(files))
    for f in files[:5]:
        log.info(" - %s", f)
    stamp_dir("data/_ingested")
    log.info("Ingesta finalizada OK")

if __name__ == "__main__":
    main()