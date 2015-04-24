#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
БД Биллинг
"""

import csv
import re
import MySQLdb
import urllib
import simplejson
import time

googleGeocodeUrl = 'http://maps.googleapis.com/maps/api/geocode/json?'
SLEEP = 1


def get_coordinates(query, from_sensor=False):
    query = query.encode('utf-8')
    params = {
        'address': query,
        'sensor': "true" if from_sensor else "false"
    }
    url = googleGeocodeUrl + urllib.urlencode(params)
    json_response = urllib.urlopen(url)
    response = simplejson.loads(json_response.read())
    # print response
    if response['results']:
        location = response['results'][0]['geometry']['location']
        latitude, longitude = location['lat'], location['lng']
        print latitude, longitude
    else:
        if response['status'] == 'OVER_QUERY_LIMIT':
            print 'OVER_QUERY_LIMIT'
            exit()
        latitude, longitude = None, None
        print query, "<no results>"
    return [latitude, longitude]


db = MySQLdb.connect(host="127.0.0.1",
                    port=3306,
                    user="root",
                    passwd="123",
                    db="csv",
                    charset='utf8')
cur = db.cursor()

cur.execute("SELECT my_id, act_position FROM `bd_billing_6` WHERE lat_a is NULL LIMIT 2000")
for row in cur.fetchall():
    parts = row[1].split(u'м.')
    if len(parts) == 2:
        address_b = ' '.join(parts[1].split(';')).replace('..', '.')
        if address_b.__contains__('(') or address_b.__contains__(')'):
            address_b = address_b.split('(')[0]
        elif address_b.__contains__(u'Кбіт') or address_b.__contains__(u'Мбіт'):
            x = ' '.join(address_b.split(' ')[:-2])
            # speed = ' '.join(address_b.split(' ')[-2:])
            address_b = x
        elif address_b.__contains__(u'В. Вал'):
            address_b = address_b.replace(u'В. Вал', u'Верхний Вал')
        if address_b.__contains__(u'Мбі'):
            address_b = ' '.join(address_b.split(' ')[:-3])
        if address_b.__contains__(')') or address_b.__contains__(')'):
            address_b = address_b.split(')')[0]
        print '[1] %s = %s' % (row[0], address_b)
        coords = get_coordinates(address_b)
        time.sleep(SLEEP)
        print
        # sql = "UPDATE `bd_billing_6` SET lat_a = '%s', longi_a = '%s' WHERE my_id = '%s'" % (str(coords[0]), str(coords[1]), row[0])
        # cur.execute(sql)
        # db.commit()
    elif len(parts) == 3:
        address_a = ' '.join(parts[1].split(';')).replace('..', '.')
        if address_a.__contains__('('):
            address_a = address_a.split('(')[0]
        print '[A] %s = %s' % (row[0], address_a)
        coords = get_coordinates(address_a)
        print
        sql = "UPDATE `bd_billing_6` SET lat_a = '%s', longi_a = '%s' WHERE my_id = '%s'" % (str(coords[0]), str(coords[1]), row[0])
        cur.execute(sql)
        db.commit()

        address_b = ' '.join(parts[2].split(';')).replace('..', '.')
        if address_b.__contains__('('):
            address_b = address_b.split('(')[0]
        print '[B] %s = %s' % (row[0], address_b)
        coords = get_coordinates(address_b)
        print
        sql = "UPDATE `bd_billing_6` SET lat_b = '%s', longi_b = '%s' WHERE my_id = '%s'" % (str(coords[0]), str(coords[1]), row[0])
        cur.execute(sql)
        db.commit()
    elif len(parts) == 1:
        pass
    else:
        pass
