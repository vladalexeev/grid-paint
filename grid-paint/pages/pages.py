# -*- coding: utf-8 -*-
'''
Created on 23.07.2013

@author: Vlad
'''

import json

import db
import tags
import cache
import dao
import convert
import cs

import zlib

from common import BasicPageRequestHandler
from common import BasicRequestHandler

page_size=10
users_page_size=50


class PageIndex(BasicPageRequestHandler):
    def get(self):
        newsfeed = None
        if self.user_info.user:
            newsfeed_artworks = db.NewsFeed.all().filter('user_email =', self.user_info.user_email).order('-date').fetch(7)
            newsfeed = [convert.convert_artwork_for_page(a, 200, 150) for a in newsfeed_artworks]
            if len(newsfeed) < 3:
                newsfeed = None
            elif len(newsfeed) < 7:
                newsfeed = newsfeed[0:3]
        
        recent_artworks = cache.get(cache.MC_MAIN_PAGE_RECENT_IMAGES_KEY)        
        if not recent_artworks:                    
            all_artworks=db.Artwork.all()
            all_artworks=all_artworks.order('-date').fetch(3,0)        
            recent_artworks=[convert.convert_artwork_for_page(a,200,150) for a in all_artworks]
            cache.add(cache.MC_MAIN_PAGE_RECENT_IMAGES_KEY, recent_artworks)

        editor_choice = cache.get(cache.MC_MAIN_PAGE_RECENT_EDITOR_CHOICE)
        if not editor_choice:
            choice_artworks = db.Artwork.all().filter('editor_choice =', True)
            choice_artworks = choice_artworks.order('-editor_choice_date').fetch(3,0)
            editor_choice = [convert.convert_artwork_for_page(a,200,150) for a in choice_artworks]
            cache.add(cache.MC_MAIN_PAGE_RECENT_EDITOR_CHOICE, editor_choice)
            
        top_favorites = cache.get(cache.MC_MAIN_PAGE_TOP_FAVORITES)
        if not top_favorites:
            top_favorite_artworks = db.FavoriteCounter.all().order('-count').order('-date')
            top_favorite_artworks = top_favorite_artworks.fetch(3,0)
            top_favorites = [convert.convert_artwork_for_page(a,200,150) for a in top_favorite_artworks]
            cache.add(cache.MC_MAIN_PAGE_TOP_FAVORITES, top_favorites)
            
        recent_favorites = cache.get(cache.MC_MAIN_PAGE_RECENT_FAVORITES)
        if not recent_favorites:
            recent_favorites_artworks = db.Favorite.all().order('-date')
            recent_favorites_artworks = recent_favorites_artworks.fetch(3,0)
            recent_favorites = [convert.convert_artwork_for_page(a,200,150) for a in recent_favorites_artworks]
            cache.add(cache.MC_MAIN_PAGE_RECENT_FAVORITES, recent_favorites)
            
        recent_comments = cache.get(cache.MC_MAIN_PAGE_RECENT_COMMENTS)
        if not recent_comments:
            comments = db.Comment.all().order('-date').fetch(5, 0)
            recent_comments = [convert.convert_comment_for_page_rich(c) for c in comments]
            cache.add(cache.MC_MAIN_PAGE_RECENT_COMMENTS, recent_comments)
            
        productive_artists = cache.get(cache.MC_MAIN_PAGE_PRODUCTIVE_ARTISTS)
        if not productive_artists:
            p_artists = db.UserProfile.all().order('-artworks_count').fetch(5)
            productive_artists = [convert.convert_user_profile(a) for a in p_artists]
            cache.add(cache.MC_MAIN_PAGE_PRODUCTIVE_ARTISTS, productive_artists)
            
        top_rated_artists = cache.get(cache.MC_MAIN_PAGE_TOP_RATED_ARTISTS)
        if not top_rated_artists:
            r_artists = db.UserProfile.all().order('-favorite_count').fetch(5)
            top_rated_artists = [convert.convert_user_profile(a) for a in r_artists]
            cache.add(cache.MC_MAIN_PAGE_TOP_RATED_ARTISTS, top_rated_artists)
        
        self.write_template('templates/index.html', 
            {
                'artworks': recent_artworks,
                'editor_choice': editor_choice,
                'top_favorites': top_favorites,
                'recent_favorites': recent_favorites,
                'comments': recent_comments,
                'productive_artists': productive_artists,
                'top_rated_artists': top_rated_artists,
                'newsfeed': newsfeed,
                'og_title': 'Grid Paint',
                'og_description': 'An online tool for pixel drawing with different shapes of pixels.',
                'og_url': 'https://grid-paint.com',
                'og_image': 'https://grid-paint.com/img/grid-paint-poster.png'
            })


