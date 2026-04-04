# 🚀 Airflow S3 Incremental Data Pipeline

## 📌 Overview

This project implements a **production-style data pipeline** using:

- Apache Airflow (workflow orchestration)
- Amazon S3 (raw data layer)
- PostgreSQL (data warehouse)
- Docker (containerized execution)

The pipeline extracts data from an API, stores it in S3, transforms it, and loads it into PostgreSQL.

---

## 🏗️ Architecture

    API
     ↓
 Extract Task
     ↓
  S3 (raw layer)
     ↓

Transform Task
↓
PostgreSQL (warehouse)
↓
Airflow DAG


---

## ⚙️ Tech Stack

- Python
- Apache Airflow 2.8.1
- PostgreSQL
- AWS S3 (boto3)
- Docker & Docker Compose

---

## 📂 Project Structure


airflow_s3_incremental_pipeline/
│
├── dags/
│ └── pipeline_dag.py
│
├── scripts/
│ ├── extract.py
│ ├── transform.py
│ └── load.py
│
├── utils/
│ └── s3_utils.py
│
├── config/
│ └── config.py
│
├── docker-compose.yml
├── requirements.txt
└── README.md


---

## 🔄 Pipeline Flow

### 1. Extract
- Fetches data from API
- Uploads JSON file to S3

### 2. Transform
- Reads data from S3
- Cleans and structures records
- Returns processed data via XCom

### 3. Load
- Inserts data into PostgreSQL
- Uses UPSERT (`ON CONFLICT`) to prevent duplicates

---

## 🧪 Database Schema

### Posts Table

```sql
CREATE TABLE IF NOT EXISTS posts (
    id INT PRIMARY KEY,
    title TEXT
);
Metadata Table (for incremental processing)
CREATE TABLE IF NOT EXISTS pipeline_metadata (
    pipeline_name TEXT PRIMARY KEY,
    last_processed_id INT,
    updated_at TIMESTAMP
);
⚙️ Configuration Management

All environment-specific values are centralized in:

config/config.py

Example:

AWS_BUCKET_NAME = "your-bucket-name"

POSTGRES_CONFIG = {
    "host": "postgres",
    "database": "airflow",
    "user": "airflow",
    "password": "airflow"
}

This avoids hardcoding values inside scripts and improves maintainability.

🐳 Setup Instructions
1. Clone Repository
git clone <your-repo-url>
cd airflow_s3_incremental_pipeline
2. Create .env file
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=eu-west-2
3. Start Services
docker compose up -d
4. Access Airflow UI
http://localhost:8080

Login:

username: airflow
password: airflow
5. Trigger DAG
Enable DAG: s3_incremental_pipeline
Click Trigger DAG
✅ Validation
Check PostgreSQL
docker exec -it airflow_postgres psql -U airflow -d airflow
SELECT COUNT(*) FROM posts;

Expected:

100
🔐 Security Note
AWS credentials are stored in .env
Never commit .env to GitHub
Use IAM roles or secret managers in production
⚠️ Current Limitations
Full data load on every run
No incremental filtering yet
No monitoring/alerting
🚀 Upcoming Improvements
Incremental processing using metadata table
Partitioned S3 storage
Data quality checks
Logging & monitoring
Cloud deployment
💡 Key Learnings
Airflow DAG orchestration
XCom for task communication (metadata only)
Containerized data pipelines using Docker
Secure credential handling
Idempotent data loading using UPSERT
📊 Versioning
v1 → End-to-end pipeline (API → S3 → PostgreSQL)
v1.1 → Config-driven architecture
v2 (next) → Incremental processing
👨‍💻 Author

Ashish Ashish


---

# 🚀 Next Step

Now push this:

```bash
git add README.md
git commit -m "Updated README with config-driven architecture"
git push