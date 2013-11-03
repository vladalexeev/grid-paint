# -*- coding: utf-8 -*-
'''
Created on 23.07.2013

@author: Vlad
'''

from google.appengine.ext import db

artwork_small_image_width=200
artwork_small_image_height=150

class Artwork(db.Model):
    name = db.StringProperty()
    description = db.TextProperty()
    author = db.UserProperty(auto_current_user_add=True)
    tags = db.StringListProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    json = db.TextProperty()
    full_image = db.BlobProperty()
    full_image_width = db.IntegerProperty()
    full_image_height = db.IntegerProperty()
    small_image = db.BlobProperty()
    small_image_width = db.IntegerProperty()
    small_image_height = db.IntegerProperty()
    
class Tag(db.Model):
    url_name = db.StringProperty()
    title = db.StringProperty()
    title_lower = db.StringProperty()
    
class Comment(db.Model):
    artwork_ref = db.ReferenceProperty(reference_class=Artwork)
    author = db.UserProperty(auto_current_user_add=True)
    text = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    
class Settings(db.Model):
    show_ads = db.BooleanProperty()
    show_analytics = db.BooleanProperty()