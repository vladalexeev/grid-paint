import colorsys

import graphics.color as clr
import grid.base as base


def iso_triangle_points(col, row, side_length):
    col_width=side_length*base.sin60
    y=row*side_length/2
    x=col*col_width
    
    if col % 2 == 0:
        if row % 2 == 0:
            return [
                {'y':y, 'x':x+col_width},
                {'y':y+side_length/2, 'x':x},
                {'y':y+side_length, 'x':x+col_width},
                {'y':y+side_length/2, 'x':x+col_width*2/3}
                ]
        else:
            return [
                {'y':y, 'x':x},
                {'y':y+side_length, 'x':x},
                {'y':y+side_length/2, 'x':x+col_width},
                {'y':y+side_length/2, 'x':x+col_width/3}
                ]
    else:
        if row % 2 == 0:
            return [
                {'y':y, 'x':x},
                {'y':y+side_length, 'x':x},
                {'y':y+side_length/2, 'x':x+col_width},
                {'y':y+side_length/2, 'x':x+col_width/3}
                ]
        else:
            return [
                {'y':y, 'x':x+col_width},
                {'y':y+side_length/2, 'x':x},
                {'y':y+side_length, 'x':x+col_width},
                {'y':y+side_length/2, 'x':x+col_width*2/3}
                ]


class ShapeFlat:
    def __init__(self, grid):
        self.grid=grid
    
    def paint(self, image, col, row, color, dx, dy):
        pp=iso_triangle_points(col, row, self.grid.cell_size);
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
        pp=iso_triangle_points(col, row, self.grid.cell_size);

        
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
        pp=iso_triangle_points(col, row, self.grid.cell_size)
        
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


class BasicShapeFramed:
    def __init__(self, grid):
        self.grid = grid
        self.frame_light = 0

    def paint(self, image, col, row, color, dx, dy):
        rgb = clr.hex_to_rgb(color)
        hls = colorsys.rgb_to_hls(*rgb)
        pp = iso_triangle_points(col, row, self.grid.cell_size)

        if self.frame_light > 0:
            c1 = clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, self.frame_light)))
        else:
            c1 = clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, -self.frame_light)))
        image.polygon(
            [(pp[0]['x'] + dx, pp[0]['y'] + dy),
             (pp[1]['x'] + dx, pp[1]['y'] + dy),
             (pp[2]['x'] + dx, pp[2]['y'] + dy)],
            fill=c1)

        image.polygon(
            [(pp[0]['x'] + (pp[3]['x'] - pp[0]['x']) / 3 + dx, pp[0]['y'] + (pp[3]['y'] - pp[0]['y']) / 3 + dy),
             (pp[1]['x'] + (pp[3]['x'] - pp[1]['x']) / 3 + dx, pp[1]['y'] + (pp[3]['y'] - pp[1]['y']) / 3 + dy),
             (pp[2]['x'] + (pp[3]['x'] - pp[2]['x']) / 3 + dx, pp[2]['y'] + (pp[3]['y'] - pp[2]['y']) / 3 + dy)],
            fill=color)


class ShapeFramedLight(BasicShapeFramed):
    def __init__(self, grid):
        BasicShapeFramed.__init__(self, grid)
        self.frame_light = 0.15


class ShapeFrameDark(BasicShapeFramed):
    def __init__(self, grid):
        BasicShapeFramed.__init__(self, grid)
        self.frame_light = -0.15

class GridIsoTriangle(base.GridBase):
    def __init__(self):
        base.GridBase.__init__(self)
        self.shapes = {
            'flat': ShapeFlat(self),
            'diamond': ShapeDiamond(self),
            'jewel': ShapeJewel(self),
            'frame3u': ShapeFramedLight(self),
            'frame3d': ShapeFrameDark(self),
        }
    

    
