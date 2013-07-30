'''
Created on 28.07.2013

@author: Vlad
'''

import colorsys

import graphics.color as clr
import grid.base as base



def triangle_points(col, row, side_length):
    row_height=side_length*base.sin60
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
        
class ShapeDiamond:
    def __init__(self, grid):
        self.grid=grid
        
    def paint(self, image, col, row, color, dx, dy):
        rgb=clr.hex_to_rgb(color)
        hls=colorsys.rgb_to_hls(*rgb)
        pp=triangle_points(col, row, self.grid.cell_size);

        
        c1=clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.2)))
        image.polygon([(pp[0]['x']+dx, pp[0]['y']+dy),
                       (pp[1]['x']+dx, pp[1]['y']+dy),
                       (pp[3]['x']+dx, pp[3]['y']+dy)],
                      fill=c1)
        
        c2=clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.1)))
        image.polygon([(pp[0]['x']+dx, pp[0]['y']+dy),
                       (pp[2]['x']+dx, pp[2]['y']+dy),
                       (pp[3]['x']+dx, pp[3]['y']+dy)],
                      fill=c2)
        
        c3=clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.1)))
        image.polygon([(pp[1]['x']+dx, pp[1]['y']+dy),
                       (pp[2]['x']+dx, pp[2]['y']+dy),
                       (pp[3]['x']+dx, pp[3]['y']+dy)],
                      fill=c3)
        
class ShapeJewel:
    def __init__(self, grid):
        self.grid=grid
        
    def paint(self, image, col, row, color, dx, dy):
        rgb=clr.hex_to_rgb(color)
        hls=colorsys.rgb_to_hls(*rgb)
        pp=triangle_points(col, row, self.grid.cell_size);
        
        c1=clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.2)))
        image.polygon([(pp[0]['x']+dx, pp[0]['y']+dy),
                       (pp[1]['x']+dx, pp[1]['y']+dy),
                       (pp[1]['x']+(pp[3]['x']-pp[1]['x'])/2+dx, pp[1]['y']+(pp[3]['y']-pp[1]['y'])/2+dy),
                       (pp[0]['x']+(pp[3]['x']-pp[0]['x'])/2+dx, pp[0]['y']+(pp[3]['y']-pp[0]['y'])/2+dy)],
                      fill=c1)

        c2=clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.1)))
        image.polygon([(pp[0]['x']+dx, pp[0]['y']+dy),
                       (pp[2]['x']+dx, pp[2]['y']+dy),
                       (pp[2]['x']+(pp[3]['x']-pp[2]['x'])/2+dx, pp[2]['y']+(pp[3]['y']-pp[2]['y'])/2+dy),
                       (pp[0]['x']+(pp[3]['x']-pp[0]['x'])/2+dx, pp[0]['y']+(pp[3]['y']-pp[0]['y'])/2+dy)],
                      fill=c2)
        
        c3=clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.1)))
        image.polygon([(pp[1]['x']+dx, pp[1]['y']+dy),
                       (pp[2]['x']+dx, pp[2]['y']+dy),
                       (pp[2]['x']+(pp[3]['x']-pp[2]['x'])/2+dx, pp[2]['y']+(pp[3]['y']-pp[2]['y'])/2+dy),
                       (pp[1]['x']+(pp[3]['x']-pp[1]['x'])/2+dx, pp[1]['y']+(pp[3]['y']-pp[1]['y'])/2+dy)],
                      fill=c3)

        image.polygon([(pp[0]['x']+(pp[3]['x']-pp[0]['x'])/2+dx, pp[0]['y']+(pp[3]['y']-pp[0]['y'])/2+dy),
                       (pp[1]['x']+(pp[3]['x']-pp[1]['x'])/2+dx, pp[1]['y']+(pp[3]['y']-pp[1]['y'])/2+dy),
                       (pp[2]['x']+(pp[3]['x']-pp[2]['x'])/2+dx, pp[2]['y']+(pp[3]['y']-pp[2]['y'])/2+dy)],
                      fill=color)
        

class GridTriangle(base.GridBase):
    def __init__(self):
        self.shapes={
                     'flat': ShapeFlat(self),
                     'diamond': ShapeDiamond(self),
                     'jewel': ShapeJewel(self)
                    }
    

    
