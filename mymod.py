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

def generate_url(web, host):
    post_dict = web['POST_DICT']
    url = 'http://%(host)s/%(app_id)s/%(module_id)s/?guid=ON&url=%(url)s' % {
            'host'      : host,
            'app_id'    : post_dict['field_app_id'][0],
            'module_id' : post_dict['field_module_id'][0],
            'url'       : post_dict['field_url'][0],
            }
    return {
        'raw':url,
        'enc':urllib.quote_plus(url),
    }

def get_host_uri(url):
    return {
        'raw':u'http://%s/'%url,
        'enc':urllib.quote_plus(u'http://%s/'%url),
        }
