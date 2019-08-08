# -*- coding: utf-8 -*-
'''
Created on 13 ���. 2013 �.

@author: Vlad
'''

from datetime import datetime
import db
import unidecode

import cache
from bad_language import hide_bad_language


def tag_url_name(title):
    return unidecode.unidecode(title.lower().strip()).\
        replace(' ', '-').\
        replace('/', '-').\
        replace('\\', '-').\
        replace(':', '-').\
        replace('#', '-').\
        replace('&', '-').\
        replace('=', '-')


def get_tag_by_title(title):
    url_name = tag_url_name(title)
    cache_tag = cache.get(cache.MC_TAG+url_name)
    
    if cache_tag:
        return cache_tag
    else:
        tag = db.Tag.all().filter('url_name =',url_name).get()
        return tag


def create_tag_by_title(title):
    if not title:
        return None

    title = title.strip()
    if title and title[0] == '#':
        title = title[1:]
    if len(title) <= 1:
        return None

    if hide_bad_language(title) != title:
        return None

    url_name = tag_url_name(title)
    cache_tag = cache.get(cache.MC_TAG+url_name)
    if cache_tag:
        return cache_tag
    else:
        tag=db.Tag.all().filter('url_name =', url_name).get()
        if not tag:
            tag = db.Tag()
            tag.title = title
            tag.title_lower = title.lower()
            tag.url_name = url_name
            tag.date = datetime.now()
            tag.put()
        
        cache.add(cache.MC_TAG + url_name, tag)
        return tag


def tag_by_url_name(url_name):
    cache_tag = cache.get(cache.MC_TAG+url_name)
    if cache_tag:
        return cache_tag
    else:
        tag = db.Tag.all().filter('url_name =',url_name).get()
        if tag:
            cache.add(cache.MC_TAG+url_name, tag)
        else:
            tag = db.Tag()
            tag.url_name = url_name
            tag.title = url_name
            tag.title_lower = url_name
        
        return tag

