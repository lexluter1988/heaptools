# -*- encoding: utf-8 -*-
# !/usr/bin/env python
import argparse
import logging
import socket
import ssl
from collections import OrderedDict

import requests

logger = logging.getLogger()


class Cert:
    """
    class to storing cert info
    domain, certs_names, issued_to, issued_by, expired
    """
    version = '0.1'

    def __init__(self, domain):
        self.domain = domain
        self.certs_names = ""
        self.issued_to = ""
        self.issued_by = ""
        self.expired = ""


class Site:
    """
    class to storing the checking site info
    contain domain name, http or https
    cert info, and history of redirects
    """
    version = '0.1'

    def __init__(self, domain):
        self.domain = domain
        self.ssl = True
        self.cert = None
        self.url_history = []

    def walk_http(self):
        pass

    def walk_https(self):
        pass

    def walk_ssl(self):
        pass


def init():
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def check_domain_cert(domain):
    result = OrderedDict()
    ctx = ssl.create_default_context()
    with ctx.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=domain) as s:
        try:
            s.settimeout(2)
            s.connect((domain, 443))
            cert = s.getpeercert()
        except Exception as e:
            result['domain'] = domain
            result['error'] = e
            return result

    subject = dict(x[0] for x in cert['subject'])
    issued_to = subject['commonName']
    issuer = dict(x[0] for x in cert['issuer'])
    issued_by = issuer['commonName']
    expired = cert['notAfter']
    dns = cert['subjectAltName']
    certs_names = []
    for k, v in dns:
        certs_names.append(v)

    result['domain'] = domain
    result['alternative_names'] = certs_names
    result['issued_to'] = issued_to
    result['issued_by'] = issued_by
    result['expired'] = expired

    return result


def check_domain_return(domain):
    history = []
    for protocol in ['http://', 'https://']:
        url = protocol+domain
        logger.info(f'Attempting to look for {url}')
        r = requests.get('http://' + domain, allow_redirects=False)
        if r.status_code == 301 or r.status_code == 302:
            history.append((url, r.status_code))
            logger.info('Redirect found')
            r = requests.get('http://' + domain, allow_redirects=True)
        history.append((r.url, r.status_code))

    return history


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", type=str, help="Do SSL lockup for provided domain", required=True)
    args = parser.parse_args()

    init()
    logger.info(f'Checking the domain {args.domain}')
    result = check_domain_cert(args.domain)
    result = check_domain_return(args.domain)
    print(result)
    logger.info(f'Success')


if __name__ == '__main__':
    main()
