from uuid import uuid4
from fastapi import UploadFile
from minio import Minio
from datetime import timedelta
from io import BytesIO
import os

minio_client = Minio(
    endpoint=os.getenv("MINIO_ENDPOINT"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False
)

BUCKET_NAME = os.getenv("MINIO_BUCKET")

def upload_file(file: UploadFile) -> str:
    object_key = f"{uuid4()}_{file.filename}"
    content = file.file

    # Ensure bucket exists
    if not minio_client.bucket_exists(BUCKET_NAME):
        minio_client.make_bucket(BUCKET_NAME)

    minio_client.put_object(
        bucket_name=BUCKET_NAME,
        object_name=object_key,
        data=content,
        length=-1,
        part_size=20 * 1024 * 1024,  # 20MB
    )
    return object_key

def upload_generated_file(content: str, filename: str) -> str:
    object_key = f"{uuid4()}_{filename}"
    file_stream = BytesIO(content.encode("utf-8"))

    if not minio_client.bucket_exists(BUCKET_NAME):
        minio_client.make_bucket(BUCKET_NAME)

    minio_client.put_object(
        bucket_name=BUCKET_NAME,
        object_name=object_key,
        data=file_stream,
        length=file_stream.getbuffer().nbytes,
        part_size=10 * 1024 * 1024,
    )
    return object_key

def get_file(object_key: str):
    try:
        response = minio_client.get_object(BUCKET_NAME, object_key)
        return response
    except Exception as e:
        print(f"Error retrieving file: {e}")
        raise


def delete_file(object_key: str):
    minio_client.remove_object(BUCKET_NAME, object_key)


def get_presigned_url(object_key: str) -> str:
    return minio_client.presigned_get_object(
        BUCKET_NAME, 
        object_key, 
        expires=timedelta(seconds=3600)
    )