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
from ga import gene, chromosome, creature
import operator

def main():
    creatures = []
    # rs.EnableRedraw(False)
    matrixSize = 100
    fintnessScore = {}

    # for i in range(-matrixSize,matrixSize):
    #     for j in range(-matrixSize,matrixSize):
    for i in range(matrixSize):
        firstGene = gene.Gene()

        cromosome = chromosome.Chromosome([firstGene])
        cromosome.grow()

        beast = creature.Creature([cromosome])
        # beast.render(i*15,j*15)
        creatures.append(beast)

        fintnessScore[i] = beast.beutifulScore()

    sorted_x = sorted(fintnessScore.iteritems(), key=operator.itemgetter(1))
    topBeasts = sorted_x[slice(0,int(matrixSize/20))]

    i = 0
    for beastIndex in topBeasts:
        creatures[beastIndex[0]].render(i*15,0)
        i+= 1



    # creatures[bestIndex].render()

    # rs.EnableRedraw(True)


main()