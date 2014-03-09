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
        self.polygons = []

    def render(self, locX=0, locY=0, locZ=0):
        for chromosome in self.chromosomeList:
            for gene in chromosome.genes:
                polygon = self.renderPolygon(gene.points, locX, locY, locZ)
                self.polygons.append(polygon)


    def renderPolygon(self, pts, offsetX, offsetY, offsetZ):
        surfaces = []
        # for x in range(4):
        #     for y in range(4):
        #         for z in range(4):
        #             if x != y and x != z and y != x:
                        # surface = rs.AddSrfPt([
                        #     [pts[x][0] + offsetX, pts[x][1] + offsetY, pts[x][2] + offsetZ],
                        #     [pts[y][0] + offsetX, pts[y][1] + offsetY, pts[y][2] + offsetZ],
                        #     [pts[z][0] + offsetX, pts[z][1] + offsetY, pts[z][2] + offsetZ]])
                        # surfaces.append(surface)
      # return surfaces

        polyline = rs.AddPolyline([
            [pts[0][0] + offsetX, pts[0][1] + offsetY, pts[0][2] + offsetZ],
            [pts[1][0] + offsetX, pts[1][1] + offsetY, pts[1][2] + offsetZ],
            [pts[2][0] + offsetX, pts[2][1] + offsetY, pts[2][2] + offsetZ],
            [pts[0][0] + offsetX, pts[0][1] + offsetY, pts[0][2] + offsetZ]])
        point = [pts[3][0] + offsetX, pts[3][1] + offsetY, pts[3][2] + offsetZ]
        solid = rs.ExtrudeCurvePoint( polyline, point )
        rs.DeleteObject(polyline)

        # cup
        # bool union
        return solid

    def sizeScore(self):
        #find bounding box
        minX = minY = minZ = 0
        maxX = maxY = maxZ = 0
        for chromosome in self.chromosomeList:
            for gene in chromosome.genes:
                for point in gene.points:
                    if point[0] > maxX: maxX = point[0]
                    if point[1] > maxY: maxY = point[1]
                    if point[2] > maxZ: maxZ = point[2]

                    if point[0] < minX: minX = point[0]
                    if point[1] < minY: minY = point[1]
                    if point[2] < minZ: minZ = point[2]

        volume = abs(maxX-minX) * abs(maxY-minY) * abs(maxZ-minZ)
        return volume

    def beutifulScore(self):
        totalScore = 0
        genesCount = 0
        for chromosome in self.chromosomeList:
            for gene in chromosome.genes:
                totalScore+= self.geneSymetryScore(gene)
                genesCount+=1
        return totalScore/genesCount

    def geneSymetryScore(self, gene):
        distances = []
        # get distances
        for point1 in gene.points:
            for point2 in gene.points:
                distances.append(rs.Distance(point1,point2))

        offsets = []
        # get offsets
        for dis1 in distances:
            for dis2 in distances:
                if dis1 and dis2:
                    offset = abs(dis1-dis2)
                    offsets.append(offset)

        return float(sum(offsets))/len(offsets)
