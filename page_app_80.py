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

CONSUMER_SECRET = cfg[50080]['secret']
HOST            = cfg['HOST']
MIXI_HOST       = cfg['MPA_HOST']
MY_HOST         = '%s:50080'%HOST
OTHER_HOST      = '%s:50081'%HOST

app_data = {'title' : u'初めてのﾍﾟｰｼﾞｱﾌﾟﾘﾓﾊﾞｲﾙ'}
app_data.update({'page':cfg[50080]['page']})
app_data.update({'other_page':cfg[50080]['other_page']})
app_data.update({'my_service_uri':get_host_uri(MY_HOST+'/m')})
app_data.update({'other_service_uri':get_host_uri(OTHER_HOST+'/m')})
app_data.update({'mixi_uri':get_host_uri(MIXI_HOST)})

init({'use_debugger': True,})

@route('/m')
def index(web):
    if (web['REQUEST_METHOD']=='POST'):
        app_data.update({'generated_url':generate_url(web, MIXI_HOST)})
        return template('url.html',{'app_data':app_data,'name':u'別ﾍﾟｰｼﾞ'})
    app_data.update(web['input'])
    app_data.update({'oauth_signature':validate_oauth_signature(web,CONSUMER_SECRET)})
    return template('mobile_80.html',{'app_data':app_data, 'name':u'ﾄｯﾌﾟﾍﾟｰｼﾞ'})

@route('/m/hello')
def index(web):
    app_data.update(web['input'])
    app_data.update({'oauth_signature':validate_oauth_signature(web,CONSUMER_SECRET)})
    return template('mobile_80.html',{'app_data':app_data,'name':u'別ﾍﾟｰｼﾞ'})

@route('/m/url')
def index(web):
    if (web['REQUEST_METHOD']!='POST'):
        return template('404.html', {"error":"405: Method Not Allowed"})
    app_data.update({'generated_url':generate_url(web, MIXI_HOST)})
    return template('url.html',{'app_data':app_data,'name':u'別ﾍﾟｰｼﾞ'})

if __name__ == '__main__':
    config('dev_port',50080)
    config('charset','sjis')
    config('content_type','application/xhtml+xml')
    run()

