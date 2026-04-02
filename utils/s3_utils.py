import boto3
import json

def get_s3_client():
    return boto3.client('s3')

def upload_file_to_s3(file_path, bucket, key):
    s3_client = get_s3_client()
    try:
        s3_client.upload_file(file_path, bucket, key)
        print(f"File {file_path} uploaded to {bucket}/{key}")
    except Exception as e:
        print(f"Error uploading file: {e}")

def read_json_from_s3(bucket, key):
    s3_client = get_s3_client()
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        return json.loads(content)
    except Exception as e:
        print(f"Error reading JSON from S3: {e}")
        return None