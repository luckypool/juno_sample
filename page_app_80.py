#!/usr/bin/env python
# -*- coding: utf-8 -*-
from juno import *
import urllib
from my_valid import validate_oauth_signature

HOST            = '219.94.242.161'
MY_HOST         = '%s:50080'%HOST
OTHER_HOST      = '%s:50081'%HOST
CONSUMER_SECRET = '9205431840be1c4f163b49c6bc99c06be6d01f65'
MIXI_HOST       = 'mpa.mixi.net'

init({'use_debugger': True,})

app_data = {
    'title' : u'初めてのﾍﾟｰｼﾞｱﾌﾟﾘﾓﾊﾞｲﾙ',
    'page'  : {
        'id': 271847,
        'module_id': {
            'self' :1530801,
            'other':1530802
        },
    },
    'other_page' : {
        'id' : 271848,
        'module_id' : {
            'self' : 1530808,
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
    return template('mobile_80.html',{'app_data':app_data, 'name':u'ﾄｯﾌﾟﾍﾟｰｼﾞ'})

@route('/m/hello')
def index(web):
    app_data.update(web['input'])
    app_data.update({'oauth_signature':validate_oauth_signature(web,CONSUMER_SECRET)})
    return template('mobile_80.html',{'app_data':app_data,'name':u'別ﾍﾟｰｼﾞだよ'})

@route('/m/url')
def index(web):
    if (web['REQUEST_METHOD']!='POST'):
        return template('404.html', {"error":"405: Method Not Allowed"})
    app_data.update({'generated_url':generate_url(web)})
    return template('url.html',{'app_data':app_data,'name':u'別ﾍﾟｰｼﾞだよ'})

if __name__ == '__main__':
    config('dev_port',50080)
    config('charset','sjis')
    config('content_type','application/xhtml+xml')
    run()

