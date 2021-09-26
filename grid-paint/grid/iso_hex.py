import colorsys

import graphics.color as clr
import grid.base as base


def iso_hex_points(col, row, side_length):
    y = (side_length + side_length * base.cos60) * row
    x = 2 * side_length * base.sin60 * col
    half_width = side_length * base.sin60
    dy = side_length * base.cos60
    if row % 2 == 1:
        x += side_length * base.sin60

    return [
        {'y': y, 'x': x + half_width},
        {'y': y + dy, 'x': x},
        {'y': y + dy + side_length, 'x': x},
        {'y': y + 2 * dy + side_length, 'x': x + half_width},
        {'y': y + dy + side_length, 'x': x + 2 * half_width},
        {'y': y + dy, 'x': x + 2 * half_width},
        {'y': y + dy + side_length / 2, 'x': x + half_width}
    ]


class ShapeFlat:
    def __init__(self, grid):
        self.grid = grid

    def paint(self, image, col, row, color, dx, dy):
        pp = iso_hex_points(col, row, self.grid.cell_size / 2)
        image.polygon([(pp[0]['x'] + dx, pp[0]['y'] + dy),
                       (pp[1]['x'] + dx, pp[1]['y'] + dy),
                       (pp[2]['x'] + dx, pp[2]['y'] + dy),
                       (pp[3]['x'] + dx, pp[3]['y'] + dy),
                       (pp[4]['x'] + dx, pp[4]['y'] + dy),
                       (pp[5]['x'] + dx, pp[5]['y'] + dy)],
                      fill=color)


class ShapeDiamond:
    def __init__(self, grid):
        self.grid = grid

    def paint(self, image, col, row, color, dx, dy):
        rgb = clr.hex_to_rgb(color)
        hls = colorsys.rgb_to_hls(*rgb)
        pp = iso_hex_points(col, row, self.grid.cell_size / 2)
        cx = pp[6]['x']
        cy = pp[6]['y']

        c0 = clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.2)))
        image.polygon([(pp[0]['x'] + dx, pp[0]['y'] + dy),
                       (pp[1]['x'] + dx, pp[1]['y'] + dy),
                       (cx + dx, cy + dy)],
                      fill=c0)

        c1 = clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.1)))
        image.polygon([(pp[1]['x'] + dx, pp[1]['y'] + dy),
                       (pp[2]['x'] + dx, pp[2]['y'] + dy),
                       (cx + dx, cy + dy)],
                      fill=c1)

        c2 = clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.1)))
        image.polygon([(pp[2]['x'] + dx, pp[2]['y'] + dy),
                       (pp[3]['x'] + dx, pp[3]['y'] + dy),
                       (cx + dx, cy + dy)],
                      fill=c2)

        c3 = clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.2)))
        image.polygon([(pp[3]['x'] + dx, pp[3]['y'] + dy),
                       (pp[4]['x'] + dx, pp[4]['y'] + dy),
                       (cx + dx, cy + dy)],
                      fill=c3)

        c4 = c2
        image.polygon([(pp[4]['x'] + dx, pp[4]['y'] + dy),
                       (pp[5]['x'] + dx, pp[5]['y'] + dy),
                       (cx + dx, cy + dy)],
                      fill=c4)

        c5 = c1
        image.polygon([(pp[5]['x'] + dx, pp[5]['y'] + dy),
                       (pp[0]['x'] + dx, pp[0]['y'] + dy),
                       (cx + dx, cy + dy)],
                      fill=c5)


