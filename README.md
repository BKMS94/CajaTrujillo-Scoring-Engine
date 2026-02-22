# 🏛️ Motor de Scoring Crediticio en Tiempo Real - Caja Trujillo

Este repositorio contiene la arquitectura y el código fuente para un motor de decisiones crediticias de baja latencia. El sistema integra el procesamiento distribuido de Big Data con capas de caché en memoria para ofrecer aprobaciones de crédito instantáneas basadas en reglas de negocio dinámicas y perfiles de riesgo de la SBS.

## 💡 Contexto de Negocio

El proyecto resuelve la necesidad de automatizar la evaluación crediticia en la Caja Trujillo. Al migrar de un modelo de evaluación manual a uno basado en **Arquitectura Medallion**, se logra:

* **Reducción de Latencia:** Procesamiento de solicitudes en milisegundos mediante una capa de velocidad.
* **Consistencia:** Aplicación uniforme de políticas de riesgo (reglas SBS).
* **Escalabilidad:** Capacidad para manejar picos de demanda mediante contenedores aislados.

## 🚀 Arquitectura del Sistema

La solución emplea un enfoque híbrido de procesamiento por lotes y tiempo real:

1. **Ingesta:** Recepción de solicitudes en formato JSON (compatible con aplicaciones móviles).
2. **Speed Layer (Redis):** Caché de alto rendimiento que almacena los sueldos y perfiles históricos para evitar consultas costosas a la base de datos principal durante el scoring.
3. **Motor de Procesamiento (Apache Spark):** Motor encargado de la validación de esquemas, enriquecimiento de datos y aplicación de lógica condicional (ej. límites de endeudamiento del 20% o 30%).
4. **Persistencia (Medallion Architecture):** * **Bronze:** Archivos crudos de ingesta.
    * **Silver:** Datos normalizados y validados.
    * **Gold:** Resultados finales almacenados en **Parquet** particionado por fecha y estado de decisión, optimizados para analítica.

## 🛠️ Stack Tecnológico

* **Core:** Python 3.x, PySpark 3.5
* **NoSQL / Cache:** Redis (Alpine version)
* **Infraestructura:** Docker & Docker Compose
* **Formato de Archivos:** Apache Parquet (Columnar Storage)

## 📂 Estructura del Proyecto

```text
.
├── docker-compose.yml       # Orquestación de contenedores (Spark & Redis)
├── src/
│   ├── jobs/
│   │   └── scoring_job.py   # Lógica principal de procesamiento en Spark
│   └── database/
│       └── redis_init.py    # Script de hidratación de datos en caché
├── data/
│   ├── bronze/              # Landing zone de datos crudos
│   ├── silver/              # Datos transformados
│   └── gold/                # Tablas finales particionadas
└── README.md
```
## ⚙️ Guía de Ejecución
Siga estos pasos para desplegar el entorno local de pruebas:

1. **Despliegue de Infraestructura**
    Levante los servicios de Spark y Redis en una red virtual aislada:

    ```bash
    docker-compose up -d
    ```

2. **Hidratación de la Capa de Velocidad**
    Cargue los datos maestros de clientes en Redis para habilitar el scoring instantáneo:

    ```bash
    docker exec -it redis_cache python /opt/bitnami/spark/src/database/redis_init.py
    ```

3. **Ejecución del Motor de Scoring**
    Inicie el job de Spark para evaluar las solicitudes de crédito:

    ```bash
    docker exec -it spark_engine spark-submit /opt/bitnami/spark/src/jobs/scoring_job.py
    ```

## 🛡️ Manejo de Excepciones y Resiliencia
El sistema implementa una Dead Letter Queue (DLQ) lógica. Cualquier registro que presente inconsistencias en los montos o no cumpla con el contrato de datos (Schema) se deriva automáticamente a una ruta de auditoría manual. Esto asegura que el pipeline principal nunca se detenga y que el Data Lake mantenga solo información de alta calidad para la toma de decisiones.