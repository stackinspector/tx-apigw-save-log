import os
from api import get_apigw_client, get_cos_client, upload_file
from proc import proc

def main_handler(event, context):
    region = os.environ.get("REGION")
    service_id = os.environ.get("SERVICE_ID")
    path = os.environ.get("PATH")
    bucket = os.environ.get("BUCKET")
    secret_id = os.environ.get("TENCENTCLOUD_SECRETID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRETKEY")

    apigw_client = get_apigw_client(secret_id, secret_key, region)
    filename, data = proc(apigw_client, service_id, None)
    full_path = os.path.join(path, filename)
    cos_client = get_cos_client(secret_id, secret_key, region)
    upload_file(cos_client, bucket, full_path, data)
    return {"statusCode": 200}
