import pandas as pd
import sqlite3
import os

# Crear conexión a la base de datos SQLite
conn = sqlite3.connect('db_BI_vacunaciones.db')
cursor = conn.cursor()

# Función para leer y procesar cada archivo CSV


def cargar_csv_a_sqlite(archivo_csv, nombre_tabla, definicion_columnas, primary_key=None, foreign_keys=None):
    df = pd.read_csv(archivo_csv)

    create_table_sql = f"CREATE TABLE IF NOT EXISTS {nombre_tabla} ({definicion_columnas}"

    if primary_key:
        create_table_sql += f", PRIMARY KEY ({primary_key})"

    if foreign_keys:
        for fk in foreign_keys:
            create_table_sql += f", FOREIGN KEY ({fk['column']}) REFERENCES {fk['ref_table']}({fk['ref_column']})"

    create_table_sql += ")"
    cursor.execute(create_table_sql)

    df.to_sql(nombre_tabla, conn, if_exists='replace', index=False)

    print(f"Tabla {nombre_tabla} creada y datos cargados exitosamente.")


cargar_csv_a_sqlite(
    'fin_dim_departamento.csv',
    'dim_departamento',
    "nombre_departamento TEXT, latitud REAL, longitud REAL",
    primary_key="nombre_departamento"
)

cargar_csv_a_sqlite(
    'fin_dim_fecha.csv',
    'dim_fecha',
    "key_fecha INTEGER, anio INTEGER",
    primary_key="key_fecha"
)

cargar_csv_a_sqlite(
    'fin_dim_cluster_departamentos.csv',
    'dim_cluster_departamentos',
    "Cluster_id INTEGER, Cluster_name TEXT, Cluster_description TEXT, nombre_departamento TEXT",
    primary_key="Cluster_id, nombre_departamento",
    foreign_keys=[
        {"column": "nombre_departamento", "ref_table": "dim_departamento",
            "ref_column": "nombre_departamento"}
    ]
)

cargar_csv_a_sqlite(
    'fin_dim_vacunacion_detail.csv',
    'dim_vacunacion_detail',
    "id_detail INTEGER, departamentos TEXT, key_fecha INTEGER, vaccine_header TEXT, doses_aplicadas INTEGER",
    primary_key="id_detail",
    foreign_keys=[
        {"column": "departamentos", "ref_table": "dim_departamento",
            "ref_column": "nombre_departamento"},
        {"column": "key_fecha", "ref_table": "dim_fecha", "ref_column": "key_fecha"}
    ]
)

cargar_csv_a_sqlite(
    'fin_fact_nacimientos.csv',
    'fact_nacimientos',
    "Departamento TEXT, key_fecha INTEGER, Numero_nacimientos INTEGER",
    primary_key="Departamento, key_fecha",
    foreign_keys=[
        {"column": "Departamento", "ref_table": "dim_departamento",
            "ref_column": "nombre_departamento"},
        {"column": "key_fecha", "ref_table": "dim_fecha", "ref_column": "key_fecha"}
    ]
)

cargar_csv_a_sqlite(
    'fin_fact_vacunacion.csv',
    'fact_vacunacion',
    "departamentos TEXT, key_fecha INTEGER, programatica1_ano INTEGER, id_detail INTEGER, pct_cobertura REAL",
    primary_key="id_detail",
    foreign_keys=[
        {"column": "departamentos", "ref_table": "dim_departamento",
            "ref_column": "nombre_departamento"},
        {"column": "key_fecha", "ref_table": "dim_fecha", "ref_column": "key_fecha"},
        {"column": "id_detail", "ref_table": "dim_vacunacion_detail",
            "ref_column": "id_detail"}
    ]
)

cursor.execute("PRAGMA foreign_keys = ON")

conn.commit()
conn.close()

print("Base de datos SQLite creada exitosamente con todas las tablas y relaciones.")
