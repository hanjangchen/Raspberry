# -*- coding: utf-8 -*-
'''
Created on May 22, 2014

@author: Alan Tai

@description:
dictionary for key-value pairs
'''

class KeysVaulesGeneral():
    """ keys values pairs """
    def __init__(self):
        self.brand_title = u'Gogistics'
        self.web_title = u'GPS Analysis'
        
        self.web_title_front_page = u'GPS Analysis - Front Page'
        self.web_title_index_page = u'GPS Analysis - Index Page'
        
        self.front_page = '/front_page_container.html'
        self.index_page = '/index_page_container.html'
        
        #webapp2 config
        self.config_setting = {
                               'webapp2_extras.auth': {'user_model': 'models.models_people.User','user_attributes': ['name']},
                               'webapp2_extras.sessions': {'secret_key': 'b4RiUe~53!kG-AqFB!.*^OHS$u2cNwOQGG',  # secret key is just a combination of random character which is better to be unguessable; user can create whatever they want
                                                           'cookie_name' : 'gogistics-tw-session',
                                                           'session_max_age' : 86400,
                                                           'cookie_args' : {'max_age' : 86400,
                                                                            'httponly' : True},} 
                               }
        
