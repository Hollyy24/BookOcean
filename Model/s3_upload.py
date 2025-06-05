import boto3
import os
import dotenv
import uuid
from fastapi import UploadFile


dotenv.load_dotenv()

CLOUDFRONT_DOMAIN = 'https://drwgulmgff88q.cloudfront.net'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SCRECT_KEY')
AWS_REGION = os.getenv('REGION')
AWS_S3_BUCKET_NAME = os.getenv('MY_BUCKET_NAME')


def generate_s3_filename(filename: UploadFile):
    extension = filename.filename.split('.')[-1]
    uid = uuid.uuid4().hex
    return f"profile/{uid}.{extension}"


def upload_files_to_S3(file: UploadFile, previous_url):

    s3_client = boto3.client(
        service_name='s3',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    try:
        objectname = generate_s3_filename(file)
        if previous_url:
            try:
                previous_key = previous_url.replace(
                    f"{CLOUDFRONT_DOMAIN}/", "")
                response = s3_client.delete_object(
                    Bucket=AWS_S3_BUCKET_NAME, Key=previous_key)
                print(f"刪除舊圖：{previous_key}")
            except Exception as e:
                print(f"刪除失敗：{e}")
                return False

        s3_client.upload_fileobj(file.file, AWS_S3_BUCKET_NAME, objectname)
        file_url = f"{CLOUDFRONT_DOMAIN}/{objectname}"
        print(f"成功：{file_url}")
        return file_url
    except Exception as e:
        print(f"失敗：{e}")
        return False
