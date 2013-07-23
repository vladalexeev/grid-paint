# -*- coding: utf-8 -*-
'''
Created on 23.07.2013

@author: Vlad
'''

import db

from common import BasicRequestHandler

class ActionSaveArtwork(BasicRequestHandler):
    def get(self):
        artwork_json=self.request.get('artwork_json')
        artwork_id=self.request.get('artwork_id')
        artwork_name=self.request.get('artwork_name')