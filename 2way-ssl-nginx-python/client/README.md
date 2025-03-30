# `demoapiclient`

A python commandline to demonstrate how 2-way SSL works from a Client's perspective.

**Prerequisite:**

1. You should have already generated all the necessary Client SSL Certificates mentioned [here](../README.md#generate-self-signed-ca-certificates).

2. Python 3.6 or higher installed in your environment.

(_Note: All commands listed in this README are only tested in an Ubuntu 18.04 environment._)

**Assumption:**

To run the commands listed below, it is assumed your current working directory is `<path to this repo>/client`.

---
- [Install the Client app](#install-the-client-app)

- [Testing (General routes)](#testing-general-routes)
  - [No client certificate supplied](#no-client-certificate-supplied)
  - [Invalid client certificate supplied](#invalid-client-certificate-supplied)
  - [Valid client certificate supplied](#valid-client-certificate-supplied)

- [Testing (Secure routes)](#testing-secure-routes)
  - [Ping hello route without client token](#ping-hello-route-without-client-token)
  - [Ping hello route with client token](#ping-hello-route-with-client-token)

- [Testing (Secure Dummy Data Lookup route)](#testing-secure-dummy-data-lookup-route)
  - [Successful action ("known" code)](#successful-action-known-code)
  - [Failed action ("unknown" code)](#failed-action-unknown-code)
---

## Install the Client app

```
python setup.py develop
```

## Testing (General routes)

#### No client certificate supplied

Run:

```
./bin/test_communication.py ncc
```

Response:

```
Server replied with status_code: 400

headers:
{'Connection': 'close',
 'Content-Length': '246',
 'Content-Type': 'text/html'}

body:
<html>
<head><title>400 No required SSL certificate was sent</title></head>
<body bgcolor="white">
<center><h1>400 Bad Request</h1></center>
<center>No required SSL certificate was sent</center>
<hr><center>nginx</center>
</body>
</html>
```

#### Invalid client certificate supplied

Run:

```
./bin/test_communication.py icc
```

Response:

```
Server replied with status_code: 400

headers:
{'Connection': 'close',
 'Content-Length': '224',
 'Content-Type': 'text/html'}

body:
<html>
<head><title>400 The SSL certificate error</title></head>
<body bgcolor="white">
<center><h1>400 Bad Request</h1></center>
<center>The SSL certificate error</center>
<hr><center>nginx</center>
</body>
</html>
```

#### Valid client certificate supplied

Run:

```
./bin/test_communication.py vcc
```

Response:

```
Server replied with status_code: 200

headers:
{'Cache-Control': 'no-cache',
 'Connection': 'keep-alive',
 'Content-Length': '17',
 'Content-Type': 'application/json'}

body:
{"success":true}
```

## Testing (Secure routes)

For added security, other then using Client Certificate to verify the Client's identity by the Server, the Client
should also supply a "shared secret" for every call to the Server's "secure routes".

The "shared secret" will be included in the header of the HTTP Request. In this `demoapiclient`, the token
parameter name will be `X-CLIENT-SERVER-TOKEN` (see [client/demoapiclient/lib/conf/app_settings.py](./demoapiclient/lib/conf/app_settings.py)).

#### Ping hello route without client token

Run:

```
./bin/test_communication.py psh
```

Response:

```
Server replied with status_code: 401

headers:
{'Connection': 'keep-alive',
 'Content-Length': '49',
 'Content-Type': 'application/json'}

body:
{"error":"Invalid client token","success":false}
```

#### Ping hello route with client token

Run:

```
./bin/test_communication.py psh --token
```

Response:

```
Server replied with status_code: 200

headers:
{'Cache-Control': 'no-cache',
 'Connection': 'keep-alive',
 'Content-Length': '17',
 'Content-Type': 'application/json',
 'X-SERVER-CLIENT-TOKEN': 'this is a shared secret from server to client'}

body:
{"success":true}
```

Notice that the Server replied with another "shared secret" token `X-SERVER-CLIENT-TOKEN`. For added security, Client
should validate this token.


## Testing (Secure Dummy Data Lookup route)

`Dummy Data Lookup` is a dummy action to demonstrate how the Server should respond upon an unsuccessful action.

#### Successful action ("known" code)

Run:

```
./bin/test_communication.py lku --token "known"
```

Response:

```
Server replied with status_code: 200

headers:
{'Cache-Control': 'no-cache',
 'Connection': 'keep-alive',
 'Content-Length': '41',
 'Content-Type': 'application/json',
 'Date': 'Sun, 25 Oct 2020 14:18:39 GMT',
 'Server': 'nginx',
 'X-SERVER-CLIENT-TOKEN': 'this is a shared secret from server to client'}

body:
{"data":{"code":"known"},"success":true}
```

#### Failed action ("unknown" code)

Run:

```
./bin/test_communication.py lku --token "unknown"
```

Response:

```
Server replied with status_code: 404

headers:
{'Connection': 'keep-alive',
 'Content-Length': '63',
 'Content-Type': 'application/json'}

body:
{"data":null,"error":"Unknown code `unknown`","success":false}
```

Notice that the Server didn't reply with `X-SERVER-CLIENT-TOKEN` during failure.
