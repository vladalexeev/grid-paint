# -*- coding: utf-8 -*-
'''
Square grid

Created on 24.07.2013
@author: Vlad
'''

import graphics.color as clr
import grid.base as base

import colorsys

class BasicShape:
    def __init__(self, grid):
        self.grid=grid

class ShapeFlat(BasicShape):
    def paint(self, image, col, row, color, dx, dy):
        x=col*self.grid.cell_size+dx
        y=row*self.grid.cell_size+dy
        image.polygon([(x,y),
                       (x, y+self.grid.cell_size),
                       (x+self.grid.cell_size, y+self.grid.cell_size),
                       (x+self.grid.cell_size, y)],
                      fill=color)
        
#        image.rectangle(
#            [x, y, x+self.grid.cell_size-1, y+self.grid.cell_size-1],
#            fill=color)
        
class ShapeDiamond(BasicShape):
    def paint(self, image, col, row, color, dx, dy):
        x=col*self.grid.cell_size+dx
        y=row*self.grid.cell_size+dy
        cell_size=self.grid.cell_size
        rgb=clr.hex_to_rgb(color)
        hls=colorsys.rgb_to_hls(*rgb)
       
        c1=clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.2)))
        image.polygon([(x, y),
                       (x+cell_size/2, y+cell_size/2),
                       (x+cell_size, y)],
                      fill=c1)
        
        c2=clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.1)))
        image.polygon([(x, y),
                       (x+cell_size/2, y+cell_size/2),
                       (x, y+cell_size)],
                      fill=c2)
       
        c3=clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.1)))
        image.polygon([(x, y+cell_size),
                       (x+cell_size/2, y+cell_size/2),
                       (x+cell_size, y+cell_size)],
                      fill=c3)

        c4=clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.2)))
        image.polygon([(x+cell_size, y+cell_size),
                       (x+cell_size/2, y+cell_size/2),
                       (x+cell_size, y)],
                      fill=c4)

class BasicShapeJewel(BasicShape):
    def __init__(self, grid):
        BasicShape.__init__(self,grid)
        self.facet=self.get_facet();
        
    def get_facet(self):
        raise NotImplementedError("Should implement this method")

    def paint(self, image, col, row, color, dx, dy):
        x=col*self.grid.cell_size+dx
        y=row*self.grid.cell_size+dy
        rgb=clr.hex_to_rgb(color)
        hls=colorsys.rgb_to_hls(*rgb)
        cell_size=self.grid.cell_size
        facet=self.facet

        image.polygon([(x+facet, y+facet),
                       (x+facet, y+cell_size-facet),
                       (x+cell_size-facet, y+cell_size-facet),
                       (x+cell_size-facet, y+facet)],
                      fill=color)
        
        c1=clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.2)))
        image.polygon([(x, y),
                       (x+facet, y+facet),
                       (x+cell_size-facet, y+facet),
                       (x+cell_size, y)],
                      fill=c1)
        
        c2=clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.1)))
        image.polygon([(x, y),
                       (x+facet, y+facet),
                       (x+facet, y+cell_size-facet),
                       (x, y+cell_size)],
                      fill=c2)
        
        c3=clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.1)))
        image.polygon([(x, y+cell_size),
                       (x+facet, y+cell_size-facet),
                       (x+cell_size-facet, y+cell_size-facet),
                       (x+cell_size, y+cell_size)],
                      fill=c3)
        
        c4=clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.2)))
        image.polygon([(x+cell_size, y),
                       (x+cell_size-facet, y+facet),
                       (x+cell_size-facet, y+cell_size-facet),
                       (x+cell_size, y+cell_size)],
                      fill=c4)
                
#        image.rectangle([x+facet,
#                         y+facet,
#                         x+cell_size-facet-1,
#                         y+cell_size-facet-1],
#                        fill=color)


class ShapeJewel(BasicShapeJewel):    
    def get_facet(self):
        return self.grid.cell_size/6;

class ShapeJewel2(BasicShapeJewel):    
    def get_facet(self):
        return self.grid.cell_size/4;

class ShapeJewel3(BasicShapeJewel):    
    def get_facet(self):
        return self.grid.cell_size/3;


class GridSquare(base.GridBase):
    def __init__(self):
        self.shapes={
                "flat": ShapeFlat(self),
                "diamond": ShapeDiamond(self),
                "jewel": ShapeJewel(self),
                "jewel2": ShapeJewel2(self),
                "jewel3": ShapeJewel3(self)
                }
        
        

    