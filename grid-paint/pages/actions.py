# -*- coding: utf-8 -*-
'''
Created on 23.07.2013

@author: Vlad
'''

import db
import json
import datetime
import StringIO

from PIL import Image, ImageDraw

from common import BasicRequestHandler
from grid.square import GridSquare
from grid.triangle import GridTriangle
from grid.iso_triangle import GridIsoTriangle
from grid.hex import GridHex
from grid.triangles4 import GridTriangles4

from graphics.svg import SvgImageWriter

import tags
import common
import cache
import dao
import convert
import cs

import zlib

from cloudstorage.errors import NotFoundError

from google.appengine.api import users

grids={
       'square': GridSquare,
       'triangle': GridTriangle,
       'iso-triangle': GridIsoTriangle,
       'hex': GridHex,
       'triangles4': GridTriangles4
       }

class ActionSaveImage(BasicRequestHandler):
    def post(self):
        if not self.user_info.user:
            self.response.set_status(403)
            return            
        
        artwork_json=self.request.get('artwork_json')
        artwork_id=self.request.get('artwork_id')
        artwork_name=self.request.get('artwork_name')
        artwork_description=self.request.get('artwork_description')
        artwork_tags=self.request.get('artwork_tags')
        artwork_grid_visible=self.request.get('artwork_grid_visible')
        
        
        if artwork_id:
            artwork=dao.get_artwork(artwork_id)
            if not self.user_info.superadmin and artwork.author <> self.user_info.user:
                # should be the same user or superadmin
                self.response.set_status(403)
                return
        else:
            artwork=db.Artwork();
            artwork.author=self.user_info.user
            
        if artwork_name:
            artwork.name=artwork_name
        else:
            artwork.name='Untitled'
            
        
            
        if artwork_description:
            artwork.description=artwork_description
        else:
            artwork.description=''
            
        json_file_content = zlib.compress(artwork_json)
        #artwork.json_compressed = True 
        
        original_tags=artwork_tags.split(',')
        url_tags=[]
        for tag_title in original_tags:
            if len(tag_title)>0:
                db_tag=tags.create_tag_by_title(tag_title);
                url_tags.append(db_tag.url_name)
        
        artwork.tags=url_tags
        
        
        json_obj=json.loads(artwork_json)
                
        ###
        image_width=json_obj['effectiveRect']['width']
        image_height=json_obj['effectiveRect']['height']
        image=Image.new('RGB', 
                        (image_width,image_height),
                        json_obj['backgroundColor'])
        image_draw=ImageDraw.Draw(image)
        
        dx=-json_obj['effectiveRect']['left']
        dy=-json_obj['effectiveRect']['top']
        
        layer=json_obj['layers'][0]
        artwork.grid = layer['grid']
        grid=grids[layer['grid']]();
        grid.cell_size=layer['cellSize']

        if json_obj['version']['major']==1:
            for cell in layer['cells']:
                grid.paintShape(image_draw, cell, dx, dy)
        elif json_obj['version']['major']==2:
            for row in layer['rows']:
                for cell in row['cells']:
                    grid.paintShape2(image_draw, cell[0], row['row'], cell[1], cell[2],dx,dy)
                    
        if artwork.grid=='square' and artwork_grid_visible:
            grid.paintGrid(image_draw, '#000000', -dx, -dy, image_width, image_height, dx, dy)
        
        memory_file = StringIO.StringIO()
        image.save(memory_file, 'png')
        
        #artwork.full_image = memory_file.getvalue()
        artwork.full_image_width = image_width
        artwork.full_image_height = image_height
        
        small_image_size = convert.calc_resize(image_width, 
                                              image_height, 
                                              db.artwork_small_image_width, 
                                              db.artwork_small_image_height)
        small_image = image.resize(small_image_size, Image.ANTIALIAS)
        small_memory_file = StringIO.StringIO()
        small_image.save(small_memory_file, 'png')
        
        #artwork.small_image = small_memory_file.getvalue()
        artwork.small_image_width = small_image_size[0]
        artwork.small_image_height = small_image_size[1]
        
        artwork.date = datetime.datetime.now()
        saved_id = artwork.put()
        
        full_image_file_name = '/images/png/'+str(saved_id.id())+'.png'
        small_image_file_name = '/images/png/'+str(saved_id.id())+'-small.png'
        json_image_file_name = '/images/json/'+str(saved_id.id())+'.json'
        
        cs.create_file(full_image_file_name, 'image/png', memory_file.getvalue())
        cs.create_file(small_image_file_name, 'image/png', small_memory_file.getvalue())
        cs.create_file(json_image_file_name, 'application/octet-stream', json_file_content)
        
        artwork.full_image_file_name = full_image_file_name
        artwork.small_image_file_name = small_image_file_name
        artwork.json_file_name = json_image_file_name
        
        if hasattr(artwork, 'json'):
            delattr(artwork, 'json')
            
        if hasattr(artwork, 'json_compressed'):
            delattr(artwork, 'json_compressed')
            
        if hasattr(artwork, 'full_image'):
            delattr(artwork, 'full_image')
            
        if hasattr(artwork, 'small_image'):
            delattr(artwork, 'small_image')
        
        artwork.put()
                
        cache.delete(cache.MC_MAIN_PAGE_RECENT_IMAGES_KEY)
        cache.delete(cache.MC_MAIN_PAGE_PRODUCTIVE_ARTISTS)
        cache.delete(cache.MC_IMAGE_PREFIX+full_image_file_name)
        cache.delete(cache.MC_IMAGE_PREFIX+small_image_file_name)
        
        if artwork.editor_choice:
            cache.delete(cache.MC_MAIN_PAGE_RECENT_EDITOR_CHOICE)
        
        del image
        del small_image
        memory_file.close()
        small_memory_file.close()
        
        user_profile = dao.get_user_profile(self.user_info.user.email())
        if not user_profile:
            user_profile = db.UserProfile()
            user_profile.email = self.user_info.user.email()
            user_profile.nickname = convert.auto_nickname(self.user_info.user.nickname())
            user_profile.artworks_count = 1
            dao.add_user_profile(user_profile)
        else:
            if not artwork_id and hasattr(user_profile,'artworks_count'):
                user_profile.artworks_count = user_profile.artworks_count+1
                dao.set_user_profile(user_profile)
        
        
        self.redirect('/images/details/'+str(saved_id.id()))
        
