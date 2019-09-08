# -*- coding: utf-8 -*-
'''
Created on 23.07.2013

@author: Vlad
'''

import db
import json
import datetime
import StringIO
import re

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
from google.appengine.api import taskqueue

import logging
import antispam
from const import NEWS_TYPE_CHANGE_ARTWORK, NEWS_TYPE_NEW_ARTWORK

from bad_language import hide_bad_language

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
        
        if self.user_info.read_only:
            self.response.set_status(403)
            return
        
        artwork_json=self.request.get('artwork_json')
        artwork_id=self.request.get('artwork_id')
        artwork_name=self.request.get('artwork_name')
        artwork_description=self.request.get('artwork_description')
        artwork_tags=self.request.get('artwork_tags')
        
        
        if artwork_id:
            news_type = NEWS_TYPE_CHANGE_ARTWORK
            artwork=dao.get_artwork(artwork_id)
            if not self.user_info.superadmin and artwork.author_email <> self.user_info.user_email:
                # should be the same user or superadmin
                self.response.set_status(403)
                return
        else:
            news_type = NEWS_TYPE_NEW_ARTWORK
            artwork=db.Artwork()
            artwork.author_email = self.user_info.user_email
            
        if artwork_name:
            artwork.name=hide_bad_language(artwork_name)
        else:
            artwork.name='Untitled'

        if artwork_description:
            artwork.description=hide_bad_language(artwork_description)
        else:
            artwork.description=''
            
        json_file_content = zlib.compress(artwork_json)
        #artwork.json_compressed = True 

        artwork_url_tags = getattr(artwork, 'tags', [])

        request_tags=artwork_tags.split(',')
        request_url_tags = [tags.tag_url_name(t) for t in request_tags]

        tags_to_add = set(request_url_tags) - set(artwork_url_tags)
        tags_to_delete = set(artwork_url_tags) - set(artwork_url_tags)

        url_tags = []
        for tag_title in request_tags:
            url_name = tags.tag_url_name(tag_title)
            if url_name in tags_to_add:
                db_tag = tags.create_tag_by_title(tag_title)
                if db_tag:
                    url_tags.append(db_tag.url_name)
            elif url_name in tags_to_delete:
                pass
            else:
                url_tags.append(url_name)
        
        artwork.tags=url_tags
        
        json_obj=json.loads(artwork_json)

        layer=json_obj['layers'][0]
        artwork.grid = layer['grid']
        grid=grids[layer['grid']]()
        grid.cell_size=layer['cellSize']
        
        if json_obj['transparentBackground']:
            background_color = (0, 0, 0, 0)
        else:
            background_color = json_obj['backgroundColor']
        
        # Create normal image
        image_width=json_obj['effectiveRect']['width']
        image_height=json_obj['effectiveRect']['height']
        image=Image.new('RGBA', 
                        (image_width,image_height),
                        background_color)
        image_draw=ImageDraw.Draw(image)
        
        dx=-json_obj['effectiveRect']['left']
        dy=-json_obj['effectiveRect']['top']

        if json_obj['version']['major']==1:
            for cell in layer['cells']:
                grid.paintShape(image_draw, cell, dx, dy)
        elif json_obj['version']['major']==2:
            for row in layer['rows']:
                for cell in row['cells']:
                    grid.paintShape2(image_draw, cell[0], row['row'], cell[1], cell[2],dx,dy)
                    
        if artwork.grid=='square' and json_obj['gridVisible']:
            grid.paintGrid(image_draw, '#000000', -dx, -dy, image_width, image_height, dx, dy)
        
        memory_file = StringIO.StringIO()
        image.save(memory_file, 'png')
        
        # Create pixel image
        pixel_memory_file = None
        if artwork.grid=='square' and json_obj['additionalPixelImage']:
            pixel_image_width=json_obj['effectivePixelArtRect']['width']
            pixel_image_height=json_obj['effectivePixelArtRect']['height']
            pixel_image=Image.new('RGBA', 
                                  (pixel_image_width, pixel_image_height),
                                  background_color)
            pixel_image_draw=ImageDraw.Draw(pixel_image)
                        
            p_dx=-json_obj['effectivePixelArtRect']['left']
            p_dy=-json_obj['effectivePixelArtRect']['top']
    
            if json_obj['version']['major']==1:
                for cell in layer['cells']:
                    grid.paintPoint(pixel_image_draw, cell['col'], cell['row'], cell['color'], p_dx, p_dy)
            elif json_obj['version']['major']==2:
                for row in layer['rows']:
                    for cell in row['cells']:
                        grid.paintPoint(pixel_image_draw, cell[0], row['row'], cell[2], p_dx, p_dy)
                        
            pixel_memory_file = StringIO.StringIO()
            pixel_image.save(pixel_memory_file, 'png')

        # Create thumbnail image
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
        
        if self.user_info.user_email == artwork.author_email:
            artwork.date = datetime.datetime.now()
            
        saved_id = artwork.put()
        
        full_image_file_name = '/images/png/'+str(saved_id.id())+'.png'
        small_image_file_name = '/images/png/'+str(saved_id.id())+'-small.png'
        json_image_file_name = '/images/json/'+str(saved_id.id())+'.json'
        pixel_image_file_name = '/images/png/'+str(saved_id.id())+'-pixel.png'
        
        cs.create_file(full_image_file_name, 'image/png', memory_file.getvalue())
        cs.create_file(small_image_file_name, 'image/png', small_memory_file.getvalue())
        cs.create_file(json_image_file_name, 'application/octet-stream', json_file_content)
        if pixel_memory_file:
            cs.create_file(pixel_image_file_name, 'image/png', pixel_memory_file.getvalue())
        
        artwork.full_image_file_name = full_image_file_name
        artwork.small_image_file_name = small_image_file_name
        artwork.json_file_name = json_image_file_name
        
        if pixel_memory_file:
            artwork.pixel_image_file_name = pixel_image_file_name
            artwork.pixel_image_width = pixel_image_width
            artwork.pixel_image_height = pixel_image_height
        else:
            if hasattr(artwork, 'pixel_image_file_name'):
                del artwork.pixel_image_file_name
            if hasattr(artwork, 'pixel_image_width'):
                del artwork.pixel_image_width
            if hasattr(artwork, 'pixel_image_height'):
                del artwork.pixel_image_height
            cs.delete_file(pixel_image_file_name)
        
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
        cache.delete(cache.MC_IMAGE_PREFIX+pixel_image_file_name)
        
        if artwork.editor_choice:
            cache.delete(cache.MC_MAIN_PAGE_RECENT_EDITOR_CHOICE)
        
        del image
        del small_image
        memory_file.close()
        small_memory_file.close()
        
        if pixel_memory_file:
            del pixel_image
            pixel_memory_file.close()
        
        user_profile = dao.get_user_profile(self.user_info.user_email)
        if not user_profile:
            user_profile = db.UserProfile()
            user_profile.email = self.user_info.user_email
            user_profile.nickname = convert.auto_nickname(self.user_info.user.nickname())
            user_profile.artworks_count = 1
            dao.add_user_profile(user_profile)
        else:
            if not artwork_id:
                user_profile.artworks_count = user_profile.artworks_count+1
                dao.set_user_profile(user_profile)
                
        taskqueue.add(
            url='/tasks/add-artwork-to-news',
            params={
                'artwork_id': saved_id.id(),
                'type': news_type
            })

        self.response.out.write(json.dumps({
            'result': saved_id.id(),
        }))


