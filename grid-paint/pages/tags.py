# -*- coding: utf-8 -*-

from datetime import datetime
import db
import unidecode

import cache
from bad_language import hide_bad_language


def tag_url_name(title):
    title = title.lower().strip()
    if title and title[0] == '#':
        title = title[1:]

    result = unidecode.unidecode(title).\
        replace(' ', '-').\
        replace('/', '-').\
        replace('\\', '-').\
        replace(':', '-').\
        replace('#', '-').\
        replace('&', '-').\
        replace('=', '-')

    return unicode(result, 'utf-8')


def get_tag_by_title(title):
    url_name = tag_url_name(title)
    cache_tag = cache.get(cache.MC_TAG+url_name)
    
    if cache_tag:
        return cache_tag
    else:
        tag = db.Tag.all().filter('url_name =', url_name).get()
        return tag


def tag_added(title, user_id, artwork):
    if not title:
        return None

    title = title.strip()
    url_name = tag_url_name(title)
    if len(title) <= 1 or len(title) > 64:
        return None

    if hide_bad_language(title) != title:
        return None

    global_tag = db.Tag.all().filter('url_name =', url_name).get()
    if global_tag:
        if getattr(global_tag, 'count') is not None:
            global_tag.count = global_tag.count + 1
            global_tag.last_date = datetime.now()
            if not global_tag.cover:
                global_tag.cover = artwork
            global_tag.put()
    else:
        tag = db.Tag.all().filter('url_name =', url_name).get()
        if not tag:
            tag = db.Tag()
            tag.title = title
            tag.title_lower = title.lower()
            tag.url_name = url_name
            tag.date = datetime.now()
            tag.last_date = datetime.now()
            tag.cover = artwork
            tag.count = 1
            tag.put()
        
    user_tag = db.UserTag.all().filter('user_id =', user_id).filter('url_name', url_name).get()
    if user_tag:
        user_tag.count = user_tag.count + 1
        user_tag.last_date = datetime.now()
        if not user_tag.cover:
            user_tag.cover = artwork
        user_tag.put()
    else:
        user_tag = db.UserTag()
        user_tag.user_id = user_id
        user_tag.url_name = url_name
        user_tag.cover = artwork
        user_tag.title = title
        user_tag.title_lower = title.lower()
        user_tag.date = datetime.now()
        user_tag.last_date = datetime.now()
        user_tag.count = 1
        user_tag.put()

    cache.delete(cache.MC_TAG + url_name)
    return url_name


def tag_deleted(title, user_id, artwork):
    if not title:
        return

    title = title.strip()
    url_name = tag_url_name(title)

    global_tag = db.Tag.all().filter('url_name =', url_name).get()
    if global_tag:
        if hasattr(global_tag, 'count') and global_tag.count > 0:
            global_tag.count = global_tag.count - 1
        if hasattr(global_tag, 'cover') and global_tag.cover is not None and global_tag.cover.key().id() == artwork.key().id():
            global_tag.cover = None

        global_tag.put()

    user_tag = db.UserTag.all().filter('user_id =', user_id).filter('url_name', url_name).get()
    if user_tag:
        if hasattr(user_tag, 'cover') and user_tag.cover is not None and user_tag.cover.key().id() == artwork.key().id():
            user_tag.cover = None
        if user_tag.count > 0:
            user_tag.count = user_tag.count - 1
        if user_tag.count <= 0:
            user_tag.delete()
        else:
            user_tag.put()


def tag_by_url_name(url_name):
    cache_tag = cache.get(cache.MC_TAG + url_name)
    if cache_tag:
        return cache_tag
    else:
        tag = db.Tag.all().filter('url_name =', url_name).get()
        if tag:
            cache.add(cache.MC_TAG + url_name, tag)
        else:
            tag = db.Tag()
            tag.url_name = url_name
            tag.title = url_name
            tag.title_lower = url_name
        
        return tag

