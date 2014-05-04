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
import rhinoscriptsyntax as rs
import copy


class Gene:
    def __init__(self, points=None):

        if points is None:
            self.generateRandom()
        else:
            self.points = points


    def generateRandom(self):
        self.points = []
        for i in range(4):
            point = [random.random() * 8 - 4,
                     random.random() * 8 - 4,
                     random.random() * 8 - 4]
            self.points.append(point)

    def size(self):
        return len(self.points)

    def grow(self):
        removeIndex = random.randint(0, self.size() - 1)

        #find plane center
        planePts = []
        for i in range(self.size()):
            if (i != removeIndex):
                planePts.append(self.points[i])

        planeCenter = self.__findCenter(planePts)

        opposite = [
            2 * planeCenter[0] - self.points[removeIndex][0],
            2 * planeCenter[1] - self.points[removeIndex][1],
            2 * planeCenter[2] - self.points[removeIndex][2]]

        point = [
            opposite[0] + random.random() * 4 - 2,
            opposite[1] + random.random() * 4 - 2,
            opposite[2] + random.random() * 4 - 2]

        planePts.append(point)
        return Gene(planePts)


    def render(self, offsetX, offsetY, offsetZ):

        tempPoints = [
            [self.points[0][0] + offsetX, self.points[0][1] + offsetY, self.points[0][2] + offsetZ],
            [self.points[1][0] + offsetX, self.points[1][1] + offsetY, self.points[1][2] + offsetZ],
            [self.points[2][0] + offsetX, self.points[2][1] + offsetY, self.points[2][2] + offsetZ],
            [self.points[3][0] + offsetX, self.points[3][1] + offsetY, self.points[3][2] + offsetZ]]

        spheres = []
        for i in range(len(tempPoints)):
            tempArray = copy.deepcopy(tempPoints)
            del tempArray[i]
            spheres.append(self.__renderSphere(tempPoints[i], tempArray))

        for index in range(len(spheres)):
            for index2 in range(index + 1, len(spheres)):
                self.__renderBone(spheres[index], spheres[index2])

    def __renderSphere(self, centerPt, points):

        distance = 0
        for pt in points:
            distance += rs.Distance(centerPt, pt)

        radius = distance / len(points) * 0.07
        return rs.AddSphere(centerPt, radius)


    def __getRadiusFromSphere(self, sphere):
        temp = rs.SurfaceVolume(sphere)
        volume = temp[0]
        return (0.75 * volume / 3.14159) ** (1 / 3)


    def __renderBone(self, sphere1, sphere2):

        temp = rs.SurfaceVolumeCentroid(sphere1)
        centerPt1 = temp[0]
        temp2 = rs.SurfaceVolumeCentroid(sphere2)
        centerPt2 = temp2[0]

        vector = rs.VectorCreate(centerPt1, centerPt2)

        # 1st Circle for loft
        plane = rs.PlaneFromNormal(centerPt1, vector)
        # print([centerPt1,centerPt2,vector])
        radius1 = self.__getRadiusFromSphere(sphere1)
        # print(plane, radius1)
        circle1 = rs.AddCircle(plane, radius1)

        # 2rdCircle for loft
        plane = rs.PlaneFromNormal(centerPt2, vector)
        radius2 = self.__getRadiusFromSphere(sphere2)
        circle2 = rs.AddCircle(plane, radius2)

        # 3rdCircle for loft
        line = rs.AddLine(centerPt1, centerPt2)

        domain = rs.CurveDomain(line)
        t = domain[1]/2.0
        centerPt3 = rs.EvaluateCurve(line, t)

        # centerPt3 = rs.EvaluateCurve(line, 0.5)

        # print([centerPt1,centerPt2,centerPt3])
        plane = rs.PlaneFromNormal(centerPt3, vector)
        radius3 = min([radius1, radius2]) * 0.66
        circle3 = rs.AddCircle(plane, radius3)

        curves = [circle1, circle3, circle2]
        return self.loft(curves)

    def loft(self, _crvList):
        crvList = _crvList
        for i in range (0,len(crvList)-1):
            rs.CurveSeam(crvList[i+1],rs.CurveClosestPoint(crvList[i+1],rs.CurveStartPoint(crvList[0])))
        srf = rs.AddLoftSrf(crvList)
        return srf

    def __findCenter(self, pts):
        x = y = z = 0

        l = len(pts)
        for i in range(l):
            x += pts[i][0]
            y += pts[i][1]
            z += pts[i][2]

        return [x / l, y / l, z / l]


def main():
    rs.EnableRedraw(False)
    creatures = []

    # generate creatures
    for i in range(100):
        firstGene = Gene()
        crmsome = chromosome.Chromosome([firstGene])
        crmsome.grow(10)
        beast = creature.Creature([crmsome])
        creatures.append(beast)

    # initialize evolution engine
    fitnessAlgorithms = {
        '500': fitness_equilateral.fitnessEquilateral(),
        '0.1': fitness_size.fitnessSize()
    }

    reproductionAlgorithm = reproduction_divider.reproductionDivider()

    engine = evolution.Evolution(creatures)
    engine.population = engine.fitness(fitnessAlgorithms, 15)

    for iteration in range(10):
        engine.population = creatures + engine.reproduce(reproductionAlgorithm)
        engine.population = engine.fitness(fitnessAlgorithms, 10)

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