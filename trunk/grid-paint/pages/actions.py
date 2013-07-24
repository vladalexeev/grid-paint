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

class ActionSaveArtwork(BasicRequestHandler):
    def post(self):
        artwork_json=self.request.get('artwork_json')
        artwork_id=self.request.get('artwork_id')
        artwork_name=self.request.get('artwork_name')
        
        if artwork_id:
            artwork=db.Artwork.get(artwork_id)
            if artwork.author <> self.user_info.user:
                # should be the same user
                self.response.set_status(403)
                return
        else:
            artwork=db.Artwork();
            artwork.author=self.user_info.user
            
        if artwork_name:
            artwork.name=artwork_name
        else:
            artwork.name='Untitled'
            
        artwork.json=artwork_json
        
        
        json_obj=json.loads(artwork_json)
        
        ###
        image=Image.new('RGB', (json_obj['width'],json_obj['height']),json_obj['backgroundColor'])
        image_draw=ImageDraw.Draw(image)
        
        grid=GridSquare();
        layer=json_obj['layers'][0]
        for cell in layer['cells']:
            grid.paintShape(image_draw, cell)
        
        memory_file=StringIO.StringIO()
        image.save(memory_file, 'png')
        
        artwork.full_image=memory_file.getvalue()
        saved_id=artwork.put()
        
        
        self.redirect('/my-images')
