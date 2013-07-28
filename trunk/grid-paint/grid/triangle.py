'''
Created on 28.07.2013

@author: Vlad
'''

import math

sin60=math.sin(math.pi*60/180)

def triangle_points(col, row, side_length):
    row_height=side_length*sin60
    x=col*side_length/2
    y=row*row_height
    
    if row % 2 == 0:
        if col % 2 == 0:
            return [
                {'x':x, 'y':y+row_height},
                {'x':x+side_length/2, 'y':y},
                {'x':x+side_length, 'y':y+row_height},
                {'x':x+side_length/2, 'y':y+row_height*2/3}
                ]
        else:
            return [
                {'x':x, 'y':y},
                {'x':x+side_length, 'y':y},
                {'x':x+side_length/2, 'y':y+row_height},
                {'x':x+side_length/2, 'y':y+row_height/3}
                ]
    else:
        if col % 2 == 0:
            return [
                {'x':x, 'y':y},
                {'x':x+side_length, 'y':y},
                {'x':x+side_length/2, 'y':y+row_height},
                {'x':x+side_length/2, 'y':y+row_height/3}
                ]
        else:
            return [
                {'x':x, 'y':y+row_height},
                {'x':x+side_length/2, 'y':y},
                {'x':x+side_length, 'y':y+row_height},
                {'x':x+side_length/2, 'y':y+row_height*2/3}
                ]


class ShapeFlat:
    def __init__(self, grid):
        self.grid=grid
    
    def paint(self, image, col, row, color, dx, dy):
        pp=triangle_points(col, row, self.grid.cell_size);
        image.polygon([(pp[0]['x']+dx, pp[0]['y']+dy),
                       (pp[1]['x']+dx, pp[1]['y']+dy),
                       (pp[2]['x']+dx, pp[2]['y']+dy)],
                      fill=color)


class GridTriangle:
    cell_size=24
    
    def __init__(self):
        self.shapes={
                     'flat': ShapeFlat(self)
                    }
    
    def paintShape(self, image, jsonCell, dx, dy):
        col=jsonCell['col']
        row=jsonCell['row']
        color=jsonCell['color']
        shape=self.shapes[jsonCell['shape']]
        shape.paint(image, col, row, color, dx, dy)

    
