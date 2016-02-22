# -*- coding: utf-8 -*-
'''
Created on 19 nov. 2013

@author: Vlad
'''

import db
import cache

def get_artwork(id_or_key):
    try:
        return db.Artwork.get_by_id(int(id_or_key))
    except:
        try:
            return db.Artwork.get(id_or_key)
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
    
def get_user_profile(user_email):
    cache_value = cache.get(cache.MC_USER_PROFILE+user_email)
    if cache_value:
        return cache_value
    else:
        user_profile = db.UserProfile.all().filter('email =', user_email).get()
        if user_profile:
            cache.add(cache.MC_USER_PROFILE+user_email, user_profile)
            return user_profile
        else:
            return None
        
def get_user_profile_by_id(profile_id):
    return db.UserProfile.get_by_id(profile_id)
    
        
def add_user_profile(profile):
    if get_user_profile(profile.email):
        raise Exception('User profile already exists '+profile.user.email())
    
    result = profile.put()
    cache.add(cache.MC_USER_PROFILE+profile.email, profile)
    cache.delete(cache.MC_MAIN_PAGE_RECENT_IMAGES_KEY)
    cache.delete(cache.MC_MAIN_PAGE_RECENT_COMMENTS)
    return result
    
def set_user_profile(profile):
    profile.put()
    cache.add(cache.MC_USER_PROFILE+profile.email, profile)
    cache.delete(cache.MC_MAIN_PAGE_RECENT_IMAGES_KEY)
    cache.delete(cache.MC_MAIN_PAGE_RECENT_COMMENTS)
    
def get_artwork_favorite_count(artwork):
    memcache_key = cache.MC_FAVORITE_COUNT+str(artwork.key().id())
    result = cache.get(memcache_key)
    if result:
        return result
    else:
        fav = db.FavoriteCounter.all().filter('artwork =', artwork).get()
        if fav:
            result = fav.count
        else:
            result = 0
        cache.add(memcache_key, result)
        return result
    
def is_artwork_favorite_by_user(artwork, user):
    if not user:
        return False
    
    memcache_key = cache.MC_FAVORITE_BY_USER+str(artwork.key().id())+'_'+user.email()
    result = cache.get(memcache_key)
    if result==True or result==False:
        return result
    else:
        fav_user = db.Favorite.all().filter('artwork =', artwork).filter('user =', user).get()
        if fav_user:
            cache.add(memcache_key, True)
            return True
        else:
            cache.add(memcache_key, False)
            return False


def favorite_artwork(artwork, user):
    cache.delete(cache.MC_FAVORITE_BY_USER+str(artwork.key().id())+'_'+user.email())
    cache.delete(cache.MC_FAVORITE_COUNT+str(artwork.key().id()))

    fav = db.Favorite()
    fav.artwork = artwork
    fav.user = user
    fav.save()
    
    fav_count = db.FavoriteCounter.all().filter('artwork =', artwork).get()
    if fav_count:
        fav_count.count = fav_count.count+1
    else:
        fav_count = db.FavoriteCounter()
        fav_count.artwork = artwork
        fav_count.author = artwork.author
        fav_count.count = 1
        
    fav_count.save()
    return fav_count.count

def unfavorite_artwork(artwork, user):
    cache.delete(cache.MC_FAVORITE_BY_USER+str(artwork.key().id())+'_'+user.email())
    cache.delete(cache.MC_FAVORITE_COUNT+str(artwork.key().id()))

    fav = db.Favorite.all().filter('artwork =', artwork).filter('user =', user).get()
    if fav:
        fav.delete()
        
    cache.delete(cache.MC_FAVORITE_BY_USER+str(artwork.key().id())+'_'+user.email())
        
    fav_count = db.FavoriteCounter.all().filter('artwork =', artwork).get()
    if fav_count:
        if fav_count.count>1:
            fav_count.count = fav_count.count-1
            fav_count.save()
            return fav_count.count
        else:
            fav_count.delete()
            return 0
    else:
        return 0

