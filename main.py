import os
import argparse
from api import get_apigw_client, get_cos_client, upload_file
from proc import proc

arg_parser = argparse.ArgumentParser(description="以天为单位保存腾讯云API网关日志。可选上传到腾讯云COS。")
arg_parser.add_argument("-r", "--region", required=True, type=str, help="目标API网关和（如上传到COS）bucket的所在区域")
arg_parser.add_argument("-s", "--service-id", required=True, type=str, help="目标API网关的service id")
arg_parser.add_argument("-p", "--path", required=True, type=str, help="保存日志的路径（本地路径或bucket路径）")
arg_parser.add_argument("-b", "--bucket", type=str, help="（如上传到COS）上传到bucket的名称")
arg_parser.add_argument("-d", "--date", type=str, help="（如要指定日期）要保存哪一天的日志，日期格式为Y-m-d")
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