class PagePrivacyPolicy(BasicPageRequestHandler):
    def get(self):
        self.write_template('templates/privacy-policy.html',{})


class PageRules(BasicPageRequestHandler):
    def get(self):
        self.write_template('templates/rules.html',{})


class PageHistory(BasicPageRequestHandler):
    def get(self):
        self.write_template('templates/history.html',{})


class PageNewImage(BasicPageRequestHandler):
    def get(self):
        if not self.user_info.user:
            self.redirect(self.user_info.login_url)
            return
        
        if self.user_info.read_only:
            self.response.set_status(403)
            return
        
        self.write_template('templates/new-image.html', {})


class PagePainter(BasicPageRequestHandler):
    def get(self):
        if not self.user_info.user:
            self.redirect(self.user_info.login_url)
            return
        
        if self.user_info.read_only:
            self.response.set_status(403)
            return
                
        if self.request.get('id'):
            artwork_id = self.request.get('id')
            artwork = dao.get_artwork(artwork_id)
            
            if artwork is None:
                self.response.set_status(404)
                return
            
            if hasattr(artwork,'json'):            
                if artwork.json_compressed:
                    artwork_json = zlib.decompress(artwork.json.encode('ISO-8859-1'))
                else:
                    artwork_json = artwork.json
            else:
                artwork_json = zlib.decompress(cs.read_file(artwork.json_file_name))
            
            self.write_template(
                'templates/painter.html',
                {
                    'artwork_id': artwork_id,
                    'artwork_name': artwork.name,
                    'artwork_description': artwork.description,
                    'artwork_json': artwork_json,
                    'artwork_tags': ','.join([tags.tag_by_url_name(t).title for t in artwork.tags])
                })
        elif self.request.get('copy_id'):
            artwork_id = self.request.get('copy_id')
            artwork = dao.get_artwork(artwork_id)
            
            if hasattr(artwork, 'json'):
                if artwork.json_compressed:
                    artwork_json = zlib.decompress(artwork.json.encode('ISO-8859-1'))
                else:
                    artwork_json = artwork.json
            else:
                artwork_json = zlib.decompress(cs.read_file(artwork.json_file_name))
            
            self.write_template(
                'templates/painter.html',
                {
                    'artwork_name': artwork.name+' (copy)',
                    'artwork_description': artwork.description+' (copy)',
                    'artwork_json': artwork_json,
                    'artwork_tags': ','.join([tags.tag_by_url_name(t).title for t in artwork.tags])
                })
        else:
            new_artwork = {
                'version': {
                    'major': 2,
                    'minor': 0
                },
                'backgroundColor': '#ffffff',
                'canvasSize':{
                    'width': int(float(self.request.get('artwork_width'))),
                    'height': int(float(self.request.get('artwork_height'))),
                },
                'layers': [{
                    'grid': self.request.get('artwork_grid'),
                    'cellSize': int(float(self.request.get('cell_size'))),
                    'rows': []
                }],
                'recentColors':[
                    '#4096EE', '#FFFFFF', '#000000', '#EEEEEE',
                    '#FFFF88', '#CDEB8B', '#6BBA70', '#006E2E',
                    '#C3D9FF', '#356AA0', '#FF0096', '#B02B2C',
                    '#FF7400', '#EF9090', '#0099FF', '#9933FF',
                    '#2E2EFF', '#8A725D', '#FF3838', '#4BC8D1',
                    '#CBD114', '#858585'
                ]
            }
            artwork_json = json.dumps(new_artwork)
            self.write_template(
                'templates/painter.html',
                {
                    'artwork_json': artwork_json
                })
            
    def post(self):
        artwork_json=self.request.get('artwork_json')
        self.write_template(
            'templates/painter.html',
            {
                'artwork_json': artwork_json
            })


