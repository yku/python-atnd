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
        None

    def prepare_query(self, param={}):
        query = ''
        for k, v in param.items():
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
result = api.event_search(param)
for r in result:
    for k, v in r.items():
        print k, v
    print 
