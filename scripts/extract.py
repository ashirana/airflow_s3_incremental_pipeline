import requests
from utils.s3_utils import upload_file_to_s3
from datetime import datetime
from config.config import AWS_BUCKET_NAME
import json

def extract():
    url = "https://jsonplaceholder.typicode.com/posts"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        raise Exception(f"API request failed: {e}")

    data = response.json()

    # unique file name (important for incremental pipelines)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"/tmp/data_{timestamp}.json"

    with open(file_path, 'w') as f:
        json.dump(data, f)

    key = f"raw/api/{timestamp}/data.json"

    print(f"Uploading to S3 → {key}")

    upload_file_to_s3(file_path, AWS_BUCKET_NAME, key)

    return key


if __name__ == "__main__":
    extract()