class ActionDeleteImage(BasicRequestHandler):
    def get(self):
        artwork_id=self.request.get('id')
        artwork=dao.get_artwork(artwork_id)
        if artwork is None:
            self.response.set_status(404)
            return
        
        if self.user_info.superadmin or artwork.author_email==self.user_info.user_email:
            if self.user_info.read_only:
                self.response.set_status(403)
                return            
            
            comments=db.Comment.all().filter('artwork_ref =', artwork)
            for comment in comments:
                comment.delete()
                
            favorite_counts = db.FavoriteCounter.all().filter('artwork =', artwork)
            decrease_count = 0
            for fc in favorite_counts:
                decrease_count += fc.count
                fc.delete()
                
            favorites = db.Favorite.all().filter('artwork =', artwork)
            for f in favorites:
                f.delete()
                
            news_items = db.NewsFeed.all().filter('artwork =', artwork)
            for ni in news_items:
                ni.delete()
                
            cs.delete_file(artwork.full_image_file_name)
            cs.delete_file(artwork.small_image_file_name)
            if hasattr(artwork,'json_file_name'):
                cs.delete_file(artwork.json_file_name)
                
            if hasattr(artwork, 'pixel_image_file_name'):
                cs.delete_file(artwork.pixel_image_file_name)
                                
            user_profile = dao.get_user_profile(artwork.author_email)
            user_profile.artworks_count = user_profile.artworks_count - 1
            user_profile.favorite_count = user_profile.favorite_count - decrease_count
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
        if notification is not None:
            if notification.recipient_email == self.user_info.user_email:
                dao.delete_notification(notification)
            else:
                self.response.set_status(403)

                
class ActionDeleteAllNotifications(BasicRequestHandler):
    def get(self):
        if not self.user_info.user:
            self.response.set_status(403)
            return

        user_email = self.user_info.user_email
        dao.delete_all_notifications(user_email)

                
class ActionComlainComment(BasicRequestHandler):
    def get(self):
        if not self.user_info.user:
            self.response.set_status(403)
            return
        
        if self.user_info.read_only:
            self.response.set_status(403)
            return

        artwork_id = self.request.get('artwork_id')
        comment_id = self.request.get('comment_id')
        
        cache_key = 'comment-complain-'+comment_id
        if cache.get(cache_key):
            self.response.set_status(200)
            return
        
        user_profile = dao.get_user_profile(self.user_info.user_email)
        if not user_profile:
            user_profile = db.UserProfile()
            user_profile.email = self.user_info.user_email
            user_profile.nickname = convert.auto_nickname(self.user_info.user.nickname())
            user_profile.artworks_count = 0
            dao.add_user_profile(user_profile)
            
        settings = self.settings
        
        artwork = dao.get_artwork(int(artwork_id))
        comment = db.Comment.get_by_id(long(comment_id), artwork.key())
        logging.error('comment = {}'.format(comment))
            
        notification = db.Notification()
        notification.recipient_email = settings.admin_email
        notification.type = 'complain'
        notification.artwork = artwork
        notification.comment = comment
        notification.sender_email = self.user_info.user_email
        dao.add_notification(notification)
        
        cache.add(cache_key, user_profile.email)
        
        self.response.set_status(200)
        
            
