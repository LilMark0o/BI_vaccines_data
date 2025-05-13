import sqlite3
import pandas as pd


def verificar_bd():
    print("Iniciando verificación de la base de datos db_BI_vacunaciones.db...")

    # Conectar a la base de datos
    conn = sqlite3.connect('db_BI_vacunaciones.db')
    cursor = conn.cursor()

    # 1. Verificar que existen las 6 tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = cursor.fetchall()
    tablas = [tabla[0] for tabla in tablas]

    print(f"\n1. Tablas encontradas ({len(tablas)}):")
    for tabla in tablas:
        print(f"   - {tabla}")

    tablas_esperadas = [
        'dim_departamento',
        'dim_fecha',
        'dim_cluster_departamentos',
        'dim_vacunacion_detail',
        'fact_nacimientos',
        'fact_vacunacion'
    ]

    # Verificar si todas las tablas esperadas existen
    todas_existen = all(tabla in tablas for tabla in tablas_esperadas)
    print(
        f"\n¿Todas las tablas esperadas existen? {'Sí' if todas_existen else 'No'}")

    # 2. Verificar la estructura de cada tabla
    print("\n2. Estructura de las tablas:")
    for tabla in tablas_esperadas:
        if tabla in tablas:
            cursor.execute(f"PRAGMA table_info({tabla})")
            columnas = cursor.fetchall()
            print(f"\n   Tabla: {tabla}")
            print(f"   {'Columna':<20} {'Tipo':<10} {'¿Nula?':<10} {'PK'}")
            print(f"   {'-'*50}")
            for col in columnas:
                print(
                    f"   {col[1]:<20} {col[2]:<10} {'No' if col[3] == 0 else 'Sí':<10} {'Sí' if col[5] == 1 else 'No'}")

    # 3. Verificar foreign keys
    print("\n3. Foreign keys definidas:")
    for tabla in tablas_esperadas:
        if tabla in tablas:
            cursor.execute(f"PRAGMA foreign_key_list({tabla})")
            fks = cursor.fetchall()
            if fks:
                print(f"\n   Tabla: {tabla}")
                print(
                    f"   {'Columna':<20} {'Ref. Tabla':<20} {'Ref. Columna':<20}")
                print(f"   {'-'*60}")
                for fk in fks:
                    print(f"   {fk[3]:<20} {fk[2]:<20} {fk[4]:<20}")
            else:
                print(f"\n   Tabla: {tabla} - No tiene foreign keys definidas")

    # 4. Contar registros en cada tabla
    print("\n4. Conteo de registros por tabla:")
    for tabla in tablas_esperadas:
        if tabla in tablas:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cursor.fetchone()[0]
            print(f"   - {tabla}: {count} registros")

    # 5. Probar algunas consultas de join para verificar relaciones
    print("\n5. Pruebas de join para verificar relaciones:")

    # Prueba 1: Join entre departamentos y clusters
    print("\n   Prueba 1: Join entre departamentos y clusters")
    try:
        query = """
        SELECT d.nombre_departamento, d.latitud, d.longitud, c.Cluster_name, c.Cluster_description
        FROM dim_departamento d
        JOIN dim_cluster_departamentos c ON d.nombre_departamento = c.nombre_departamento
        LIMIT 5
        """
        result = pd.read_sql_query(query, conn)
        print("   Resultado:")
        print(result)
        print("   ✅ Join exitoso entre departamentos y clusters")
    except Exception as e:
        print(f"   ❌ Error en join: {e}")

    # Prueba 2: Join entre hechos de nacimientos y dimensión de fechas
    print("\n   Prueba 2: Join entre hechos de nacimientos y dimensión de fechas")
    try:
        query = """
        SELECT f.anio, n.Departamento, SUM(n.Numero_nacimientos) as total_nacimientos
        FROM fact_nacimientos n
        JOIN dim_fecha f ON n.key_fecha = f.key_fecha
        GROUP BY f.anio, n.Departamento
        LIMIT 5
        """
        result = pd.read_sql_query(query, conn)
        print("   Resultado:")
        print(result)
        print("   ✅ Join exitoso entre nacimientos y fechas")
    except Exception as e:
        print(f"   ❌ Error en join: {e}")

    # Prueba 3: Join entre hechos de vacunación y sus detalles
    print("\n   Prueba 3: Join entre hechos de vacunación y sus detalles")
    try:
        query = """
        SELECT v.departamentos, v.pct_cobertura, d.vaccine_header, d.doses_aplicadas
        FROM fact_vacunacion v
        JOIN dim_vacunacion_detail d ON v.id_detail = d.id_detail
        LIMIT 5
        """
        result = pd.read_sql_query(query, conn)
        print("   Resultado:")
        print(result)
        print("   ✅ Join exitoso entre vacunación y detalles")
    except Exception as e:
        print(f"   ❌ Error en join: {e}")

    # Prueba 4: Join complejo entre múltiples tablas
    print("\n   Prueba 4: Join complejo entre múltiples tablas")
    try:
        query = """
        SELECT 
            d.nombre_departamento, 
            f.anio, 
            c.Cluster_name,
            SUM(vd.doses_aplicadas) as total_dosis,
            AVG(v.pct_cobertura) as promedio_cobertura
        FROM fact_vacunacion v
        JOIN dim_vacunacion_detail vd ON v.id_detail = vd.id_detail
        JOIN dim_departamento d ON v.departamentos = d.nombre_departamento
        JOIN dim_fecha f ON v.key_fecha = f.key_fecha
        JOIN dim_cluster_departamentos c ON d.nombre_departamento = c.nombre_departamento
        GROUP BY d.nombre_departamento, f.anio, c.Cluster_name
        LIMIT 5
        """
        result = pd.read_sql_query(query, conn)
        print("   Resultado:")
        print(result)
        print("   ✅ Join complejo exitoso entre múltiples tablas")
    except Exception as e:
        print(f"   ❌ Error en join complejo: {e}")

    # Cerrar conexión
    conn.close()
    print("\nVerificación de la base de datos completada.")


if __name__ == "__main__":
    verificar_bd()
