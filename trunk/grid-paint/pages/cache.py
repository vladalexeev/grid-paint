# -*- coding: utf-8 -*-
'''
Created on 19 nov 2013

@author: Vlad
'''

from google.appengine.api import memcache


mm_cache = memcache.Client();

# memcache prefixes
MC_SMALL_IMAGE_PREFIX = 'small_image_'
MC_MAIN_PAGE_RECENT_IMAGES_KEY = 'main_page_recent_images'
MC_USER_NOTIFICATION_PREFIX = 'user_notification_count_'


def get(key):
    return mm_cache.get(key)

def delete(key):
    mm_cache.delete(key)
    
def add(key,value):
    mm_cache.add(key, value)