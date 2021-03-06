# -*- coding: utf-8 -*-
__author__ = 'Alan Tai'
'''
Created on Jun 24, 2014

@author: Alan Tai
'''
from models.models_gps_data import GPSData
from google.appengine.ext import blobstore
from google.appengine.api import users
from handlers.handler_webapp2_extra_auth import BaseHandler
from handlers.handler_general_functions import generate_random_id
import logging, jinja2, webapp2, json, datetime, time

from handlers.handler_encryption import EncryptionTools

# dictionaries
from dictionaries.dict_keys_values import KeysVaulesGeneral
dict_general = KeysVaulesGeneral()

# jinja environment
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader('static/templates'))

# encryption tools
basic_encrypt = EncryptionTools()

# dispatchers
class FrontPageDispatcher(BaseHandler):
    def get(self):
        """ front page dispatcher """
        # session test
        session_name = self.request.remote_addr
        self.set_session(arg_session_name = session_name, arg_backend_name = 'memcache')
        app_session = self.session
        
        # set expire timespane
        expire_timespan = (datetime.datetime.now() - datetime.timedelta(days = 2)).strftime('%a, %d-%b-%Y %H:%M:%S')
        expire_timespan = expire_timespan
        
        # random number id
        time_stamp = int(round(time.time())).__str__()
        random_id = generate_random_id(50)
        random_id = "GOGIS-TOKEN-" + time_stamp + "-" + random_id
        random_id = basic_encrypt.encode(key = None, clear = random_id)
        # cookie_content = "session_id_test_8={cookie_random_id}".format(cookie_random_id = random_id)
        # my_cookie = Cookie.SimpleCookie()
        # my_cookie["session_id_test_15"] = random_id
        # self.response.headers.add_header("Set-Cookie", my_cookie.output(header=''))
        # self.response.headers.add_header("Set-Cookie", "test_cookie=hello_world; expires=Thu, 25-Dec-2014 12:21:43 GMT")
        
        self.response.headers['Set-Cookie'] = "{session_id_title}={session_id_val}; path=/".format( session_id_title = "session_id", session_id_val = random_id)
        self.response.headers['Expires'] = expire_timespan
        session_id = self.request.cookies.get("session_id")
        # end of session test
        
        template_values = {}
        template_values.update({'title': dict_general.web_title_front_page, "session" : app_session, "session_id" : session_id })
        self.render_template(dict_general.front_page, template_values)
        
# dispatchers
class IndexPageDispatcher(BaseHandler):
    def get(self):
        """ index page dispatcher """
        # session_id from cookie
        session_id = self.request.cookies.get("session_id")
        
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
            template_values.update({'title':dict_general.web_title_index_page, 'gps_data_list': json.dumps(gps_data_list), 'upload_url' : upload_url, 'is_admin' : is_admin, "session_id" : session_id})
            self.render_template(dict_general.index_page, template_values)
            
        else:
            self.redirect(users.create_login_url('/base/index'))
        

# temp solution for wrong img-url request
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
    