class PageMyImages(BasicPageRequestHandler):
    def get(self):
        if not self.user_info.user:
            self.redirect(self.user_info.login_url)
            return

        self.redirect('/profiles/' + str(self.user_info.profile_id) + '/images')
        

def create_user_model(offset_param, user_query_func, href_create_func, memcache_cursor_key_func):
    if offset_param:
        offset=int(offset_param)
    else:
        offset=0
            
    if offset<0:
        offset=0
            
    fetch_count = users_page_size        
    query = user_query_func()
    
    if offset==0:
        all_users = query.run(limit=fetch_count+1)
    else:
        cursor=cache.get(memcache_cursor_key_func(offset))
        if cursor:
            query = query.with_cursor(start_cursor=cursor)
            all_users = query.run(limit=fetch_count+1)
        else:
            all_users = query.run(limit=fetch_count+1,offset=offset)
            cache.add(memcache_cursor_key_func(offset), query.cursor())
    
    import logging
    has_prev_page = (offset>0)
    has_next_page = False
    
    logging.error('offset={0} has_prev_page={1}'.format(offset, has_prev_page))
    
    index = 0
    users = []    
    for u in all_users:
        index = index+1
        if index>fetch_count:
            has_next_page = True
        else:
            converted_user = convert.convert_user_profile(u)                
            users.append(converted_user)
            if index==fetch_count:
                cache.add(memcache_cursor_key_func(offset+fetch_count), query.cursor())
                        
    next_page_href=href_create_func(offset+fetch_count)
        
    if offset-users_page_size <=1:
        prev_page_href=href_create_func(0)
    else:
        prev_page_href=href_create_func(offset-users_page_size)
        
    return  {
             'has_next_page': has_next_page,
             'has_prev_page': has_prev_page,
             'next_page_href': next_page_href,
             'prev_page_href': prev_page_href,
             'first_page_href': href_create_func(0),
             'users': users
            }

        
def create_gallery_model(offset_param, artworks_query_func, href_create_func, 
                         memcache_cursor_key_func, additional_values_func=None):
    """
    Create a model of artwork list based on request.
    offset_param - offset parameter from request
    artworks_query_func() - function for create query for artworks
    href_create_func(offset) - function for create next and prev page hyperlinks
    memcache_cursor_key_func(offset) - function to generate keys for cursors stored in MemCache
    additional_values_func(object, values_dict) - function extracts additional values from objects of query result
    """
    if offset_param:
        offset=int(offset_param)
    else:
        offset=0
            
    if offset<0:
        offset=0
            
    if offset == 0:
        fetch_count = page_size+1
    else:
        fetch_count = page_size
            
    query = artworks_query_func()
    
    if offset==0:
        all_artworks = query.run(limit=fetch_count+1)
    else:
        cursor=cache.get(memcache_cursor_key_func(offset))
        if cursor:
            query = query.with_cursor(start_cursor=cursor)
            all_artworks = query.run(limit=fetch_count+1)
        else:
            all_artworks = query.run(limit=fetch_count+1,offset=offset)
            cache.add(memcache_cursor_key_func(offset), query.cursor())
        
    has_prev_page = (offset>0)
    has_next_page = False
    
    index = 0
    artworks = []    
    for a in all_artworks:
        index = index+1
        if index>fetch_count:
            has_next_page = True
        else:
            converted_artwork = convert.convert_artwork_for_page(a,200,150)
                
            if additional_values_func:
                additional_values_func(a, converted_artwork)
                
            artworks.append(converted_artwork)
            if index==fetch_count:
                cache.add(memcache_cursor_key_func(offset+fetch_count), query.cursor())
                        
    next_page_href=href_create_func(offset+fetch_count)
        
    if offset-page_size <=1:
        prev_page_href=href_create_func(0)
    else:
        prev_page_href=href_create_func(offset-page_size)
        
    return  {
             'has_next_page': has_next_page,
             'has_prev_page': has_prev_page,
             'next_page_href': next_page_href,
             'prev_page_href': prev_page_href,
             'artworks': artworks
            }

        
