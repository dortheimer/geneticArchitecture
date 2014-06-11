# The MIT License (MIT)
#
# Copyright (c) 2014 Tom Shaked & Jonathan Dortheimer
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
from ga import chromosome, creature, evolution, fitness_equilateral, fitness_size, reproduction_divider
import random
#import rhinoscriptsyntax as rs
import math
import copy
import time


class Gene:
    def __init__(self, points=None, boundingPolygon=None):

        self.maxX = 0
        self.minX = 0
        self.minY = 0
        self.maxY = 0
        if boundingPolygon:
            self.setBoundingPolygon(boundingPolygon)
        if points is None:
            self.generateRandom()
        else:
            self.points = points

    # determine if a point is inside a given polygon or not
    # Polygon is a list of (x,y) pairs.
    def point_inside_polygon(self,x,y,poly):

        n = len(poly)
        inside =False
        p1x,p1y = poly[0]
        for i in range(n+1):
            p2x,p2y = poly[i % n]
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x,p1y = p2x,p2y

        return inside

    def setBoundingPolygon(self, boundingPolygon):

        self.boundingPolygon = boundingPolygon
        for pt in boundingPolygon:
            if pt[0]> self.maxX:
                # print(pt[0],self.maxX)
                self.maxX = pt[0]
            if pt[1]> self.maxY:
                self.maxY = pt[1]
            if pt[0]< self.minX:
                self.minX = pt[0]
            if pt[1]< self.minY:
                self.minY = pt[1]

    def generateRandom(self):
        self.points = []
        for x in range(10):
            point = [self.rand(self.minX,self.maxX),self.rand(self.minY, self.maxY),0]
            while True != self.point_inside_polygon(point[0],point[1],self.boundingPolygon):
                point = [self.rand(self.minX,self.maxX),self.rand(self.minY, self.maxY),0]
            self.points.append(point)

    def rand(self,min=None,max=None):
        if min == None: min = 0
        if max == None: max = 0


        return min + random.random()* (max-min)

    def size(self):
        return len(self.points)

    def grow(self):
        pts = [];
        for x in range(10):
            point = [self.rand(self.minX,self.maxX),self.rand(self.minY, self.maxY),self.points[0][2]+20]
            while True != self.point_inside_polygon(point[0],point[1],self.boundingPolygon):
                point = [self.rand(self.minX,self.maxX),self.rand(self.minY, self.maxY),self.points[0][2]+20]
            pts.append(point)
        return Gene(pts,self.boundingPolygon)


    def render(self, offsetX, offsetY, offsetZ):
        for i in range(len(self.points)) :
            tempP =  [self.points[i][0] + offsetX, self.points[i][1] + offsetY, self.points[i][2] + offsetZ]
            #rs.AddPoint(tempP)


def renderFile(f, creature, offsetX, offsetY, offsetZ):
    oldPoints = False
    for chromosome in creature.chromosomeList:
        for y in range(len(chromosome.genes)):

            #fileWrite(f, "rs.AddSrfPt([")
            i=0
            newPoints = []
            for point in chromosome.genes[y].points:
                p1 = str(float(point[0])+float(offsetX))
                p2 = str(float(point[1])+float(offsetY))
                p3 = str(float(point[2])+float(offsetZ))
                newPoints.append([p1,p2,p3])

            newPoints = reOrder(newPoints)

            fileWrite(f, "curve"+str(y)+" = rs.AddPolyline(["+doPolygon(newPoints)+"])")
            #extrude
            # fileWrite(f, "rs.ExtrudeCurveStraight( curve, ["+str(newPoints[0][0])+","+str(newPoints[0][1])+","+str(newPoints[0][2])+
            #              "],  ["+str(newPoints[0][0])+","+str(newPoints[0][1])+","+str(float(newPoints[0][2])+20)+"])")
            if oldPoints != False:
                fileWrite(f, "rs.AddLoftSrf( [curve"+str(y)+",curve"+str(y-1)+"])")

            oldPoints = newPoints


