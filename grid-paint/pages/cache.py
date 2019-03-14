# -*- coding: utf-8 -*-
'''
Created on 19 nov 2013

@author: Vlad
'''

from google.appengine.api import memcache


mm_cache = memcache.Client();

MC_SETTINGS = 'settings'

# memcache prefixes
MC_MAIN_PAGE_RECENT_IMAGES_KEY = 'main_page_recent_images'
MC_MAIN_PAGE_RECENT_COMMENTS = 'main_page_recent_comments'
MC_MAIN_PAGE_RECENT_EDITOR_CHOICE = 'main_page_recent_editor_choice'
MC_MAIN_PAGE_TOP_FAVORITES = 'main_page_top_favorites'
MC_MAIN_PAGE_RECENT_FAVORITES = 'main_page_recent_favorites'
MC_MAIN_PAGE_PRODUCTIVE_ARTISTS = 'main_page_productive_artists'
MC_MAIN_PAGE_TOP_RATED_ARTISTS = 'main_page_top_rated_artists'

MC_USER_NOTIFICATION_PREFIX = 'user_notification_count_'
MC_USER_PROFILE = 'user_profile_'
MC_TAG = 'tag_'
MC_ARTWORK_LIST = 'list_'
MC_USER_LIST = 'user_list_'
MC_FAVORITE_COUNT = 'img_fav_count_'
MC_FAVORITE_BY_USER = 'img_fav_user_'

MC_FOLLOW = 'follow_'

MC_IMAGE_PREFIX = 'img:'

# This key is used for protection against spam clicks on Star
MC_ANTISPAM_FAVORITE_USER_ARTWORK = 'antispam_fav_user_art_'

MC_ANTISPAM_FOLLOW = 'antispam_follow_'


def get(key):
    return mm_cache.get(key)

def delete(key):
    mm_cache.delete(key)
    
def add(key, value):
    mm_cache.set(key, value)
    