class PageGallery(BasicPageRequestHandler):
    def get(self):
        query=self.request.get('q')
        
        def artworks_query_func():
            all_artworks=db.Artwork.all()
            if query:
                all_artworks=all_artworks.filter('tags =', tags.tag_url_name(query))                

            return all_artworks.order('-date')
        
        def href_create_func(offset):
            if query:
                return '/gallery?offset='+str(offset)+'&q='+query
            else:
                return '/gallery?offset='+str(offset)
            
        def memcache_cursor_key_func(offset):
            if query:
                return cache.MC_ARTWORK_LIST+'gallery_'+query+'_'+str(offset)
            else:
                return cache.MC_ARTWORK_LIST+'gallery_'+str(offset)
            
        model = create_gallery_model(self.request.get('offset'), 
                                     artworks_query_func, 
                                     href_create_func,
                                     memcache_cursor_key_func)
        
        model['search_query'] = query
        
        self.write_template('templates/gallery.html', model)
        
        
class PageEditorChoice(BasicPageRequestHandler):
    def get(self):
        query=self.request.get('q')
        
        def artworks_query_func():
            all_artworks=db.Artwork.all().filter('editor_choice =', True)
            return all_artworks.order('-editor_choice_date')
        
        def href_create_func(offset):
            return '/editor-choice?offset='+str(offset)
            
        def memcache_cursor_key_func(offset):
            return cache.MC_ARTWORK_LIST+'editors_choice_'+str(offset)
            
        model = create_gallery_model(self.request.get('offset'), 
                                     artworks_query_func, 
                                     href_create_func,
                                     memcache_cursor_key_func)
        
        model['search_query'] = query
        
        self.write_template('templates/editor-choice.html', model)
                
        
class PageImage(BasicPageRequestHandler):
    def get(self, *arg):
        artwork_id = arg[0]
        artwork = dao.get_artwork(artwork_id)
        if not artwork:
            self.response.set_status(404)
            return
        
        favorite_count = dao.get_artwork_favorite_count(artwork)
        favorite = dao.is_artwork_favorite_by_user(artwork, self.user_info.user_email)
        
        db_comments = db.Comment.all().filter('artwork_ref =', artwork).order('date')
        comments = [convert.convert_comment_for_page(c) for c in db_comments]
        
        converted_artwork = convert.convert_artwork_for_page(artwork, 600, 400)
        if 'tags' in converted_artwork:
            converted_artwork['tags_merged'] = ','.join([tags.tag_by_url_name(t.title).title for t in converted_artwork['tags']])
            
        if self.user_info.user:
            following = dao.is_follower(artwork.author_email, self.user_info.user_email)
        else:
            following = None 
        
        self.write_template('templates/artwork-details.html', 
            {
                'artwork': converted_artwork,
                'can_edit_artwork': self.user_info.superadmin or artwork.author_email==self.user_info.user_email,
                'comments': comments,
                'favorite_count': favorite_count,
                'favorite': favorite,
                'following': following,
                'og_title': converted_artwork['name'],
                'og_image': 'https://grid-paint.com/images/png/' + artwork_id + '.png',
                'og_image_width': converted_artwork['full_image_width'],
                'og_image_height': converted_artwork['full_image_height'],
                'og_url': 'https://grid-paint.com/images/details/' + artwork_id,
                'og_description': u'Created by {} in Grid Paint'.format(converted_artwork['author']['nickname'])
            })
        
        
class PageAdmin(BasicPageRequestHandler):
    def get(self):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return

        task_statuses = db.TaskStatus.all()
        
        self.write_template(
            'templates/admin.html',
            {
                'task_statuses': task_statuses
            }
        )


class PageAdminTaskStatus(BasicPageRequestHandler):
    def get(self, *args):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return

        task_name = args[0]
        task_status = db.TaskStatus.all().filter('task_name =', task_name).get()
        task_log = db.TaskLog.all().filter('task_name =', task_name).order('date')

        self.write_template(
            'templates/admin-task-status.html',
            {
                'task_status': task_status,
                'task_log': task_log
            }
        )


