import pandas as pd
import numpy as np

# ---------------------------------------------------------------
# 0. Leer el archivo CSV de entrada
# ---------------------------------------------------------------
input_df = pd.read_csv("fin_normalized_cobertura_2016-2019_v8.csv")
df = input_df.copy()

# ---------------------------------------------------------------
# 1. Columnas “meta” → no se des‑pivotan
# ---------------------------------------------------------------
meta_cols = [
    "codigo_depto", "departamentos",
    "programatica_menor_1_ano", "programatica1_ano",
    "programatica_5_anos", "region",
    "total_dosis", "ano"
]

# ---------------------------------------------------------------
# 2. Detectar columnas de dosis y su % inmediatamente posterior
# ---------------------------------------------------------------
dose_cols = []
pct_map = {}
cols = df.columns.tolist()
i = 0

while i < len(cols):
    c = cols[i]
    if c in meta_cols:
        i += 1
        continue

    if any(k in c for k in ["dosis", "_d_", "ref"]):
        pct_col = None
        if i + 1 < len(cols):
            nxt = cols[i + 1]
            is_pct = (
                nxt not in meta_cols and
                not any(k in nxt for k in ["dosis", "_d_", "ref"])
            )
            if is_pct:
                pct_col = nxt
                i += 1  # saltar la % en el loop
        dose_cols.append(c)
        pct_map[c] = pct_col
    i += 1

# ---------------------------------------------------------------
# 3. Convertir a formato largo
# ---------------------------------------------------------------
records = []

for _, row in df.iterrows():
    meta_data = row[meta_cols].to_dict()

    for dose_col in dose_cols:
        pct_col = pct_map[dose_col]
        record = meta_data.copy()
        record["vaccine_header"] = dose_col
        record["doses_aplicadas"] = row[dose_col]
        record["pct_cobertura"] = row[pct_col] if pct_col else np.nan
        records.append(record)

long_df = pd.DataFrame(records)
final_cols = [
    "departamentos",
    "programatica1_ano",
    "total_dosis",
    "ano",
    "vaccine_header",
    "doses_aplicadas",
    "pct_cobertura"
]

# ---------------------------------------------------------------
# 4. Guardar el DataFrame resultante como CSV
# ---------------------------------------------------------------
long_df[final_cols].to_csv("fin_fact_vacunacion.csv", index=False)
