import os
import sys
import argparse
from api import get_apigw_client, get_cos_client, upload_file
from proc import proc

arg_parser = argparse.ArgumentParser(description="Collect logs of API gateway service of Tencent Cloud.")
arg_parser.add_argument("-r", "--region", required=True, type=str)
arg_parser.add_argument("-s", "--service-id", required=True, type=str)
arg_parser.add_argument("-p", "--path", required=True, type=str)
arg_parser.add_argument("-b", "--bucket", type=str)
arg_parser.add_argument("-d", "--date", type=str, help="%Y-%m-%d")
args = arg_parser.parse_args()

region = args.region
service_id = args.service_id
path = args.path
bucket = args.bucket
date = args.date
access = (
    os.environ.get("TENCENTCLOUD_SECRETID"),
    os.environ.get("TENCENTCLOUD_SECRETKEY"),
    None,
)

apigw_client = get_apigw_client(region, access)
filename, data = proc(apigw_client, service_id, date)
full_path = os.path.join(path, filename)

if bucket is None:
    with open(full_path, "xb") as file:
        file.write(data)
else:
    cos_client = get_cos_client(region, access)
    upload_file(cos_client, bucket, full_path, data)
