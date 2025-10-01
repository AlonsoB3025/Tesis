# src/run_pipeline.py
from __future__ import annotations

from pathlib import Path
from datetime import datetime
import papermill as pm

from src.utils import get_logger, save_json, stamp_dir
from src.features.preprocess import prepare_dataset
from src.models.baseline import fit_and_eval

# Directorios y orden de notebooks
NB_DIR = Path("notebooks")
EXEC_DIR = NB_DIR / "_executed"
ORDER = []

# Parámetros que tus notebooks pueden leer (si no los usan, no pasa nada)
PARAMS = {
    "RAW_DIR": "data/raw/",
    "PROCESSED_DIR": "data/processed/",
    "RANDOM_STATE": 42
}


def run_notebook(name: str) -> Path | None:
    from pathlib import Path
    from datetime import datetime
    import papermill as pm
    from src.utils import get_logger

    log = get_logger("pipeline")
    NB_DIR = Path("notebooks")
    EXEC_DIR = NB_DIR / "_executed"

    infile = NB_DIR / f"{name}.ipynb"
    if not infile.exists():
        log.warning("No encontrado notebook %s (saltando)", infile)
        return None

    EXEC_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = EXEC_DIR / f"{name}.{ts}.executed.ipynb"

    try:
        pm.execute_notebook(
            str(infile),
            str(outfile),
            parameters=PARAMS,
            report_mode=True,
            kernel_name="python3"  # <--- fuerza kernel
        )
        log.info("Ejecutado: %s → %s", infile, outfile)
        return outfile
    except Exception as e:
        log.exception("Fallo ejecutando %s: %s", infile, e)
        return None


def main():
    log = get_logger("pipeline")
    log.info("=== PIPELINE (notebooks + baseline) INICIADO ===")

    # 1) Ejecutar notebooks en orden (solo los que existan)
    executed = []
    for nb in ORDER:
        out = run_notebook(nb)
        if out:
            executed.append(str(out))

    try:
        df, clean_path = prepare_dataset()
        log.info("Dataset limpio generado: %s (shape=%s)", clean_path, df.shape)
    except AssertionError as e:
        log.warning("No se pudo preparar dataset automáticamente: %s", e)
        clean_path = Path("data/processed/dataset_clean.csv")
        if not clean_path.exists():
            log.error("No existe %s. Genera este archivo desde tu notebook de EDA.", clean_path)
            return

    # 3) Entrenar y evaluar baseline (usa split temporal si hay timestamp)
    metrics = fit_and_eval(path_csv=str(clean_path), use_temporal=True)
    save_json(metrics, "reports/metrics/baseline_metrics.json")
    stamp_dir("reports/metrics")
    log.info("Métricas baseline: %s", metrics)

    log.info("=== PIPELINE FINALIZADO ===")


if __name__ == "__main__":
    main()
