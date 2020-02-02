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

    def paint_layer_2(self, image, layer, dx, dy):
        for row in layer['rows']:
            for cell in row['cells']:
                self.paintShape2(image, cell[0], row['row'], cell[1], cell[2], dx, dy)
