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
import operator

class Evolution:
    def __init__(self, population):
        self.population = population

    def fitness(self, fitnessAlgorithms, creatureLimit):

        fintnessScore = []
        i = 0;
        for creature in self.population:
            score = 0
            #loop on algorithms and sum the score
            for weight, algorithm in fitnessAlgorithms.items():
                score+= float(weight) * algorithm.score(creature)
                # print ([float(weight), algorithm.score(creature)])
            creature.fitnessScore = score
            fintnessScore.append((score,creature))
            i+=1

        sorted_x = sorted(fintnessScore, key=operator.itemgetter(0), reverse=True)
        topCreaturesTuples = sorted_x[slice(0,creatureLimit)]
        topCreatures = []
        for creature in topCreaturesTuples:
            topCreatures.append(creature[1])
        return topCreatures

    def reproduce(self, reproductionAlgorithm):
        newCreatures = []

        for creature1 in self.population:
            for creature2 in self.population:
                creature = reproductionAlgorithm.mitosis(creature1, creature2)
                newCreatures.append(creature)
        return newCreatures