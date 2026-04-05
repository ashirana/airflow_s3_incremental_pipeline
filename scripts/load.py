import psycopg2
from psycopg2.extras import execute_batch
from config.config import POSTGRES_CONFIG


def load(**context):
    data = context['ti'].xcom_pull(task_ids='transform')

    if not data:
        print("No data to load")
        return

    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cursor = conn.cursor()

    # ✅ STEP 1: Create tables if not exist (CRITICAL)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INT PRIMARY KEY,
            title TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pipeline_metadata (
            pipeline_name TEXT PRIMARY KEY,
            last_processed_id INT,
            updated_at TIMESTAMP
        );
    """)

    # ✅ STEP 2: Prepare data
    records = [(item["id"], item["title"]) for item in data]

    # ✅ STEP 3: UPSERT
    query = """
        INSERT INTO posts (id, title)
        VALUES (%s, %s)
        ON CONFLICT (id) DO UPDATE SET
            title = EXCLUDED.title;
    """

    execute_batch(cursor, query, records)

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Loaded {len(records)} records successfully")