# The MIT License (MIT)
#
# Copyright (c) 2014 Jonathan Dortheimer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import rhinoscriptsyntax as rs


class Creature:
    def __init__(self, chromosomeList):
        self.chromosomeList = chromosomeList
        self.poligons = []

    def render(self, locX = 0, locY = 0, locZ = 0):
        for chromosome in self.chromosomeList:
            for gene in chromosome.genes:
                poligon = self.renderPolygon(gene.points, locX, locY, locZ)
                self.poligons.append(poligon)


    def renderPolygon(self,pts, offsetX, offsetY, offsetZ):
        surfaces = []
        for x in range(4):
            for y in range(4):
                for z in range (4):
                    if x!=y and x!=z and y!=x:

                        surface = rs.AddSrfPt([
                            [pts[x][0]+offsetX, pts[x][1]+offsetY, pts[x][2]+offsetZ],
                            [pts[y][0]+offsetX, pts[y][1]+offsetY, pts[y][2]+offsetZ],
                            [pts[z][0]+offsetX, pts[z][1]+offsetY, pts[z][2]+offsetZ]])
                        surfaces.append(surface)

        return surfaces