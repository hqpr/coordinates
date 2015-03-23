#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, urllib

addr = 'Киев, ул. И.Франка, 16/2'


url = 'http://maps.google.com.ua/?q=' + urllib.quote(addr) + '&output=js'
print '\nQuery: %s' % (url)

# Get XML location
xml = urllib.urlopen(url).read()

if '<error>' in xml:
    print '\nGoogle cannot interpret the address.'
else:
    # Strip lat/long coordinates from XML
    lat, lng = 0.0,0.0
    center = xml[xml.find('{center')+10:xml.find('}',xml.find('{center'))]
    center = center.replace('lat:','').replace('lng:','')
    lat,lng = center.split(',')
    url = lat,lng

if url:
    print 'Map: %s' % (url)
