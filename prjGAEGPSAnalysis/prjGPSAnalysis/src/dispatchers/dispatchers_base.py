# -*- coding: utf-8 -*-
'''
Created on Jun 24, 2014

@author: Alan Tai
'''
from models.models_gps_data import GPSData, ImageDetail
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images
__author__ = 'Alan Tai'


from handlers.handler_webapp2_extra_auth import BaseHandler
import logging
import jinja2
import webapp2
import json
import time
# dictionaries

from dictionaries.dict_keys_values import KeysVaulesGeneral
dict_general = KeysVaulesGeneral()

# jinja environment
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader('static/templates'))

# dispatchers
class FrontPageDispatcher(BaseHandler):
    def get(self):
        """ front page dispatcher """
        template_values = {}
        template_values.update({'title': dict_general.web_title_front_page})
        self.render_template(dict_general.front_page, template_values)
        
# dispatchers
class IndexPageDispatcher(BaseHandler):
    def get(self):
        """ front page dispatcher """
        template_values = {}
        gps_data_dict = {}
        # retrieve data
        gps_module_data_set = GPSData.query()
        if gps_module_data_set.count() <=0:
            gps_module_data_set = None
        else:
            for data_entity in gps_module_data_set:
                gps_data_dict.update({"gps_data" : data_entity.gps_data})
            
        #
        is_admin = True
            
        # create blob upload path
        upload_url = blobstore.create_upload_url('/base/upload_img')
        template_values.update({'title':dict_general.web_title_index_page, 'gps_data_dict': json.dumps(gps_data_dict), 'upload_url' : upload_url, 'is_admin' : is_admin})
        self.render_template(dict_general.index_page, template_values)
        
        
class UploadImgDispatcher(blobstore_handlers.BlobstoreUploadHandler):
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
        
        
class RegxTestDispatcher(BaseHandler):
    def get(self, regx_id):
        """ Regx testing path dispatcher """
        template_values = {}
        template_values.update({'title':u'Regx Demo' + regx_id })
        self.render_template(dict_general.index, template_values)

# configuration
config = dict_general.config_setting

# app
app = webapp2.WSGIApplication([
    webapp2.Route(r'/', FrontPageDispatcher, name='front_page'),
    webapp2.Route(r'/base/index', IndexPageDispatcher, name='index_page'),
    webapp2.Route(r'/base/upload_img', UploadImgDispatcher, name= 'base_upload_img'),
    webapp2.Route(r'/base/test/<regx_id:\d+>', RegxTestDispatcher, name='regx_page')
], debug=True, config=config)

# log
logging.getLogger().setLevel(logging.DEBUG) 
    
