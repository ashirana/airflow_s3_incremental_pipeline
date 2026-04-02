import requests
from utils.s3_utils import upload_file_to_s3
from datetime import datetime
import json

def extract():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    data = response.json()
    file_path = "/tmp/data.json"
    with open(file_path, 'w') as f:
        json.dump(data, f)
    bucket = "ashish-data-pipeline-2026"
    today = datetime.now().strftime("%Y-%m-%d")
    key = f"raw/api/{today}/data.json"
    upload_file_to_s3(file_path, bucket, key)
    return key