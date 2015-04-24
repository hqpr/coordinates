#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

import csv
import re
import MySQLdb
import urllib
import simplejson
import time

googleGeocodeUrl = 'http://maps.googleapis.com/maps/api/geocode/json?'


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

cur.execute("SELECT * FROM `bd_se_5` WHERE lat IS NULL LIMIT 200")
for row in cur.fetchall():
    if row[8] != u'нету':
        address_b = u'%s, г.%s, %s' % (row[5], row[7], row[8])
        print row[9], address_b
        coords = get_coordinates(address_b)
        print
        sql = "UPDATE `bd_se_5` SET lat = '%s', longi = '%s' WHERE my_id = '%s'" % (str(coords[0]), str(coords[1]), str(row[9]))
        cur.execute(sql)
        db.commit()