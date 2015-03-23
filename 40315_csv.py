#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
address 1 - rus (separate columns) - 12 rows - address:
6 - country
7 - oblast
8 - city
9 - street, build.


address 2 - ukr - 6 rows - address: 4

Львів, вул. Мечнікова, 16
49.8317362, 24.049277

Заменить в первой таблице - 22087
Все координаты

"""

import csv
import re
import MySQLdb
import urllib
import simplejson
import time

SLEEP = 0

googleGeocodeUrl = 'http://maps.googleapis.com/maps/api/geocode/json?'


def get_coordinates(query, from_sensor=False):
    # query = query.encode('utf-8')
    params = {
        'address': query,
        'sensor': "true" if from_sensor else "false"
    }
    url = googleGeocodeUrl + urllib.urlencode(params)
    json_response = urllib.urlopen(url)
    time.sleep(SLEEP)
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
                charset='utf8',
        )
cur = db.cursor()


cur.execute("SELECT country, city, street, id FROM `first` WHERE lat IS NULL LIMIT 1000")
for row in cur.fetchall():
    if row[2]:
        addr = '%s, %s, %s' % (row[0].encode('utf-8'), row[1].encode('utf-8'), row[2].encode('utf-8'))
        print addr, row[3]
        coords = get_coordinates(addr)
        # coords = ['50.449228', '30.508947']
        print
        sql = "UPDATE `first` SET lat = '%s', longi = '%s' WHERE ID = '%s'" % (str(coords[0]), str(coords[1]), str(row[3]))
        try:
            cur.execute(sql)
            db.commit()
        except:
            db.rollback()
            print '[!] Error on %s' % row[3]

print '----------------------'

# cur.execute("SELECT uniqe_number, acts_position FROM `second` LIMIT 2")
# for row in cur.fetchall():
#     if row[0]:
#         parts = row[1].split(u'м.')
#         if len(parts)>1:
#             print parts[1], row[0]
#             coords = get_coordinates(parts[1])
#             print
            # sql = "UPDATE `first` SET lat = '%s', longi = '%s' WHERE uniqe_number = '%s'" % (str(coords[0]), str(coords[1]), str(row[0]))
            # try:
            #     cur.execute(sql)
            #     db.commit()
            # except:
            #     db.rollback()
            #     print '[!] Error on %s' % row[0]


cur.execute("""
SELECT
`first`.ID,
`first`.planerid,
`first`.svodnaya,
`first`.client,
`first`.service,
`first`.speed,
`first`.country,
`second`.uniqe_number,
`second`.`name`,
`second`.service_pack,
`second`.service_pack_type,
`second`.acts_position,
`second`.addon,
`first`.region,
`first`.city,
`first`.street
FROM
`first` ,
`second`
WHERE
`first`.lat = `second`.lat AND
`first`.longi = `first`.longi

""")
for row in cur.fetchall():
    print 'ID = %s // unique_number = %s' % (row[0], row[7])





        # if parts.__contains__(u'Київ'):
        #     addr = row[0].replace(u'вул', u'ул').replace(u'б-р Л.Українки', u'бул. Леси Украинки')\
        #         .replace(u'Київ', u'Киев')
        #     print addr




#     # match = re.findall('[м]\.(\S+)\,.[в]|[у][л].(\S+.\d+).', row[4])
#     # match = re.findall('[м]\.(\S+)\,.[в]', row[4])  # city
#     match = re.findall('[вул]..\..(\S+.\d+)', row[4])  # street
#     for m in match:
#         d2.update({row[0]: m})


