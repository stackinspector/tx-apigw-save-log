import os
import sys
from api import Client
from proc import proc

date = None if (len(sys.argv) == 1) else sys.argv[1]
client = Client(os.environ.get("TENCENTCLOUD_SECRETID"), os.environ.get("TENCENTCLOUD_SECRETKEY"))
service_id = os.environ.get("APIGW_SERVICE_ID")

filename, data = proc(client, service_id, date)

with open(filename, "xb") as file:
    file.write(data)