class PageAdminUpdateIterate(BasicPageRequestHandler):
    def get(self):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return
        
        self.write_template('templates/admin-update-iterate.html', 
                            {
                            })
        
        
class PageNotifications(BasicPageRequestHandler):
    def get(self):
        if not self.user_info.user:
            self.response.set_status(403)
            return
        
        self.write_template(
            'templates/notifications.html', 
            {
                'hide_ads': True
            })
        
        
class PageMyProfile(BasicPageRequestHandler):
    def get(self):
        if not self.user_info.user:
            self.response.set_status(403)
            return;
        
        user_profile = dao.get_user_profile(self.user_info.user_email)
        
        self.write_template('templates/my-profile.html', 
                            {
                             'profile': user_profile
                             })


class PageProfile(BasicRequestHandler):
    def get(self, *arg):
        try:
            profile_id = int(arg[0])
        except ValueError:
            self.response.set_status(404)
            return
            
        user_profile = dao.get_user_profile_by_id(profile_id)
        if not user_profile:
            self.response.set_status(404)
            return

        recent_db_images = db.Artwork.all().filter('author_email', user_profile.email).order('-date').fetch(3, 0)
        recent_user_images = [convert.convert_artwork_for_page(a, 200, 150) for a in recent_db_images]

        recent_db_tags = db.UserTag.all().filter('user_id', user_profile.key().id()).order('-last_date').fetch(3, 0)
        recent_user_tags = [convert.convert_tag_for_page(t) for t in recent_db_tags]
        for t in recent_user_tags:
            t['url'] = '/profiles/{}/tags/{}/images'.format(profile_id, t['url_name'])

        model = {
            'profile': convert.convert_user_profile(user_profile),
            'recent_images': recent_user_images,
            'has_any_recent_images': len(recent_user_images) > 0,
            'has_more_recent_images': len(recent_user_images) >= 3,
            'recent_tags': recent_user_tags,
            'has_any_recent_tags': len(recent_user_tags) > 0,
            'has_more_recent_tags': len(recent_user_tags) >= 3,
        }

        if self.user_info.user:
            model['following'] = dao.is_follower(user_profile.email, self.user_info.user_email)

        if self.user_info.superadmin:
            model['profile']['email'] = user_profile.email
            model['profile']['alternative_emails'] = getattr(user_profile, 'alternative_emails', [])

        if self.user_info.user and profile_id == self.user_info.profile_id:
            model['this_user_profile'] = True
        
        self.write_template('templates/profile.html', model)


class PageUserImages(BasicRequestHandler):
    def get(self, *arg):
        try:
            profile_id = int(arg[0])
        except ValueError:
            self.response.set_status(404)
            return

        user_profile = dao.get_user_profile_by_id(profile_id)
        if not user_profile:
            self.response.set_status(404)
            return

        def artworks_query_func():
            return db.Artwork.all().filter('author_email =', user_profile.email).order('-date')

        def href_create_func(offset):
            return '/profiles/' + str(profile_id) + '/images?offset=' + str(offset)

        def memcache_cursor_key_func(offset):
            return cache.MC_ARTWORK_LIST + 'profile_' + str(profile_id) + '_' + str(offset)

        model = create_gallery_model(self.request.get('offset'),
                                     artworks_query_func,
                                     href_create_func,
                                     memcache_cursor_key_func)
        model['profile'] = convert.convert_user_profile(user_profile)
        if self.user_info.user:
            model['following'] = dao.is_follower(user_profile.email, self.user_info.user_email)

        if self.user_info.user and profile_id == self.user_info.profile_id:
            model['this_user_profile'] = True

        model['user_page_title'] = 'Images of'

        self.write_template('templates/user-images.html', model)


