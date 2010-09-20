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
        
        results = doc.getElementsByTagName('results_returned')[0].firstChild.data
        event_id = doc.getElementsByTagName('event_id')
        title = doc.getElementsByTagName('title')
        catche = doc.getElementsByTagName('catch')
        description = doc.getElementsByTagName('description')
        event_url = doc.getElementsByTagName('event_url')
        started_at = doc.getElementsByTagName('started_at')
        ended_at = doc.getElementsByTagName('ended_at')
        url = doc.getElementsByTagName('url')
        limit = doc.getElementsByTagName('limit')
        addresse = doc.getElementsByTagName('address')
        place = doc.getElementsByTagName('place')
        lat = doc.getElementsByTagName('lat')
        lon = doc.getElementsByTagName('lon')
        owner_id = doc.getElementsByTagName('owner_id')
        owner_nickname = doc.getElementsByTagName('owner_nickname')
        owner_twitter_id = doc.getElementsByTagName('owner_twitter_id')
        accepted = doc.getElementsByTagName('accepted')
        waiting = doc.getElementsByTagName('waiting')
        updated_at = doc.getElementsByTagName('updated_at')

        ret = [] 
        for i in xrange(0, int(results)):
            ret.append({'event_id':event_id[i].firstChild.data,
                        'title':title[i].firstChild.data,
                        'catch':catche[i].firstChild.data,
                        'description':description[i].firstChild.data,
                        'event_url':event_url[i].firstChild.data,
                        'started_at':started_at[i].firstChild.data,
                        'ended_at':ended_at[i].firstChild.data,
                        'url':url[i].firstChild.data,
                        'limit':limit[i].firstChild.data,
                        'address':addresse[i].firstChild.data,
                        'place':place[i].firstChild.data,
                        'lat':lat[i].firstChild.data,
                        'lon':lon[i].firstChild.data,
                        'owner_id':owner_id[i].firstChild.data,
                        'owner_twitter_id':'' if owner_twitter_id[i].getAttribute('nil') else owner_twitter_id[i].firstChild.data,
                        'accepted':accepted[i].firstChild.data,
                        'waiting':waiting[i].firstChild.data,
                        'updated_at':updated_at[i].firstChild.data,
                        })
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
result = api.event_user_search(param)
for r in result:
    for k, v in r.items():
        print k, v
    print 
