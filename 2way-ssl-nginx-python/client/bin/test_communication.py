#!/usr/bin/env python
import argparse
import os
import pprint
import sys

import requests
from demoapiclient.lib.conf import app_settings

_cur_path = os.path.dirname(os.path.realpath(__file__))
_repo_path = _cur_path.split(os.sep)[:-2]


api_nginx_url = "https://middle.nginx1.ddl.com:8000/"


def http_get(url, headers=None, key_path=None, cert_path=None, cacert_path=None):
    """

    Args:
        url (str):
        headers (dict):
        key_path (str): The path to the Client cert key.
        cert_path (str): The path to the Client cert.
        cacert_path (str): The path to the CA cert. Only needed if Server is using a self-signed certificate

    Returns: (requests.Response)

    """
    if key_path and not cert_path:
        raise ValueError("Missing `cert_path`.")

    if not key_path and cert_path:
        raise ValueError("Missing `key_path`.")

    cert = None
    if key_path and cert_path:
        cert = (cert_path, key_path)

    res = requests.get(url, headers=headers, verify=cacert_path, cert=cert)
    print("Server replied with status_code: {}\n\nheaders:\n{}\n\nbody:\n{}\n\n".format(
        res.status_code,
        pprint.pformat(dict(res.headers)),
        res.text
    ))
    return res


def secure_http_get(url, headers=None, key_path=None, cert_path=None, cacert_path=None):
    """

    Args:
        url (str):
        headers (dict):
        key_path (str): The path to the Client cert key.
        cert_path (str): The path to the Client cert.
        cacert_path (str): The path to the CA cert. Only needed if Server is using a self-signed certificate

    Returns: (requests.Response)

    """
    if not headers:
        headers = {}

    headers[app_settings.SHARED_SECRET_CLIENT2SERVER_PARAM] = app_settings.SHARED_SECRET_CLIENT2SERVER_VALUE
    return http_get(url, headers=headers, key_path=key_path, cert_path=cert_path, cacert_path=cacert_path)

if __name__ == '__main__':
    http_get(
        f"{api_nginx_url}hello",
        cacert_path="./certs/ca.crt",
        key_path="./certs/client.key",
        cert_path="./certs/client.crt",
    )

if __name__ == '__55main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ca', type=str, help="Path to CA cert")
    parser.add_argument('--key', type=str, help="Path to client cert key")
    parser.add_argument('--cert', type=str, help="Path to client cert")

    subparsers = parser.add_subparsers()

    ncc_parser = subparsers.add_parser('ncc', help='Test - No client certificate supplied')
    ncc_parser.set_defaults(cmd='ncc')

    icc_parser = subparsers.add_parser('icc', help='Test - Invalid client certificate supplied')
    icc_parser.set_defaults(cmd='icc')

    vcc_parser = subparsers.add_parser('vcc', help='Test - Valid client certificate supplied')
    vcc_parser.set_defaults(cmd='vcc')

    psh_parser = subparsers.add_parser('psh', help='Ping secure hello route')
    psh_parser.set_defaults(cmd='psh')
    psh_parser.add_argument('--token', action='store_true', help="Add client token")

    lku_parser = subparsers.add_parser('lku', help='Lookup code')
    lku_parser.set_defaults(cmd='lku')
    lku_parser.add_argument('--token', action='store_true', help="Add client token")
    lku_parser.add_argument('code', action='store', nargs='?', help="Any code (any random string)")

    args = parser.parse_args()

    if not hasattr(args, "cmd"):
        print("")
        parser.print_help()
        print("")
        sys.exit(1)

    the_ca_path = args.ca
    if not the_ca_path:
        the_ca_path = os.path.join(os.sep.join(_repo_path), "certs", "ca.crt")

    the_key_path = args.key
    if not the_key_path:
        the_key_path = os.path.join(os.sep.join(_repo_path), "certs", "client.key")

    the_cert_path = args.cert
    if not the_cert_path:
        the_cert_path = os.path.join(os.sep.join(_repo_path), "certs", "client.crt")

    if args.cmd == 'ncc':
        http_get(f"{api_nginx_url}hello", cacert_path=the_ca_path)

    elif args.cmd == 'icc':
        http_get(
            f"{api_nginx_url}hello",
            cacert_path=the_ca_path,
            key_path=os.path.join(os.sep.join(_repo_path), "certs", "client_bad.key"),
            cert_path=os.path.join(os.sep.join(_repo_path), "certs", "client_bad.crt"),
        )

    elif args.cmd == 'vcc':
        http_get(
            f"{api_nginx_url}hello",
            cacert_path=the_ca_path,
            key_path=the_key_path,
            cert_path=the_cert_path,
        )

    elif args.cmd == 'psh':
        if args.token:
            secure_http_get(
                f"{api_nginx_url}secure/hello",
                cacert_path=the_ca_path,
                key_path=the_key_path,
                cert_path=the_cert_path,
            )
        else:
            http_get(
                f"{api_nginx_url}secure/hello",
                cacert_path=the_ca_path,
                key_path=the_key_path,
                cert_path=the_cert_path,
            )

    elif args.cmd == 'lku':
        the_url = f"{api_nginx_url}secure/lookup/%s"%args.code
        if args.token:
            secure_http_get(
                the_url,
                cacert_path=the_ca_path,
                key_path=the_key_path,
                cert_path=the_cert_path,
            )
        else:
            http_get(
                the_url,
                cacert_path=the_ca_path,
                key_path=the_key_path,
                cert_path=the_cert_path,
            )

    else:
        print("")
        parser.print_help()
        print("")
        sys.exit(1)
