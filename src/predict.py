# src/predict.py
import os, pandas as pd, joblib
from glob import glob
from src.utils import setup_logging, stamp_dir

PROC = "data/processed"

def main():
    log = setup_logging()
    log.info("Predicción iniciada")

    feats = os.path.join(PROC, "features.parquet")
    if not os.path.exists(feats):
        log.warning("No existe %s. ¿Ejecutaste preprocess?", feats)
        return
    X = pd.read_parquet(feats).select_dtypes(include=["number"]).fillna(0)

    preds_dir = os.path.join(PROC, "predictions"); os.makedirs(preds_dir, exist_ok=True)

    # Busca cualquier modelo entrenado y predice
    for mdl_path in glob(os.path.join(PROC, "models", "*.pkl")):
        mdl = joblib.load(mdl_path)
        yhat = None
        if hasattr(mdl, "predict"):
            yhat = mdl.predict(X)
        elif hasattr(mdl, "predict_proba"):
            yhat = mdl.predict_proba(X)[:, 1]

        if yhat is not None:
            base = os.path.splitext(os.path.basename(mdl_path))[0]
            out = os.path.join(preds_dir, f"{base}_predicciones.csv")
            pd.DataFrame({"pred": yhat}).to_csv(out, index=False)
            log.info("Predicciones guardadas: %s", out)

    stamp_dir(os.path.join(PROC, "_predicted"))
    log.info("Predicción finalizada OK")

if __name__ == "__main__":
    main()