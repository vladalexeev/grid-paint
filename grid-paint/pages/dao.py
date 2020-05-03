# -*- coding: utf-8 -*-
'''
Created on 19 nov. 2013

@author: Vlad
'''

import db
import cache

from datetime import datetime

def get_artwork(id_or_key):
    try:
        return db.Artwork.get_by_id(int(id_or_key))
    except:
        try:
            return db.Artwork.get(id_or_key)
        except:
            return None
        
def get_notification_count(user_email):
    cache_key = cache.MC_USER_NOTIFICATION_PREFIX + user_email
    value = cache.get(cache_key)
    
    if value<>None:
        return value
    else:
        count = db.Notification.all().filter('recipient_email =', user_email).filter('read =',False).count()
        cache.add(cache_key, count)
        return count
    
def delete_notification(notification):
    cache_key = cache.MC_USER_NOTIFICATION_PREFIX + notification.recipient_email
    cache.delete(cache_key)
    notification.delete()
    
def delete_all_notifications(user_email):
    notifications = db.Notification.all().filter('recipient_email =', user_email)
    for n in notifications:
        n.delete()
    cache_key = cache.MC_USER_NOTIFICATION_PREFIX + user_email
    cache.add(cache_key, 0)        
    
def add_notification(notification):
    cache_key = cache.MC_USER_NOTIFICATION_PREFIX + notification.recipient_email
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
            user_profile = db.UserProfile.all().filter('alternative_emails =', user_email).get()
            if user_profile:
                cache.add(cache.MC_USER_PROFILE+user_email, user_profile)
                return user_profile
            else:
                return None
        
def get_user_profile_by_nickname(nickname):
    return db.UserProfile.all().filter('nickname =', nickname).get()
        
def get_user_profile_by_id(profile_id):
    return db.UserProfile.get_by_id(profile_id)
    
        
def add_user_profile(profile):
    profile_exist = get_user_profile(profile.email)
    if profile_exist:
        return profile_exist
    
    result = profile.put()
    cache.add(cache.MC_USER_PROFILE+profile.email, profile)
    cache.delete(cache.MC_MAIN_PAGE_RECENT_IMAGES_KEY)
    cache.delete(cache.MC_MAIN_PAGE_RECENT_COMMENTS)
    return result
    
def set_user_profile(profile):
    profile.put()
    for email in getattr(profile, 'alternative_email', []):
        cache.delete(cache.MC_USER_PROFILE+email)

    cache.delete(cache.MC_USER_PROFILE + profile.email)
    cache.delete(cache.MC_MAIN_PAGE_RECENT_IMAGES_KEY)
    cache.delete(cache.MC_MAIN_PAGE_RECENT_COMMENTS)
    cache.delete(cache.MC_MAIN_PAGE_PRODUCTIVE_ARTISTS)
    cache.delete(cache.MC_MAIN_PAGE_TOP_RATED_ARTISTS)
    
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
    
def is_artwork_favorite_by_user(artwork, user_email):
    if not user_email:
        return False
    
    memcache_key = cache.MC_FAVORITE_BY_USER+str(artwork.key().id())+'_'+user_email
    result = cache.get(memcache_key)
    if result==True or result==False:
        return result
    else:
        fav_user = db.Favorite.all().filter('artwork =', artwork).filter('user_email =', user_email).get()
        if fav_user:
            cache.add(memcache_key, True)
            return True
        else:
            cache.add(memcache_key, False)
            return False


def favorite_artwork(artwork, user_email):
    cache.delete(cache.MC_FAVORITE_BY_USER+str(artwork.key().id())+'_'+user_email)
    cache.delete(cache.MC_FAVORITE_COUNT+str(artwork.key().id()))

    fav = db.Favorite()
    fav.artwork = artwork
    fav.user_email = user_email
    fav.save()
    
    fav_count = db.FavoriteCounter.all().filter('artwork =', artwork).get()
    if fav_count:
        fav_count.count = fav_count.count+1
    else:
        fav_count = db.FavoriteCounter()
        fav_count.artwork = artwork
        fav_count.count = 1
        
    fav_count.save()
    
    user_profile = db.UserProfile.all().filter('email =', artwork.author_email).get()
    if hasattr(user_profile, 'favorite_count'):
        if user_profile.favorite_count is None:
            user_profile.favorite_count = 1
        else:
            user_profile.favorite_count = user_profile.favorite_count + 1
        user_profile.put()
    else:
        user_profile.favorite_count = 1
        user_profile.put()
    
    return fav_count.count

