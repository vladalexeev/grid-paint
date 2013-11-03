# -*- coding: utf-8 -*-
'''
Created on 23.07.2013

@author: Vlad
'''

import db
import json
import StringIO

from PIL import Image, ImageDraw

from common import BasicRequestHandler
from grid.square import GridSquare
from grid.triangle import GridTriangle
from grid.hex import GridHex
from grid.triangles4 import GridTriangles4

from graphics.svg import SvgImageWriter

import tags
import common

import logging

grids={
       'square': GridSquare,
       'triangle': GridTriangle,
       'hex': GridHex,
       'triangles4': GridTriangles4
       }

class ActionSaveImage(BasicRequestHandler):
    def post(self):
        artwork_json=self.request.get('artwork_json')
        artwork_id=self.request.get('artwork_id')
        artwork_name=self.request.get('artwork_name')
        artwork_description=self.request.get('artwork_description')
        artwork_tags=self.request.get('artwork_tags')
        
        if artwork_id:
            artwork=db.Artwork.get(artwork_id)
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
            
        logging.error('artwork_description = '+artwork_description)
            
        if artwork_description:
            artwork.description=artwork_description
        else:
            artwork.description=''
            
        artwork.json=artwork_json
        
        original_tags=artwork_tags.split(',')
        url_tags=[]
        for tag_title in original_tags:
            if len(tag_title)>0:
                db_tag=tags.tag_by_title(tag_title);
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
        grid=grids[layer['grid']]();
        grid.cell_size=layer['cellSize']

        for cell in layer['cells']:
            grid.paintShape(image_draw, cell, dx, dy)
        
        memory_file = StringIO.StringIO()
        image.save(memory_file, 'png')
        
        artwork.full_image = memory_file.getvalue()
        artwork.full_image_width = image_width
        artwork.full_image_height = image_height
        
        small_image_size = common.calc_resize(image_width, 
                                              image_height, 
                                              db.artwork_small_image_width, 
                                              db.artwork_small_image_height)
        small_image = image.resize(small_image_size, Image.ANTIALIAS)
        small_memory_file = StringIO.StringIO()
        small_image.save(small_memory_file, 'png')
        
        artwork.small_image = small_memory_file.getvalue()
        artwork.small_image_width = small_image_size[0]
        artwork.small_image_height = small_image_size[1]
        
        saved_id=artwork.put()
        
        common.mm_cache.delete(common.MC_SMALL_IMAGE_PREFIX+str(saved_id))
        common.mm_cache.delete(common.MC_MAIN_PAGE_RECENT_IMAGES_KEY)
        
        
        self.redirect('/images/details/'+str(saved_id))
        
class ActionDeleteImage(BasicRequestHandler):
    def get(self):
        artwork_id=self.request.get('id')
        artwork=db.Artwork.get(artwork_id)
        if self.user_info.superadmin or artwork.author==self.user_info.user:
            comments=db.Comment.all().filter('artwork_ref =', artwork)
            for comment in comments:
                comment.delete()
                
            artwork.delete();
            
            common.mm_cache.delete(common.MC_SMALL_IMAGE_PREFIX+str(artwork_id))
            common.mm_cache.delete(common.MC_MAIN_PAGE_RECENT_IMAGES_KEY)

            self.redirect("/my-images")
        else:
            self.response.set_status(403)
            
class ActionSaveComment(BasicRequestHandler):
    def post(self):
        if not self.user_info.user:
            self.response.set_status(403)
            return
        
        artwork_id=self.request.get('artwork_id')
        comment_text=self.request.get('comment_text')
        
        artwork=db.Artwork.get(artwork_id)
        if not artwork:
            self.response.set_status(403)
            return
        
        comment=db.Comment(parent=artwork)
        comment.artwork_ref=artwork
        comment.text=comment_text
        comment.put()
        
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
            self.redirect('/images/details/'+str(artwork.key()))
        else:
            self.response.set_status(404)
            return

class PNGImageRequest(BasicRequestHandler):
    def get(self, *ar):
        artwork_id=ar[0]
        artwork=db.Artwork.get(artwork_id)
        
        self.response.headers['Content-Type']='image/png'     
        self.response.out.write(artwork.full_image)
        
class PNGSmallImageRequest(BasicRequestHandler):
    def get(self, *ar):
        artwork_id=ar[0]
        
        small_image=common.mm_cache.get('small_image_'+artwork_id)
        
        if not small_image:        
            artwork=db.Artwork.get(artwork_id)
            small_image = artwork.small_image;
            common.mm_cache.add(common.MC_SMALL_IMAGE_PREFIX+artwork_id, small_image)
        
        self.response.headers['Content-Type']='image/png'     
        self.response.out.write(small_image)
        
class SVGImageRequest(BasicRequestHandler):
    def get(self, *ar):
        artwork_id=ar[0]
        artwork=db.Artwork.get(artwork_id)
        
        if not artwork:
            self.response.set_status(404)
            return
        
        self.response.headers['Content-Type']='image/svg'
        
        json_obj=json.loads(artwork.json)
        
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
        
        for cell in layer['cells']:
            grid.paintShape(image, cell, dx, dy)
            
        image.endImage()
        
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
        
        