class ShapeCube:
    def __init__(self, grid):
        self.grid = grid

    def paint(self, image, col, row, color, dx, dy):
        rgb = clr.hex_to_rgb(color)
        hls = colorsys.rgb_to_hls(*rgb)
        pp = iso_hex_points(col, row, self.grid.cell_size / 2)
        cx = pp[6]['x']
        cy = pp[6]['y']

        c0 = clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.2)))
        image.polygon([(pp[0]['x'] + dx, pp[0]['y'] + dy),
                       (pp[1]['x'] + dx, pp[1]['y'] + dy),
                       (pp[2]['x'] + dx, pp[2]['y'] + dy),
                       (cx + dx, cy + dy)],
                      fill=c0)

        c1 = color
        image.polygon([(pp[2]['x'] + dx, pp[2]['y'] + dy),
                       (pp[3]['x'] + dx, pp[3]['y'] + dy),
                       (pp[4]['x'] + dx, pp[4]['y'] + dy),
                       (cx + dx, cy + dy)],
                      fill=c1)

        c2 = clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.2)))
        image.polygon([(pp[4]['x'] + dx, pp[4]['y'] + dy),
                       (pp[5]['x'] + dx, pp[5]['y'] + dy),
                       (pp[0]['x'] + dx, pp[0]['y'] + dy),
                       (cx + dx, cy + dy)],
                      fill=c2)


class ShapeJewel:
    def __init__(self, grid):
        self.grid = grid

    def paint(self, image, col, row, color, dx, dy):
        rgb = clr.hex_to_rgb(color)
        hls = colorsys.rgb_to_hls(*rgb)
        pp = iso_hex_points(col, row, self.grid.cell_size / 2)
        cx = pp[6]['x']
        cy = pp[6]['y']

        c0 = clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.2)))
        image.polygon([(pp[0]['x'] + dx, pp[0]['y'] + dy),
                       (pp[1]['x'] + dx, pp[1]['y'] + dy),
                       (pp[1]['x'] + dx + (cx - pp[1]['x']) / 2, pp[1]['y'] + dy + (cy - pp[1]['y']) / 2),
                       (pp[0]['x'] + dx + (cx - pp[0]['x']) / 2, pp[0]['y'] + dy + (cy - pp[0]['y']) / 2)],
                      fill=c0)

        c1 = clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.1)))
        image.polygon([(pp[1]['x'] + dx, pp[1]['y'] + dy),
                       (pp[2]['x'] + dx, pp[2]['y'] + dy),
                       (pp[2]['x'] + dx + (cx - pp[2]['x']) / 2, pp[2]['y'] + dy + (cy - pp[2]['y']) / 2),
                       (pp[1]['x'] + dx + (cx - pp[1]['x']) / 2, pp[1]['y'] + dy + (cy - pp[1]['y']) / 2)],
                      fill=c1)

        c2 = clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.1)))
        image.polygon([(pp[2]['x'] + dx, pp[2]['y'] + dy),
                       (pp[3]['x'] + dx, pp[3]['y'] + dy),
                       (pp[3]['x'] + dx + (cx - pp[3]['x']) / 2, pp[3]['y'] + dy + (cy - pp[3]['y']) / 2),
                       (pp[2]['x'] + dx + (cx - pp[2]['x']) / 2, pp[2]['y'] + dy + (cy - pp[2]['y']) / 2)],
                      fill=c2)

        c3 = clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.2)))
        image.polygon([(pp[3]['x'] + dx, pp[3]['y'] + dy),
                       (pp[4]['x'] + dx, pp[4]['y'] + dy),
                       (pp[4]['x'] + dx + (cx - pp[4]['x']) / 2, pp[4]['y'] + dy + (cy - pp[4]['y']) / 2),
                       (pp[3]['x'] + dx + (cx - pp[3]['x']) / 2, pp[3]['y'] + dy + (cy - pp[3]['y']) / 2)],
                      fill=c3)

        c4 = c2
        image.polygon([(pp[4]['x'] + dx, pp[4]['y'] + dy),
                       (pp[5]['x'] + dx, pp[5]['y'] + dy),
                       (pp[5]['x'] + dx + (cx - pp[5]['x']) / 2, pp[5]['y'] + dy + (cy - pp[5]['y']) / 2),
                       (pp[4]['x'] + dx + (cx - pp[4]['x']) / 2, pp[4]['y'] + dy + (cy - pp[4]['y']) / 2)],
                      fill=c4)

        c5 = c1
        image.polygon([(pp[5]['x'] + dx, pp[5]['y'] + dy),
                       (pp[0]['x'] + dx, pp[0]['y'] + dy),
                       (pp[0]['x'] + dx + (cx - pp[0]['x']) / 2, pp[0]['y'] + dy + (cy - pp[0]['y']) / 2),
                       (pp[5]['x'] + dx + (cx - pp[5]['x']) / 2, pp[5]['y'] + dy + (cy - pp[5]['y']) / 2)],
                      fill=c5)

        image.polygon([(pp[0]['x'] + dx + (cx - pp[0]['x']) / 2, pp[0]['y'] + dy + (cy - pp[0]['y']) / 2),
                       (pp[1]['x'] + dx + (cx - pp[1]['x']) / 2, pp[1]['y'] + dy + (cy - pp[1]['y']) / 2),
                       (pp[2]['x'] + dx + (cx - pp[2]['x']) / 2, pp[2]['y'] + dy + (cy - pp[2]['y']) / 2),
                       (pp[3]['x'] + dx + (cx - pp[3]['x']) / 2, pp[3]['y'] + dy + (cy - pp[3]['y']) / 2),
                       (pp[4]['x'] + dx + (cx - pp[4]['x']) / 2, pp[4]['y'] + dy + (cy - pp[4]['y']) / 2),
                       (pp[5]['x'] + dx + (cx - pp[5]['x']) / 2, pp[5]['y'] + dy + (cy - pp[5]['y']) / 2)],
                      fill=color)


