# -*- coding: utf-8 -*-
'''
Created on 13 ���. 2013 �.

@author: Vlad
'''

import db
import unidecode

def tag_by_title(title):
    url_name=unidecode.unidecode(title).\
                        replace(' ','-').\
                        replace('/','-').\
                        replace('\\','-').\
                        replace(':','-')
    tag=db.Tag.all().filter('url_name =',url_name).get()
    if not tag:
        tag=db.Tag()
        tag.title=title
        tag.url_name=url_name
        tag.put()
        
    return tag

def tag_by_url_name(url_name):
    tag=db.Tag.all().filter('url_name =',url_name).get()
    if not tag:
        tag=db.Tag()
        tag.url_name=url_name
        tag.title=url_name
        
    return tag
    