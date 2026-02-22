from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lit

spark = SparkSession.builder.appName("ScoringEngine").getOrCreate()

# 1. Simulación de Ingesta (Capa Bronze)
solicitudes_raw = [
    ("CLI_001", 1200, 1), # Pide 1200, SBS Excelente
    ("CLI_002", 1000, 3)  # Pide 1000, SBS Deficiente
]
df = spark.createDataFrame(solicitudes_raw, ["id_cliente", "monto_solicitado", "score_sbs"])

# 2. Lógica de Negocio (Capa Silver)
# (Aquí simularíamos el join con Redis, pero usaremos valores fijos para el ejemplo)
df_scoring = df.withColumn(
    "limite_permitido",
    when(col("score_sbs") == 1, 0.30).otherwise(0.20)
)

# 3. Decisión Final (Capa Gold)
df_final = df_scoring.withColumn(
    "decision",
    when(col("monto_solicitado") <= (lit(5000) * col("limite_permitido")), "APROBADO")
    .otherwise("RECHAZADO")
)

# Guardar resultado en Gold (Parquet particionado)
# df_final.write.partitionBy("decision").mode("overwrite").parquet("data/gold/scoring_results")
df_final.show()