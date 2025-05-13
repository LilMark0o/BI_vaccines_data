import pandas as pd
import sys
from pathlib import Path

NAME_MAP = {
    "Amazonas": "AMAZONAS",
    "Antioquia": "ANTIOQUIA",
    "Atlántico": "ATLANTICO",
    "Bogotá": "BOGOTA D.C.",
    "Bolívar": "BOLIVAR",
    "Boyacá": "BOYACA",
    "Caldas": "CALDAS",
    "Caquetá": "CAQUETA",
    "Cauca": "CAUCA",
    "Cesar": "CESAR",
    "Córdoba": "CORDOBA",
    "Cundinamarca": "CUNDINAMARCA",
    "Chocó": "CHOCO",
    "Huila": "HUILA",
    "La Guajira": "LA GUAJIRA",
    "Magdalena": "MAGDALENA",
    "Meta": "META",
    "Nariño": "NARIÑO",
    "Norte de Santander": "NORTE DE SANTANDER",
    "Quindío": "QUINDIO",
    "Risaralda": "RISARALDA",
    "Santander": "SANTANDER",
    "Sucre": "SUCRE",
    "Tolima": "TOLIMA",
    "Valle del Cauca": "VALLE DEL CAUCA",
    "Arauca": "ARAUCA",
    "Casanare": "CASANARE",
    "Putumayo": "PUTUMAYO",
    "Archipiélago de San Andrés y Providencia": "SAN ANDRES ISLA",
    "Guainía": "GUAINIA",
    "Guaviare": "GUAVIARE",
    "Vaupés": "VAUPES",
    "Vichada": "VICHADA",
}

def standardize_departments(infile: str, outfile: str, column: str = "departamento") -> None:
    df = pd.read_csv(infile)
    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found in {infile}.")
    df[column] = df[column].map(NAME_MAP)
    if df[column].isna().any():
        missing = df[df[column].isna()][column].unique()
        raise ValueError(f"Unmapped department names: {missing}")
    df.to_csv(outfile, index=False)
    print(f"✔ Saved standardized file to {outfile}")

if __name__ == "__main__":
    args = sys.argv[1:]
    in_path = args[0] if len(args) >= 1 else "clusters_departamentos_colombia.csv"
    out_path = args[1] if len(args) >= 2 else Path(in_path).with_stem(Path(in_path).stem + "_estandarizados").with_suffix(".csv")
    standardize_departments(in_path, out_path)
