# -*- coding: utf-8 -*-
'''
Created on 19 nov 2013

@author: Vlad
'''

from google.appengine.api import memcache


mm_cache = memcache.Client();

# memcache prefixes
MC_MAIN_PAGE_RECENT_IMAGES_KEY = 'main_page_recent_images'
MC_MAIN_PAGE_RECENT_COMMENTS = 'main_page_recent_comments'
MC_MAIN_PAGE_RECENT_EDITOR_CHOICE = 'main_page_recent_editor_choice'
MC_USER_NOTIFICATION_PREFIX = 'user_notification_count_'
MC_USER_PROFILE = 'user_profile_'
MC_TAG = 'tag_'
MC_ARTWORK_LIST = 'list_'

MC_IMAGE_PREFIX = 'img:'


def get(key):
    return mm_cache.get(key)

def delete(key):
    mm_cache.delete(key)
    
def add(key, value):
    mm_cache.set(key, value)
    
