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

class Creature:
    def __init__(self, chromosomeList):
        self.chromosomeList = chromosomeList
        self.renderedGenes = []
        self.fitnessScore = 0
        self.validate()

    def validate(self):
        if type(self.chromosomeList) is not list:
            raise TypeError("Creature must get a list of chromosomes. "+str(type(self.chromosomeList))+" given instead")

        for chrmsm in self.chromosomeList:
            if chrmsm.__class__.__name__ != 'Chromosome':
                raise TypeError("Creature must get Chromosome object. "+str(chrmsm.__class__.__name__)+" given instead")
            else:
                chrmsm.validate()


    def render(self, locX=0, locY=0, locZ=0):
        for chromosome in self.chromosomeList:
            for gene in chromosome.genes:
                self.renderedGenes.append(gene.render(locX, locY, locZ))