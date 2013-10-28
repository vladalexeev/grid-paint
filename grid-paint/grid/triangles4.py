'''
Created on 27.10.2013

@author: Vlad
'''

import grid.base as base


def triangle_points(col, row, cell_size): 
    square_col=int(col/4);
    inner_triangle=col % 4;
    
    square_top=row*cell_size;
    square_left=square_col*cell_size;
    center_x=square_left+float(cell_size+1)/2;
    center_y=square_top+float(cell_size+1)/2;
    
    if inner_triangle==0:
        return [{'x': square_left, 'y': square_top},
                {'x': square_left+cell_size, 'y': square_top},
                {'x': center_x, 'y': center_y}]
    elif inner_triangle==1:
        return [{'x': square_left, 'y': square_top+cell_size},
                {'x': square_left, 'y': square_top},
                {'x': center_x, 'y': center_y}]
    elif inner_triangle==2:
        return [{'x': square_left+cell_size, 'y': square_top},
                {'x': square_left+cell_size, 'y': square_top+cell_size},
                {'x': center_x, 'y': center_y}]
    else: # innerTriangle==3
        return [{'x': square_left+cell_size, 'y': square_top+cell_size},
                {'x': square_left, 'y': square_top+cell_size},
                {'x': center_x, 'y': center_y}]        


class ShapeFlat:
    def __init__(self, grid):
        self.grid=grid
    
    def paint(self, image, col, row, color, dx, dy):
        pp=triangle_points(col, row, self.grid.cell_size);
        image.polygon([(pp[0]['x']+dx, pp[0]['y']+dy),
                       (pp[1]['x']+dx, pp[1]['y']+dy),
                       (pp[2]['x']+dx, pp[2]['y']+dy)],
                      fill=color)
        #image.point([(pp[2]['x'], pp[2]['y']-1)], fill=color)


class GridTriangles4(base.GridBase):
    def __init__(self):
        self.shapes={
                     'flat': ShapeFlat(self)
                    }