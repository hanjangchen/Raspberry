# -*- coding: utf-8 -*-
__author__ = 'Alan Tai'
'''
Created on Jun 24, 2014

@author: Alan Tai
'''
import json

from google.appengine.api import images
from handlers.handler_webapp2_extra_auth import BaseHandler
from google.appengine.ext.webapp import blobstore_handlers
import logging
import jinja2
import webapp2
import time

# data model
from models.models_gps_data import GPSData, ImageDetail

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
        
class ImagesDataDownloadDispatcher(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        """ images upload handler """
        
        img_file = self.get_uploads('image_for_upload') # to get image file
        img_urls = [] # img urls list for storing img key
        blob_key = img_file[0].key()
        img_url = images.get_serving_url(blob_key)
        img_urls.append(img_url)
        
        #
        img_title = u"No Title"
        img_description = u"No Description"
        time_stamp = int(round(time.time())).__str__()
        img_id = u'GOGIS-IMG-' + time_stamp
        new_img_file = ImageDetail()
        new_img_file.img_id = img_id
        new_img_file.img_blob_url = img_url
        new_img_file.img_title = img_title
        new_img_file.img_description = img_description
        new_img_file.put()
        
            
        ajax_response = {"img_urls" : img_urls, "img_title" : img_title, "img_description" : img_description }
        self.response.write(json.dumps(ajax_response))
        

# configuration
config = dict_general.config_setting

# app routing
app = webapp2.WSGIApplication([
    webapp2.Route(r'/data_retrieving/gps_module', GPSDataRetrievingDispatcher, name='data_retrieving_gps_module'),
    webapp2.Route(r'/data_retrieving/upload_img', ImagesDataDownloadDispatcher, name='data_retrieving_upload_img')
], debug=True, config=config)

# log info.
logging.getLogger().setLevel(logging.DEBUG) 
    
