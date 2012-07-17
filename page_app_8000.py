#!/usr/bin/env python
# -*- coding: utf-8 -*-
from juno import *
import urllib
from my_valid import validate_oauth_signature

HOST            = 'XXXXXXXXXXX'
MY_HOST         = '%s:8000'%HOST
OTHER_HOST      = '%s:8001'%HOST
CONSUMER_SECRET = 'XXXXXX'
MIXI_HOST       = 'mpa.mixi.net'

#debugger使用時に指定。werkzeugのdebuggerで表示される。
init({'use_debugger': True,})

app_data = {
    'title' : u'初めてのﾍﾟｰｼﾞｱﾌﾟﾘﾓﾊﾞｲﾙ',
    'page'  : {
        'id': 15027,
        'module_id': {
            'self' :60953,
            'other':60954
        },
    },
    'other_page' : {
        'id' : 15124,
        'module_id' : {
            'self' : 61426,
        },
    }
}

def get_host_uri(url):
    return {
        'raw':u'http://%s/'%url,
        'enc':urllib.quote_plus(u'http://%s/'%url),
        }
app_data.update({'my_service_uri':get_host_uri(MY_HOST+'/m')})
app_data.update({'other_service_uri':get_host_uri(OTHER_HOST+'/m')})
app_data.update({'mixi_uri':get_host_uri(MIXI_HOST)})

def generate_url(web):
    post_dict = web['POST_DICT']
    url = 'http://%(host)s/%(app_id)s/%(module_id)s/?guid=ON&url=%(url)s' % {
            'host'      : MIXI_HOST,
            'app_id'    : post_dict['field_app_id'][0],
            'module_id' : post_dict['field_module_id'][0],
            'url'       : post_dict['field_url'][0],
            }
    return {
        'raw':url,
        'enc':urllib.quote_plus(url),
    }

@route('/m')
def index(web):
    app_data.update(web['input'])
    app_data.update({'oauth_signature':validate_oauth_signature(web,CONSUMER_SECRET)})
    return template('mobile_8000.html',{'app_data':app_data, 'name':u'ﾄｯﾌﾟﾍﾟｰｼﾞ'})

@route('/m/hello')
def index(web):
    app_data.update(web['input'])
    app_data.update({'oauth_signature':validate_oauth_signature(web,CONSUMER_SECRET)})
    return template('mobile_8000.html',{'app_data':app_data,'name':u'別ﾍﾟｰｼﾞだよ'})

@route('/m/url')
def index(web):
    if (web['REQUEST_METHOD']!='POST'):
        return template('404.html', {"error":"405: Method Not Allowed"})
    app_data.update({'generated_url':generate_url(web)})
    return template('url.html',{'app_data':app_data,'name':u'別ﾍﾟｰｼﾞだよ'})

if __name__ == '__main__':
    config('dev_port',8000)
    config('charset','sjis')
    config('content_type','application/xhtml+xml')
    run()

