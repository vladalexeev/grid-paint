# -*- coding: utf-8 -*-
'''
Created on 23.07.2013

@author: Vlad
'''

from google.appengine.ext import db

class Artwork(db.Model):
    name = db.StringProperty()
    author = db.UserProperty(auto_current_user_add=True)
    tags = db.StringListProperty()
    date = db.DateTimeProperty(auto_now=True)
    json = db.TextProperty()
    full_image = db.BlobProperty()
    full_image_width = db.IntegerProperty()
    full_image_height = db.IntegerProperty();
    
class Tag(db.Model):
    url_name = db.StringProperty()
    title = db.StringProperty()