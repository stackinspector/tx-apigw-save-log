import os
import sys
import argparse
from api import get_apigw_client, get_cos_client, upload_file
from proc import proc

arg_parser = argparse.ArgumentParser(description="Collect logs of API gateway service of Tencent Cloud.")
arg_parser.add_argument("-r", "--region", required=True, type=str)
arg_parser.add_argument("-s", "--service-id", required=True, type=str)
arg_parser.add_argument("-b", "--bucket", type=str)
arg_parser.add_argument("-p", "--path", type=str)
arg_parser.add_argument("-d", "--date", type=str, help="%Y-%m-%d")
args = arg_parser.parse_args()

if args.bucket is not None and args.path is None:
    raise Exception("bucket name provided but path not provided")

secret_id = os.environ.get("TENCENTCLOUD_SECRETID")
secret_key = os.environ.get("TENCENTCLOUD_SECRETKEY")

apigw_client = get_apigw_client(secret_id, secret_key, args.region)

filename, data = proc(apigw_client, args.service_id, args.date)

if args.bucket is None:
    with open(filename, "xb") as file:
        file.write(data)
else:
    cos_client = get_cos_client(secret_id, secret_key, args.region)
    path = (args.path + "/" + filename).replace("//", "/")
    upload_file(cos_client, args.bucket, path, data)
