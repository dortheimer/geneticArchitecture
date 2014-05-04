import rhinoscriptsyntax as rs
import random

class Creature:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def MakeRandom(self):
        self.points = []
        for i in range(4):
            pt = [self.x+random.random()*8-4 ,self.y+random.random()*8-4,random.random()*8-4]
            self.points.append(pt)

    def grow(self,times):
        self.createPts = []
        #add polygons
        points = self.createPts = self.points
        for pol in range(times):
            #remove on index
            index = random.randint(0,3)

            #find plane center
            planePts = []
            for i in range(4):
                if (i!=index):
                    planePts.append(self.points[i])
            planeCenter = findCenter(planePts)

            opposite = [2*planeCenter[0]-points[index][0],2*planeCenter[1]-points[index][1],2*planeCenter[2]-points[index][2]]

            points[index] = [opposite[0]+random.random()*4-2 ,opposite[1]+random.random()*4-2,opposite[2]+random.random()*4-2]

            self.createPts.append(points[index])
            Polygon(points)

    def validate(self):
        return

def findCenter(pts):
    x = y = z = 0
    l = len(pts)
    for i in range(l):
        x+= pts[i][0]
        y+= pts[i][1]
        z+= pts[i][2]

    return [x/l, y/l, z/l]


def Polygon(pts):
    myPts = []
    for x in range(4):
        for y in range(4):
            for z in range (4):
                if x!=y and x!=z and y!=x:
                    polyPoints = [pts[x], pts[y], pts[z]]
                    myPts.append(polyPoints)
                    rs.AddSrfPt(polyPoints)
    return myPts



def main():
    creatures = []
    rs.EnableRedraw(False)
    matrixSize = 10

    for i in range(-matrixSize,matrixSize):
        for j in range(-matrixSize,matrixSize):
            creature = Creature(i*20, j*20)
            creature.MakeRandom()
            creature.grow(20)
            creatures.append(creature)

    print "done"
    rs.EnableRedraw(True)


main()