class ActionSaveComment(BasicRequestHandler):
    def post(self):
        if not self.user_info.user:
            self.response.set_status(403)
            return
        
        if self.user_info.read_only:
            self.response.set_status(403)
            return
        
        user_profile = dao.get_user_profile(self.user_info.user_email)
        if not user_profile:
            user_profile = db.UserProfile()
            user_profile.email = self.user_info.user_email
            user_profile.nickname = convert.auto_nickname(self.user_info.user.nickname())
            user_profile.artworks_count = 0
            dao.add_user_profile(user_profile)
        
        artwork_id = self.request.get('artwork_id')
        comment_text = self.request.get('comment_text').strip();
        ref_comment_id = self.request.get('ref_comment_id')
        
        if not antispam.check_comment(user_profile.email, artwork_id, comment_text):
            self.redirect('/images/details/'+artwork_id)
            return
        
        if not comment_text or len(comment_text)==0 or len(comment_text)>1000:
            self.redirect('/images/details/'+artwork_id)
            return
        
        artwork=dao.get_artwork(artwork_id)
        if not artwork:
            self.response.set_status(404)
            return
        
        comment=db.Comment(parent=artwork)
        comment.author_email = self.user_info.user_email
        comment.artwork_ref = artwork
        comment.text = hide_bad_language(comment_text)
        comment.put()
        
        if artwork.author_email and artwork.author_email<>self.user_info.user_email:
            notification = db.Notification()
            notification.recipient_email = artwork.author_email
            notification.type = 'comment'
            notification.artwork = artwork
            notification.comment = comment
            notification.sender_email = self.user_info.user_email
            dao.add_notification(notification)
            
        if ref_comment_id:
            ref_comment = db.Comment.get_by_id(int(ref_comment_id), artwork)
            if ref_comment and ref_comment.author_email <> artwork.author_email and ref_comment.author_email <> self.user_info.user_email:
                ref_notification = db.Notification()
                ref_notification.recipient_email = ref_comment.author_email
                ref_notification.type = 'comment'
                ref_notification.artwork = artwork
                ref_notification.comment = comment
                ref_notification.sender_email = self.user_info.user_email
                dao.add_notification(ref_notification)
                
            
        cache.delete(cache.MC_MAIN_PAGE_RECENT_COMMENTS)
        
        self.redirect('/images/details/'+artwork_id)
        
class ActionDeleteComment(BasicRequestHandler):
    def get(self):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return
        
        comment_id = self.request.get('id')
        parent_id = self.request.get('parent_id')
        
        artwork = dao.get_artwork(parent_id)
        if not artwork:
            self.response.set_status(404)
            return
        
        comment=db.Comment.get_by_id(long(comment_id), artwork.key())
        
        if comment:
            artwork=comment.artwork_ref
            comment.delete()
            cache.delete(cache.MC_MAIN_PAGE_RECENT_COMMENTS)
            self.response.out.write(json.dumps('OK'))
        else:
            self.response.set_status(404)
            return
        
class ActionHideComment(BasicRequestHandler):
    def get(self):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return
        
        comment_id = self.request.get('id')
        parent_id = self.request.get('parent_id')
        
        artwork = dao.get_artwork(parent_id)
        if not artwork:
            self.response.set_status(404)
            return
        
        comment=db.Comment.get_by_id(long(comment_id), artwork.key())
        if comment:
            comment.hidden = True
            comment.put()
            cache.delete(cache.MC_MAIN_PAGE_RECENT_COMMENTS)
            self.response.write(json.dumps('OK'))
        else:
            self.response.write(json.dumps('404'))
            
class ActionShowComment(BasicRequestHandler):
    def get(self):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return
        
        comment_id = self.request.get('id')
        parent_id = self.request.get('parent_id')
        
        artwork = dao.get_artwork(parent_id)
        if not artwork:
            self.response.set_status(404)
            return
        
        comment=db.Comment.get_by_id(long(comment_id), artwork.key())
        if comment:
            if hasattr(comment, 'hidden'):
                del comment.hidden
                comment.put()

            cache.delete(cache.MC_MAIN_PAGE_RECENT_COMMENTS)
            self.response.write(json.dumps('OK'))
        else:
            self.response.write(json.dumps('404'))

        
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
            
        settings.admin_email= self.request.get('admin_email')
            
        common.save_settings(settings)
        cache.add(cache.MC_SETTINGS, settings)
        
        self.redirect('/admin')
        
