# src/utils.py
import os, json, logging
from datetime import datetime

LOG_PATH = "logs/pipeline.log"

def setup_logging():
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()]
    )
    return logging.getLogger("pipeline")

def save_json(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def stamp_dir(path):
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "_SUCCESS"), "w") as f:
        f.write(datetime.now().isoformat())
