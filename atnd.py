# coding: utf-8
# vim: fileencoding=utf-8
import time
import datetime
import urllib
import urllib2
import xml.dom.minidom

class Atnd:
    def __init__(self):
        None

    def event_search(self, param={}):
        url = 'http://api.atnd.org/events/?%s' % (self.prepare_query(param))
        print url
        doc = xml.dom.minidom.parseString(urllib2.urlopen(url).read())
        root = doc.documentElement 
        events_dom = root.getElementsByTagName('event')
    
        ret = {}
        ret['results_returned'] = root.getElementsByTagName('results_returned')[0].firstChild.data
        ret['results_start'] = root.getElementsByTagName('results_start')[0].firstChild.data
    
        event_structure = (
                           'event_id',
                           'title',
                           'catch',
                           'description',
                           'event_url',
                           'started_at',
                           'ended_at',
                           'url',
                           'limit',
                           'address',
                           'place',
                           'lat',
                           'lon',
                           'owner_id',
                           'owner_nickname',
                           'owner_twitter_id',
                           'accepted',
                           'waiting',
                           'updated_at')
        event = []
        for e in events_dom:
            data = {}
            for tag in event_structure:
                elem = e.getElementsByTagName(tag)[0]
                if elem.hasChildNodes():
                    data[tag] = elem.firstChild.data
            event.append(data)

        ret['event'] = event
        
        return ret 
 
    def event_user_search(self, param={}):
        url = 'http://api.atnd.org/events/users/?%s' % (self.prepare_query(param))
        print url
        doc = xml.dom.minidom.parseString(urllib2.urlopen(url).read())
        results_returned = doc.getElementsByTagName('results_returned')[0].firstChild.data
        results_start = doc.getElementsByTagName('results_start')[0].firstChild.data
        event = doc.getElementsByTagName('event')
        ret = []
        # 0 replace results_start?
        for i in xrange(0, int(results_returned)):
            event_id = event[i].getElementsByTagName('event_id')
            title = event[i].getElementsByTagName('title')
            event_url = event[i].getElementsByTagName('event_url')
            limit = event[i].getElementsByTagName('limit')
            accepted = event[i].getElementsByTagName('accepted')
            waiting = event[i].getElementsByTagName('waiting')
            users = event[i].getElementsByTagName('users')
            
            user_id = []
            nickname = []
            twitter_id = []
            status = []
            user = users.item(0).getElementsByTagName('user')
            for j in xrange(0, int(user.length)):
                user_id.append(user.item(j).getElementsByTagName('user_id').item(0).firstChild.data)
                nickname.append(user.item(j).getElementsByTagName('nickname').item(0).firstChild.data)
                #twitter_id.append(user.item(j).getElementsByTagName('twitter_id').item(0).firstChild.data)
                status.append(user.item(j).getElementsByTagName('status').item(0).firstChild.data)
            
            ret.append({'event_id':event_id.item(0).firstChild.data,
                        'title':title.item(0).firstChild.data,
                        'event_url':event_url.item(0).firstChild.data,
                        'limit':limit.item(0).firstChild.data,
                        'accepted':accepted.item(0).firstChild.data,
                        'waiting':waiting.item(0).firstChild.data,
                        'user_id':user_id,
                        'nickname':nickname,
                        #'twitter_id':twitter_id,
                        'status':status
                         })
        return ret 

    def prepare_query(self, param={}):
        query = ''
        for k, v in param.items():
            # Target format is XML
            if k == 'format': continue
            if isinstance(v, list):
                for e in v:
                    query += '%s=%s&' % (k, e)
            elif isinstance(v, str):
                query += '%s=%s&' % (k, v)
            else:
                # TODO: raise exception
                None
        return query[:-1]


api = Atnd()
param = { 'user':'yku',
          'status':['foo', 'bar'] }
param = { 'twitter_id':'yku_',
          'keyword':['VM', 'カーネル']}
param = { 'twitter_id':'yku_',
          'keyword':['OS', 'コマンド'],
          'count': '1'
        }
param = { 'twitter_id':'yku_', 'count':'3' }
result = api.event_search(param)
for r in result['event']:
    for k, v in r.items():
        print k, v
    print 