class JSONSaveProfile(BasicRequestHandler):
    def post(self):
        if not self.user_info.user:
            self.response.set_status(403)
            return
        
        if self.user_info.read_only:
            self.response.set_status(403)
            return
        
        nickname = self.request.get('nickname')
        if not nickname:
            self.response.set_status(400)
            return
        
        nickname = hide_bad_language(nickname)

        user_profile = dao.get_user_profile(self.user_info.user_email)
        if user_profile:
            if user_profile.nickname != nickname:
                if dao.get_user_profile_by_nickname(nickname):
                    self.response.set_status(400)
                    return
                else:
                    user_profile.nickname = nickname
                    dao.set_user_profile(user_profile)
        else:
            if dao.get_user_profile_by_nickname(nickname):
                self.response.set_status(400)
                return
            else:
                user_profile = db.UserProfile()
                user_profile.email = self.user_info.user.email()
                user_profile.nickname = nickname
                user_profile.artworks_count = 0
                dao.add_user_profile(user_profile)

        cache.delete(cache.MC_MAIN_PAGE_PRODUCTIVE_ARTISTS)
        cache.delete(cache.MC_MAIN_PAGE_TOP_RATED_ARTISTS)
            
        self.response.out.write(json.dumps({'result': 'ok'}))
                

class ActionUpdateIterate(BasicRequestHandler):
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
        
        limit = int(self.request.get('limit'))
        offset = int(self.request.get('offset'))
        
        date1 = datetime.datetime(year=year1, month=month1, day=day1)
        
        date2 = datetime.datetime(year=year2, month=month2, day=day2)
        
        all_items = db.Artwork.all().filter('date >=', date1).filter('date <=', date2).fetch(limit,offset)
        total_count = 0
        updated_count = 0
        skipped_count = 0
        error_count = 0
        
        for a in all_items:
            try:
                total_count = total_count+1
                
                if hasattr(a,'author'):
                    del a.author
                    
                    a.put()
                    updated_count = updated_count +1
                else:
                    skipped_count = skipped_count + 1
#                     
            except:
                logging.exception('Iterate error')
                error_count = error_count + 1
                
        result = {
                  'total_count': total_count,
                  'updated_count': updated_count,
                  'skipped_count': skipped_count,
                  'error_count': error_count,
                  'all_done': total_count<limit
                  }
        self.response.write(json.dumps(result))
        
class ActionUpdateEditorChoice(BasicRequestHandler):
    def get(self):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return

        artworks = db.Artwork.all().filter('editor_choice =', True).order('-date')
        for a in artworks:
            a.editor_choice_date = a.date
            a.put()
            
        self.response.write("OK")

                
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
        artwork_copyright_block = self.request.get('admin_artwork_copyright_block')
        artwork_block = self.request.get('admin_artwork_block')
        artwork_block_reason = self.request.get('admin_artwork_block_reason')
        
        artwork = db.Artwork.get_by_id(artwork_id)
        artwork.name = artwork_name
        artwork.description = artwork_description
        if artwork_editor_choice:
            artwork.editor_choice = True
            artwork.editor_choice_date = datetime.datetime.now()
        else:
            artwork.editor_choice = False
            artwork.editor_choice_date = None
        
        original_tags=artwork_tags.split(',')
        url_tags=[]
        for tag_title in original_tags:
            if len(tag_title)>0:
                db_tag=tags.create_tag_by_title(tag_title);
                url_tags.append(db_tag.url_name)
        
        artwork.tags=url_tags
        
        if artwork_copyright_block:
            artwork.copyright_block = True
        else:
            if hasattr(artwork, 'copyright_block'):
                del artwork.copyright_block
                
        if artwork_block:
            artwork.block = True
            artwork.block_reason = artwork_block_reason
        else:
            if hasattr(artwork, 'block'):
                del artwork.block
            if hasattr(artwork, 'block_reason'):
                del artwork.block_reason
        
        artwork.put()
        
        cache.delete(cache.MC_MAIN_PAGE_RECENT_EDITOR_CHOICE)
        cache.delete(cache.MC_MAIN_PAGE_RECENT_IMAGES_KEY)
        
        self.redirect('/images/details/'+str(artwork_id))
        
class ActionAdminUpdateUserFavoritesCount(BasicRequestHandler):
    def get(self):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return
        
        try:
            profile_id = int(self.request.get('profile_id'))
            user_profile = dao.get_user_profile_by_id(profile_id)
            user_email = user_profile.email
            
            artworks = db.Artwork.all().filter('author_email =', user_email).order('-date')
            count = 0
            for a in artworks:
                count += dao.get_artwork_favorite_count(a)
                
            user_profile.favorite_count = count
            dao.set_user_profile(user_profile)
            
            self.response.out.write(json.dumps({
                                'count': count 
                                }))
        except Exception as e:
            logging.exception('Error updating favorites count')
            self.response.out.write(json.dumps({
                                'error': '{}'.format(e) 
                                }))
            
class ActionAdminUpdateArtworkFavoriteCount(BasicRequestHandler):
    def get(self):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return
        
        try:
            artwork_id = int(self.request.get('artwork_id'))
            artwork = dao.get_artwork(artwork_id)
            count = db.Favorite.all().filter('artwork', artwork).count()
            
            favorite_counter = db.FavoriteCounter.all().filter('artwork', artwork).get()
            favorite_counter.count = count
            favorite_counter.put()
            
            self.response.out.write(json.dumps({
                                'count': count 
                                }))
        except Exception as e:
            logging.exception('Error updating favorites count for artwork')
            self.response.out.write(json.dumps({
                                'error': '{}'.format(e) 
                                }))
            
            