def unfavorite_artwork(artwork, user_email):
    cache.delete(cache.MC_FAVORITE_BY_USER+str(artwork.key().id())+'_'+user_email)
    cache.delete(cache.MC_FAVORITE_COUNT+str(artwork.key().id()))

    fav = db.Favorite.all().filter('artwork =', artwork).filter('user_email =', user_email).get()
    if fav:
        fav.delete()
        
    cache.delete(cache.MC_FAVORITE_BY_USER+str(artwork.key().id())+'_'+user_email)
        
    fav_count = db.FavoriteCounter.all().filter('artwork =', artwork).get()
    result = 0
    if fav_count:
        if fav_count.count>1:
            fav_count.count = fav_count.count-1
            fav_count.save()
            result = fav_count.count
        else:
            fav_count.delete()
            
    user_profile = db.UserProfile.all().filter('email =', artwork.author_email).get()
    if hasattr(user_profile, 'favorite_count'):
        user_profile.favorite_count = user_profile.favorite_count - 1
        user_profile.put()
    
    return result


def is_follower(leader_email, follower_email):
    memcache_key = cache.MC_FAVORITE_BY_USER+leader_email+'_'+follower_email
    result = cache.get(memcache_key)
    
    if result==True or result==False:
        return result
    else:
        follow = db.Follow.all().filter('leader_email =', leader_email).filter('follower_email =', follower_email).get()
        if follow:
            cache.add(memcache_key, True)
            return True
        else:
            cache.add(memcache_key, False)
            return False
        
        
def follow(leader_email, follower_email):
    memcache_key = cache.MC_FAVORITE_BY_USER+leader_email+'_'+follower_email
    cache.delete(memcache_key)
    cache.delete(cache.MC_USER_PROFILE + leader_email)
    cache.delete(cache.MC_USER_PROFILE + follower_email)
    
    follow = db.Follow.all().filter('leader_email =', leader_email).filter('follower_email =', follower_email).get()
    if not follow:
        follow = db.Follow()
        follow.leader_email = leader_email
        follow.follower_email = follower_email
        follow.put()
        return True
    else:
        return False
        
        
def unfollow(leader_email, follower_email):
    memcache_key = cache.MC_FAVORITE_BY_USER+leader_email+'_'+follower_email
    cache.delete(memcache_key)
    cache.delete(cache.MC_USER_PROFILE + leader_email)
    cache.delete(cache.MC_USER_PROFILE + follower_email)
    
    follow = db.Follow.all().filter('leader_email =', leader_email).filter('follower_email =', follower_email).get()
    if follow:
        follow.delete()
        return True
    else:
        return False
        
        
def get_followers(leader_email, limit, offset):
    followers = db.Follow.all().filter('leader_email =', leader_email).order('since_date').fetch(limit,offset)
    return [get_user_profile(f.follower_email) for f in followers]


def get_leaders(follower_email, limit, offset):
    leaders = db.Follow.all().filter('follower_email =', follower_email).order('since_date').fetch(limit, offset)
    return [get_user_profile(f.leader_email) for f in leaders]

def add_to_news_feed(user_email, artwork, news_type, date=None):
    news_feed_item = db.NewsFeed.all().filter('artwork =', artwork).filter('user_email =', user_email).get()
    if news_feed_item:
        news_feed_item.date = datetime.now()
        news_feed_item.type = news_type
        news_feed_item.put()
    else:
        news_feed_item = db.NewsFeed()
        news_feed_item.user_email = user_email
        news_feed_item.artwork = artwork
        news_feed_item.type = news_type
        if date:
            news_feed_item.date = date
        news_feed_item.put()
    