# -*- coding: utf-8 -*-
'''
Created on 19 nov. 2013

@author: Vlad
'''

import db
import cache

def get_artwork(id_or_key):
    try:
        return db.Artwork.get(id_or_key)
    except:
        try:
            return db.Artwork.get_by_id(int(id_or_key))
        except:
            return None


def get_notification_count(user):
    cache_key = cache.MC_USER_NOTIFICATION_PREFIX + user.email()
    value = cache.get(cache_key)
    
    if value<>None:
        return value
    else:
        count = db.Notification.all().filter('recipient', user).filter('read =',False).count()
        cache.add(cache_key, count)
        return count
    
def delete_notification(notification):
    cache_key = cache.MC_USER_NOTIFICATION_PREFIX + notification.recipient.email()
    cache.delete(cache_key)
    notification.delete()
    
def add_notification(notification):
    cache_key = cache.MC_USER_NOTIFICATION_PREFIX + notification.recipient.email()
    cache.delete(cache_key)
    notification.put()
    
def get_user_profile(user):
    cache_value = cache.get(cache.MC_USER_PROFILE+user.email())
    if cache_value:
        return cache_value
    else:
        user_profile = db.UserProfile.all().filter('user =', user).get()
        if user_profile:
            cache.add(cache.MC_USER_PROFILE+user.email(), user_profile)
            return user_profile
        else:
            return None
        
def add_user_profile(profile):
    if get_user_profile(profile.user):
        raise Exception('User profile already exists '+profile.user.email())
    
    return profile.put()
    
def set_user_profile(profile):
    profile.put()
    

