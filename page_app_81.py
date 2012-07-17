#!/usr/bin/env python
# -*- coding: utf-8 -*-
from juno import *
import urllib
import sha
import hmac
import re
from my_valid import validate_oauth_signature

HOST            = '291.94.24.161'
MY_HOST         = '%s:50081'%HOST
OTHER_HOST      = '%s:50080'%HOST
CONSUMER_SECRET = '4f1b49683604271dbb1168a277021887e37459e5'
MIXI_HOST       = 'mpa.mixi.net'


#debugger使用時に指定。werkzeugのdebuggerで表示される。
init({'use_debugger': True,})

app_data = {
    'title'    : u'続・初めてのﾍﾟｰｼﾞｱﾌﾟﾘﾓﾊﾞｲﾙ',
}

def get_host_uri(url):
    return {
        'raw':u'http://%s/'%url,
        'enc':urllib.quote_plus(u'http://%s/'%url),
        }
app_data.update({'host':MY_HOST})
app_data.update({'my_service_uri':get_host_uri(MY_HOST+'/m')})
app_data.update({'other_service_uri':get_host_uri(OTHER_HOST+'/m')})
app_data.update({'mixi_uri':get_host_uri(MIXI_HOST)})

@route('/m')
def index(web):
    app_data.update({'request_uri':web['REQUEST_URI']})
    app_data.update(web['input'])
    app_data.update({'oauth_signature':validate_oauth_signature(web,CONSUMER_SECRET)})
    return template('mobile_81.html',{'app_data':app_data, 'name':u'ﾄｯﾌﾟﾍﾟｰｼﾞ'})

@route('/m/:name')
def index(web,name):
    app_data.update({'request_uri':web['REQUEST_URI']})
    app_data.update(web['input'])
    app_data.update({'oauth_signature':validate_oauth_signature(web,CONSUMER_SECRET)})
    return template('mobile_81.html',{'app_data':app_data,'name':name})

if __name__ == '__main__':
    config('dev_port',50081)
    config('charset','sjis')
    config('content_type','application/xhtml+xml')
    run()