class ActionDeleteImage(BasicRequestHandler):
    def get(self):
        artwork_id=self.request.get('id')
        artwork=dao.get_artwork(artwork_id)
        if self.user_info.superadmin or artwork.author==self.user_info.user:
            comments=db.Comment.all().filter('artwork_ref =', artwork)
            for comment in comments:
                comment.delete()
                
            favorite_counts = db.FavoriteCounter.all().filter('artwork =', artwork)
            for fc in favorite_counts:
                fc.delete()
                
            favorites = db.Favorite.all().filter('artwork =', artwork)
            for f in favorites:
                f.delete()
                
            cs.delete_file(artwork.full_image_file_name)
            cs.delete_file(artwork.small_image_file_name)
            if hasattr(artwork,'json_file_name'):
                cs.delete_file(artwork.json_file_name)
                
            user_profile = dao.get_user_profile(artwork.author.email())
            if hasattr(user_profile, 'artworks_count'):
                user_profile.artworks_count = user_profile.artworks_count - 1
                dao.set_user_profile(user_profile)
                
            artwork.delete();
            
            cache.delete(cache.MC_MAIN_PAGE_RECENT_IMAGES_KEY)
            cache.delete(cache.MC_MAIN_PAGE_RECENT_EDITOR_CHOICE)
            cache.delete(cache.MC_MAIN_PAGE_RECENT_COMMENTS)
            cache.delete(cache.MC_MAIN_PAGE_TOP_FAVORITES)
            cache.delete(cache.MC_MAIN_PAGE_PRODUCTIVE_ARTISTS)

            self.redirect("/my-images")
        else:
            self.response.set_status(403)
            
class ActionDeleteNotification(BasicRequestHandler):
    def get(self):
        notification_id = self.request.get('id')
        notification = db.Notification.get(notification_id)
        if notification.recipient == self.user_info.user:
            dao.delete_notification(notification)
        else:
            self.response.set_status(403)
            
class ActionSaveComment(BasicRequestHandler):
    def post(self):
        if not self.user_info.user:
            self.response.set_status(403)
            return
        
        artwork_id=self.request.get('artwork_id')
        comment_text=self.request.get('comment_text').strip();
        
        if not comment_text or len(comment_text)==0 or len(comment_text)>1000:
            self.redirect('/images/details/'+artwork_id)
            return
        
        artwork=dao.get_artwork(artwork_id)
        if not artwork:
            self.response.set_status(404)
            return
        
        comment=db.Comment(parent=artwork)
        comment.artwork_ref=artwork
        comment.text=comment_text
        comment.put()
        
        if artwork.author and artwork.author<>self.user_info.user:
            notification = db.Notification()
            notification.recipient = artwork.author
            notification.type = 'comment'
            notification.artwork = artwork
            notification.comment = comment
            notification.sender = self.user_info.user
            dao.add_notification(notification)
            
        cache.delete(cache.MC_MAIN_PAGE_RECENT_COMMENTS)
        
        self.redirect('/images/details/'+artwork_id)
        
