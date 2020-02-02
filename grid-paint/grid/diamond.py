import colorsys

import graphics.color as clr
import grid.base as base


def diamond_points(col, row, cell_size):
    d_sub = row * 2
    d_sum = col
    if d_sum % 2 != 0:
        d_sub += 1

    d2 = (d_sum - d_sub) / 2
    d1 = d_sub + d2

    x1 = d1 * cell_size + cell_size / 2
    x2 = d2 * cell_size + cell_size / 2

    x = (x1 + x2) / 2
    y = x1 - x

    half_cell = cell_size / 2

    return [
        {
            'x': x,
            'y': y
        },
        {
            'x': x + half_cell,
            'y': y + half_cell
        },
        {
            'x': x,
            'y': y + cell_size
        },
        {
            'x': x - half_cell,
            'y': y + half_cell
        }
    ]


class ShapeFlat:
    def __init__(self, grid):
        self.grid = grid
    
    def paint(self, image, col, row, color, dx, dy):
        pp = diamond_points(col, row, self.grid.cell_size)
        image.polygon(
            [
                (pp[0]['x']+dx, pp[0]['y']+dy),
                (pp[1]['x']+dx, pp[1]['y']+dy),
                (pp[2]['x']+dx, pp[2]['y']+dy),
                (pp[3]['x'] + dx, pp[3]['y'] + dy),
            ],
            fill=color
        )
        image.point([(pp[0]['x']+dx, pp[0]['y']+dy - 1)], color)


class ShapeDiamond:
    def __init__(self, grid):
        self.grid = grid
        
    def paint(self, image, col, row, color, dx, dy):
        rgb = clr.hex_to_rgb(color)
        hls = colorsys.rgb_to_hls(*rgb)
        points = diamond_points(col, row, self.grid.cell_size)

        cx = points[0]['x']
        cy = points[1]['y']
        
        c1 = clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.2)))
        image.polygon(
            [
                (points[0]['x'] + dx, points[0]['y'] + dy),
                (cx + dx, cy + dy),
                (points[3]['x'] + dx, points[3]['y'] + dy),
            ],
            fill=c1
        )
        
        c2 = clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.1)))
        image.polygon(
            [
                (points[0]['x'] + dx, points[0]['y'] + dy),
                (cx + dx, cy + dy),
                (points[1]['x'] + dx, points[1]['y'] + dy)
            ],
            fill=c2
        )
        
        c3 = clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.1)))
        image.polygon(
            [
                (points[2]['x'] + dx, points[2]['y'] + dy),
                (cx + dx, cy + dy),
                (points[3]['x'] + dx, points[3]['y'] + dy),
            ],
            fill=c3
        )

        c4 = clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.2)))
        image.polygon(
            [
                (points[1]['x'] + dx, points[1]['y'] + dy),
                (cx + dx, cy + dy),
                (points[2]['x'] + dx, points[2]['y'] + dy),
            ],
            fill=c4
        )

        image.point([(points[0]['x'] + dx, points[0]['y'] + dy - 1)], c1)


