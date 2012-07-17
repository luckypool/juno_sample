#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import sha
import hmac
import re

def get_input_data(web):
    return web['input']

def get_header(web):
    header = {}
    for value in web['HTTP_AUTHORIZATION'].replace('OAuth ','').split(', '):
        k = value.split('=')[0]
        v = value.split('=')[1]
        header[k] = v.replace('"','')
    return header

def validate_oauth_signature(web, secret):
    base_url = u'http://%(host)s%(uri)s' % {'host':web['HTTP_HOST'],'uri':web['REQUEST_URI']}
    if re.search('\?.*',base_url):
        base_url = re.sub('\?.*','',base_url)
    base   = 'GET&%s&' % urllib.quote_plus(base_url)

    header = get_header(web)
    base_param_dict = header.copy()
    del base_param_dict['realm']
    del base_param_dict['oauth_signature']
    base_param_dict.update(get_input_data(web).copy())
    base_str = ''
    for k in sorted(base_param_dict.keys()):
        base_str = base_str + '&%(k)s=%(v)s' % {'k':k,'v':base_param_dict[k]}
    base_str = base_str.lstrip('&')

    base = base+urllib.quote_plus(base_str)
    key = '%s&'%secret
    digested = hmac.new(key,base,sha).digest().encode('base64').strip()
    expect = urllib.unquote_plus(header['oauth_signature'])
    return {
        "result":digested==expect,
        "got":digested,
        "expect":expect
        }

