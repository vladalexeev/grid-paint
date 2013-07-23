
# -*- coding: utf-8 -*-
'''
Created on 14.07.2013
@author: Vlad
'''
import os
import json
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

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

class BasicRequestHandler(webapp.RequestHandler):
    def initialize(self, request, response):
        webapp.RequestHandler.initialize(self, request, response)
        self.user_info=UserInfo(self.request.uri)
        
    def write_template(self,template_name,template_values):
        """Вывод шаблона в выходной поток"""
        template_values['user_info']=self.user_info
        path = os.path.join(os.path.dirname(__file__), "../"+template_name)
        self.response.out.write(template.render(path, template_values))
        
    def handle_exception(self, exception, debug_mode):
        if isinstance(exception, BasicRequestHandlerException):
#            logger.error("Request handler exception code="+str(exception.code)+" - "+str(exception.message))
#            logger.exception(exception)
            self.error(exception.code)
            self.response.out.write('<p>('+str(exception.code)+') '+exception.message+'</p>')
            self.response.out.write('<p>Return to <a href="\\">home page</a></p>')    
        else:
#            logger.error("Exception "+str(exception))
            super(BasicRequestHandler,self).handle_exception(exception,debug_mode)
            
class BasicRequestHandlerException(Exception):
    def __init__(self,code,message):
        self.code = code
        self.message = message          

class BasicPageRequestHandler(BasicRequestHandler):
    def write_template(self, template_name, template_values):
        super(BasicPageRequestHandler, self).write_template(template_name,template_values)



class PageIndex(BasicPageRequestHandler):
    def get(self):
        self.write_template('templates/index.html', {})
        
class PageNewImage(BasicPageRequestHandler):
    def get(self):
        self.write_template('templates/new-image.html', {})
        
class PagePainter(BasicPageRequestHandler):
    def get(self):
        new_artwork={
                     'grid':self.request.get('grid'),
                     'cellSize':24,
                     'workspace': {
                                   'backgroundColor': '#ffffff',
                                   'width': 2000,
                                   'height': 2000
                                   },
                     'items':[]
                     }
        artwork_json=json.dumps(new_artwork)
        self.write_template('templates/painter.html', 
                            {
                             'artwork_json':artwork_json
                             })