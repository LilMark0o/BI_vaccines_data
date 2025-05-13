import pandas as pd
import unicodedata
import re
from pathlib import Path

# ------------------------------------------------------------------
# CONFIGURA AQUÍ EL NOMBRE/UBICACIÓN DE TU EXCEL DE ENTRADA
# ------------------------------------------------------------------
INPUT_FILE  = Path("cobertura_2016-2019_v8.xlsx")         # <-- ajústalo si tu nombre es otro
OUTPUT_FILE = INPUT_FILE.with_name(f"normalized_{INPUT_FILE.stem}.csv")

# ------------------------------------------------------------------
# FUNCIÓN DE NORMALIZACIÓN DE ENCABEZADOS
# ------------------------------------------------------------------
def normalize(col: str) -> str:
    """
    Normaliza un encabezado:
    - quita tildes y diéresis
    - pasa a minúsculas
    - cambia espacios y puntuación por guión bajo
    - colapsa guiones bajos repetidos
    - elimina guiones bajos al inicio / final
    """
    col = col.strip()
    # quitar acentos
    col = unicodedata.normalize("NFD", col).encode("ascii", "ignore").decode()
    # a minúsculas
    col = col.lower()
    # todo lo que no sea letra/número/espacio -> espacio
    col = re.sub(r"[^\w\s]", " ", col)
    # espacios -> _
    col = re.sub(r"\s+", "_", col)
    # colapsar ____ -> _
    col = re.sub(r"_+", "_", col)
    return col.strip("_")

# ------------------------------------------------------------------
# LECTURA DEL EXCEL
# ------------------------------------------------------------------
if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"No se encontró {INPUT_FILE}. Verifica el nombre o sube el archivo."
    )

df = pd.read_excel(INPUT_FILE)             # lee la 1.ª hoja (puedes indicar sheet_name)
original_cols   = df.columns.tolist()
normalized_cols = [normalize(c) for c in original_cols]
df.columns      = normalized_cols

# ------------------------------------------------------------------
# ESCRITURA A CSV
# ------------------------------------------------------------------
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
print(f"→ CSV creado: {OUTPUT_FILE.resolve()}")

# ------------------------------------------------------------------
# MUESTRA DE MAPEO (original -> normalizado)
# ------------------------------------------------------------------
mapping = pd.DataFrame({"original": original_cols, "normalizado": normalized_cols})
print("\nVista rápida del mapeo de columnas:")
print(mapping.head(20))
