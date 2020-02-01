'''
Created on 29.07.2013

@author: Vlad
'''

import math

sin60=math.sin(math.pi*60/180)
cos60=math.cos(math.pi*60/180)


class GridBase:
    cell_size=24
    
    def __init__(self):
        self.shapes = {}
        
    def paintShape(self, image, json_cell, dx, dy):
        col = json_cell['col']
        row = json_cell['row']
        color = json_cell['color']
        shape = self.shapes[json_cell['shape']]
        shape.paint(image, col, row, color, dx, dy)
        
    def paintShape2(self, image, col, row, shape_name, color, dx, dy):
        shape = self.shapes[shape_name]
        shape.paint(image, col, row, color, dx, dy)