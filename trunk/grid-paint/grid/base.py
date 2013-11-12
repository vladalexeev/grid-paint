'''
Created on 29.07.2013

@author: Vlad
'''

import math

sin60=math.sin(math.pi*60/180)
cos60=math.cos(math.pi*60/180)

class GridBase:
    cell_size=24;
    
    def __init__(self):
        self.shapes={}
        
    def paintShape(self, image, jsonCell, dx, dy):
        col=jsonCell['col']
        row=jsonCell['row']
        color=jsonCell['color']
        shape=self.shapes[jsonCell['shape']]
        shape.paint(image, col, row, color, dx, dy)
        
    def paintShape2(self, image, col, row, shapeName, color, dx, dy):
        shape=self.shapes[shapeName]
        shape.paint(image, col, row, color, dx, dy)