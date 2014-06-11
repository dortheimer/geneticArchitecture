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
# import rhinoscriptsyntax as rs

class fitnessSize:
    def __init__(self):
        return

    def score(self, creature):

        #find bounding box
        minX = minY = minZ = 0
        maxX = maxY = maxZ = 0
        counter = 0
        for chromosome in creature.chromosomeList:

            for gene in chromosome.genes:
                for point in gene.points:
                    if point[0] > maxX: maxX = point[0]
                    if point[1] > maxY: maxY = point[1]
                    if point[2] > maxZ: maxZ = point[2]

                    if point[0] < minX: minX = point[0]
                    if point[1] < minY: minY = point[1]
                    if point[2] < minZ: minZ = point[2]

                    counter+=1

        return abs(maxX-minX) * abs(maxY-minY) * abs(maxZ-minZ)/counter

