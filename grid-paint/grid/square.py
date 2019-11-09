# -*- coding: utf-8 -*-

import math

import graphics.color as clr
import grid.base as base

import colorsys


class BasicShape:
    def __init__(self, grid):
        self.grid=grid


class BasicShapeFlat(BasicShape):
    def __init__(self, grid):
        BasicShape.__init__(self,grid)
        self.facet=self.get_facet()
        
    def get_facet(self):
        raise NotImplementedError("Should implement this method")
    
    def paint(self, image, col, row, color, dx, dy):
        x=col*self.grid.cell_size+dx
        y=row*self.grid.cell_size+dy
        facet = self.facet
        image.polygon([(x+facet,y+facet),
                       (x+facet, y+self.grid.cell_size-facet),
                       (x+self.grid.cell_size-facet, y+self.grid.cell_size-facet),
                       (x+self.grid.cell_size-facet, y+facet)],
                      fill=color)


class ShapeFlat(BasicShapeFlat):
    def get_facet(self):
        return 0


class ShapeFlat1(BasicShapeFlat):
    def get_facet(self):
        return self.grid.cell_size/6


class ShapeFlat2(BasicShapeFlat):
    def get_facet(self):
        return self.grid.cell_size/4


class ShapeFlat3(BasicShapeFlat):
    def get_facet(self):
        return self.grid.cell_size/3


class BasicShapeCircle(BasicShape):
    def __init__(self, grid):
        BasicShape.__init__(self,grid)
        self.facet=self.get_facet();
        
    def get_facet(self):
        raise NotImplementedError("Should implement this method")
    
    def paint(self, image, col, row, color, dx, dy):
        x=col*self.grid.cell_size+dx
        y=row*self.grid.cell_size+dy
        facet = self.facet
        image.ellipse([(x+facet,y+facet),
                       (x+self.grid.cell_size-facet, y+self.grid.cell_size-facet)],
                      fill=color)


class ShapeCircle(BasicShapeCircle):
    def get_facet(self):
        return 0


class ShapeCircle1(BasicShapeCircle):
    def get_facet(self):
        return self.grid.cell_size/6


class ShapeCircle2(BasicShapeCircle):
    def get_facet(self):
        return self.grid.cell_size/4


class ShapeCircle3(BasicShapeCircle):
    def get_facet(self):
        return self.grid.cell_size/3
        
        
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
        self.facet=self.get_facet()
        
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


class ShapeJewel(BasicShapeJewel):    
    def get_facet(self):
        return self.grid.cell_size/6


class ShapeJewel2(BasicShapeJewel):    
    def get_facet(self):
        return self.grid.cell_size/4


class ShapeJewel3(BasicShapeJewel):    
    def get_facet(self):
        return self.grid.cell_size/3


class BasicShapeFramed(BasicShape):
    def __init__(self, grid):
        BasicShape.__init__(self, grid)
        self.frame_width = 0
        self.frame_light = 0

    def paint(self, image, col, row, color, dx, dy):
        x = col * self.grid.cell_size + dx
        y = row * self.grid.cell_size + dy
        facet = self.grid.cell_size * self.frame_width

        rgb = clr.hex_to_rgb(color)
        hls = colorsys.rgb_to_hls(*rgb)
        if self.frame_light > 0:
            frame_color = clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, self.frame_light)))
        else:
            frame_color = clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, -self.frame_light)))

        image.polygon([
            (x, y),
            (x, y + self.grid.cell_size),
            (x + self.grid.cell_size, y + self.grid.cell_size),
            (x + self.grid.cell_size, y)
        ], fill=frame_color)

        image.polygon([(x + facet, y + facet),
                       (x + facet, y + self.grid.cell_size - facet),
                       (x + self.grid.cell_size - facet, y + self.grid.cell_size - facet),
                       (x + self.grid.cell_size - facet, y + facet)],
                      fill=color)


class ShapeFramed5Dark(BasicShapeFramed):
    def __init__(self, grid):
        BasicShapeFramed.__init__(self, grid)
        self.frame_width = 0.05
        self.frame_light = -0.15


class ShapeFramed10Dark(BasicShapeFramed):
    def __init__(self, grid):
        BasicShapeFramed.__init__(self, grid)
        self.frame_width = 0.10
        self.frame_light = -0.15


class ShapeFramed5Light(BasicShapeFramed):
    def __init__(self, grid):
        BasicShapeFramed.__init__(self, grid)
        self.frame_width = 0.05
        self.frame_light = 0.15


class ShapeFramed10Light(BasicShapeFramed):
    def __init__(self, grid):
        BasicShapeFramed.__init__(self, grid)
        self.frame_width = 0.10
        self.frame_light = 0.15


class GridSquare(base.GridBase):
    def __init__(self):
        base.GridBase.__init__(self)
        self.shapes={
            "flat": ShapeFlat(self),
            "flat1": ShapeFlat1(self),
            "flat2": ShapeFlat2(self),
            "flat3": ShapeFlat3(self),
            "circle": ShapeCircle(self),
            "circle1": ShapeCircle1(self),
            "circle2": ShapeCircle2(self),
            "circle3": ShapeCircle3(self),
            "diamond": ShapeDiamond(self),
            "jewel": ShapeJewel(self),
            "jewel2": ShapeJewel2(self),
            "jewel3": ShapeJewel3(self),
            "frame5d": ShapeFramed5Dark(self),
            "frame10d": ShapeFramed10Dark(self),
            "frame5u": ShapeFramed5Light(self),
            "frame10u": ShapeFramed10Light(self),
        }
        
    def paintGrid(self, image, color, left, top, width, height, dx=0, dy=0):
        startx = int(math.floor(left / self.cell_size)) * self.cell_size
        starty = int(math.floor(top / self.cell_size)) * self.cell_size
        
        for x in xrange(startx, left+width, self.cell_size):
            image.line([(x+dx, top+dy), (x+dx, top+height+dy)], fill=color, width=1)
            
        for y in xrange(starty, top+height, self.cell_size):
            image.line([(left+dx, y+dy), (left+width+dx, y+dy)], fill=color, width=1)
            
    def paintPoint(self, image, col, row, color, dx, dy):
        image.point((col+dx, row+dy), color)
        

    