def reOrder(p):
    # center
    xs = 0;
    ys = 0;
    for p1 in p:
        ys = ys + float(p1[1])
        xs = xs + float(p1[0])
    center = [
        xs / len(p),
        ys / len(p)
    ]
    rad = []
    for p1 in p:
        val = [
            p1,
            math.atan2(float(p1[0])-center[0], float(p1[1])-center[1])
        ]
        rad.append(val)
    # print(rad)
    sort = sorted(rad, key=lambda x: x[1])

    rt = []
    for p1 in sort:
        rt.append(p1[0])

    return rt


def doPolygon(points):

    l = len(points)-1
    if points[0][0]!= points[l][0] or points[0][1]!=points[l][1]:
        points.append(points[0])
    return (', '.join([str(x) for x in points]))
    # return "rs.AddPolyline (["+p1+","+p2+","+p3+"])")


class fitnessAlgo:
    def __init__(self):
        return

    def score(self, creature):
        num = 0
        offset = 0
        oldPoint =[]
        for chromo in creature.chromosomeList:
            for line in range(len(chromo.genes[0].points)):
                for story in range(len(chromo.genes)):
                    num = num + 1
                    point = chromo.genes[story].points[line]
                    if len(oldPoint)!=0:
                        offset = offset + math.sqrt(abs(point[0]--oldPoint[0])**2 + abs(point[1]--oldPoint[1])**2)
                    oldPoint = point
        avg = offset/num/len(chromo.genes)
        score = 100 - abs(3-avg)
        # print(score)
        return score


def fileWrite(f,txt):
    f.seek(0,2)
    f.write(txt+"\n")

class reproduction_divider:
    def __init__(self):
        return

    def mitosis(self, creature1, creature2):
        chromo = []

        #cut this in half
        for i in range(len(creature1.chromosomeList)):
            genes = []
            for j in range(len(creature1.chromosomeList[i].genes)):
                if random.randint(0,1):
                    genes.append(creature1.chromosomeList[i].genes[j])
                else:
                    genes.append(creature2.chromosomeList[i].genes[j])
            chromo.append(chromosome.Chromosome( genes))
        return creature.Creature(chromo)


def main():
    #rs.EnableRes = draw(False)
    creatures = []
    boundingPolygon = [
        [0,0],
        [70,5],
        [75,60],
        [80,30],
        [10,50],
        [0,0]
    ]

    # generate creatures
    for i in range(1000):
        firstGene = Gene(None,boundingPolygon)
        crmsome = chromosome.Chromosome([firstGene])
        crmsome.grow(10)
        beast = creature.Creature([crmsome])
        creatures.append(beast)

    # initialize evolution engine
    fitnessAlgorithms = {
        '1': fitnessAlgo()    }
    #
    reproductionAlgorithm = reproduction_divider()
    #
    engine = evolution.Evolution(creatures)
    engine.population = engine.fitness(fitnessAlgorithms, 100)
    #
    for iteration in range(10):
        print ("Begin "+str(len( engine.population))+" creatures")
        engine.population = creatures + engine.reproduce(reproductionAlgorithm)
        print ("Reproduction "+str(len(engine.population))+" creatures")
        engine.population = engine.fitness(fitnessAlgorithms, 100)
        print ("Fitness "+str(len( engine.population))+" creatures")

    engine.population = engine.fitness(fitnessAlgorithms, 1)
    #render the best creatures
    i = 0
    j = 0
    f = open('generated/workfile'+str(time.time())+'.py', 'w')
    fileWrite(f,"import rhinoscriptsyntax as rs")
    fileWrite(f, "rs.EnableRedraw(False)")
    for beast in engine.population:
        # print(beast.fitnessScore)
        # myRender(beast,i * 500, j * 500)
        renderFile(f, beast, i * 500, j * 500, 0)
        i += 1
        if not (i % 5): j += 1; i = 0


        #rs.EnableRedraw(True)
    fileWrite(f, "rs.EnableRedraw(True)")
    f.close()
main()