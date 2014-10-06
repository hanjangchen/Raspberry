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