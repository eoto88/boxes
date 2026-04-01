# Copyright (C) 2013-2019 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import math
from boxes.walledges import _WallMountedBox
from build.lib.boxes import BoolArg

REINFORCED_MARGIN = 20

class WallSprayCans(_WallMountedBox):
    """Hook to install on a wall"""

    def __init__(self) -> None:
        super().__init__()

        self.buildArgParser()
        self.argparser.add_argument(
            "--width",  action="store", type=float, default=10.0,
            help="width of the back panel")
        self.argparser.add_argument(
            "--can_diameter",  action="store", type=float, default=70.0,
            help="Spray can diameter")
        self.argparser.add_argument(
            "--num_holes",  action="store", type=int, default=4,
            help="Spray can diameter")
        self.argparser.add_argument(
            "--reinforced",  action="store", type=BoolArg(), default=True,
            help="Reinforce shelves")

    def side(self, move=None):
        t = self.thickness
        reinforced = self.reinforced
        diameter = self.can_diameter

        h = 300
        depth = 60
        radius = diameter / 2
        total_depth = depth + radius

        tw = self.edges["b"].spacing() + total_depth + 5

        if self.move(tw, h, move, True):
            return

        self.moveTo(self.edges["b"].margin())
        self.polyline(
            self.edges["b"].startWidth() + depth - t,
            (90, radius),
            h - (radius * 2),
            (90, radius),
            depth,
            90
        )

        self.edges["b"](h)
        # self.edges["e"](h / 2)
        # self.edges["F"](h / 4)

        top_shelf_x = -(h - 5)
        middle_shelf_x = -(h / 2) - (total_depth / 2) + 10
        bottom_shelf_x = -(total_depth - 20)
        self.fingerHolesAt(top_shelf_x, 10, total_depth, 45)
        self.fingerHolesAt(middle_shelf_x, 10, total_depth, 45)
        self.fingerHolesAt(bottom_shelf_x, 10, total_depth, 45)

        if reinforced:
            c = (REINFORCED_MARGIN / 2) * math.sqrt(2)
            self.fingerHolesAt(top_shelf_x + c + t, 10 + c, 15, -45)
            self.fingerHolesAt(middle_shelf_x + c + t, 10 + c, 15, -45)

        self.move(tw, h, move)

    def shelf_with_holes(self, move=None):
        diameter = self.can_diameter
        depth = 60 + diameter
        num_holes = self.num_holes
        width = (diameter * num_holes) + (10 * (num_holes + 1))
        radius = diameter / 2
        holes_x = depth - radius - 10
        reinforced = self.reinforced

        tw = depth + 5

        if self.move(tw, width, move, True):
            return

        self.edges["f"](depth - radius)
        self.corner(90, radius)
        self.edge(width - (radius * 2))
        self.corner(90, radius)
        self.edges["f"](depth - radius)
        self.corner(90)
        self.edge(width)
        self.corner(90)
        for i in range(num_holes):
            if i == 0:
                self.hole(holes_x, width - (radius + 10), r=radius)
            else:
                index = i + 1
                num_radius = (index * 2) - 1
                self.hole(holes_x, width - ((radius * num_radius) + (index * 10)), r=radius)

        if reinforced:
            self.fingerHolesAt(REINFORCED_MARGIN, 0, width, 90)

        self.move(tw, width, move)

    def shelf(self, move=None):
        diameter = self.can_diameter
        num_holes = self.num_holes
        width = (diameter * num_holes) + (10 * (num_holes + 1))
        depth = 110
        radius = 10
        reinforced = self.reinforced

        tw = depth + 5

        if self.move(tw, width, move, True):
            return

        self.edges["f"](depth - radius)
        self.corner(90, radius)
        self.edge(width - (radius * 2))
        self.corner(90, radius)
        self.edges["f"](depth - radius)
        self.corner(90)
        self.edge(width)
        self.corner(90)

        if reinforced:
            self.fingerHolesAt(REINFORCED_MARGIN, 0, width, 90)

        self.move(tw, width, move)

    def render(self):
        self.generateWallEdges()

        h = 300
        t = self.thickness
        reinforced = self.reinforced

        diameter = self.can_diameter
        num_holes = self.num_holes
        width = (diameter * num_holes) + (10 * (num_holes + 1))

        self.rectangularWall(width, h, "eCec", label="Back", move="right")

        self.side(move="right")
        self.side(move="mirror right")

        # self.moveTo(0, 0)


        # self.moveTo(0, h + (t * 2))
        self.shelf_with_holes(move="right")
        # self.moveTo(0, width + (t * 3))
        self.shelf_with_holes(move="right")

        self.shelf(move="right")

        self.moveTo(0, 0)

        if reinforced:
            self.rectangularWall(15, width, "feff", move="right")
            self.rectangularWall(15, width, "feff", move="right")
            self.rectangularWall(15, width, "feff", move="right")

        # self.moveTo(0, h + (t * 3))

        # self.rectangularWall(h, h / 4, "efef", label="Back (bottom)", move="right rotated")
        # self.flangedWall(h, h / 4, flanges=[10, 2*t, 0, 2*t], edges="eeee",
        #                  r=2*t,
        #                  callback=[lambda:(self.wallHolesAt(1.5*t, 0, h / 4, 90), self.wallHolesAt(h+2.5*t, 0, h / 4, 90))], move="up rotated")

        # self.flangedWall(h, h / 4, flanges=[10, 2*t, 0, 2*t], edges="eeee",
        #                  r=2*t,
        #                  callback=[lambda:(self.wallHolesAt(1.5*t, 0, h / 4, 90), self.wallHolesAt(h+2.5*t, 0, h / 4, 90))], move="right rotated")