class PageUserFavorites(BasicPageRequestHandler):
    def get(self, *arg):
        profile_id = int(arg[0])        
        user_profile = dao.get_user_profile_by_id(profile_id)
        
        def artworks_query_func():
            all_artworks=db.Favorite.all()
            all_artworks=all_artworks.filter('user_email =', user_profile.email)                
            return all_artworks.order('-date')
        
        def href_create_func(offset):
            return '/profiles/'+str(profile_id)+'/favorites?offset='+str(offset)
            
        def memcache_cursor_key_func(offset):
            return cache.MC_ARTWORK_LIST+'user_favorites_'+str(profile_id)+'_'+str(offset)
            
        model = create_gallery_model(self.request.get('offset'), 
                                     artworks_query_func, 
                                     href_create_func,
                                     memcache_cursor_key_func)
        model['user_page_title'] = 'Favorites of'
        model['profile'] = convert.convert_user_profile(user_profile)
    
        if self.user_info.user and self.user_info.profile_id==profile_id:
            model['this_user_profile']=True
        
        self.write_template('templates/user-favorites.html', model)


class PageMyFavorites(BasicPageRequestHandler):
    def get(self, *arg):
        if not self.user_info.user:
            self.response.set_status(403)
            return

        self.redirect('/profiles/{}/favorites'.format(self.user_info.profile_id))


class PageTopFavorites(BasicPageRequestHandler):
    def get(self):
        def artworks_query_func():
            all_artworks=db.FavoriteCounter.all()
            return all_artworks.order('-count').order('-date')
        
        def href_create_func(offset):
            return '/top-favorites?offset='+str(offset)
            
        def memcache_cursor_key_func(offset):
            return cache.MC_ARTWORK_LIST+'top_favorites_'+str(offset)
        
        def additional_values_func(obj, values):
            values['favorites_count'] = obj.count
            
        model = create_gallery_model(self.request.get('offset'), 
                                     artworks_query_func, 
                                     href_create_func,
                                     memcache_cursor_key_func,
                                     additional_values_func)
                
        self.write_template('templates/top-favorites.html', model)
        
class PageRecentFavorites(BasicPageRequestHandler):
    def get(self):
        def artworks_query_func():
            all_artworks=db.Favorite.all()
            return all_artworks.order('-date')
        
        def href_create_func(offset):
            return '/favorites?offset='+str(offset)
            
        def memcache_cursor_key_func(offset):
            return cache.MC_ARTWORK_LIST+'recent_favorites_'+str(offset)
        
        def addition_values_func(obj, values):
            user_profile = dao.get_user_profile(obj.user_email)
            if user_profile:
                values['favoriter'] = convert.convert_user_profile(user_profile)
            else:
                values['favoriter'] = convert.convert_user(obj.user_email)
            
        model = create_gallery_model(self.request.get('offset'), 
                                     artworks_query_func, 
                                     href_create_func,
                                     memcache_cursor_key_func,
                                     addition_values_func)
        
        self.write_template('templates/recent-favorites.html', model)


class PageNewsFeed(BasicPageRequestHandler):
    def get(self):
        if not self.user_info.user:
            self.redirect('/')
            return
        
        user_email = self.user_info.user_email
        
        def artworks_query_func():
            all_artworks=db.NewsFeed.all()
            return all_artworks.filter('user_email =', user_email).order('-date')
        
        def href_create_func(offset):
            return '/newsfeed?offset='+str(offset)
            
        def memcache_cursor_key_func(offset):
            return cache.MC_ARTWORK_LIST+'newsfeed_' + user_email+ '_'  + str(offset)
        
        def addition_values_func(obj, values):
            pass
        
        model = create_gallery_model(self.request.get('offset'), 
                                     artworks_query_func, 
                                     href_create_func,
                                     memcache_cursor_key_func,
                                     addition_values_func)
        
        self.write_template('templates/newsfeed.html', model)

        
class PageUsersByArtworksCount(BasicPageRequestHandler):
    def get(self):
        def users_query_func():
            all_users=db.UserProfile.all()
            return all_users.order('-artworks_count')
        
        def href_create_func(offset):
            return '/profiles/by-artwork-count?offset='+str(offset)
            
        def memcache_cursor_key_func(offset):
            return cache.MC_USER_LIST+'by_artworks_count_'+str(offset)
            
        model = create_user_model(self.request.get('offset'), 
                                  users_query_func, 
                                  href_create_func,
                                  memcache_cursor_key_func)
        model['list_title'] = 'Artists by artworks count'
        
        self.write_template('templates/user-list-by-artworks-count.html', model)

