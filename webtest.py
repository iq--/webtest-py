#! /usr/bin/env python

import os
import re
import sys
import urllib2
import logging as log

log.basicConfig(format='%(levelname)s:%(message)s', level=log.DEBUG)


class PreventHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, hdrs):
        raise urllib2.HTTPError(req.get_full_url(), code, msg, hdrs, fp)
    
    http_error_301 = http_error_303 = http_error_307 = http_error_302


def prepare_urllib2():
    cookie_processor = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(PreventHTTPRedirectHandler, cookie_processor)
    urllib2.install_opener(opener)


def run(file_name):
    with open(file_name, 'r') as f:
        for line in f:
            line = re.sub(r'#.*$', '', line).strip()
            if not line:
                continue
            code, url = line.split()
            check_url(url, int(code))
    f.closed


def check_url(url, code):
    try:
        response = urllib2.urlopen(url)
        resp_code = response.code
    except urllib2.HTTPError as e:
        resp_code = e.code
    
    if resp_code == code:
        log.info('%d for %s' % (code, url))
    else:
        log.warning('%d for %s (expect %d)' % (resp_code, url, code))


if __name__ == '__main__':
    if len(sys.argv) < 2 or not os.path.isfile(sys.argv[1]):
        sys.stderr.write('Usage: ./webtest.py PATH_TO_CONFIG\n')
        sys.exit(1)
    
    prepare_urllib2()
    run(sys.argv[1])

