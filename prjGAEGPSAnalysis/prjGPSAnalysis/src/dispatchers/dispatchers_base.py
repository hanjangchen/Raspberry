# -*- coding: utf-8 -*-
'''
Created on Jun 24, 2014

@author: Alan Tai
'''
from models.models_gps_data import GPSData
from google.appengine.ext import blobstore
from google.appengine.api import users
from handlers.handler_webapp2_extra_auth import BaseHandler
import logging
import jinja2
import webapp2
import json

# dictionaries
from dictionaries.dict_keys_values import KeysVaulesGeneral
dict_general = KeysVaulesGeneral()

__author__ = 'Alan Tai'
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
        gps_data_list = []
        # retrieve data
        gps_module_data_set = GPSData.query()
        if gps_module_data_set.count() <=0:
            gps_module_data_set = None
        else:
            for data_entity in gps_module_data_set:
                if isinstance(data_entity.gps_data, str):
                    gps_data_list.append(json.loads(data_entity.gps_data))
                else:
                    gps_data_list.append(data_entity.gps_data)
            
        # admin filter factor ; han.jang.chen@gmail.com, gogistics.tw@gmail
        
        is_admin = False
        user = users.get_current_user()
        if user:
            if user.nickname() == 'han.jang.chen' or user.nickname() == 'gogistics.tw':
                is_admin = True
                
            # create blob upload path
            upload_url = blobstore.create_upload_url('/data_retrieving/upload_img')
            template_values.update({'title':dict_general.web_title_index_page, 'gps_data_list': json.dumps(gps_data_list), 'upload_url' : upload_url, 'is_admin' : is_admin})
            self.render_template(dict_general.index_page, template_values)
            
        else:
            self.redirect(users.create_login_url('/base/index'))
        

class FaultImgURLDispatcher(BaseHandler):
    def get(self):
        """ temp solution """
        pass
        
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
    webapp2.Route(r'/base/[[item.img_blob_url]]', FaultImgURLDispatcher, name='img_blob_page'),
    webapp2.Route(r'/base/test/<regx_id:\d+>', RegxTestDispatcher, name='regx_page')
], debug=True, config=config)

# log
logging.getLogger().setLevel(logging.DEBUG)
    
