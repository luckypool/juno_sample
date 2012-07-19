#!/usr/bin/env python
# -*- coding: utf-8 -*-
from juno import *
import urllib
import yaml
import codecs
from mymod import validate_oauth_signature
from mymod import get_host_uri

fh = codecs.open('./config/config.yaml','r','utf8')
cfg = yaml.load(fh)

CONSUMER_SECRET = cfg[50081]['secret']
HOST            = cfg['HOST']
MIXI_HOST       = cfg['MPA_HOST']
MY_HOST         = '%s:50081'%HOST
OTHER_HOST      = '%s:50080'%HOST

app_data = {'title': u'続・初めてのﾍﾟｰｼﾞｱﾌﾟﾘﾓﾊﾞｲﾙ'}
app_data.update({'host':MY_HOST})
app_data.update({'my_service_uri':get_host_uri(MY_HOST+'/m')})
app_data.update({'other_service_uri':get_host_uri(OTHER_HOST+'/m')})
app_data.update({'mixi_uri':get_host_uri(MIXI_HOST)})
app_data.update({'other_page':cfg[50080]['page']})

init({'use_debugger': True,})

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
    return template('mobile_81.html',{'app_data':app_data,'name':u'別ﾍﾟｰｼﾞ(%s)'%name})

if __name__ == '__main__':
    config('dev_port',50081)
    config('charset','sjis')
    config('content_type','application/xhtml+xml')
    run()