class ActionToggleFavorite(BasicRequestHandler):            
    def get(self):
        if not self.user_info.user:
            self.response.set_status(403)
            return
        
        if self.user_info.read_only:
            self.response.set_status(403)
            return
        
        artwork_id = int(self.request.get('id'))
        artwork = db.Artwork.get_by_id(artwork_id)
        
        if not artwork:
            self.response.set_status(404)
            return
        else:
            antispam_key = cache.MC_ANTISPAM_FAVORITE_USER_ARTWORK + self.user_info.user_email + '_' + str(artwork_id)
            last_fav_time = cache.get(antispam_key)
            if last_fav_time and datetime.datetime.now() - last_fav_time < datetime.timedelta(seconds=60):
                self.response.out.write(json.dumps({
                    'not_changed': True
                    }))
                return
            else:
                cache.add(antispam_key, datetime.datetime.now())

            if artwork.author_email == self.user_info.user_email:
                # Do not allow to favorite artworks by author himself
                self.response.out.write(json.dumps({
                    'not_allowed_for_author': True
                    }))
                return

            cache.delete(cache.MC_MAIN_PAGE_TOP_FAVORITES)
            if dao.is_artwork_favorite_by_user(artwork, self.user_info.user_email):
                fav_count = dao.unfavorite_artwork(artwork, self.user_info.user_email)
                self.response.out.write(json.dumps({
                        'favorite': False,
                        'favorite_count': fav_count 
                        }))
            else:
                fav_count = dao.favorite_artwork(artwork, self.user_info.user_email)
                
                if antispam.check_favorite(self.user_info.user_email, artwork_id):
                    notification = db.Notification()
                    notification.recipient_email = artwork.author_email
                    notification.type = 'favorite'
                    notification.artwork = artwork
                    notification.sender_email = self.user_info.user_email
                    dao.add_notification(notification)
        
                self.response.out.write(json.dumps({
                        'favorite': True,
                        'favorite_count': fav_count 
                        }))
                
            cache.delete(cache.MC_MAIN_PAGE_RECENT_FAVORITES)
            cache.delete(cache.MC_MAIN_PAGE_TOP_RATED_ARTISTS)
            cache.delete(cache.MC_USER_PROFILE+artwork.author_email)
                
class JSONComments(BasicRequestHandler):
    def get(self):
        limit = 11
        offset = 0
        
        if (self.request.get('limit')):        
            limit = int(self.request.get('limit'))
            
        if (limit > 101):
            limit = 101
            
        if (self.request.get('offset')):
            offset = int(self.request.get('offset'))
        
        def json_serial(obj):
            if isinstance(obj, datetime.datetime):
                serial = obj.isoformat()
                return serial
            raise TypeError ("Type not serializable {}", repr(obj))
        
        comments = db.Comment.all()
        str_profile_id = self.request.get('profile_id')
        if str_profile_id:
            profile_id = int(str_profile_id)
            user_profile = dao.get_user_profile_by_id(profile_id)
            comments = comments.filter('author_email =', user_profile.email)
        
        comments = comments.order('-date').run(limit=limit, offset=offset)
        dict_comments = [convert.convert_comment_for_page_rich(c) for c in comments]
        
        self.response.out.write(json.dumps(dict_comments, default=json_serial))
        
class JSONNotifications(BasicRequestHandler):
    def get(self):
        if not self.user_info.user:
            self.response.set_status(403)
            return
        
        req_limit = self.request.get('limit')
        req_offset = self.request.get('offset')
        
        if req_offset:
            offset = int(req_offset)
        else:
            offset = 0
            
        if req_limit:
            limit = int(req_limit)
        else:
            limit = 21
            
        if limit > 101:
            limit = 101
            
        query = db.Notification.all().filter('recipient_email =', self.user_info.user_email).order('-date').fetch(limit,offset)
        
        def json_serial(obj):
            if isinstance(obj, datetime.datetime):
                serial = obj.isoformat()
                return serial
            raise TypeError ("Type not serializable {}", repr(obj))
        
        notifications = [convert.convert_notification_json(n) for n in query]
        self.response.out.write(json.dumps(notifications, default=json_serial))

        
class JSONGetUserIdByNickname(BasicRequestHandler):
    def post(self, *args):
        if not self.user_info.user:
            self.response.set_status(403)
            return
 
        nickname = self.request.get('nickname')
        nickname = hide_bad_language(nickname)      
        profile = dao.get_user_profile_by_nickname(nickname)
        if profile:
            self.response.out.write(json.dumps({'id':profile.key().id()}))
        else:
            self.response.out.write(json.dumps({}))
            
        