class ShapeJewel:
    def __init__(self, grid):
        self.grid = grid
        
    def paint(self, image, col, row, color, dx, dy):
        rgb = clr.hex_to_rgb(color)
        hls = colorsys.rgb_to_hls(*rgb)
        points = diamond_points(col, row, self.grid.cell_size)

        facet = self.grid.cell_size / 4

        points2 = [
            {
                'x': points[0]['x'],
                'y': points[0]['y'] + facet
            },
            {
                'x': points[1]['x'] - facet,
                'y': points[1]['y']
            },
            {
                'x': points[2]['x'],
                'y': points[2]['y'] - facet
            },
            {
                'x': points[3]['x'] + facet,
                'y': points[3]['y']
            }
        ]

        c1 = clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.2)))
        image.polygon(
            [
                (points[0]['x'] + dx, points[0]['y'] + dy),
                (points2[0]['x'] + dx, points2[0]['y'] + dy),
                (points2[3]['x'] + dx, points2[3]['y'] + dy),
                (points[3]['x'] + dx, points[3]['y'] + dy),
            ],
            fill=c1
        )

        c2 = clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, 0.1)))
        image.polygon(
            [
                (points[0]['x'] + dx, points[0]['y'] + dy),
                (points2[0]['x'] + dx, points2[0]['y'] + dy),
                (points2[1]['x'] + dx, points2[1]['y'] + dy),
                (points[1]['x'] + dx, points[1]['y'] + dy),
            ],
            fill=c2
        )
        
        c3 = clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.1)))
        image.polygon(
            [
                (points[2]['x'] + dx, points[2]['y'] + dy),
                (points2[2]['x'] + dx, points2[2]['y'] + dy),
                (points2[3]['x'] + dx, points2[3]['y'] + dy),
                (points[3]['x'] + dx, points[3]['y'] + dy),
            ],
            fill=c3
        )

        c4 = clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, 0.2)))
        image.polygon(
            [
                (points[1]['x'] + dx, points[1]['y'] + dy),
                (points2[1]['x'] + dx, points2[1]['y'] + dy),
                (points2[2]['x'] + dx, points2[2]['y'] + dy),
                (points[2]['x'] + dx, points[2]['y'] + dy),
            ],
            fill=c4
        )

        image.polygon(
            [
                (points2[0]['x'] + dx, points2[0]['y'] + dy),
                (points2[1]['x'] + dx, points2[1]['y'] + dy),
                (points2[2]['x'] + dx, points2[2]['y'] + dy),
                (points2[3]['x'] + dx, points2[3]['y'] + dy),
            ],
            fill=color
        )

        image.point([(points[0]['x'] + dx, points[0]['y'] + dy - 1)], c1)


class BasicShapeFramed:
    def __init__(self, grid):
        self.grid = grid
        self.frameLight = 0

    def paint(self, image, col, row, color, dx, dy):
        rgb = clr.hex_to_rgb(color)
        hls = colorsys.rgb_to_hls(*rgb)
        points = diamond_points(col, row, self.grid.cell_size)

        frame = self.grid.cell_size * 0.1
        points2 = [
            {
                'x': points[0]['x'],
                'y': points[0]['y'] + frame
            },
            {
                'x': points[1]['x'] - frame,
                'y': points[1]['y']
            },
            {
                'x': points[2]['x'],
                'y': points[2]['y'] - frame
            },
            {
                'x': points[3]['x'] + frame,
                'y': points[3]['y']
            }
        ]

        if self.frameLight > 0:
            c1 = clr.rgb256(*colorsys.hls_to_rgb(*clr.lighten_hls(hls, self.frameLight)))
        else:
            c1 = clr.rgb256(*colorsys.hls_to_rgb(*clr.darken_hls(hls, -self.frameLight)))

        image.polygon(
            [
                (points[0]['x'] + dx, points[0]['y'] + dy),
                (points[1]['x'] + dx, points[1]['y'] + dy),
                (points[2]['x'] + dx, points[2]['y'] + dy),
                (points[3]['x'] + dx, points[3]['y'] + dy)
            ],
            fill=c1
        )

        image.polygon(
            [
                (points2[0]['x'] + dx, points2[0]['y'] + dy),
                (points2[1]['x'] + dx, points2[1]['y'] + dy),
                (points2[2]['x'] + dx, points2[2]['y'] + dy),
                (points2[3]['x'] + dx, points2[3]['y'] + dy)
            ],
            fill=color
        )

        image.point([(points[0]['x'] + dx, points[0]['y'] + dy - 1)], c1)


class ShapeFramedLight(BasicShapeFramed):
    def __init__(self, grid):
        BasicShapeFramed.__init__(self, grid)
        self.frameLight = 0.15


class ShapeFramedDark(BasicShapeFramed):
    def __init__(self, grid):
        BasicShapeFramed.__init__(self, grid)
        self.frameLight = -0.15


class GridDiamond(base.GridBase):
    def __init__(self):
        base.GridBase.__init__(self)
        self.shapes = {
            'flat': ShapeFlat(self),
            'diamond': ShapeDiamond(self),
            'jewel': ShapeJewel(self),
            'frame10u': ShapeFramedLight(self),
            'frame10d': ShapeFramedDark(self)
        }

    def paint_layer_2(self, image, layer, dx, dy):
        # It is needed to paint pixel in special order for diamond grid
        for row in layer['rows']:
            for cell in row['cells']:
                if cell[0] % 2 == 0:
                    self.paintShape2(image, cell[0], row['row'], cell[1], cell[2], dx, dy)

            for cell in row['cells']:
                if cell[0] % 2 == 1:
                    self.paintShape2(image, cell[0], row['row'], cell[1], cell[2], dx, dy)



