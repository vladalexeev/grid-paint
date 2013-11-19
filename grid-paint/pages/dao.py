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
