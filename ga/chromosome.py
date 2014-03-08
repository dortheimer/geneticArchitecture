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

import random
from ga import gene

class Chromosome:
    def __init__(self, geneList):
        self.genes = geneList

    def grow(self, growSize=20):
        for index in range(growSize):
            removeIndex = random.randint(0,self.genes[index].size()-1)

            #find plane center
            planePts = []
            for i in range(self.genes[index].size()):
                if (i!=removeIndex):
                    planePts.append(self.genes[index].points[i])

            planeCenter = self.findCenter(planePts)

            opposite = [
                2*planeCenter[0]-self.genes[index].points[removeIndex][0],
                2*planeCenter[1]-self.genes[index].points[removeIndex][1],
                2*planeCenter[2]-self.genes[index].points[removeIndex][2]]

            point = [
                opposite[0]+random.random()*4-2 ,
                opposite[1]+random.random()*4-2,
                opposite[2]+random.random()*4-2]

            planePts.append(point)
            newGene = gene.Gene(planePts)

            self.genes.append(newGene)

    def findCenter(self, pts):
        x = y = z = 0

        l = len(pts)
        for i in range(l):
            x+= pts[i][0]
            y+= pts[i][1]
            z+= pts[i][2]

        return [x/l, y/l, z/l]