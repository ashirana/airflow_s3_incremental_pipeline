from utils.s3_utils import read_json_from_s3


def transform(ti):
    bucket = "ashish-data-pipeline-2026"
    key = ti.xcom_pull(task_ids='extract')

    print(f"Reading from s3://{bucket}/{key}")

    data = read_json_from_s3(bucket, key)

    transformed_data = []

    for record in data:
        transformed_data.append({
            "id": record["id"],
            "title": record["title"]
        })

    print(f"Transformed records: {len(transformed_data)}")

    return transformed_data 