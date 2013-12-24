'''
Created on 29.07.2013

@author: Vlad
'''

import colorsys

import graphics.color as clr
import grid.base as base

def hex_points(col, row, side_length):
    x=(side_length+side_length*base.cos60)*col
    y=2*side_length*base.sin60*row
    half_height=side_length*base.sin60
    dx=side_length*base.cos60
    if col % 2 == 1:
        y+=side_length*base.sin60
    
    return [
        {'x': x, 'y': y+half_height},
        {'x': x+dx, 'y': y},
        {'x': x+dx+side_length, 'y': y},
        {'x': x+2*dx+side_length, 'y': y+half_height},
        {'x': x+dx+side_length, 'y': y+2*half_height},
        {'x': x+dx, 'y': y+2*half_height},
        {'x': x+dx+side_length/2, 'y': y+half_height}
    ]

class ShapeFlat:
    def __init__(self, grid):
        self.grid=grid
    
    def paint(self, image, col, row, color, dx, dy):
        pp=hex_points(col, row, self.grid.cell_size/2);
        image.polygon([(pp[0]['x']+dx, pp[0]['y']+dy),
                       (pp[1]['x']+dx, pp[1]['y']+dy),
                       (pp[2]['x']+dx, pp[2]['y']+dy),
                       (pp[3]['x']+dx, pp[3]['y']+dy),
                       (pp[4]['x']+dx, pp[4]['y']+dy),
                       (pp[5]['x']+dx, pp[5]['y']+dy)],
                      fill=color)
        
class ShapeDiamond:
    def __init__(self, grid):
        self.grid=grid
        
    def paint(self, image, col, row, color, dx, dy):
        rgb=clr.hex_to_rgb(color)
        hls=colorsys.rgb_to_hls(*rgb)
        pp=hex_points(col, row, self.grid.cell_size/2);
        cx=pp[6]['x']
        cy=pp[6]['y']

        
        c0=clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.2)))
        image.polygon([(pp[0]['x']+dx, pp[0]['y']+dy),
                       (pp[1]['x']+dx, pp[1]['y']+dy),
                       (cx+dx, cy+dy)],
                      fill=c0)
        
        c1=clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.1)))
        image.polygon([(pp[1]['x']+dx, pp[1]['y']+dy),
                       (pp[2]['x']+dx, pp[2]['y']+dy),
                       (cx+dx, cy+dy)],
                      fill=c1)

        c2=clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.1)))
        image.polygon([(pp[2]['x']+dx, pp[2]['y']+dy),
                       (pp[3]['x']+dx, pp[3]['y']+dy),
                       (cx+dx, cy+dy)],
                      fill=c2)

        c3=clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.2)))
        image.polygon([(pp[3]['x']+dx, pp[3]['y']+dy),
                       (pp[4]['x']+dx, pp[4]['y']+dy),
                       (cx+dx, cy+dy)],
                      fill=c3)
        
        c4=c2
        image.polygon([(pp[4]['x']+dx, pp[4]['y']+dy),
                       (pp[5]['x']+dx, pp[5]['y']+dy),
                       (cx+dx, cy+dy)],
                      fill=c4)
        
        c5=c1
        image.polygon([(pp[5]['x']+dx, pp[5]['y']+dy),
                       (pp[0]['x']+dx, pp[0]['y']+dy),
                       (cx+dx, cy+dy)],
                      fill=c5)
        
class ShapeCube:
    def __init__(self, grid):
        self.grid=grid
        
    def paint(self, image, col, row, color, dx, dy):
        rgb=clr.hex_to_rgb(color)
        hls=colorsys.rgb_to_hls(*rgb)
        pp=hex_points(col, row, self.grid.cell_size/2);
        cx=pp[6]['x']
        cy=pp[6]['y']

        
        c0=clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.2)))
        image.polygon([(pp[0]['x']+dx, pp[0]['y']+dy),
                       (pp[1]['x']+dx, pp[1]['y']+dy),
                       (pp[2]['x']+dx, pp[2]['y']+dy),
                       (cx+dx, cy+dy)],
                      fill=c0)
        
        c1=color
        image.polygon([(pp[2]['x']+dx, pp[2]['y']+dy),
                       (pp[3]['x']+dx, pp[3]['y']+dy),
                       (pp[4]['x']+dx, pp[4]['y']+dy),
                       (cx+dx, cy+dy)],
                      fill=c1)

        c2=clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.2)))
        image.polygon([(pp[4]['x']+dx, pp[4]['y']+dy),
                       (pp[5]['x']+dx, pp[5]['y']+dy),
                       (pp[0]['x']+dx, pp[0]['y']+dy),
                       (cx+dx, cy+dy)],
                      fill=c2)


