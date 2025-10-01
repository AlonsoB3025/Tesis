# src/utils.py
from __future__ import annotations

import os
import json
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Optional
import random

import numpy as np

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "pipeline.log"


def ensure_dir(path: str | Path) -> Path:
    """Crea el directorio si no existe y devuelve Path."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def get_logger(name: str = "pipeline", level: int = logging.INFO) -> logging.Logger:
    """
    Crea (o recupera) un logger con salida a archivo rotativo y a consola.
    Evita duplicar handlers cuando se llama múltiples veces.
    """
    ensure_dir(LOG_DIR)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Si ya tiene handlers, no agregamos de nuevo (evita logs duplicados).
    if logger.handlers:
        return logger

    # Formato uniforme
    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Archivo con rotación: 5 MB por archivo, 3 backups
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(fmt)
    file_handler.setLevel(level)

    # Consola/STDOUT
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(fmt)
    stream_handler.setLevel(level)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # Mensaje de arranque con sello de tiempo único
    logger.debug("Logger inicializado.")
    return logger


def save_json(obj: Dict[str, Any], path: str | Path) -> None:
    """Guarda un dict como JSON (UTF-8, pretty) y crea el directorio si no existe."""
    path = Path(path)
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def load_json(path: str | Path) -> Dict[str, Any]:
    """Carga un JSON a dict (si no existe, devuelve dict vacío)."""
    path = Path(path)
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def stamp_dir(path: str | Path, filename: str = "_SUCCESS") -> Path:
    """
    Crea un archivo marcador con timestamp ISO dentro de `path`.
    Útil para pipeline: indicar que una etapa concluyó correctamente.
    """
    path = ensure_dir(path)
    stamp_path = Path(path) / filename
    with stamp_path.open("w", encoding="utf-8") as f:
        f.write(datetime.now().isoformat())
    return stamp_path


def set_seed(seed: int = 42) -> None:
    """Fija semillas para reproducibilidad (numpy, random)."""
    np.random.seed(seed)
    random.seed(seed)
    try:
        import torch  # opcional: solo si lo tienes instalado
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True  # type: ignore[attr-defined]
        torch.backends.cudnn.benchmark = False     # type: ignore[attr-defined]
    except Exception:
        pass


def timeit(fn: Callable) -> Callable:
    """Decorador simple para medir tiempo de funciones y loguearlo."""
    import time

    def _wrap(*args, **kwargs):
        logger = get_logger(fn.__module__)
        start = time.time()
        try:
            return fn(*args, **kwargs)
        finally:
            elapsed = time.time() - start
            logger.info(f"{fn.__name__} terminó en {elapsed:.2f}s")

    return _wrap