class ActionAdminBlockUser(BasicRequestHandler):
    def post(self):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return
        
        profile_id = int(self.request.get('profile_id'))
        block_reason = self.request.get('block_reason')
        
        user_profile = dao.get_user_profile_by_id(profile_id);
        user_profile.read_only = True
        user_profile.block_date = datetime.datetime.now()
        user_profile.block_reason = block_reason
        dao.set_user_profile(user_profile)

        self.redirect('/profiles/'+str(profile_id))
        
class ActionAdminUnblockUser(BasicRequestHandler):
    def get(self):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return
        
        profile_id = int(self.request.get('profile_id'))
        
        user_profile = dao.get_user_profile_by_id(profile_id);
        if hasattr(user_profile, 'read_only'):
            del user_profile.read_only
        if hasattr(user_profile, 'block_date'):
            del user_profile.block_date
        if hasattr(user_profile, 'block_reason'):
            del user_profile.block_reason
        dao.set_user_profile(user_profile)

        self.redirect('/profiles/'+str(profile_id))
        
class ActionAdminFlushMemcacheForIndexPage(BasicRequestHandler):
    def get(self):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return
        
        cache.delete(cache.MC_MAIN_PAGE_RECENT_IMAGES_KEY)
        cache.delete(cache.MC_MAIN_PAGE_RECENT_COMMENTS)
        cache.delete(cache.MC_MAIN_PAGE_RECENT_EDITOR_CHOICE)
        cache.delete(cache.MC_MAIN_PAGE_TOP_FAVORITES)
        cache.delete(cache.MC_MAIN_PAGE_RECENT_FAVORITES)
        cache.delete(cache.MC_MAIN_PAGE_PRODUCTIVE_ARTISTS)
        cache.delete(cache.MC_MAIN_PAGE_TOP_RATED_ARTISTS)
        
        self.redirect('/')
        

class JSONSaveAlternativeEmail(BasicRequestHandler):
    def post(self, *args):
        if not self.user_info.user:
            self.response.set_status(403)
            return
 
        alternative_email = self.request.get('alternative_email')
        if not re.match("[^@]+@[^@]+\.[^@]+", alternative_email):
            self.response.out.write(json.dumps({'error': 'invalid_email'}))
            return
        
        user_profile = dao.get_user_profile(self.user_info.user_email)
        if user_profile:
            test_profile = dao.get_user_profile(alternative_email)
            if test_profile:
                self.response.out.write(json.dumps({'error': 'already_used'}))
                return
            
            if hasattr(user_profile, 'alternative_emails'):
                if alternative_email not in user_profile.alternative_emails:
                    user_profile.alternative_emails.append(alternative_email)
            else:
                user_profile.alternative_emails = [alternative_email]
            
            dao.set_user_profile(user_profile)
            self.response.out.write(json.dumps({'result': 'success'}))
        else:
            self.response.set_status(400)
            return
        
        
class JsonDeleteAlternativeEmail(BasicRequestHandler):
    def post(self, *args):
        if not self.user_info.user:
            self.response.set_status(403)
            return
 
        alternative_email = self.request.get('alternative_email')
        
        user_profile = dao.get_user_profile(self.user_info.user_email)
        if user_profile:
            if alternative_email not in getattr(user_profile, 'alternative_emails', []):
                self.response.out.write(json.dumps({'error': 'no_such_alternative_email'}))
                return
            
            if self.user_info.user.email() == alternative_email:
                self.response.out.write(json.dumps({'error': 'cannot_delete_yourself'}))
                return
            
            user_profile.alternative_emails.remove(alternative_email)
            dao.set_user_profile(user_profile)
            self.response.out.write(json.dumps({'result': 'success'}))
        else:
            self.response.set_status(400)
            return
        
        

class ActionFollow(BasicRequestHandler):            
    def get(self):
        if not self.user_info.user:
            self.response.set_status(403)
            return
        
        if self.user_info.read_only:
            self.response.set_status(403)
            return
                
        user_id = int(self.request.get('user_id'))
        user = dao.get_user_profile_by_id(user_id)
        
        if user.email == self.user_info.user_email:
            self.response.out.write(json.dumps('cannot_follow_yourself'))
            return        
        
        antispam_key = cache.MC_ANTISPAM_FOLLOW + user.email + '_' + self.user_info.user_email
        last_follow_time = cache.get(antispam_key)
        if last_follow_time and datetime.datetime.now() - last_follow_time < datetime.timedelta(seconds=60):
            self.response.out.write(json.dumps('not_changed'))
            return
        else:
            cache.add(antispam_key, datetime.datetime.now())
            
        dao.follow(user.email, self.user_info.user_email)
        
        user.followers_count = getattr(user, 'followers_count', 0) + 1;
        user.put()
        
        current_user = dao.get_user_profile_by_id(self.user_info.profile_id)
        current_user.leaders_count = getattr(current_user, 'leaders_count', 0) + 1
        current_user.put()
        
        artworks = db.Artwork.all().filter('author_email =', user.email).order('-date').fetch(3)
        for a in artworks:
            dao.add_to_news_feed(self.user_info.user_email, a, NEWS_TYPE_NEW_ARTWORK, a.date)
        
        notification = db.Notification()
        notification.recipient_email = user.email
        notification.type = 'follow'
        notification.sender_email = self.user_info.user_email
        dao.add_notification(notification)
        
        self.response.out.write(json.dumps('OK'))


