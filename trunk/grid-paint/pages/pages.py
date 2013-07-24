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
        new_artwork={
                     'backgroundColor': '#ffffff',
                     'width': 2000,
                     'height': 2000,
                     'layers': [{
                                'grid':self.request.get('grid'),
                                'cellSize':24,                     
                                'items':[]
                                }]
                     }
        artwork_json=json.dumps(new_artwork)
        self.write_template('templates/painter.html', 
                            {
                             'artwork_json':artwork_json
                             })
        
class PageMyImages(BasicPageRequestHandler):
    def get(self):
        my_artworks=db.Artwork.all().filter('author', self.user_info.user).order('-date').fetch(20,0)
        self.write_template('templates/my-artworks.html', 
                            {
                             'artworks': my_artworks
                             })