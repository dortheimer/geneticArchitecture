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
from ga import creature,chromosome, gene
import random

class reproductionMerger:
    def __init__(self):
        return

    def mitosis(self, creature1, creature2):
        chromoList = []
        #loop on lists
        for i in range(len(creature1.chromosomeList)):
            chromoList.append(chromosome.Chromosome())
            # loop on chromosomes
            for l in range(len(creature1.chromosomeList[i].genes)):
                ptList = []
                # loop on points

                for k in range(len(creature1.chromosomeList[i].genes[l].points)):
                    point = []
                    point.append(creature1.chromosomeList[i].genes[l].points[k][0] + creature2.chromosomeList[i].genes[l].points[k][0])
                    point.append(creature1.chromosomeList[i].genes[l].points[k][1] + creature2.chromosomeList[i].genes[l].points[k][1])
                    point.append(creature1.chromosomeList[i].genes[l].points[k][2] + creature2.chromosomeList[i].genes[l].points[k][2])
                    # point.append(creature1.chromosomeList[i].genes[l].points[l][3] + creature2.chromosomeList[i].genes[l].points[l][3])
                    ptList.append(point);

                newGene = gene.Gene(ptList)
                chromoList[i].genes.append(newGene)

        return creature.Creature(chromoList)
