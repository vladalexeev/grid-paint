# -*- coding: utf-8 -*-
'''
Created on 23.07.2013

@author: Vlad
'''

import db

from common import BasicRequestHandler

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
        saved_id=artwork.put()
        
        self.redirect('/images/my')
