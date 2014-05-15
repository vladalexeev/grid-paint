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

import zlib

from common import BasicPageRequestHandler
from common import BasicRequestHandler

from google.appengine.api import users

page_size=10


class PageIndex(BasicPageRequestHandler):
    def get(self):
        recent_artworks = cache.get(cache.MC_MAIN_PAGE_RECENT_IMAGES_KEY)        
        if not recent_artworks:                    
            all_artworks=db.Artwork.all()
            all_artworks=all_artworks.order('-date').fetch(3,0)        
            recent_artworks=[convert.convert_artwork_for_page(a,200,150) for a in all_artworks]
            cache.add(cache.MC_MAIN_PAGE_RECENT_IMAGES_KEY, recent_artworks)

        editor_choice = cache.get(cache.MC_MAIN_PAGE_RECENT_EDITOR_CHOICE)
        if not editor_choice:
            choice_artworks = db.Artwork.all().filter('editor_choice =', True)
            choice_artworks = choice_artworks.order('-date').fetch(3,0)
            editor_choice = [convert.convert_artwork_for_page(a,200,150) for a in choice_artworks]
            cache.add(cache.MC_MAIN_PAGE_RECENT_EDITOR_CHOICE, editor_choice)
            
        recent_comments = cache.get(cache.MC_MAIN_PAGE_RECENT_COMMENTS)
        
        if not recent_comments:
            comments = db.Comment.all().order('-date').fetch(5, 0)
            recent_comments = [convert.convert_comment_for_page(c) for c in comments]
            cache.add(cache.MC_MAIN_PAGE_RECENT_COMMENTS, recent_comments)
        
        self.write_template('templates/index.html', 
                            {
                             'artworks': recent_artworks,
                             'editor_choice': editor_choice,
                             'comments': recent_comments
                             })
        
class PagePrivacyPolicy(BasicPageRequestHandler):
    def get(self):
        self.write_template('templates/privacy-policy.html',{})

class PageHistory(BasicPageRequestHandler):
    def get(self):
        self.write_template('templates/history.html',{})
        
class PageNewImage(BasicPageRequestHandler):
    def get(self):
        if not self.user_info.user:
            self.redirect(self.user_info.login_url)
            return;
        
        self.write_template('templates/new-image.html', {})
        
class PagePainter(BasicPageRequestHandler):
    def get(self):
        if self.request.get('id'):
            artwork_id=self.request.get('id')
            artwork=dao.get_artwork(artwork_id)
            
            if artwork.json_compressed:
                artwork_json = zlib.decompress(artwork.json.encode('ISO-8859-1'))
            else:
                artwork_json = artwork.json
            
            self.write_template('templates/painter.html', 
                                {
                                 'artwork_id': artwork_id,
                                 'artwork_name': artwork.name,
                                 'artwork_description': artwork.description,
                                 'artwork_json': artwork_json,
                                 'artwork_tags': ','.join([tags.tag_by_url_name(t).title for t in artwork.tags])
                                 })
        else:
            new_artwork={
                         'version': {
                                     'major': 2,
                                     'minor': 0
                                     },
                         'backgroundColor': '#ffffff',
                         'canvasSize':{
                                       'width': int(self.request.get('artwork_width')),
                                       'height': int(self.request.get('artwork_height')),                                       
                                       },
                         'layers': [{
                                     'grid': self.request.get('artwork_grid'),
                                     'cellSize': int(self.request.get('cell_size')),                     
                                     'rows':[]
                                     }],
                         'recentColors':['#4096EE', '#FFFFFF', '#000000', '#EEEEEE', 
                                         '#FFFF88', '#CDEB8B', '#6BBA70', '#006E2E', 
                                         '#C3D9FF', '#356AA0', '#FF0096', '#B02B2C',
                                         '#FF7400', '#EF9090', '#0099FF', '#9933FF' 
                                         ]
                         }
            artwork_json=json.dumps(new_artwork)
            self.write_template('templates/painter.html', 
                                {
                                 'artwork_json': artwork_json
                                 })
            
    def post(self):
        artwork_json=self.request.get('artwork_json')
        self.write_template('templates/painter.html', 
                                {
                                 'artwork_json': artwork_json
                                 })

