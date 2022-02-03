from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.apigateway.v20180808 import apigateway_client, models

class Client:
    def __init__(self, secret_id, secret_key):
        cred = credential.Credential(secret_id, secret_key)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "apigateway.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        self.inner = apigateway_client.ApigatewayClient(cred, "ap-shanghai", clientProfile)

    def get_log(self, start, end, service_id, context):
        req = models.DescribeLogSearchRequest()
        req._deserialize({
            "StartTime": start,
            "EndTime": end,
            "Limit": 100,
            "Sort": "desc",
            "ServiceId": service_id,
            "ConText": context,
        })
        resp = self.inner.DescribeLogSearch(req)
        return resp.LogSet, resp.ConText
