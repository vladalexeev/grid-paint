# -*- coding: utf-8 -*-
'''
Created on 23.07.2013

@author: Vlad
'''

import json

from common import BasicPageRequestHandler

import db

page_size=6

class PageIndex(BasicPageRequestHandler):
    def get(self):
        self.write_template('templates/index.html', {})
        
class PageNewImage(BasicPageRequestHandler):
    def get(self):
        self.write_template('templates/new-image.html', {})
        
class PagePainter(BasicPageRequestHandler):
    def get(self):
        if self.request.get('id'):
            artwork_id=self.request.get('id')
            artwork=db.Artwork.get(artwork_id)
            self.write_template('templates/painter.html', 
                                {
                                 'artwork_id': artwork_id,
                                 'artwork_name': artwork.name,
                                 'artwork_json': artwork.json
                                 })
        else:
            new_artwork={
                         'backgroundColor': '#ffffff',
                         'canvasSize':{
                                       'width': 2000,
                                       'height': 2000,                                       
                                       },
                         'layers': [{
                                     'grid':self.request.get('grid'),
                                     'cellSize':24,                     
                                     'cells':[]
                                     }]
                         }
            artwork_json=json.dumps(new_artwork)
            self.write_template('templates/painter.html', 
                                {
                                 'artwork_json': artwork_json
                                 })


def convert_artwork_for_page(artwork, thumbnail_width, thumbnail_height):
    result={
            'key': artwork.key(),
            'name': artwork.name,
            'date': artwork.date,
            'author': artwork.author,
            'full_image_width': artwork.full_image_height,
            'full_image_height': artwork.full_image_height
            }
        
    width_aspect=float(artwork.full_image_width)/thumbnail_width
    height_aspect=float(artwork.full_image_height)/thumbnail_height
        
    if width_aspect>height_aspect:
        divisor=width_aspect
    else:
        divisor=height_aspect
        
    if divisor<1:
        divisor=1
        
    result['thumbnail_width']=int(artwork.full_image_width/divisor)
    result['thumbnail_height']=int(artwork.full_image_height/divisor)
    
    return result
    
    
        
class PageMyImages(BasicPageRequestHandler):
    def get(self):
        if self.request.get('offset'):
            offset=int(self.request.get('offset'))
        else:
            offset=0
            
        if offset<0:
            offset=0
        
        my_artworks=db.Artwork.\
                        all().\
                        filter('author', self.user_info.user).\
                        order('-date').\
                        fetch(page_size+1,offset)
        
        has_prev_page=(offset>0)
        has_next_page=len(my_artworks)>page_size
        
        if len(my_artworks)>page_size:
            my_artworks=my_artworks[:page_size]
            
        artworks=[convert_artwork_for_page(ma,300,200) for ma in my_artworks]

        
        self.write_template('templates/my-artworks.html', 
                            {
                             'has_next_page': has_next_page,
                             'has_prev_page': has_prev_page,
                             'next_offset': offset+page_size,
                             'prev_offset': offset-page_size,                             
                             'artworks': artworks
                             })
        
class PageAllImages(BasicPageRequestHandler):
    def get(self):
        if self.request.get('offset'):
            offset=int(self.request.get('offset'))
        else:
            offset=0
            
        if offset<0:
            offset=0
        
        all_artworks=db.Artwork.all().order('-date').fetch(page_size+1,offset)
        
        has_prev_page=(offset>0)
        has_next_page=len(all_artworks)>page_size
        
        if len(all_artworks)>page_size:
            all_artworks=all_artworks[:page_size]
            
        artworks=[convert_artwork_for_page(a,300,200) for a in all_artworks]

        
        self.write_template('templates/index.html', 
                            {
                             'has_next_page': has_next_page,
                             'has_prev_page': has_prev_page,
                             'next_offset': offset+page_size,
                             'prev_offset': offset-page_size,
                             'artworks': artworks
                             })
        
        
class PageImage(BasicPageRequestHandler):
    def get(self, *arg):
        artwork_id=arg[0]
        artwork=db.Artwork.get(artwork_id)
        self.write_template('templates/artwork-details.html', 
                            {
                             'artwork': convert_artwork_for_page(artwork, 600, 400),
                             'can_edit_artwork': self.user_info.superadmin or artwork.author==self.user_info.user
                            })
        
