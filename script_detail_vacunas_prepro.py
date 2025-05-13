import pandas as pd
import numpy as np
import os


def main():
    # Verificar si el archivo mid_dim_vacunacion_detail.csv existe
    input_file = 'mid_dim_vacunacion_detail.csv'

    if not os.path.exists(input_file):
        print(f"Error: No se encuentra el archivo {input_file}")
        print("Por favor, asegúrate de que el archivo está en el mismo directorio que este script.")
        return

    # Cargar el CSV en un DataFrame
    print(f"Leyendo archivo {input_file}...")
    df = pd.read_csv(input_file)

    # Crear una columna id_detail única
    print("Generando identificadores únicos...")
    df['id_detail'] = df.apply(
        lambda row: f"{row['departamentos']}_{row['key_fecha']}_{row['vaccine_header']}".replace(
            ' ', '_'),
        axis=1
    )

    # También creamos una versión numérica del id_detail
    df['id_detail_num'] = df['id_detail'].factorize()[0] + \
        1  # Empezamos desde 1

    # Crear el primer dataframe: fin_dim_vacunacion_detail.csv
    print("Preparando archivo fin_dim_vacunacion_detail.csv...")
    df_detail = df[['id_detail_num', 'departamentos',
                    'key_fecha', 'vaccine_header', 'doses_aplicadas']].copy()
    df_detail.rename(columns={'id_detail_num': 'id_detail'}, inplace=True)

    # Crear el segundo dataframe: fin_fact_vacunacion.csv
    print("Preparando archivo fin_fact_vacunacion.csv...")
    df_fact = df[['departamentos', 'key_fecha',
                  'programatica1_ano', 'id_detail_num', 'pct_cobertura']].copy()
    df_fact.rename(columns={'id_detail_num': 'id_detail'}, inplace=True)

    # Guardar los dataframes como CSV
    output_detail = 'fin_dim_vacunacion_detail.csv'
    output_fact = 'fin_fact_vacunacion.csv'

    df_detail.to_csv(output_detail, index=False)
    df_fact.to_csv(output_fact, index=False)

    print(f"\nArchivos creados exitosamente:")
    print(f"- {output_detail} ({len(df_detail)} registros)")
    print(f"- {output_fact} ({len(df_fact)} registros)")

    # Mostrar las primeras filas de cada DataFrame para verificación
    print("\nPrimeras filas de fin_dim_vacunacion_detail.csv:")
    print(df_detail.head())

    print("\nPrimeras filas de fin_fact_vacunacion.csv:")
    print(df_fact.head())


if __name__ == "__main__":
    print("Iniciando procesamiento de datos de vacunación...")
    main()
    print("\nProcesamiento completado.")
