from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.apigateway.v20180808 import models
from tencentcloud.apigateway.v20180808.apigateway_client import ApigatewayClient
from qcloud_cos import CosConfig, CosS3Client

def get_apigw_client(secret_id, secret_key, region):
    cred = credential.Credential(secret_id, secret_key)
    http_profile = HttpProfile()
    http_profile.endpoint = "apigateway.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.http_profile = http_profile
    return ApigatewayClient(cred, region, client_profile)

def get_cos_client(secret_id, secret_key, region):
    cos_config = CosConfig(SecretId=secret_id, SecretKey=secret_key, Region=region)
    return CosS3Client(cos_config)

def get_log(client, start, end, service_id, context):
    req = models.DescribeLogSearchRequest()
    req._deserialize({
        "StartTime": start,
        "EndTime": end,
        "Limit": 100,
        "Sort": "desc",
        "ServiceId": service_id,
        "ConText": context,
    })
    resp = client.DescribeLogSearch(req)
    return resp.LogSet, resp.ConText

def upload_file(client, bucket, filename, data):
    resp = client.put_object(Bucket=bucket, Body=data, Key=filename)
    print(resp)
