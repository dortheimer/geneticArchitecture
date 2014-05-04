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

class fitnessEquilateral:
    def __init__(self):
        return

    def score(self, creature):
        totalScore = 0
        genesCount = 0
        for chromosome in creature.chromosomeList:
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