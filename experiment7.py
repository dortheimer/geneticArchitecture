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


class StructureGene:
    def __init__(self, points=None, boundingPolygon=None):

        self.maxX = 0
        self.minX = 0
        self.minY = 0
        self.maxY = 0
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

        self.points = reOrder(self.points)

    def rand(self,min=None,max=None):
        if min == None: min = 0
        if max == None: max = 0
        return min + random.random()* (max-min)

    def size(self):
        return len(self.points)

    def grow(self):
        pts = [];
        z = z1 = self.points[0][2]+20
        # print(self.points)
        # print("------------")
        for x in range(10):
            # if x > 0:
            z = self.rand(z1-5, z1+5)

            point = [self.rand(self.minX,self.maxX),self.rand(self.minY, self.maxY),z]
            while True != self.point_inside_polygon(point[0],point[1],self.boundingPolygon):
                point = [self.rand(self.minX,self.maxX),self.rand(self.minY, self.maxY),z]
            pts.append(point)

        pts = reOrder(pts)
        return StructureGene(pts,self.boundingPolygon)


    def render(self, offsetX, offsetY, offsetZ):
        for i in range(len(self.points)) :
            tempP =  [self.points[i][0] + offsetX, self.points[i][1] + offsetY, self.points[i][2] + offsetZ]
            #rs.AddPoint(tempP)


def renderFile(f, creature, offsetX, offsetY, offsetZ):
    oldPoints = False

    for y in range(len(creature.chromosomeList[0].genes)):
        i=0
        newPoints = []
        for point in creature.chromosomeList[0].genes[y].points:
            p1 = str(float(point[0])+float(offsetX))
            p2 = str(float(point[1])+float(offsetY))
            p3 = str(float(point[2])+float(offsetZ))
            newPoints.append([p1,p2,p3])

        fileWrite(f, "curve"+str(y)+" = rs.AddPolyline(["+doPolygon(newPoints)+"])")
        fileWrite(f, "rs.RebuildCurve ( curve"+str(y)+", degree=3, point_count=10)")
        fileWrite(f, "curves.append(curve"+str(y)+")")

def reOrder(p):
    # center
    center = polyCenter(p)
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

def polyCenter(p):
    xs = 0;
    ys = 0;
    for p1 in p:
        ys = ys + float(p1[1])
        xs = xs + float(p1[0])
    return [
        xs / len(p),
        ys / len(p)
    ]

def doPolygon(points):

    l = len(points)-1
    if points[0][0]!= points[l][0] or points[0][1]!=points[l][1]:
        points.append(points[0])
    return (', '.join([str(x) for x in points]))
    # return "rs.AddPolyline (["+p1+","+p2+","+p3+"])")

class scopeSizeAlgo:
     def __init__(self):
        return
     def score(self, creature):
        score = [];

        for geneIndex in range(len(creature.chromosomeList[0].genes)):
            scope = polyScope(creature.chromosomeList[0].genes[geneIndex].points)
            area = polyArea(creature.chromosomeList[0].genes[geneIndex].points)

            score.append(area / scope)
        return sum(score)/len(score)

class sizeAlgo:
     def __init__(self):
        return
     def score(self, creature):
        score = [];
        for geneIndex in range(len(creature.chromosomeList[0].genes)):
            area = polyArea(creature.chromosomeList[0].genes[geneIndex].points)
            score.append(area)
        return sum(score)

class fitnessAlgo:
    def __init__(self):
        return

    def score(self, creature):
        num = 0
        offset = 0
        oldPoint =[]

        for line in range(len(creature.chromosomeList[0].genes[0].points)):
            for story in range(len(creature.chromosomeList[0].genes)):
                num = num + 1
                point = creature.chromosomeList[0].genes[story].points[line]
                if len(oldPoint)!=0:
                    offset = offset + pythagoras(point,oldPoint)
                oldPoint = point
        avg = offset/num/len(creature.chromosomeList[0].genes)
        score = 100 - abs(3-avg)
        return score


def pythagoras(pt1,pt2):
    return math.sqrt(math.pow(abs(pt2[0] - pt1[0]),2)+ math.pow(abs(pt2[1] - pt1[1]),2))

def polyScope(p):
    oldPt = p[0]
    ln = 0
    for newPt in p:
        ln = ln + pythagoras(newPt,oldPt)
        oldPt = newPt
    return ln

def polyArea(pts):
    center = polyCenter(pts)
    area = 0
    for i in range(len(pts)-1):
        sideA = pythagoras(pts[i],pts[i+1])
        sideB = pythagoras(pts[i],center)
        sideC = pythagoras(pts[i+1],center)
        p = (sideA + sideB + sideC)/2
        area = area + math.sqrt( p * (p-sideA) * (p-sideB) * (p-sideC))
    return area



def fileWrite(f,txt):
    f.seek(0,2)
    f.write(txt+"\n\r")

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

def initFile():

    f = open('generated/workfile'+str(time.time())+'.py', 'w')
    fileWrite(f,"import rhinoscriptsyntax as rs")
    fileWrite(f, "rs.EnableRedraw(False)")
    fileWrite(f, "curves=[]")
    return f

def closeFile(f):
    fileWrite(f, "srf = rs.AddLoftSrf(curves)")
    fileWrite(f, "rs.EnableRedraw(True)")
    f.close()

def getRandomCreatures(howMany, howBig, boundingPolygon):
    creatures = []
    for i in range(howMany):
        gene1 = StructureGene(None,boundingPolygon)
        crmsome1 = chromosome.Chromosome([gene1])
        crmsome1.grow(howBig)
        beast = creature.Creature([crmsome1])
        creatures.append(beast)
    return creatures

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
    creatures = getRandomCreatures(1000,10, boundingPolygon);

    # initialize evolution engine
    fitnessAlgorithms = {
        '1.2': fitnessAlgo(),
        '20': scopeSizeAlgo(),
        '0.01': sizeAlgo()
    }
    #
    reproductionAlgorithm = reproduction_divider()
    #
    engine = evolution.Evolution(creatures)
    engine.population = engine.fitness(fitnessAlgorithms, 20)
    #
    for iteration in range(3):
        print ("Begin "+str(len( engine.population))+" creatures")
        engine.population = creatures + engine.reproduce(reproductionAlgorithm)
        print ("Reproduction "+str(len(engine.population))+" creatures")
        engine.population = creatures + getRandomCreatures(1000,10, boundingPolygon);
        print ("Random new "+str(len(engine.population))+" creatures")
        engine.population = engine.fitness(fitnessAlgorithms, 20)
        print ("Fitness "+str(len( engine.population))+" creatures")

    engine.population = engine.fitness(fitnessAlgorithms, 1)
    #render the best creatures
    i = 0
    j = 0
    f= initFile()
    for beast in engine.population:
        # print(beast.fitnessScore)
        # myRender(beast,i * 500, j * 500)
        renderFile(f, beast, i * 500, j * 500, 0)
        i += 1
        if not (i % 5): j += 1; i = 0


        #rs.EnableRedraw(True)

    closeFile(f)

main()