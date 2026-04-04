import psycopg2


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

    for record in data:
        cursor.execute("""
            INSERT INTO posts (id, title)
            VALUES (%s, %s)
            ON CONFLICT (id) DO UPDATE
            SET title = EXCLUDED.title;
        """, (record["id"], record["title"]))

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Loaded {len(data)} records")