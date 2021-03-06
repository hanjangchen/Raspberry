# -*- coding: utf-8 -*-
__author__ = 'Alan Tai'
'''
Created on Oct 3, 2014

@author: alan tai
'''
from google.appengine.ext import ndb

class GPSData(ndb.Model):
    gps_data_id = ndb.StringProperty()
    gps_data = ndb.JsonProperty()
    create_datetime = ndb.DateTimeProperty(auto_now_add = True) #time zone is in UTC
    update_datetime = ndb.DateTimeProperty(auto_now = True) #UTC time zone
    
    
class ImageDetail(ndb.Model):
    img_id = ndb.StringProperty()
    img_title = ndb.StringProperty()
    img_blob_url = ndb.StringProperty()
    img_description = ndb.TextProperty()
    create_datetime = ndb.DateTimeProperty(auto_now_add = True)
    update_datetime = ndb.DateTimeProperty(auto_now = True)