class PageUsersByFavortiesCount(BasicPageRequestHandler):
    def get(self):
        def users_query_func():
            all_users=db.UserProfile.all()
            return all_users.order('-favorite_count')
        
        def href_create_func(offset):
            return '/profiles/by-stars-count?offset='+str(offset)
            
        def memcache_cursor_key_func(offset):
            return cache.MC_USER_LIST+'by_stars_count_'+str(offset)
            
        model = create_user_model(self.request.get('offset'), 
                                  users_query_func, 
                                  href_create_func,
                                  memcache_cursor_key_func)
        model['list_title'] = 'Artists by stars count'
        
        self.write_template('templates/user-list-by-stars-count.html', model)

class PageUsersBlocked(BasicPageRequestHandler):
    def get(self):
        def users_query_func():
            all_users=db.UserProfile.all().filter('read_only =', True)
            return all_users.order('nickname')
        
        def href_create_func(offset):
            return '/profiles/blocked?offset='+str(offset)
            
        def memcache_cursor_key_func(offset):
            return cache.MC_USER_LIST+'blocked_count_'+str(offset)
            
        model = create_user_model(self.request.get('offset'), 
                                  users_query_func, 
                                  href_create_func,
                                  memcache_cursor_key_func)
        model['list_title'] = 'Blocked artists'
        
        self.write_template('templates/user-list-blocked.html', model)
        
class PageProfiles(BasicPageRequestHandler):
    def get(self):
        self.redirect('/profiles/by-stars-count', True)
        
class PageComments(BasicPageRequestHandler):
    def get(self):
        self.write_template('templates/comments.html', {})
        
class PageUserComments(BasicPageRequestHandler):
    def get(self, *arg):
        profile_id = int(arg[0])        
        user_profile = dao.get_user_profile_by_id(profile_id)
        
        model = {
            'profile_id': user_profile.key().id(),
            'nickname': user_profile.nickname
            }
        
        self.write_template('templates/comments.html', model)
        

class PageUserFollowers(BasicPageRequestHandler):
    def get(self, *arg):
        profile_id = int(arg[0])
        user_profile = dao.get_user_profile_by_id(profile_id)
        
        model = {
            'profile_id': user_profile.key().id(),
            'nickname': user_profile.nickname
            }
        
        self.write_template('templates/user-followers.html', model)
        
        
class PageMyFollowers(BasicPageRequestHandler):
    def get(self, *arg):
        if not self.user_info.user:
            self.response.set_status(403)
            return
        
        self.write_template('templates/user-followers.html', {})
        

class PageMyLeaders(BasicPageRequestHandler):
    def get(self, *arg):
        if not self.user_info.user:
            self.response.set_status(403)
            return
        
        self.write_template('templates/user-leaders.html', {})


class PageAdminTags(BasicPageRequestHandler):
    def get(self):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return

        limit = int(self.request.get('limit'))
        offset = int(self.request.get('offset'))
        order = self.request.get('order')

        if not order:
            order = 'url_name'

        fetched_tags = db.Tag.all().order(order).fetch(limit + 1, offset)
        query_tags = [t for t in fetched_tags]

        prev_offset = offset - limit
        if prev_offset < 0:
            prev_offset = 0

        if len(query_tags) > limit:
            query_tags = query_tags[:-1]
            next_offset = offset + limit
        else:
            next_offset = -1

        self.write_template(
            'templates/admin-tags.html',
            {
                'tags': query_tags,
                'limit': limit,
                'offset': offset,
                'next_offset': next_offset,
                'prev_offset': prev_offset,
                'order': order,
            }
        )


class PageGlobalTags(BasicPageRequestHandler):
    def get(self):
        if self.request.get('offset'):
            offset = int(self.request.get('offset'))
        else:
            offset = 0

        limit = 11 if offset == 0 else 10

        fetched_tags = db.Tag.all().order('-last_date').fetch(limit, offset)
        query_tags = [convert.convert_tag_for_page(t) for t in fetched_tags]
        for t in query_tags:
            t['url'] = '/tags/' + t['url_name'] + '/images'

        prev_offset = offset - limit
        if prev_offset < 0:
            prev_offset = 0

        if len(query_tags) > limit:
            query_tags = query_tags[:-1]
            next_offset = offset + limit
        else:
            next_offset = -1

        self.write_template(
            'templates/global-tags.html',
            {
                'tags': query_tags,
                'limit': limit,
                'offset': offset,
                'next_offset': next_offset,
                'prev_offset': prev_offset,
            }
        )


