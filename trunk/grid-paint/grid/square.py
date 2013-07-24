# -*- coding: utf-8 -*-
'''
Square grid

Created on 24.07.2013
@author: Vlad
'''

class ShapeFlat:
    def paint(self, image, grid, x, y, color):
        image.rectangle(
            [x, y, x+grid.cell_size, y+grid.cell_size],
            fill=color)

class GridSquare:
    cell_size=24;
    shapes={
            "flat":ShapeFlat()
            }
    def paintShape(self, image, jsonCell):
        x=jsonCell['col']*self.cell_size
        y=jsonCell['row']*self.cell_size
        shape=self.shapes[jsonCell['shape']]
        shape.paint(image, self, x, y, jsonCell['color'])
    
