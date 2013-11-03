# -*- coding: utf-8 -*-
'''
Created on 14.07.2013
@author: Vlad
'''
import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

import db

mm_cache = memcache.Client();

# Ключи memcache
MC_SMALL_IMAGE_PREFIX = 'small_image_'
MC_MAIN_PAGE_RECENT_IMAGES_KEY = 'main_page_recent_images'


class UserInfo:
    """ Информация о пользователе для страницы """
    user=None
    user_name=''
    
    superadmin = False
    
    login_url=None
    login_url_text=None
        
    def __init__(self,request_uri):
        self.user=users.get_current_user()
        if users.get_current_user():
            self.user_name=users.get_current_user().nickname()
            self.superadmin = users.is_current_user_admin()
            
            self.login_url=users.create_logout_url('/')
            self.login_url_text='Logout'
        else:
            self.login_url=users.create_login_url(request_uri)
            self.login_url_text='Login into Google account'
            
def get_settings():
    settings=db.Settings.all().get()
    if settings:
        return settings
    else:
        settings=db.Settings()
        settings.show_ads=False
        settings.show_analytics=False
        return settings
        
def save_settings(settings):
    settings.put()
        

class BasicRequestHandler(webapp.RequestHandler):
    def initialize(self, request, response):
        webapp.RequestHandler.initialize(self, request, response)
        self.user_info=UserInfo(self.request.uri)
        self.settings=get_settings()
        
    def write_template(self,template_name,template_values):
        """Вывод шаблона в выходной поток"""
        template_values['user_info']=self.user_info
        template_values['settings']=self.settings
        template_values['app_version']=os.environ.get('CURRENT_VERSION_ID').split('.')[0]
        path = os.path.join(os.path.dirname(__file__), "../"+template_name)
        self.response.out.write(template.render(path, template_values))
        
    def handle_exception(self, exception, debug_mode):
        if isinstance(exception, BasicRequestHandlerException):
            self.error(exception.code)
            self.response.out.write('<p>('+str(exception.code)+') '+exception.message+'</p>')
            self.response.out.write('<p>Return to <a href="\\">home page</a></p>')    
        else:
            super(BasicRequestHandler,self).handle_exception(exception,debug_mode)
            
class BasicRequestHandlerException(Exception):
    def __init__(self,code,message):
        self.code = code
        self.message = message          

class BasicPageRequestHandler(BasicRequestHandler):
    def write_template(self, template_name, template_values):
        super(BasicPageRequestHandler, self).write_template(template_name,template_values)



def calc_resize(image_width, image_height, max_width, max_height):
    '''
    Calculates resized image dimensions and return tuple (width,height)
    '''
    width_aspect=float(image_width)/max_width
    height_aspect=float(image_height)/max_height
        
    if width_aspect>height_aspect:
        divisor=width_aspect
    else:
        divisor=height_aspect
        
    if divisor<1:
        divisor=1
    
    return (
            int(image_width/divisor),
            int(image_height/divisor)
            )