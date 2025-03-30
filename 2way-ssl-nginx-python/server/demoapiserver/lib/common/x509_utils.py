import urllib
from base64 import b64decode
from urllib import parse

from OpenSSL import crypto

from demoapiserver.lib.common.flask_utils import log_error


def pem_str_to_x509(pem_str_url_encoded):
    """

    Args:
        pem_str (str): the X509 certificate PEM string

    Returns: (OpenSSL.crypto.X509)

    """
    if not pem_str_url_encoded:
        return None

    try:
        assert isinstance(pem_str_url_encoded, str), type(pem_str_url_encoded)
        pem_str = parse.unquote(pem_str_url_encoded)
        assert pem_str, 'Empty data'
        pem_lines = [pem_str.strip() for pem_str in pem_str.strip().split('\n')]
        assert pem_lines[0] == '-----BEGIN CERTIFICATE-----', 'Bad begin'
        assert pem_lines[-1] == '-----END CERTIFICATE-----', 'Bad end'
    except AssertionError as e:
        log_error(e)
        raise ValueError("`pem_str` is not a valid PEM string. Error: {}".format(e))

    der_data = b64decode("".join(pem_lines[1:-1]))
    return crypto.load_certificate(crypto.FILETYPE_ASN1, der_data)


def get_issuer_cn_from_x509(x509):
    """

    Args:
        x509 (OpenSSL.crypto.X509):

    Returns: (str)

    """
    issuer = x509.get_issuer()
    return issuer.CN


def get_subject_cn_from_x509(x509):
    """

    Args:
        x509 (OpenSSL.crypto.X509):

    Returns: (str)

    """
    subject = x509.get_subject()
    return subject.CN
