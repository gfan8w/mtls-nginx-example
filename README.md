# Example of mTLS with NGINX

This example is to introduce you to the world of mutual authentication. This tutorial walks you through the steps of configuring two-way security using a NGINX server and connect a website. Therefore, I assume you have some familiarity with the above technologies as well as using Bash and Docker.
```
               client.crt     middle.crt  backend.crt
┌─────────┐           ┌─────────┐           ┌─────────┐       ┌─────────┐
│         │           │         │           │         │       │         │
│ Browser ├──────────►│ nginx 1 ├──────────►│ nginx 2 ├──────►│ Website │
│         │    HTTPS  │         │ mTLS      │         │ HTTPS │         │
└─────────┘           └─────────┘           └─────────┘       └─────────┘
```

`client.crt` used for web browser like Chrome, installed on `nginx 1`

`middle.crt` `middle.key` used for two-way security, installed on `nginx 1`

`backend.crt` `backend.key` used for two-way security, installed on `nginx 2`


## Create Server Certificate and Key

Clone this repository and open a terminal in the new subdirectory. Change the working directory to the following to `certs`.

```
mkdir certs
cd certs
```

Run the following command to generate the a server certificate and its corresponding private key. We are are going to use X.509 Certificate Data Management which is the standard format for public key certificates which contain the cryptographic key pairs with identities and information related to websites or organizations.

`openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout backend.key -out backend.crt`

For this example the `Common Name (e.g. server FQDN or YOUR name)` must be `backend`.

```
Generating a RSA private key
......+++++
.............................................+++++
writing new private key to 'backend.key'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:
State or Province Name (full name) [Some-State]:
Locality Name (eg, city) []:
Organization Name (eg, company) [Internet Widgits Pty Ltd]:
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:backend
Email Address []:
```

It will prompt for some details, simply hit enter all the way till the end. It will generate the following files:

`backend.crt` — Certificate for your server.

`backend.key` — Private key for your server.

In fact, you can now use this self-signed certificate to run your server as https. You should not use self-signed certificate for production server.

## Middle Certificate and Key

For mutual TLS authentication, you will need a certificate and private key for middle. Run the following command to generate them.

`openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout middle.key -out middle.crt`

Likewise, you should get the following certificates and private key

`middle.crt` — Certificate for your frontend, which used for communication with backend.

`middle.key` — Private key for your frontend, which used for communication with backend.

The next step is to combine both of them together as PKCS12 file so that you can use it with curl for mutual TLS authentication. It will prompt you for a password. Simply click enter to create a PKCS12 file without a password.

`openssl pkcs12 -export -out middle.pfx -inkey middle.key -in middle.crt`

Curl typically works with PEM format certificates, so you'll need to convert your PFX certificate to PEM format

`openssl pkcs12 -in middle.pfx -clcerts -out middle.pem -nodes`

if you add `-nodes`, then it gen without passphrase
if without `-nodes`, you just use 123456
```shell
Enter Import Password:         <blank, just hit enter to continue because we create it with no password>
Enter PEM pass phrase: 123456
Verifying - Enter PEM pass phrase: 123456
```

## Deploy the NGINX mTLS Proxies 

To finally spin up all components implemented before, we use Docker Compose for deploying the NGINX proxies. 

`docker-compose up --build`


## update the local host:

```
127.0.0.1  www.godppt.com
127.0.0.1  backend
```


## Rebuild the client cert for browser

1. generate root key, password is 123456

`openssl genrsa -des3 -out rootCA.key 2048`

  Enter PEM pass phrase: `123456`

2. generate the root cert:

`openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 1024 -out rootCA.pem`

**add the rootCA.pem to the list of your trusted root CAs**

3. create client cert request file and client key:

`openssl req -new -sha256 -nodes -out client.csr -newkey rsa:2048 -keyout client.key -config <( cat ../frontend.web.csr.cnf )`

4. create client cert by the client cert request file and root ca

`openssl x509 -req -in client.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out client.crt -days 500 -sha256 -extfile ../v3.ext`

create a X509 v3 certificate with `v3.ext` instead of a v1 which is the default when not specifying an extension file

using `godppt.com` as the CN, `*.godppt.com` as the SAN (Subject Alternative Name).

5. view cert info:
`openssl x509 -text -in client.crt -noout`
   
you can use the client.key and client.crt in your frontend web server and browse [https://www.godppt.com] without cert warning.

7. use `curl` to access the backend:
```shell
#--cert 指定客户端公钥证书的路径
#--key 指定客户端私钥文件的路径
#-k 使用本参数不校验证书的合法性，因为我们用的是自签名证书
#-v 可以使用 -v 来观察具体的SSL握手过程
curl --cert ./middle.crt --key ./middle.key https://backend:444 -k -v
# or try, if prompt: Enter PEM pass phrase: just type 123456, it depends on wether you create it w/o password
curl -E middle.pem https://backend:444 -k -v
```

if request without the cert:

`curl https://backend:444 -v -k`

backend nginx report: `400 No required SSL certificate was sent`

8. open the Chrome, visit: `https://www.godppt.com`.


## References
https://levelup.gitconnected.com/certificate-based-mutual-tls-authentication-with-nginx-57c7e693

https://mailman.nginx.org/pipermail/nginx/2020-June/059526.html

https://medium.com/geekculture/mtls-with-nginx-and-nodejs-e3d0980ed950

https://smallstep.com/hello-mtls/doc/client/nginx-proxy

https://alexanderzeitler.com/articles/Fixing-Chrome-missing_subjectAltName-selfsigned-cert-openssl/[https://alexanderzeitler.com/articles/Fixing-Chrome-missing_subjectAltName-selfsigned-cert-openssl/]
