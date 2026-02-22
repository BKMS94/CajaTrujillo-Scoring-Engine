from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lit

def run_scoring():
    # Inicializar Spark
    spark = SparkSession.builder \
        .appName("CajaTrujillo_Scoring_Engine") \
        .getOrCreate()

    print("--- Motor de Scoring Iniciado ---")

    # 1. Simulación de solicitudes entrantes (Capa Bronze)
    # Formato: ID_Cliente, Monto_Pedido, Calificacion_SBS (1=Exc, 2=Normal, 3=Riesgo)
    raw_data = [
        ("CLI_001", 1200, 1), 
        ("CLI_002", 900, 2),
        ("CLI_003", 500, 3),
        ("CLI_004", 3000, 1)
    ]
    
    df_requests = spark.createDataFrame(raw_data, ["id_cliente", "monto_pedido", "sbs_score"])

    # 2. Lógica de Enriquecimiento y Reglas de Negocio (Capa Silver)
    # Aquí simulamos los sueldos que Spark "leerá" (en producción sería un Join con Redis)
    df_enriched = df_requests.withColumn(
        "sueldo_estimado",
        when(col("id_cliente") == "CLI_001", 5000)
        .when(col("id_cliente") == "CLI_002", 2800)
        .when(col("id_cliente") == "CLI_003", 1500)
        .otherwise(8000)
    )

    # 3. Aplicación de la Regla de Arquitecto:
    # Si SBS = 1 (Excelente) -> Límite 30% del sueldo
    # Si SBS > 1 -> Límite 20% del sueldo
    df_final = df_enriched.withColumn(
        "resultado",
        when(
            (col("sbs_score") == 1) & (col("monto_pedido") <= col("sueldo_estimado") * 0.30), "APROBADO"
        ).when(
            (col("sbs_score") > 1) & (col("monto_pedido") <= col("sueldo_estimado") * 0.20), "APROBADO"
        ).otherwise("RECHAZADO")
    )

    # Mostrar resultados en consola
    df_final.select("id_cliente", "monto_pedido", "sueldo_estimado", "resultado").show()

    # Guardar en Capa Gold (Simulado)
    print("Guardando resultados en data/gold/ en formato Parquet...")
    # df_final.write.mode("overwrite").parquet("data/gold/scoring_results")

if __name__ == "__main__":
    run_scoring()