class ActionDeleteComment(BasicRequestHandler):
    def get(self):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return
        
        comment_id=self.request.get('id')
        
        comment=db.Comment.get(comment_id)
        
        if comment:
            artwork=comment.artwork_ref
            comment.delete()
            cache.delete(cache.MC_MAIN_PAGE_RECENT_COMMENTS)
            self.redirect('/images/details/'+str(artwork.key().id()))
        else:
            self.response.set_status(404)
            return
        
class PNGImageRequest(BasicRequestHandler):
    def get(self, *ar):
        image_name=ar[0]
        file_name = '/images/png/'+image_name
        cache_key = cache.MC_IMAGE_PREFIX+file_name
        
        file_content = cache.get(cache_key)
        if not file_content:
            try:
                file_content = cs.read_file(file_name)
            except NotFoundError:
                self.response.set_status(404)
                return
                
            if len(file_content)<50000:
                cache.add(cache_key, file_content)
        
        self.response.headers['Content-Type']='image/png'     
        self.response.out.write(file_content)        
        
class SVGImageRequest(BasicRequestHandler):
    def get(self, *ar):
        artwork_id=ar[0]
        
        artwork=dao.get_artwork(artwork_id)        
        if not artwork:
            self.response.set_status(404)
            return
        
        self.response.headers['Content-Type']='image/svg'
        
        if hasattr(artwork, 'json'):
            if artwork.json_compressed:
                artwork_json = zlib.decompress(artwork.json.encode('ISO-8859-1'))
            else:
                artwork_json = artwork.json
        else:
            artwork_json = zlib.decompress(cs.read_file(artwork.json_file_name))
                    
        
        json_obj=json.loads(artwork_json)
        
        image_width=json_obj['effectiveRect']['width']
        image_height=json_obj['effectiveRect']['height']
        image=SvgImageWriter(self.response.out)
        
        image.startImage(image_width, image_height)
        image.rectangle((0,0,image_width,image_height), fill=json_obj['backgroundColor'])
        
        dx=-json_obj['effectiveRect']['left']
        dy=-json_obj['effectiveRect']['top']
        
        layer=json_obj['layers'][0]
        grid=grids[layer['grid']]()
        grid.cell_size=layer['cellSize']
        
        if json_obj['version']['major']==1:
            for cell in layer['cells']:
                grid.paintShape(image, cell, dx, dy)
        elif json_obj['version']['major']==2:
            for row in layer['rows']:
                for cell in row['cells']:
                    grid.paintShape2(image, cell[0], row['row'], cell[1], cell[2],dx,dy)
            
        image.endImage()
        
class JSONImageRequest(BasicRequestHandler):
    def get(self, *ar):
        artwork_id=ar[0]
        
        artwork=dao.get_artwork(artwork_id)        
        if not artwork:
            self.response.set_status(404)
            return
        
        self.response.headers['Content-Type']='text/json'
        
        if hasattr(artwork, 'json'):
            if artwork.json_compressed:
                artwork_json = zlib.decompress(artwork.json.encode('ISO-8859-1'))
            else:
                artwork_json = artwork.json
        else:
            artwork_json = zlib.decompress(cs.read_file(artwork.json_file_name))
        
        self.response.out.write(artwork_json)
        
        
class ActionTagTypeahead(BasicRequestHandler):
    def get(self):
        self._tag_typeahead()
    
    def post(self):
        self._tag_typeahead()
    
    def _tag_typeahead(self):
        query=self.request.get('query').lower()
        tags=db.Tag.all().filter('title_lower >=', query).filter('title_lower <', query+u'\ufffd').order('title_lower')
        tag_titles=[t.title for t in tags]
        self.response.out.write(json.dumps(tag_titles))
        
class ActionSaveSettings(BasicRequestHandler):
    def post(self):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return            
        
        settings=common.get_settings()
        
        if self.request.get('show_ads'):
            settings.show_ads=True
        else:
            settings.show_ads=False
            
        if self.request.get('show_analytics'):
            settings.show_analytics=True
        else:
            settings.show_analytics=False
            
        common.save_settings(settings)
        
        self.redirect('/admin')
        
class ActionSaveProfile(BasicRequestHandler):
    def post(self):
        if not self.user_info.user:
            self.response.set_status(403)
            return
        
        nickname = self.request.get('nickname')
        if not nickname:
            self.response.set_status(400)
            return

        user_profile = dao.get_user_profile(self.user_info.user.email())
        if user_profile:
            user_profile.nickname = nickname
            dao.set_user_profile(user_profile)
        else:
            user_profile = db.UserProfile()
            user_profile.email = self.user_info.user.email()
            user_profile.nickname = nickname
            user_profile.artworks_count = 0
            dao.add_user_profile(user_profile)
            
        self.redirect('/')
        

class ActionUpdate2(BasicRequestHandler):
    def get(self):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return

        favorites = db.Favorite.all()
        for f in favorites:
            try:
                value = f.artwork.name
            except:
                f.delete()
                
        counts = db.FavoriteCounter.all()
        for c in counts:
            try:
                value = c.artwork.name
            except:
                c.delete()
                


