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
    query = query.encode('utf-8')
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

cur.execute("SELECT id, act_position FROM `new_second` WHERE speed IS NULL")
for row in cur.fetchall():
    parts = row[1].split(u'м.')
    if len(parts) == 3:
        address_b = ' '.join(parts[2].split(';')).replace('..', '.')
        if address_b.__contains__(')'):
            address_b = address_b.split('(')[0]
        elif address_b.__contains__(u'Кбіт') or address_b.__contains__(u'Мбіт'):
            x = ' '.join(address_b.split(' ')[:-2])
            speed = ' '.join(address_b.split(' ')[-2:])
            address_b = x
            sql = "UPDATE `new_second` SET speed='%s' WHERE id=%s" % (speed, str(row[0]))
            cur.execute(sql)
            db.commit()

        # speed = ' '.join(parts[2].split(';')[-1:])
        # print row[0], address_b
        # coords = get_coordinates(address_b)
        # print
        # sql = "UPDATE `new_second` SET lat_b='%s', longi_b='%s' WHERE id = '%s'" \
        #       % (str(coords[0]), str(coords[1]), str(row[0]))
        # cur.execute(sql)
        # db.commit()



# cur.execute("SELECT * FROM `new` WHERE type_serv = 'передача данных' AND lat_a IS NULL LIMIT 100")
# """ сменить запрос и в вызове get_coordinates """
# for row in cur.fetchall():
#     address_a = ', '.join(row[2].split(', ')[1:])
#     if address_a:
#         print row[0], address_a
#         coords = get_coordinates(address_a)
#         print
#         sql = "UPDATE `new` SET lat_a = '%s', longi_a = '%s' WHERE id_data = '%s'" \
#               % (str(coords[0]), str(coords[1]), str(row[0]))
#         try:
#             cur.execute(sql)
#             db.commit()
#         except:
#             db.rollback()
#             print '[!] Error on %s' % row[0]

    # address_b = ', '.join(row[4].split(', ')[1:])
    # if address_b:
    #     print row[0], address_b
    #     coords = get_coordinates(address_b)
    #     print
    #     sql = "UPDATE `new` SET lat_b = '%s', longi_b = '%s' WHERE id_data = '%s'" \
    #           % (str(coords[0]), str(coords[1]), str(row[0]))
    #     try:
    #         cur.execute(sql)
    #         db.commit()
    #     except:
    #         db.rollback()
    #         print '[!] Error on %s' % row[0]







# -----------------------------------------------
# cur.execute("""
# SELECT
# `second`.uniqe_number,
# `second`.`name`,
# `second`.service_pack,
# `second`.service_pack_type,
# `second`.acts_position,
# `second`.addon,
# `first`.ID,
# `first`.planerid,
# `first`.client,
# `first`.service,
# `first`.speed,
# `first`.country,
# `first`.region,
# `first`.city,
# `first`.street,
# `first`.sap_id,
# `first`.spp
#
# FROM
#     `first`
# INNER JOIN `second` ON `first`.lat = `second`.lat AND `first`.longi = `second`.longi
# WHERE
# `first`.lat IS NOT NULL AND
# `first`.lat <> 'None'
#
# """)
# new_db_name = 'result.csv'
# writer = csv.writer(open(new_db_name, 'wb+'), delimiter=';', quotechar='"')
# for row in cur.fetchall():
#     if row[5]:
#         addon = row[5].encode('utf-8')
#     else:
#         addon = 'None'
#     if row[8]:
#         client = row[8].encode('utf-8')
#     else:
#         client = 'None'
#     if row[9]:
#         service = row[9].encode('utf-8')
#     else:
#         service = 'None'
#     if row[10]:
#         speed = row[10].encode('utf-8')
#     else:
#         speed = 'None'
#     if row[0] and row:
#         writer.writerow([row[0].encode('utf-8'), row[1].encode('utf-8'), row[2].encode('utf-8'), row[3].encode('utf-8'),
#                          row[4].encode('utf-8'), addon, row[6].encode('utf-8'), row[7].encode('utf-8'),
#                          client, service, speed,
#                          row[11].encode('utf-8'), row[12].encode('utf-8'), row[13].encode('utf-8'),
#                          row[14].encode('utf-8'), row[15].encode('utf-8'), row[16].encode('utf-8')])
#     # print 'ID = %s & unique_number = %s (%s == %s) // ' % (row[0], row[7], row[11], row[14])