class ActionUnfollow(BasicRequestHandler):            
    def get(self):
        if not self.user_info.user:
            self.response.set_status(403)
            return
        
        if self.user_info.read_only:
            self.response.set_status(403)
            return
        
        user_id = int(self.request.get('user_id'))
        user = dao.get_user_profile_by_id(user_id)
        
        if user.email == self.user_info.user_email:
            self.response.out.write(json.dumps('cannot_follow_yourself'))
            return        
        
        antispam_key = cache.MC_ANTISPAM_FOLLOW + user.email + '_' + self.user_info.user_email
        last_follow_time = cache.get(antispam_key)
        if last_follow_time and datetime.datetime.now() - last_follow_time < datetime.timedelta(seconds=60):
            self.response.out.write(json.dumps('not_changed'))
            return
        else:
            cache.add(antispam_key, datetime.datetime.now())
                    
        dao.unfollow(user.email, self.user_info.user_email)
        
        user.followers_count = getattr(user, 'followers_count', 0) - 1;
        user.put()
        
        current_user = dao.get_user_profile_by_id(self.user_info.profile_id)
        current_user.leaders_count = getattr(current_user, 'leaders_count', 0) - 1
        current_user.put()
        
        self.response.out.write(json.dumps('OK'))
            
            
class JSONFollowers(BasicRequestHandler):
    def get(self):
        if not self.user_info.user:
            self.response.set_status(403)
            return
        
        req_limit = self.request.get('limit')
        req_offset = self.request.get('offset')
        
        if req_offset:
            offset = int(req_offset)
        else:
            offset = 0
            
        if req_limit:
            limit = int(req_limit)
        else:
            limit = 21
            
        if limit > 101:
            limit = 101
            
        req_profile_id = int(self.request.get('profile_id'))

        result = []        
        
        user = dao.get_user_profile_by_id(req_profile_id)
        if user:
            query = db.Follow.all().filter('leader_email =', user.email).order('follower_email').fetch(limit,offset)
            
            for f in query:
                follower_profile = dao.get_user_profile(f.follower_email)
                result.append(convert.convert_user_profile_for_json(follower_profile)) 
                
        self.response.out.write(json.dumps(result))


class JSONLeaders(BasicRequestHandler):
    def get(self):
        if not self.user_info.user:
            self.response.set_status(403)
            return
        
        req_limit = self.request.get('limit')
        req_offset = self.request.get('offset')
        
        if req_offset:
            offset = int(req_offset)
        else:
            offset = 0
            
        if req_limit:
            limit = int(req_limit)
        else:
            limit = 21
            
        if limit > 101:
            limit = 101
            
        req_profile_id = int(self.request.get('profile_id'))

        result = []        
        
        user = dao.get_user_profile_by_id(req_profile_id)
        if user:
            query = db.Follow.all().filter('follower_email =', user.email).order('leader_email').fetch(limit,offset)
            
            for f in query:
                leader_profile = dao.get_user_profile(f.leader_email)
                result.append(convert.convert_user_profile_for_json(leader_profile)) 
                
        self.response.out.write(json.dumps(result))

        
class ActionUploadUserAvatar(BasicRequestHandler):
    def post(self):
        if not self.user_info.user:
            self.response.set_status(403)
            return
        
        user_profile = dao.get_user_profile(self.user_info.user_email)

        # filename = self.request.POST['file'].filename
        # content_type = self.request.POST['file'].type
        # logging.error(self.request.POST['file'].filename)
        # logging.error(self.request.POST['file'].type)
        
        file_content = self.request.get('file')
        #logging.error('file_length = ' + str(len(file_content)))

        try:
            image = Image.open(StringIO.StringIO(file_content))
        except IOError:
            self.response.out.write(json.dumps({
                'error': 'invalid_image_format'
            }))
            return

        image_width, image_height = image.size
        max_avatar_size = 150
        if image_width > image_height:
            new_image_width = int(image_width * max_avatar_size / image_height)
            new_image_height = max_avatar_size
        else:
            new_image_width = max_avatar_size
            new_image_height = int(image_height * max_avatar_size / image_width)

        rgb_image = image.convert('RGB')
        resized_image = rgb_image.resize((new_image_width, new_image_height))
        cropped_image = resized_image.crop((
                int((new_image_width - max_avatar_size) / 2),
                int((new_image_height - max_avatar_size) / 2),
                int((new_image_width - max_avatar_size) / 2) + max_avatar_size,
                int((new_image_height - max_avatar_size) / 2) + max_avatar_size
            ))
        
        avatar_memory_file = StringIO.StringIO()
        cropped_image.save(avatar_memory_file, 'jpeg')
        
        file_name = '/images/avatar/' + str(self.user_info.profile_id) + '.jpg'
        cs.create_file(file_name, 'image/jpeg', avatar_memory_file.getvalue())
        
        user_profile.avatar_file = file_name
        dao.set_user_profile(user_profile)

        cache_key = cache.MC_IMAGE_PREFIX + file_name
        cache.delete(cache_key)
        cache.delete(cache.MC_MAIN_PAGE_PRODUCTIVE_ARTISTS)
        cache.delete(cache.MC_MAIN_PAGE_TOP_RATED_ARTISTS)

        self.response.out.write(json.dumps({
            'result': 'ok'
        }))


