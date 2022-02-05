import os
from api import get_apigw_client, get_cos_client, upload_file
from proc import proc

def main_handler(event, context):
    region = os.environ.get("REGION")
    service_id = os.environ.get("SERVICE_ID")
    path = os.environ.get("FILE_PATH")
    bucket = os.environ.get("BUCKET")
    access = (
        os.environ.get("TENCENTCLOUD_SECRETID"),
        os.environ.get("TENCENTCLOUD_SECRETKEY"),
        os.environ.get("TENCENTCLOUD_SESSIONTOKEN"),
    )

    apigw_client = get_apigw_client(region, access)
    filename, data = proc(apigw_client, service_id, None)
    full_path = os.path.join(path, filename)
    cos_client = get_cos_client(region, access)
    upload_file(cos_client, bucket, full_path, data)
    return {"statusCode": 200}
