import pandas as pd

NAME_MAP = {
"Amazonas":"AMAZONAS",
"Antioquia":"ANTIOQUIA",
"Atlántico":"ATLANTICO",
"Bogotá":  "BOGOTA D.C.",
"Bolívar": "BOLIVAR",
"Boyacá":  "BOYACA",
"Caldas":  "CALDAS",
"Caquetá": "CAQUETA",
"Cauca":   "CAUCA",
"Cesar":   "CESAR",
"Córdoba": "CORDOBA",
"Cundinamarca":"CUNDINAMARCA",
"Chocó":   "CHOCO",
"Huila":   "HUILA",
"La Guajira":  "LA GUAJIRA",
"Magdalena":"MAGDALENA",
"Meta":    "META",
"Nariño":  "NARIÑO",
"Norte de Santander":"NORTE DE SANTANDER",
"Quindío": "QUINDIO",
"Risaralda":"RISARALDA",
"Santander":"SANTANDER",
"Sucre":   "SUCRE",
"Tolima":  "TOLIMA",
"Valle del Cauca":"VALLE DEL CAUCA",
"Arauca":  "ARAUCA",
"Casanare":"CASANARE",
"Putumayo":"PUTUMAYO",
"Archipiélago de San Andrés y Providencia":"SAN ANDRES ISLA",
"Guainía": "GUAINIA",
"Guaviare":"GUAVIARE",
"Vaupés":  "VAUPES",
"Vichada": "VICHADA",
}


df = pd.read_csv("nacimientos_departamento_anio.csv")

df = df[df["Departamento"] != "Total Nacional"] #drop

df["Departamento"] = df["Departamento"].map(NAME_MAP)

if df["Departamento"].isna().any():
    missing = df[df["Departamento"].isna()]
    raise ValueError(
        f"Unmapped department names found:\n{missing['Departamento'].unique()}"
    )

df.to_csv("nacimientos_estandarizados.csv", index=False)

print("✔ Archivo ‘nacimientos_estandarizados.csv’ creado con éxito.")
