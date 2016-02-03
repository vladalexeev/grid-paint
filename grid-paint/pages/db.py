# -*- coding: utf-8 -*-
'''
Created on 23.07.2013

@author: Vlad
'''

from google.appengine.ext import db

artwork_small_image_width=200
artwork_small_image_height=150

class Artwork(db.Expando):
    name = db.TextProperty()
    description = db.TextProperty()
    author = db.UserProperty()
    tags = db.StringListProperty()
    date = db.DateTimeProperty()
    #json = db.TextProperty()
    #json_compressed = db.BooleanProperty()
    json_file_name = db.StringProperty(indexed=False)
    grid = db.StringProperty()
    #full_image = db.BlobProperty()
    full_image_file_name = db.TextProperty()
    full_image_width = db.IntegerProperty(indexed=False)
    full_image_height = db.IntegerProperty(indexed=False)
    #small_image = db.BlobProperty()
    small_image_file_name = db.TextProperty()
    small_image_width = db.IntegerProperty(indexed=False)
    small_image_height = db.IntegerProperty(indexed=False)
    editor_choice = db.BooleanProperty()
    
class Tag(db.Model):
    url_name = db.StringProperty()
    title = db.StringProperty()
    title_lower = db.StringProperty()
    
class Comment(db.Model):
    artwork_ref = db.ReferenceProperty(reference_class=Artwork)
    author = db.UserProperty(auto_current_user_add=True)
    text = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    
class Notification(db.Expando):
    date = db.DateTimeProperty(auto_now_add=True)
    recipient = db.UserProperty()
    read = db.BooleanProperty(default = False)
    type = db.StringProperty(indexed=False)
    artwork = db.ReferenceProperty(reference_class=Artwork, indexed=False)
    comment = db.ReferenceProperty(reference_class=Comment, indexed=False)
    sender = db.UserProperty(indexed=False)
    
class UserProfile(db.Model):
    email = db.StringProperty()
    nickname = db.StringProperty()
    join_date = db.DateTimeProperty(auto_now_add=True)
    
    
class Settings(db.Model):
    show_ads = db.BooleanProperty()
    show_analytics = db.BooleanProperty()
    
class Favorite(db.Model):
    user = db.UserProperty()
    artwork = db.ReferenceProperty(reference_class=Artwork)
    date = db.DateTimeProperty(auto_now_add=True)
    
class FavoriteCounter(db.Model):
    artwork = db.ReferenceProperty(reference_class=Artwork)
    count = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add=True)