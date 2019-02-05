# -*- coding: utf-8 -*-
'''
Created on 14.07.2013
@author: Vlad
'''
import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import db
import dao
import cache
import convert


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
            user_profile = dao.get_user_profile(self.user.email())
            if not user_profile:
                user_profile = db.UserProfile()
                user_profile.email = self.user.email()
                user_profile.nickname = convert.auto_nickname(self.user.nickname())
                user_profile.artworks_count = 0                
                dao.add_user_profile(user_profile)
                user_profile = dao.get_user_profile(self.user.email())
                
            self.user_email = user_profile.email
            self.user_name = user_profile.nickname
            self.has_profile = True
            self.profile_id = user_profile.key().id()
            self.read_only = hasattr(user_profile, 'read_only')
                
            self.superadmin = users.is_current_user_admin()            
            self.login_url = users.create_logout_url('/')
            self.login_url_text = 'Logout'
            self.notifications_count = dao.get_notification_count(self.user_email)
            self.has_notifications = self.notifications_count > 0
        else:
            self.user_email = None
            self.login_url = users.create_login_url(request_uri)
            self.login_url_text = 'Login'
            
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
        user_agent = request.headers.get('User-Agent')
        if user_agent:
            user_agent = user_agent.lower() 
            if user_agent.find('ahrefs') >= 0 or user_agent.find('blexbot') >=0 or user_agent.find('semrush') >=0 or user_agent.find('dotbot') >=0:
                raise Exception('Banned user agent')
            
        
        webapp.RequestHandler.initialize(self, request, response)
        self.user_info=UserInfo(self.request.uri)
        
        self.settings = cache.get(cache.MC_SETTINGS)
        if not self.settings:
            self.settings=get_settings()
            cache.add(cache.MC_SETTINGS, self.settings)
        
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



