# -*- coding: utf-8 -*-
__author__ = 'Alan Tai'
'''
Created on Jun 24, 2014

@author: Alan Tai
'''
import json


from handlers.handler_webapp2_extra_auth import BaseHandler
import logging
import jinja2
import webapp2
import time

# data model
from models.models_gps_data import GPSData

# dictionaries
from dictionaries.dict_keys_values import KeysVaulesGeneral
dict_general = KeysVaulesGeneral()

# jinja environment setting
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader('static/templates'))

# dispatchers
class GPSDataRetrievingDispatcher(BaseHandler):
    def post(self):
        """ gps data retrieving handler """
        assert self.request.get('data'), 'fail to retrieve data from raspberry pi'
        
        
        time_stamp = int(round(time.time())).__str__()
        gps_data_id = 'GOGIS-GPS-' + time_stamp
         
        json_obj = self.request.get('data') #from raspberry pi and data format already in json format
        new_gps_data = GPSData()
        new_gps_data.gps_data_id = gps_data_id
        new_gps_data.gps_data = json_obj
        new_gps_data.put()
        
        ajax_response = {'processing_status' : 'success'}
        self.response.out.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(ajax_response))
        

# configuration
config = dict_general.config_setting

# app routing
app = webapp2.WSGIApplication([
    webapp2.Route(r'/data_retrieving/gps_module', GPSDataRetrievingDispatcher, name='data_retrieving_gps_module')
], debug=True, config=config)

# log info.
logging.getLogger().setLevel(logging.DEBUG) 
    
