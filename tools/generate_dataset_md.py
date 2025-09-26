import os, json, hashlib, datetime
from pathlib import Path

try:
    import pandas as pd
except:
    pd = None

try:
    import pyarrow.parquet as pq
except:
    pq = None

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw"
DOCS = BASE / "docs"
DOCS.mkdir(parents=True, exist_ok=True)

def sha256_dir(directory: Path) -> str:
    sha256 = hashlib.sha256()
    if not directory.exists():
        return ""
    for root, _, files in os.walk(directory):
        for f in sorted(files):
            p = Path(root) / f
            try:
                with open(p, "rb") as fh:
                    for chunk in iter(lambda: fh.read(8192), b""):
                        sha256.update(chunk)
            except:
                continue
    return sha256.hexdigest()

def human(n: int) -> str:
    units = ["B","KB","MB","GB","TB"]
    size = float(n)
    for u in units:
        if size < 1024.0 or u == units[-1]:
            return f"{size:.2f} {u}"
        size /= 1024.0

files = [p for p in RAW.rglob("*") if p.is_file()] if RAW.exists() else []
infos = []
total_bytes = 0
formats = {}
cols_sets = []

for p in files:
    info = {
        "path": str(p),
        "size_bytes": p.stat().st_size,
        "rows": None,
        "format": p.suffix.lower().lstrip("."),
        "columns": None
    }
    total_bytes += info["size_bytes"]
    formats[info["format"]] = formats.get(info["format"], 0) + 1

    suf = p.suffix.lower()
    try:
        if suf == ".csv" and pd is not None:
            rows = 0
            cols = None
            for chunk in pd.read_csv(p, chunksize=100000, low_memory=False):
                rows += len(chunk)
                if cols is None:
                    cols = list(chunk.columns)
            info["rows"] = rows
            info["columns"] = cols
        elif suf in [".json", ".jsonl", ".ndjson"]:
            rows = 0
            keys = set()
            with open(p, "r", encoding="utf-8", errors="ignore") as fh:
                for i, line in enumerate(fh):
                    rows += 1
                    if i < 200:
                        try:
                            obj = json.loads(line)
                            if isinstance(obj, dict):
                                keys.update(obj.keys())
                        except:
                            pass
            info["rows"] = rows
            info["columns"] = sorted(list(keys)) if keys else None
    except Exception as e:
        info["columns"] = [f"Error: {e}"]

    if info.get("columns"):
        cols_sets.append(set(info["columns"]))
    infos.append(info)

total_rows = sum(i["rows"] or 0 for i in infos)
common_cols = sorted(list(set.intersection(*cols_sets))) if cols_sets else []
example_cols = sorted(list(set.union(*cols_sets)))[:20] if cols_sets else []
sha_digest = sha256_dir(RAW)

today = datetime.date.today().isoformat()
with open(DOCS / "DATASET.md", "w", encoding="utf-8") as f:
    f.write(f"""# DATASET Documentation

## Fuente
(Completar manualmente: Elastic Agent, módulos, herramientas, etc.)

## Fecha de adquisición
{today}

## Tamaño & Formato
- Archivos: {len(files)}
- Eventos (aprox.): {total_rows}
- Tamaño total: {human(total_bytes)}
- Formatos detectados: {formats}

## Variables principales (detectadas)
- Columnas comunes: {', '.join(common_cols) if common_cols else 'No detectadas'}
- Ejemplo de columnas: {', '.join(example_cols) if example_cols else 'No detectadas'}

## Integridad / Control de versión
SHA256 data/raw: {sha_digest}

## Inventario de archivos
""")
    for fi in infos:
        f.write(f"- {fi['path']} — {human(fi['size_bytes'])}, filas: {fi['rows']}, formato: {fi['format']}\n")
        if fi.get("columns"):
            f.write(f"  - columnas (muestra): {', '.join(fi['columns'][:20])}\n")

print("[OK] DATASET.md generado en docs/")