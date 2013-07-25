# -*- coding: utf-8 -*-
'''
Square grid

Created on 24.07.2013
@author: Vlad
'''

import grid.color as clr

import colorsys

class ShapeFlat:
    def paint(self, image, grid, x, y, color):
        image.rectangle(
            [x, y, x+grid.cell_size, y+grid.cell_size],
            fill=color)
        
class ShapeDiamond:
    def paint(self, image, grid, x, y, color):
        rgb=clr.hex_to_rgb(color)
        hls=colorsys.rgb_to_hls(*rgb)
       
        c1=clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.2)))
        image.polygon([(x, y),
                       (x+grid.cell_size/2, y+grid.cell_size/2),
                       (x+grid.cell_size, y)],
                      fill=c1)
        
        c2=clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.1)))
        image.polygon([(x, y),
                       (x+grid.cell_size/2, y+grid.cell_size/2),
                       (x, y+grid.cell_size)],
                      fill=c2)
       
        c3=clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.1)))
        image.polygon([(x, y+grid.cell_size),
                       (x+grid.cell_size/2, y+grid.cell_size/2),
                       (x+grid.cell_size, y+grid.cell_size)],
                      fill=c3)

        c4=clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.2)))
        image.polygon([(x+grid.cell_size, y+grid.cell_size),
                       (x+grid.cell_size/2, y+grid.cell_size/2),
                       (x+grid.cell_size, y)],
                      fill=c4)
        
class ShapeJewel:
    def paint(self, image, grid, x, y, color):
        rgb=clr.hex_to_rgb(color)
        hls=colorsys.rgb_to_hls(*rgb)
        facet=grid.cell_size/6
        
        c1=clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.2)))
        image.polygon([(x, y),
                       (x+facet, y+facet),
                       (x+grid.cell_size-facet, y+facet),
                       (x+grid.cell_size, y)],
                      fill=c1)
        
        c2=clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.1)))
        image.polygon([(x, y),
                       (x+facet, y+facet),
                       (x+facet, y+grid.cell_size-facet),
                       (x, y+grid.cell_size)],
                      fill=c2)
        
        c3=clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.1)))
        image.polygon([(x, y+grid.cell_size),
                       (x+facet, y+grid.cell_size-facet),
                       (x+grid.cell_size-facet, y+grid.cell_size-facet),
                       (x+grid.cell_size, y+grid.cell_size)],
                      fill=c3)
        
        c4=clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.2)))
        image.polygon([(x+grid.cell_size, y),
                       (x+grid.cell_size-facet, y+facet),
                       (x+grid.cell_size-facet, y+grid.cell_size-facet),
                       (x+grid.cell_size, y+grid.cell_size)],
                      fill=c4)
                
        image.rectangle([x+facet,
                         y+facet,
                         x+grid.cell_size-facet-1,
                         y+grid.cell_size-facet-1],
                        fill=color)
       

class GridSquare:
    cell_size=24;
    shapes={
            "flat": ShapeFlat(),
            "diamond": ShapeDiamond(),
            "jewel": ShapeJewel()
            }
    def paintShape(self, image, jsonCell):
        x=jsonCell['col']*self.cell_size
        y=jsonCell['row']*self.cell_size
        shape=self.shapes[jsonCell['shape']]
        shape.paint(image, self, x, y, jsonCell['color'])
        

    
