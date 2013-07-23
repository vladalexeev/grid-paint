# -*- coding: utf-8 -*-
'''
Created on 23.07.2013

@author: Vlad
'''

from google.appengine.ext import db

class Artwork(db.Model):
    name = db.StringProperty()
    author = db.UserProperty()
    json = db.StringProperty()