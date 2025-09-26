# src/train.py
import os, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import classification_report
import joblib
from src.utils import setup_logging, save_json, stamp_dir

PROC = "data/processed"

def main():
    log = setup_logging()
    log.info("Entrenamiento iniciado")
    feats = os.path.join(PROC, "features.parquet")
    if not os.path.exists(feats):
        log.warning("No existe %s. ¿Ejecutaste preprocess?", feats)
        return

    df = pd.read_parquet(feats)

    # DEMO: si tienes label/etiqueta_binaria úsalo; si no, hace un unsupervised simple
    models_dir = os.path.join(PROC, "models"); os.makedirs(models_dir, exist_ok=True)

    if "etiqueta_binaria" in df.columns:
        y = df["etiqueta_binaria"].astype(int)
        X = df.drop(columns=["etiqueta_binaria"])
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        clf = RandomForestClassifier(n_estimators=150, random_state=42, n_jobs=-1)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        joblib.dump(clf, os.path.join(models_dir, "rf_supervisado.pkl"))
        rep = classification_report(y_test, y_pred, output_dict=True)
        save_json(rep, os.path.join(models_dir, "rf_supervisado_metrics.json"))
        log.info("Modelo supervisado y métricas guardadas.")
    else:
        iso = IsolationForest(random_state=42, n_estimators=150)
        iso.fit(df.select_dtypes(include=["number"]).fillna(0))
        joblib.dump(iso, os.path.join(models_dir, "if_unsupervisado.pkl"))
        log.info("Modelo no supervisado guardado.")

    stamp_dir(os.path.join(PROC, "_trained"))
    log.info("Entrenamiento finalizado OK")

if __name__ == "__main__":
    main()
