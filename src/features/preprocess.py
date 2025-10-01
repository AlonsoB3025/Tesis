# src/features/preprocess.py
from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer


DEFAULT_TIME_COL = "timestamp"     
DEFAULT_TARGET   = "action"        
DEFAULT_DROP     = [
    "event_id", "description", "object_name",
    "rule.name", "rule.id", "event.outcome", "event.kind",
    "id", "_id"
]
DEFAULT_PATH_IN  = Path("data/processed_logs/logs_normalizados.csv")
DEFAULT_PATH_OUT = Path("data/processed/dataset_clean.csv")


def _derive_time_features(df: pd.DataFrame, time_col: str) -> pd.DataFrame:
    """Crea features de calendario básicas solo si el timestamp se puede parsear."""
    if time_col not in df.columns:
        return df
    d = df.copy()
    dt = pd.to_datetime(d[time_col], errors="coerce", utc=True)
    has = dt.notna()
    if not has.any():
        # No se pudo interpretar ninguna fecha -> no agregamos features
        return d

    d.loc[has, "hour"]  = dt[has].dt.hour.astype("Int64")
    d.loc[has, "wday"]  = dt[has].dt.weekday.astype("Int64")
    d.loc[has, "month"] = dt[has].dt.month.astype("Int64")

    # Relleno para no dejar NaN por filas sin timestamp
    for c in ["hour", "wday", "month"]:
        if c in d.columns:
            d[c] = d[c].fillna(-1).astype(int)
    return d


def _standard_min_clean(df: pd.DataFrame, target: str, drop_cols: List[str]) -> pd.DataFrame:
    """Limpieza mínima para baseline: quitar duplicados, columnas de fuga y nulos en y."""
    d = df.copy()
    # Drop candidatos de leakage/IDs si existen
    to_drop = [c for c in drop_cols if c in d.columns]
    if to_drop:
        d = d.drop(columns=to_drop)

    # Quitar duplicados exactos
    d = d.drop_duplicates()

    # No entrenar con y nula
    if target in d.columns:
        d = d.dropna(subset=[target])

    return d


def prepare_dataset(
    path_in: Path = DEFAULT_PATH_IN,
    path_out: Path = DEFAULT_PATH_OUT,
    target: str = DEFAULT_TARGET,
    time_col: Optional[str] = DEFAULT_TIME_COL,
    extra_drop: Optional[List[str]] = None
) -> Tuple[pd.DataFrame, Path]:
    """
    Lee el CSV ya normalizado por tu notebook, aplica limpieza mínima y exporta
    `data/processed/dataset_clean.csv` (ruta configurable).

    Devuelve el DataFrame limpio y la ruta de salida.
    """
    path_in = Path(path_in)
    assert path_in.exists(), f"No se encontró el archivo de entrada: {path_in}"

    df = pd.read_csv(path_in)

    # Features derivadas de tiempo (opcionales)
    if time_col:
        df = _derive_time_features(df, time_col)

    # Limpieza estándar
    drop_cols = list(DEFAULT_DROP)
    if extra_drop:
        drop_cols.extend(extra_drop)
    df = _standard_min_clean(df, target=target, drop_cols=drop_cols)

    # Guarda
    path_out = Path(path_out)
    path_out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path_out, index=False)
    return df, path_out


def build_preprocess(X: pd.DataFrame) -> ColumnTransformer:
    
    num_cols = X.select_dtypes(include=[np.number, "Int64", "Float64"]).columns.tolist()
    cat_cols = [c for c in X.columns if c not in num_cols]

    transformers = []

    if len(num_cols) > 0:
        num_pipe = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value=0)),
            ("scaler", StandardScaler(with_mean=False)),
        ])
        transformers.append(("num", num_pipe, num_cols))

    if len(cat_cols) > 0:
        cat_pipe = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ])
        transformers.append(("cat", cat_pipe, cat_cols))

    if not transformers:
        raise ValueError("No hay columnas numéricas ni categóricas utilizables tras la selección.")

    pre = ColumnTransformer(
        transformers=transformers,
        remainder="drop",
        sparse_threshold=0.3,
        n_jobs=None,
    )
    return pre