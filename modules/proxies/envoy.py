#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import requests
import random

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


def envoy(url, s):
    """
        Envoy:
        X-Envoy-external-adress
        X-Envoy-internal
        X-Envoy-Original-Dst-Host
        X-Echo-Set-Header: X-Foo: value1
    """
    url = "{}?cb={}".format(url, random.randint(1, 100))
    envoy_header_list = [
        {"X-Envoy-external-adress": "plop123"},
        {"X-Envoy-internal": "plop123"}, 
        {"X-Envoy-Original-Dst-Host": "plop123"},
        {"X-Echo-Set-Header": "X-Foo: plop123"},
        {"x-envoy-original-path": "/plop123"},
    ]
    for ehl in envoy_header_list:
        x_req = s.get(url, headers=ehl, verify=False, timeout=10)
        print(f"   └── {ehl}{'→':^3} {x_req.status_code:>3} [{len(x_req.content)} bytes]")
        if "plop123" in x_req.text or "plop123" in x_req.headers:
            print("\033[33m   └── INTERESTING BEHAVIOR\033[0m | HEADER REFLECTION | \033[34m{}\033[0m | PAYLOAD: {}".format(url, ehl))

if __name__ == '__main__':

    url = sys.argv[1]
    url = "{}?cb={}".format(url, random.randint(1, 100))
    s = requests.session()

    envoy(url, s)