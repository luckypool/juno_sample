#!/usr/bin/env python
# -*- coding: utf-8 -*-
from juno import *
import urllib
import sha
import hmac
import re

HOST            = 'XXXX'
MY_HOST         = '%s:8004'%HOST
OTHER_HOST      = '%s:8003'%HOST
CONSUMER_SECRET = 'XXXX'
MIXI_HOST       = 'ma.mixi.net'


#debugger使用時に指定。werkzeugのdebuggerで表示される。
init({'use_debugger': True,})

app_data = {
    'title'    : u'初めてのﾓﾊﾞｲﾙｱﾌﾟﾘ 2nd',
    'id'       : {'self':2333, 'other':2332},
}

def get_host_uri(url):
    return {
        'raw':u'http://%s/'%url,
        'enc':urllib.quote_plus(u'http://%s/'%url),
        }
app_data.update({'my_service_uri':get_host_uri(MY_HOST+'/m')})
app_data.update({'other_service_uri':get_host_uri(OTHER_HOST+'/m')})
app_data.update({'mixi_uri':get_host_uri(MIXI_HOST)})

def get_input_data(web):
    return web['input']

def get_header(web):
    header = {}
    for value in web['HTTP_AUTHORIZATION'].replace('OAuth ','').split(', '):
        k = value.split('=')[0]
        v = value.split('=')[1]
        header[k] = v.replace('"','')
    return header

def validate_oauth_signature(web):
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
    key    = '%s&'%CONSUMER_SECRET
    digested = hmac.new(key,base,sha).digest().encode('base64').strip()
    expect = urllib.unquote_plus(get_header(web)['oauth_signature'])
    return {
        "result":digested==expect,
        "got":digested,
        "expect":expect
        }

@route('/m')
def index(web):
    app_data.update({'oauth_signature':validate_oauth_signature(web)})
    return template('mobile_8004.html',{'app_data':app_data, 'name':u'ﾄｯﾌﾟﾍﾟｰｼﾞ'})

@route('/m/:name')
def index(web,name):
    app_data.update({'oauth_signature':validate_oauth_signature(web)})
    return template('mobile_8004.html',{'app_data':app_data,'name':name})

if __name__ == '__main__':
    config('dev_port',8004)
    config('charset','sjis')
    config('content_type','application/xhtml+xml')
    run()

