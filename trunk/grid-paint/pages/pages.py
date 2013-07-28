# -*- coding: utf-8 -*-
'''
Created on 23.07.2013

@author: Vlad
'''

import json

from common import BasicPageRequestHandler

import db

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
        
class PageMyImages(BasicPageRequestHandler):
    def get(self):
        my_artworks=db.Artwork.all().filter('author', self.user_info.user).order('-date').fetch(20,0)
        self.write_template('templates/my-artworks.html', 
                            {
                             'artworks': my_artworks
                             })
        
class FullImageRequest(BasicPageRequestHandler):
    def get(self, *ar):
        artwork_id=ar[0]
        artwork=db.Artwork.get(artwork_id)
        
        self.response.headers['Content-Type']='image/png'     
        self.response.out.write(artwork.full_image)