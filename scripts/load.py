import psycopg2
from psycopg2.extras import execute_batch

def load(ti):
    data = ti.xcom_pull(task_ids='transform')

    if not data:
        print("No data received from transform task")
        return

    conn = psycopg2.connect(
        host="postgres",
        database="airflow",
        user="airflow",
        password="airflow"
    )

    cursor = conn.cursor()

    # prepare batch data
    records = [(r["id"], r["title"]) for r in data]

    query = """
        INSERT INTO posts (id, title)
        VALUES (%s, %s)
        ON CONFLICT (id) DO UPDATE
        SET title = EXCLUDED.title;
    """

    execute_batch(cursor, query, records)

    conn.commit()

    # update metadata (VERY IMPORTANT)
    cursor.execute("""
        INSERT INTO pipeline_metadata (last_run)
        VALUES (NOW())
    """)

    conn.commit()

    cursor.close()
    conn.close()

    print(f"Loaded {len(data)} records")