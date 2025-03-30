import ssl
import sys
from pathlib import Path

from bin.test_communication import http_get

# 获取当前文件的父目录的父目录（即client目录）
sys.path.append(str(Path(__file__).parent.parent))

# set your python working dir to: client, NOT the client/bin


####################################################
#  unset https_proxy      #disable you local http proxy
####################################################

# api_nginx_url = "https://backend.nginx2.ddl.com:444/"
api_nginx_url = "https://middle.nginx1.ddl.com/"

http_get(
            f"{api_nginx_url}secure/hello",
            headers={"X-CLIENT-SERVER-TOKEN":"this is a shared secret from client to server"},
            cacert_path="./certs/ca.crt",
            key_path="./certs/client.key",
            cert_path="./certs/client.crt",
        )