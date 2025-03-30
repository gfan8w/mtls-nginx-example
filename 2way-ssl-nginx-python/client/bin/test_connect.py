import ssl
import sys
from pathlib import Path
import requests
from requests.adapters import HTTPAdapter
from urllib3 import PoolManager
from urllib3.util import create_urllib3_context

# 获取当前文件的父目录的父目录（即client目录）
sys.path.append(str(Path(__file__).parent.parent))

####################################################
#  unset https_proxy      #disable you local http proxy
####################################################

# curl https://backend.nginx2.ddl.com:444/hello \
# --cacert certs/ca.crt --cert certs/client.crt --key certs/client.key  \
# -H 'X-CLIENT-SERVER-TOKEN:this is a shared secret from client to server'

api_nginx_url = "https://backend.nginx2.ddl.com:444/"

CIPHERS = (
    'AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA'
)


class TlsAdapter(HTTPAdapter):

    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = create_urllib3_context(ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args,
                                       ssl_context=ctx,
                                       **pool_kwargs)


session = requests.session()
adapter = TlsAdapter(ssl.OP_NO_TLSv1_3 | ssl.OP_NO_TLSv1_3)
session.mount("https://", adapter)

try:
    response = session.get(
        "https://backend.nginx2.ddl.com:444/hello",
        cert=("./certs/client.crt", "./certs/client.key"),
        verify="./certs/ca.crt"
    )
    print(response.text)
finally:
    pass


# http_get(
#             f"{api_nginx_url}hello",
#             cacert_path="./certs/ca.crt",
#             key_path="./certs/client.key",
#             cert_path="./certs/client.crt",
#         )