class JSONDeleteUserAvatar(BasicRequestHandler):
    def post(self):
        if not self.user_info.user:
            self.response.set_status(403)
            return

        profile_id = int(self.request.get('profile_id'))
        if self.user_info.superadmin and self.user_info.profile_id != profile_id:
            self.response.set_status(403)
            return

        user_profile = dao.get_user_profile_by_id(profile_id)
        if user_profile.avatar_file:
            cache_key = cache.MC_IMAGE_PREFIX + user_profile.avatar_file
            cache.delete(cache_key)
            cache.delete(cache.MC_MAIN_PAGE_PRODUCTIVE_ARTISTS)
            cache.delete(cache.MC_MAIN_PAGE_TOP_RATED_ARTISTS)

            cs.delete_file(user_profile.avatar_file)
            user_profile.avatar_file = ''
            dao.set_user_profile(user_profile)

        self.response.out.write(json.dumps({'result': 'ok'}))

        
class AvatarImageRequest(BasicRequestHandler):
    def get(self, *ar):
        profile_id = ar[0]
        user_profile = dao.get_user_profile_by_id(int(profile_id))
        if user_profile.avatar_file:
            file_name = user_profile.avatar_file
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
            
            self.response.headers['Content-Type']='image/jpeg'     
            self.response.out.write(file_content)        
        else:
            self.response.set_status(404)


class JSONAdminDeleteTag(BasicRequestHandler):
    def post(self):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return

        tag_id = int(self.request.get('tag_id'))
        tag = db.Tag.get_by_id(tag_id)
        if tag:
            max_count = 200
            artworks = db.Artwork.all().filter('tags =', tags.tag_url_name(tag.url_name)).fetch(max_count + 1)
            count = 0
            has_more = False
            for a in artworks:
                if count < max_count:
                    count = count + 1
                    if tag.url_name in a.tags:
                        a.tags.remove(tag.url_name)
                    if tags.tag_url_name(tag.title) in a.tags:
                        a.tags.remove(tags.tag_url_name(tag.title))
                    if tags.tag_url_name(tag.url_name) in a.tags:
                        a.tags.remove(tags.tag_url_name(tag.url_name))
                    a.put()
                else:
                    has_more = True
            if not has_more:
                cache.delete(cache.MC_TAG + tag.url_name)
                tag.delete()

            self.response.out.write(json.dumps({
                'result': 'ok',
                'count': count,
                'has_more': has_more
            }))
        else:
            self.response.out.write(json.dumps({
                'error': 'not_found',
            }))


class JSONAdminRenameTag(BasicRequestHandler):
    def post(self):
        if not self.user_info.superadmin:
            self.response.set_status(403)
            return

        tag_id = int(self.request.get('tag_id'))
        new_title = self.request.get('title').strip()
        new_url_name = tags.tag_url_name(new_title)
        tag_by_id = db.Tag.get_by_id(tag_id)
        if tag_by_id:
            if tag_by_id.url_name == new_url_name:
                cache.delete(cache.MC_TAG + tag_by_id.url_name)
                tag_by_id.title = new_title
                tag_by_id.title_lower = new_title.lower()
                tag_by_id.put()

                same_tags = db.Tag.all().filter('url_name =', new_url_name)
                for t in same_tags:
                    if t.key().id() != tag_id:
                        t.delete()
                self.response.out.write(json.dumps({
                    'result': 'renamed',
                }))
            else:
                tag_by_url_name = db.Tag.all().filter('url_name =', new_url_name).get()
                if not tag_by_url_name:
                    new_tag = db.Tag()
                    new_tag.title = new_title
                    new_tag.title_lower = new_title.lower()
                    new_tag.url_name = new_url_name
                    new_tag.put()

                max_count = 200
                artworks = db.Artwork.all().filter('tags =', tags.tag_url_name(tag_by_id.url_name)).fetch(max_count + 1)
                count = 0
                has_more = False
                for a in artworks:
                    if count < max_count:
                        count = count + 1
                        if tag_by_id.url_name in a.tags:
                            a.tags.remove(tag_by_id.url_name)
                        if tags.tag_url_name(tag_by_id.title) in a.tags:
                            a.tags.remove(tags.tag_url_name(tag_by_id.title))
                        if tags.tag_url_name(tag_by_id.url_name) in a.tags:
                            a.tags.remove(tags.tag_url_name(tag_by_id.url_name))
                        if new_url_name not in a.tags:
                            a.tags.append(new_url_name)
                        a.put()
                    else:
                        has_more = True
                if not has_more:
                    cache.delete(cache.MC_TAG + tag_by_id.url_name)
                    tag_by_id.delete()

                self.response.out.write(json.dumps({
                    'result': 'ok',
                    'count': count,
                    'has_more': has_more
                }))
        else:
            self.response.out.write(json.dumps({
                'error': 'not_found',
            }))





