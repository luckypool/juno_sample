#!/usr/bin/env python
# -*- coding: utf-8 -*-
from juno import *
import urllib
import yaml
import codecs
from mymod import validate_oauth_signature
from mymod import generate_url
from mymod import get_host_uri

fh  = codecs.open('./config/config.yaml','r','utf8')
cfg = yaml.load(fh)

CONSUMER_SECRET = cfg[50083]['secret']
HOST            = cfg['HOST']
MIXI_HOST       = cfg['MA_HOST']
MY_HOST         = '%s:50083'%HOST
OTHER_HOST      = '%s:50084'%HOST

app_data = {'title': u'初めてのmixiｱﾌﾟﾘﾓﾊﾞｲﾙ'}
app_data.update({'id':cfg[50083]['id']})
app_data.update({'my_service_uri':get_host_uri(MY_HOST+'/m')})
app_data.update({'other_service_uri':get_host_uri(OTHER_HOST+'/m')})
app_data.update({'mixi_uri':get_host_uri(MIXI_HOST)})

init({'use_debugger': True,})

@route('/m')
def index(web):
    app_data.update({'oauth_signature':validate_oauth_signature(web, CONSUMER_SECRET)})
    return template('mobile_83.html',{'app_data':app_data, 'name':u'ﾄｯﾌﾟﾍﾟｰｼﾞ'})

@route('/m/hello')
def index(web):
    app_data.update({'oauth_signature':validate_oauth_signature(web, CONSUMER_SECRET)})
    return template('mobile_83.html',{'app_data':app_data,'name':u'別ﾍﾟｰｼﾞだよ'})

@route('/m/url')
def index(web):
    if (web['REQUEST_METHOD']!='POST'):
        return template('404.html', {"error":"405: Method Not Allowed"})
    app_data.update({'generated_url':generate_url(web,MIXI_HOST)})
    return template('url.html',{'app_data':app_data,'name':u'別ﾍﾟｰｼﾞだよ'})

if __name__ == '__main__':
    config('dev_port',50083)
    config('charset','sjis')
    config('content_type','application/xhtml+xml')
    run()