class BasicShapeFramed:
    def __init__(self, grid):
        self.grid = grid
        self.frame_light = 0

    def paint(self, image, col, row, color, dx, dy):
        rgb = clr.hex_to_rgb(color)
        hls = colorsys.rgb_to_hls(*rgb)
        pp = iso_hex_points(col, row, self.grid.cell_size / 2)
        cx = pp[6]['x']
        cy = pp[6]['y']

        if self.frame_light > 0:
            c0 = clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, self.frame_light)))
        else:
            c0 = clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, -self.frame_light)))

        image.polygon([(pp[0]['x'] + dx, pp[0]['y'] + dy),
                       (pp[1]['x'] + dx, pp[1]['y'] + dy),
                       (pp[2]['x'] + dx, pp[2]['y'] + dy),
                       (pp[3]['x'] + dx, pp[3]['y'] + dy),
                       (pp[4]['x'] + dx, pp[4]['y'] + dy),
                       (pp[5]['x'] + dx, pp[5]['y'] + dy)],
                      fill=c0)

        image.polygon([(pp[0]['x'] + dx + (cx - pp[0]['x']) / 4, pp[0]['y'] + dy + (cy - pp[0]['y']) / 4),
                       (pp[1]['x'] + dx + (cx - pp[1]['x']) / 4, pp[1]['y'] + dy + (cy - pp[1]['y']) / 4),
                       (pp[2]['x'] + dx + (cx - pp[2]['x']) / 4, pp[2]['y'] + dy + (cy - pp[2]['y']) / 4),
                       (pp[3]['x'] + dx + (cx - pp[3]['x']) / 4, pp[3]['y'] + dy + (cy - pp[3]['y']) / 4),
                       (pp[4]['x'] + dx + (cx - pp[4]['x']) / 4, pp[4]['y'] + dy + (cy - pp[4]['y']) / 4),
                       (pp[5]['x'] + dx + (cx - pp[5]['x']) / 4, pp[5]['y'] + dy + (cy - pp[5]['y']) / 4)],
                      fill=color)


class ShapeFramedLight(BasicShapeFramed):
    def __init__(self, grid):
        BasicShapeFramed.__init__(self, grid)
        self.frame_light = 0.15


class ShapeFramedDark(BasicShapeFramed):
    def __init__(self, grid):
        BasicShapeFramed.__init__(self, grid)
        self.frame_light = -0.15


class GridIsoHex(base.GridBase):
    def __init__(self):
        base.GridBase.__init__(self)
        self.shapes = {
            'flat': ShapeFlat(self),
            'diamond': ShapeDiamond(self),
            'jewel': ShapeJewel(self),
            'cube': ShapeCube(self),
            'frame4u': ShapeFramedLight(self),
            'frame4d': ShapeFramedDark(self)
        }