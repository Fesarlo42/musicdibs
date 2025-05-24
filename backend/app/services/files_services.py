from uuid import uuid4
from fastapi import UploadFile
from google.cloud import storage
from google.oauth2 import service_account
from datetime import timedelta
from io import BytesIO
import os
import json

# configure google storage client
service_account_info = json.loads(os.getenv("GCS_SERVICE_ACCOUNT_KEY"))
credentials = service_account.Credentials.from_service_account_info(service_account_info)
storage_client = storage.Client(credentials=credentials)
BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")

def upload_file(file: UploadFile) -> str:
    object_key = f"{uuid4()}_{file.filename}"
    content = file.file

    bucket = storage_client.bucket(BUCKET_NAME)
    
    # Create a new blob in the bucket and upload the file content
    blob = bucket.blob(object_key)
    blob.upload_from_file(content, content_type=file.content_type)

    return object_key

def upload_generated_file(content: str, filename: str) -> str:
    object_key = f"{uuid4()}_{filename}"
    file_stream = BytesIO(content.encode("utf-8"))

    bucket = storage_client.bucket(BUCKET_NAME)

    blob = bucket.blob(object_key)
    blob.upload_from_file(file_stream, content_type="text/plain")

    return object_key

def get_file(object_key: str):
    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        
        # Reference the blob (file) in the bucket
        blob = bucket.blob(object_key)
        
        file_content = blob.download_as_bytes()
        return file_content

    except Exception as e:
        print(f"Error retrieving file: {e}")
        raise

def delete_file(object_key: str):
    bucket = storage_client.bucket(BUCKET_NAME)
    
    blob = bucket.blob(object_key)
    blob.delete()

def get_presigned_url(object_key: str, file_name: str) -> str:
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(object_key)

    # Generate a signed URL for the blob (valid for 1 hour)
    url = blob.generate_signed_url(
        expiration=timedelta(seconds=3600), 
        method="GET",
        version="v4",
        response_disposition=f'attachment; filename="{file_name}"',

    )

    return url