class PageUserTags(BasicPageRequestHandler):
    def get(self, *args):
        profile_id = int(args[0])
        if self.request.get('offset'):
            offset = int(self.request.get('offset'))
        else:
            offset = 0

        user_profile = dao.get_user_profile_by_id(profile_id)
        if not user_profile:
            self.response.set_status(404)
            return

        limit = 11 if offset == 0 else 10

        fetched_tags = db.UserTag.all().filter('user_id', profile_id).order('-last_date').fetch(limit + 1, offset)
        query_tags = [convert.convert_tag_for_page(t) for t in fetched_tags]
        for t in query_tags:
            t['url'] = '/profiles/{}/tags/{}/images'.format(profile_id, t['url_name'])

        if offset == 11:
            prev_offset = 0
        else:
            prev_offset = offset - limit
        if prev_offset < 0:
            prev_offset = 0

        has_prev_page = offset > 0

        if len(query_tags) > limit:
            query_tags = query_tags[:-1]
            next_offset = offset + limit
            has_next_page = True
        else:
            next_offset = -1
            has_next_page = False

        self.write_template(
            'templates/user-tags.html',
            {
                'user_page_title': 'Tags of',
                'profile': convert.convert_user_profile(user_profile),
                'tags': query_tags,
                'limit': limit,
                'offset': offset,
                'next_offset': next_offset,
                'prev_offset': prev_offset,
                'has_next_page': has_next_page,
                'has_prev_page': has_prev_page,
                'next_page_href': '/profiles/{}/tags?offset={}'.format(profile_id, next_offset),
                'prev_page_href': '/profiles/{}/tags?offset={}'.format(profile_id, prev_offset)
            }
        )


class PageTagImages(BasicPageRequestHandler):
    def get(self, *args):
        tag_name = args[0]

        def artworks_query_func():
            all_artworks = db.Artwork.all()
            all_artworks = all_artworks.filter('tags =', tags.tag_url_name(tag_name))
            return all_artworks.order('-date')

        def href_create_func(offset):
            return '/tags/' + tag_name + '/images?offset=' + str(offset)

        def memcache_cursor_key_func(offset):
            return cache.MC_ARTWORK_LIST + 'gallery_' + tag_name + '_' + str(offset)

        model = create_gallery_model(self.request.get('offset'),
                                     artworks_query_func,
                                     href_create_func,
                                     memcache_cursor_key_func)

        model['search_query'] = tag_name

        self.write_template('templates/gallery.html', model)


class PageUserTagImages(BasicPageRequestHandler):
    def get(self, *args):
        profile_id = int(args[0])
        tag_name = args[1]

        user = dao.get_user_profile_by_id(profile_id)
        if not user:
            self.response.set_status(404)
            return

        def artworks_query_func():
            all_artworks = db.Artwork.all()
            all_artworks = all_artworks.filter('author_email', user.email)
            all_artworks = all_artworks.filter('tags =', tags.tag_url_name(tag_name))
            return all_artworks.order('-date')

        def href_create_func(offset):
            return '/profiles/{}/tags/{}/images?offset={}'.format(profile_id, tag_name, offset)

        def memcache_cursor_key_func(offset):
            return cache.MC_ARTWORK_LIST + 'gallery_' + str(profile_id) + '_' + tag_name + '_' + str(offset)

        model = create_gallery_model(self.request.get('offset'),
                                     artworks_query_func,
                                     href_create_func,
                                     memcache_cursor_key_func)

        user_tag = db.UserTag.all().filter('user_id', profile_id).filter('url_name', tag_name).get()
        if user_tag:
            tag_title = user_tag.title
            model['tag'] = convert.convert_tag_for_page(user_tag)
        else:
            tag_title = tag_name

        model['search_query'] = tag_name
        model['user_page_title'] = 'Images by tag "{}" of'.format(tag_title)
        model['profile'] = convert.convert_user_profile(user)

        self.write_template('templates/user-images-by-tag.html', model)