class PageMyImages(BasicPageRequestHandler):
    def get(self):
        if not self.user_info.user:
            self.redirect(self.user_info.login_url)
            return;
        
        def artworks_query_func():
            return db.Artwork.all().filter('author', self.user_info.user).order('-date')
        
        def href_create_func(offset):
            return '/my-images?offset='+str(offset)
        
        model = create_gallery_model(self.request.get('offset'), 
                                     artworks_query_func, 
                                     href_create_func)
        
        self.write_template('templates/my-artworks.html', model)

        
def create_gallery_model(offset_param, artworks_query_func, href_create_func):
    """
    Create a model of artwork list based on request.
    offset_param - offset parameter from request
    artworks_query_func() - function for create query for artworks
    href_create_func(offset) - function for create next and prev page hyperlinks
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
            
    all_artworks=artworks_query_func().fetch(fetch_count+1,offset)
        
    has_prev_page=(offset>0)
    has_next_page=len(all_artworks)>fetch_count
        
    if len(all_artworks)>fetch_count:
        all_artworks=all_artworks[:fetch_count]
            
    artworks=[convert.convert_artwork_for_page(a,200,150) for a in all_artworks]
        
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
            
        model = create_gallery_model(self.request.get('offset'), 
                                     artworks_query_func, 
                                     href_create_func)
        
        model['search_query'] = query
        
        self.write_template('templates/gallery.html', model)
        
        
class PageEditorChoice(BasicPageRequestHandler):
    def get(self):
        query=self.request.get('q')
        
        def artworks_query_func():
            all_artworks=db.Artwork.all().filter('editor_choice =', True)
            return all_artworks.order('-date')
        
        def href_create_func(offset):
            if query:
                return '/editor-choice?offset='+str(offset)
            else:
                return '/editor-choice?offset='+str(offset)
            
        model = create_gallery_model(self.request.get('offset'), 
                                     artworks_query_func, 
                                     href_create_func)
        
        model['search_query'] = query
        
        self.write_template('templates/editor-choice.html', model)
        
        
        
class PageImage(BasicPageRequestHandler):
    def get(self, *arg):
        artwork_id = arg[0]
        artwork = dao.get_artwork(artwork_id)
        if not artwork:
            self.response.set_status(404)
            return
        
        db_comments = db.Comment.all().filter('artwork_ref =', artwork).order('date')
        comments = [convert.convert_comment_for_page(c) for c in db_comments]
        
        converted_artwork = convert.convert_artwork_for_page(artwork, 600, 400)
        converted_artwork['tags_merged'] = ','.join([tags.tag_by_url_name(t.title).title for t in converted_artwork['tags']]) 
        
        self.write_template('templates/artwork-details.html', 
                            {
                             'artwork': converted_artwork,
                             'can_edit_artwork': self.user_info.superadmin or artwork.author==self.user_info.user,
                             'comments': comments
                            })
        
        
class PageAdmin(BasicPageRequestHandler):
    def get(self):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return
        
        self.write_template('templates/admin.html', 
                            {
                            })
        
class PageAdminUpdateArtworkIterate(BasicPageRequestHandler):
    def get(self):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return
        
        self.write_template('templates/admin-update-artwork-iterate.html', 
                            {
                            })
        
        
class PageNotifications(BasicPageRequestHandler):
    def get(self):
        if not self.user_info.user:
            self.response.set_status(403)
            return
        
        req_offset = self.request.get('offset')
        
        if req_offset:
            offset = int(req_offset)
        else:
            offset = 0
            
        query = db.Notification.all().filter('recipient =', self.user_info.user).order('-date').fetch(20,offset)
        
        self.write_template('templates/notifications.html', 
                            {
                             'notifications': [convert.convert_notification(n) for n in query]
                             })
        
        
class PageMyProfile(BasicPageRequestHandler):
    def get(self):
        if not self.user_info.user:
            self.response.set_status(403)
            return;
        
        user_profile = dao.get_user_profile(self.user_info.user.email())
        
        self.write_template('templates/my-profile.html', 
                            {
                             'profile': user_profile
                             })
        
class PageProfile(BasicRequestHandler):
    def get(self, *arg):
        profile_id = int(arg[0])
        user_profile = dao.get_user_profile_by_id(profile_id)
        
        def artworks_query_func():
            return db.Artwork.all().filter('author =',users.User(user_profile.email)).order('-date')
        
        def href_create_func(offset):
            return '/profiles/'+str(profile_id)+'?offset='+str(offset)
        
        model = create_gallery_model(self.request.get('offset'), 
                                     artworks_query_func, 
                                     href_create_func)
        model['profile'] = convert.convert_user_profile(user_profile)
        
        self.write_template('templates/profile.html', model)
