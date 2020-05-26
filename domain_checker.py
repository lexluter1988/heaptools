# -*- encoding: utf-8 -*-
# !/usr/bin/env python
import argparse
import socket
import ssl
from collections import OrderedDict
from pprint import pprint


def check_domain(domain):
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", type=str, help="Do SSL lockup for provided domain", required=True)
    args = parser.parse_args()
    result = check_domain(args.domain)
    pprint(result)


if __name__ == '__main__':
    main()