class ActionUpdate(BasicRequestHandler):
    def get(self):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return
        
        year1 = int(self.request.get('year1'))
        month1 = int(self.request.get('month1'))
        day1 = int(self.request.get('day1'))
        year2 = int(self.request.get('year2'))
        month2 = int(self.request.get('month2'))
        day2 = int(self.request.get('day2'))
        
        date1 = datetime.datetime(year=year1, month=month1, day=day1)
        
        date2 = datetime.datetime(year=year2, month=month2, day=day2)
        
        all_users = db.UserProfile.all().filter('join_date >=', date1).filter('join_date <=', date2).fetch(1000,0)
        total_count = 0
        updated_count = 0
        skipped_count = 0
        
        for u in all_users:
            total_count = total_count+1
            if not hasattr(u, 'artworks_count'):
                uu = users.User(str(u.email))
                count = db.Artwork.all().filter('author =', uu).count()
                u.artworks_count = count
                u.put()
                updated_count = updated_count + 1
            else:
                skipped_count = skipped_count + 1
                    
                
        
        self.response.write('<html><body>')
        self.response.write('total_count = '+str(total_count)+'<br>')
        self.response.write('updated_count = '+str(updated_count)+'<br>')
        self.response.write('skipped_count = '+str(skipped_count)+'<br>')
        self.response.write('</body></html>')
        
                

class ActionUpdateArtworkIterate(BasicRequestHandler):
    def get(self):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return

        offset = int(self.request.get('offset'))
        limit = 20
        
        artworks = db.Artwork.all().order('-date').fetch(limit, offset)
        

    
        for a in artworks:
            filename = '/images/png/'+str(a.key().id())+'.png'
            a.full_image_file_name = filename
            cs.create_file(filename, 'image/png', a.full_image)
            
            filename_small = '/images/png/'+str(a.key().id())+'-small.png'
            a.small_image_file_name = filename_small
            cs.create_file(filename_small, 'image/png', a.small_image)
            
            a.put()
            
            
        
        self.response.headers['Content-Type']='text/plain'
        
        if len(artworks) == limit:
            self.response.out.write(str(offset+limit))
        else:
            self.response.out.write('end')


                
class ActionAdminSetArtworkProperties(BasicRequestHandler):
    def post(self):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return
        
        artwork_id = int(self.request.get('admin_artwork_id'))
        artwork_name = self.request.get('admin_artwork_name')
        artwork_description = self.request.get('admin_artwork_description')
        artwork_tags = self.request.get('admin_artwork_tags')
        artwork_editor_choice = self.request.get('admin_artwork_editor_choice')
        
        artwork = db.Artwork.get_by_id(artwork_id)
        artwork.name = artwork_name
        artwork.description = artwork_description
        if artwork_editor_choice:
            artwork.editor_choice = True
        else:
            artwork.editor_choice = False
        
        original_tags=artwork_tags.split(',')
        url_tags=[]
        for tag_title in original_tags:
            if len(tag_title)>0:
                db_tag=tags.create_tag_by_title(tag_title);
                url_tags.append(db_tag.url_name)
        
        artwork.tags=url_tags
        
        artwork.put()
        
        cache.delete(cache.MC_MAIN_PAGE_RECENT_EDITOR_CHOICE)
        cache.delete(cache.MC_MAIN_PAGE_RECENT_IMAGES_KEY)
        
        self.redirect('/images/details/'+str(artwork_id))
            
            
class ActionToggleFavorite(BasicRequestHandler):            
    def get(self):
        if not self.user_info.user:
            self.response.set_status(403)
            return
        else:
            artwork_id = int(self.request.get('id'))
            artwork = db.Artwork.get_by_id(artwork_id)
            
            if not artwork:
                self.response.set_status(404)
                return
            else:
                cache.delete(cache.MC_MAIN_PAGE_TOP_FAVORITES)
                if dao.is_artwork_favorite_by_user(artwork, self.user_info.user):
                    fav_count = dao.unfavorite_artwork(artwork, self.user_info.user)
                    self.response.out.write(json.dumps({
                            'favorite': False,
                            'favorite_count': fav_count 
                            }))
                else:
                    fav_count = dao.favorite_artwork(artwork, self.user_info.user)
                    
                    notification = db.Notification()
                    notification.recipient = artwork.author
                    notification.type = 'favorite'
                    notification.artwork = artwork
                    notification.sender = self.user_info.user
                    dao.add_notification(notification)
            
                    self.response.out.write(json.dumps({
                            'favorite': True,
                            'favorite_count': fav_count 
                            }))
                    
                cache.delete(cache.MC_MAIN_PAGE_RECENT_FAVORITES)
            