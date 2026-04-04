import os

# AWS
AWS_BUCKET_NAME = "ashish-data-pipeline-2026"
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "eu-west-2")

# Database
POSTGRES_CONFIG = {
    "host": "postgres",
    "database": "airflow",
    "user": "airflow",
    "password": "airflow"
}

# Pipeline
PIPELINE_NAME = "s3_incremental_pipeline"