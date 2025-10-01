# src/models/baseline.py
from pathlib import Path
import json, joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    roc_auc_score, f1_score, accuracy_score,
    precision_recall_curve, roc_curve, confusion_matrix
)

from src.features.preprocess import build_preprocess
from src.utils import get_logger

# ======== CONFIGURACIÓN (ajusta si lo necesitas) ========
TARGET   = "action"          # <- tu columna objetivo real
TIME_COL = "timestamp"       # <- pon None si no tienes tiempo
POS_LABEL = "credential-manager-credentials-were-read"   # <- clase positiva
CSV_IN   = "data/processed/dataset_clean.csv"
# ========================================================


def _temporal_split(df: pd.DataFrame, months_test: int = 1):
    """Split temporal simple: último 'months_test' mes(es) como test. Fallback a aleatorio si no hay tiempo válido."""
    log = get_logger("baseline")
    if not TIME_COL or TIME_COL not in df.columns:
        log.warning("TIME_COL no está definido o no existe en el dataset. Usando split aleatorio.")
        return _random_split(df)

    d = df.copy()
    d[TIME_COL] = pd.to_datetime(d[TIME_COL], errors="coerce", utc=True)
    d = d.sort_values(TIME_COL)
    if d[TIME_COL].isna().all():
        log.warning("No se pudo parsear %s como datetime. Usando split aleatorio.", TIME_COL)
        return _random_split(df)

    cutoff = d[TIME_COL].max() - pd.DateOffset(months=months_test)
    train_df = d[d[TIME_COL] <= cutoff]
    test_df  = d[d[TIME_COL] >  cutoff]

    # Si por algún motivo queda vacío, cae a aleatorio
    if train_df.empty or test_df.empty:
        log.warning("Split temporal produjo conjuntos vacíos. Usando split aleatorio.")
        return _random_split(df)

    X_train, y_train = train_df.drop(columns=[TARGET]), train_df[TARGET]
    X_test,  y_test  = test_df.drop(columns=[TARGET]),  test_df[TARGET]
    log.info("Temporal split -> train=%s, test=%s (cutoff=%s)", len(train_df), len(test_df), cutoff.date())
    return X_train, X_test, y_train, y_test


def _random_split(df: pd.DataFrame, test_size: float = 0.2, seed: int = 42):
    """Split aleatorio estratificado si aplica."""
    X = df.drop(columns=[TARGET])
    y = df[TARGET]
    strat = y if y.nunique() <= 20 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=seed, stratify=strat
    )
    log = get_logger("baseline")
    log.info("Random split -> train=%s, test=%s", len(y_train), len(y_test))
    return X_train, X_test, y_train, y_test


def _binarize_target(df: pd.DataFrame):
    """
    Convierte TARGET a binario:
    - 1 si action == POS_LABEL
    - 0 en caso contrario
    Si POS_LABEL no está en los datos, usa como positiva la clase menos frecuente.
    """
    log = get_logger("baseline")
    if TARGET not in df.columns:
        raise AssertionError(f"Columna objetivo '{TARGET}' no encontrada")

    # Asegura que trabajamos como string para comparar
    labels = df[TARGET].astype(str)
    uniques = set(labels.unique())

    pos_label = POS_LABEL
    if pos_label not in uniques:
        # Fallback: tomar la clase menos frecuente como positiva
        vc = labels.value_counts()
        pos_label = vc.index[-1]
        log.warning("POS_LABEL '%s' no está en los datos. Usando '%s' (clase menos frecuente) como positiva.",
                    POS_LABEL, pos_label)

    df[TARGET] = (labels == pos_label).astype(int)

    # Validación: deben existir ambas clases
    nunique = df[TARGET].nunique()
    if nunique < 2:
        raise ValueError(
            f"Tras binarizar no hay ambas clases (nunique={nunique}). "
            f"Revisa POS_LABEL='{POS_LABEL}' y la distribución original de '{TARGET}'."
        )

    # Log de distribución
    vc_bin = df[TARGET].value_counts()
    log.info("Distribución de y tras binarizar (%s=1): %s", pos_label, dict(vc_bin))


def fit_and_eval(path_csv: str = CSV_IN, use_temporal: bool = True):
    """
    Lee el dataset limpio, binariza la etiqueta, separa train/test,
    entrena Logistic Regression y guarda métricas + gráficas + modelo.
    """
    log = get_logger("baseline")
    Path("reports/figures").mkdir(parents=True, exist_ok=True)
    Path("reports/metrics").mkdir(parents=True, exist_ok=True)

    # 1) Leer datos (robusto)
    df = pd.read_csv(path_csv, low_memory=False)
    if TARGET not in df.columns:
        raise AssertionError(f"Columna objetivo '{TARGET}' no encontrada en {path_csv}")

    # 2) Binarizar etiqueta
    _binarize_target(df)

    # 3) Split
    if use_temporal:
        X_train, X_test, y_train, y_test = _temporal_split(df)
    else:
        X_train, X_test, y_train, y_test = _random_split(df)

    # 4) Preprocesamiento + modelo baseline
    pre = build_preprocess(X_train)
    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        # solver por defecto 'lbfgs' funciona bien; si quieres usar n_jobs, cambia a 'liblinear'
    )
    pipe = Pipeline(steps=[("pre", pre), ("model", model)])

    # 5) Entrenar
    pipe.fit(X_train, y_train)

    # 6) Predicción + métricas
    probas = pipe.predict_proba(X_test)[:, 1]
    preds  = (probas >= 0.5).astype(int)

    metrics = {
        "roc_auc": float(roc_auc_score(y_test, probas)),
        "f1":      float(f1_score(y_test, preds)),
        "accuracy": float(accuracy_score(y_test, preds)),
        "n_train": int(len(y_train)),
        "n_test":  int(len(y_test)),
        "target": TARGET,
        "positive_label": POS_LABEL,
        "use_temporal": use_temporal,
    }
    log.info("Métricas baseline: %s", metrics)

    # 7) Gráficas
    fpr, tpr, _ = roc_curve(y_test, probas)
    plt.figure()
    plt.plot(fpr, tpr, label=f"ROC AUC={metrics['roc_auc']:.3f}")
    plt.plot([0, 1], [0, 1], "--")
    plt.xlabel("FPR"); plt.ylabel("TPR"); plt.title("ROC"); plt.legend()
    plt.savefig("reports/figures/roc_curve.png", bbox_inches="tight")
    plt.close()

    precision, recall, _ = precision_recall_curve(y_test, probas)
    plt.figure()
    plt.plot(recall, precision)
    plt.xlabel("Recall"); plt.ylabel("Precision"); plt.title("Precision-Recall")
    plt.savefig("reports/figures/pr_curve.png", bbox_inches="tight")
    plt.close()

    cm = confusion_matrix(y_test, preds, labels=[0, 1])
    plt.figure()
    sns.heatmap(cm, annot=True, fmt="d", cbar=False, xticklabels=[0,1], yticklabels=[0,1])
    plt.title("Matriz de confusión"); plt.xlabel("Pred"); plt.ylabel("True")
    plt.savefig("reports/figures/confusion_matrix.png", bbox_inches="tight")
    plt.close()

    # 8) Guardar artefactos
    with open("reports/metrics/baseline_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    joblib.dump(pipe, "reports/baseline_model.joblib")

    return metrics


if __name__ == "__main__":
    m = fit_and_eval(path_csv=CSV_IN, use_temporal=True)
    print(m)