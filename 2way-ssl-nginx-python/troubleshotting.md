Error:
```  File "/Users/mac/miniconda3/envs/py12/lib/python3.12/site-packages/requests/adapters.py", line 698, in send
    raise SSLError(e, request=request)
requests.exceptions.SSLError: HTTPSConnectionPool(host='backend.nginx2.ddl.com', port=444): Max retries exceeded with url: /hello (Caused by SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1010)')))
```

1. 先用 openssl 测试连接
```openssl s_client -connect backend.nginx2.ddl.com:444 -servername backend.nginx2.ddl.com -showcerts -CAfile certs/ca.crt
CONNECTED(00000003)
depth=0 C = SG, O = Server Backend Nginx2 Ltd, OU = Engineering, CN = backend.nginx2.ddl.com
verify error:num=20:unable to get local issuer certificate
verify return:1
depth=0 C = SG, O = Server Backend Nginx2 Ltd, OU = Engineering, CN = backend.nginx2.ddl.com
verify error:num=21:unable to verify the first certificate
verify return:1
depth=0 C = SG, O = Server Backend Nginx2 Ltd, OU = Engineering, CN = backend.nginx2.ddl.com
verify return:1
---
```
如果连接失败，说明是服务器端问题

如果成功，继续检查 Python 代码

 % openssl verify -CAfile ./certs/ca.crt ./certs/client.crt
./certs/client.crt: OK


```
 openssl s_client -connect backend.nginx2.ddl.com:444 \
  -cert ./certs/client.crt \
  -key ./certs/client.key \
  -CAfile ./certs/ca.crt \
  -tlsextdebug -state
```
出现：
```SSL handshake has read 2505 bytes and written 3911 bytes
Verification: OK
```
表示成功
