# -*- coding: utf-8 -*-
'''
Created on 13 ���. 2013 �.

@author: Vlad
'''

import db
import unidecode

import cache

def tag_url_name(title):
    return unidecode.unidecode(title).\
                     replace(' ','-').\
                     replace('/','-').\
                     replace('\\','-').\
                     replace(':','-')

def get_tag_by_title(title):
    url_name = tag_url_name(title)
    cache_tag = cache.get(cache.MC_TAG+url_name)
    
    if cache_tag:
        return cache_tag
    else:
        tag=db.Tag.all().filter('url_name =',url_name).get()
        return tag

def create_tag_by_title(title):
    url_name = tag_url_name(title)
    cache_tag = cache.get(cache.MC_TAG+url_name)
    if cache_tag:
        return cache_tag
    else:
        tag=db.Tag.all().filter('url_name =',url_name).get()
        if not tag:
            tag=db.Tag()
            tag.title=title
            tag.title_lower=title.lower()
            tag.url_name=url_name
            tag.put()
        
        cache.add(cache.MC_TAG+url_name, tag)
        return tag

def tag_by_url_name(url_name):
    cache_tag = cache.get(cache.MC_TAG+url_name)
    if cache_tag:
        return cache_tag
    else:
        tag=db.Tag.all().filter('url_name =',url_name).get()
        if tag:
            cache.add(cache.MC_TAG+url_name, tag)
        else:
            tag=db.Tag()
            tag.url_name=url_name
            tag.title=url_name
            tag.title_lower=url_name
        
        return tag
    