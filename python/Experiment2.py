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
from ga import chromosome, creature, evolution, fitness_equilateral, fitness_volume, reproduction_divider, gene
import random
import rhinoscriptsyntax as rs
import copy

def main():
    rs.EnableRedraw(False)
    creatures = []

    # generate creatures
    for i in range(1000):
        firstGene = gene.Gene()
        crmsome = chromosome.Chromosome([firstGene])
        crmsome.grow(20)
        beast = creature.Creature([crmsome])
        creatures.append(beast)

    # initialize evolution engine
    fitnessAlgorithms = {
        '500': fitness_equilateral.fitnessEquilateral(),
        '1': fitness_volume.fitnessVolume()
    }

    # reproductionAlgorithm = reproduction_divider.reproductionDivider()
    #
    engine = evolution.Evolution(creatures)
    engine.population = engine.fitness(fitnessAlgorithms, 15)
    #
    # for iteration in range(10):
    #     engine.population = creatures + engine.reproduce(reproductionAlgorithm)
    #     engine.population = engine.fitness(fitnessAlgorithms, 10)

    #render the best creatures
    i = 0
    j = 0
    for beast in engine.population:
        print(beast.fitnessScore)
        beast.render(i * 50, j * 50)
        i += 1
        if not (i % 5): j += 1; i = 0

        rs.EnableRedraw(True)


main()