class ShapeJewel:
    def __init__(self, grid):
        self.grid=grid
        
    def paint(self, image, col, row, color, dx, dy):
        rgb=clr.hex_to_rgb(color)
        hls=colorsys.rgb_to_hls(*rgb)
        pp=hex_points(col, row, self.grid.cell_size/2);
        cx=pp[6]['x']
        cy=pp[6]['y']

        c0=clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.2)))
        image.polygon([(pp[0]['x']+dx, pp[0]['y']+dy),
                       (pp[1]['x']+dx, pp[1]['y']+dy),
                       (pp[1]['x']+dx+(cx-pp[1]['x'])/2, pp[1]['y']+dy+(cy-pp[1]['y'])/2),
                       (pp[0]['x']+dx+(cx-pp[0]['x'])/2, pp[0]['y']+dy+(cy-pp[0]['y'])/2)],
                      fill=c0)
        
        c1=clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.1)))
        image.polygon([(pp[1]['x']+dx, pp[1]['y']+dy),
                       (pp[2]['x']+dx, pp[2]['y']+dy),
                       (pp[2]['x']+dx+(cx-pp[2]['x'])/2, pp[2]['y']+dy+(cy-pp[2]['y'])/2),
                       (pp[1]['x']+dx+(cx-pp[1]['x'])/2, pp[1]['y']+dy+(cy-pp[1]['y'])/2)],
                      fill=c1)

        c2=clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.1)))
        image.polygon([(pp[2]['x']+dx, pp[2]['y']+dy),
                       (pp[3]['x']+dx, pp[3]['y']+dy),
                       (pp[3]['x']+dx+(cx-pp[3]['x'])/2, pp[3]['y']+dy+(cy-pp[3]['y'])/2),
                       (pp[2]['x']+dx+(cx-pp[2]['x'])/2, pp[2]['y']+dy+(cy-pp[2]['y'])/2)],
                      fill=c2)

        c3=clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.2)))
        image.polygon([(pp[3]['x']+dx, pp[3]['y']+dy),
                       (pp[4]['x']+dx, pp[4]['y']+dy),
                       (pp[4]['x']+dx+(cx-pp[4]['x'])/2, pp[4]['y']+dy+(cy-pp[4]['y'])/2),
                       (pp[3]['x']+dx+(cx-pp[3]['x'])/2, pp[3]['y']+dy+(cy-pp[3]['y'])/2)],
                      fill=c3)
        
        c4=c2
        image.polygon([(pp[4]['x']+dx, pp[4]['y']+dy),
                       (pp[5]['x']+dx, pp[5]['y']+dy),
                       (pp[5]['x']+dx+(cx-pp[5]['x'])/2, pp[5]['y']+dy+(cy-pp[5]['y'])/2),
                       (pp[4]['x']+dx+(cx-pp[4]['x'])/2, pp[4]['y']+dy+(cy-pp[4]['y'])/2)],
                      fill=c4)
        
        c5=c1
        image.polygon([(pp[5]['x']+dx, pp[5]['y']+dy),
                       (pp[0]['x']+dx, pp[0]['y']+dy),
                       (pp[0]['x']+dx+(cx-pp[0]['x'])/2, pp[0]['y']+dy+(cy-pp[0]['y'])/2),
                       (pp[5]['x']+dx+(cx-pp[5]['x'])/2, pp[5]['y']+dy+(cy-pp[5]['y'])/2)],
                      fill=c5)
        
        image.polygon([(pp[0]['x']+dx+(cx-pp[0]['x'])/2, pp[0]['y']+dy+(cy-pp[0]['y'])/2),
                       (pp[1]['x']+dx+(cx-pp[1]['x'])/2, pp[1]['y']+dy+(cy-pp[1]['y'])/2),
                       (pp[2]['x']+dx+(cx-pp[2]['x'])/2, pp[2]['y']+dy+(cy-pp[2]['y'])/2),
                       (pp[3]['x']+dx+(cx-pp[3]['x'])/2, pp[3]['y']+dy+(cy-pp[3]['y'])/2),
                       (pp[4]['x']+dx+(cx-pp[4]['x'])/2, pp[4]['y']+dy+(cy-pp[4]['y'])/2),
                       (pp[5]['x']+dx+(cx-pp[5]['x'])/2, pp[5]['y']+dy+(cy-pp[5]['y'])/2)],
                      fill=color)
        

class GridHex(base.GridBase):
    def __init__(self):
        self.shapes={
                     'flat': ShapeFlat(self),
                     'diamond': ShapeDiamond(self),
                     'jewel': ShapeJewel(self),
                     'cube': ShapeCube(self)
                    }