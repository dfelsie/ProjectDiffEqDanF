from graphics import *
import time
import math

MR = 5


# Remember that 0,0 (x,y) is the upper left corner
# P1 is the upper left point
# P2 is the lower right

def decRou(x, place):
    num = 10 ** place
    return int((x * num)) / num


class wallEnt:
    def __init__(self, x, y, r, col="red"):
        self.c = Circle(Point(x, y), r)
        self.c.setOutline("white")
        self.c.setFill("")
        self.radius = r

    def X(self):
        return self.c.getCenter().getX()

    def Y(self):
        return self.c.getCenter().getY()

    def undraw(self):
        self.c.undraw()

    def draw(self, wind):
        self.c.draw(wind)


# This is the person class, basically a modified version of the low level circle class in this graphics library
class ent:
    def __init__(self, x, y, dvx, dvy, r, col="red"):
        self.c = Circle(Point(x, y), r)
        self.c.setOutline("white")
        self.c.setFill("red")
        self.vx = dvx
        self.vy = dvy
        self.rad = r
        self.c.setFill(col)

    # this is just move from the low level library
    def move(self):
        self.c.move(self.vx, self.vy)

    # this is just undraw
    def undraw(self):
        self.c.undraw()

    # this is just draw
    def draw(self, wind):
        self.c.draw(wind)

    # This method is unused rn
    def acc(self, dvx, dvy):
        self.vx += dvx
        self.vy += dvy

    def X(self):
        return self.c.getCenter().getX()

    def Y(self):
        return self.c.getCenter().getY()

    def dist(self, other):
        return math.sqrt((self.X() - other.X()) ** 2 + (self.Y() - other.Y()) ** 2)

    def nDist(self, other):
        return math.sqrt((self.X() + self.vx - other.X()) ** 2 + (self.Y() + self.vy - other.Y()) ** 2)

    # Finds the best path from one ent to another
    def vecTo(self, other):
        vex = other.X() - self.X()
        vey = other.Y() - self.Y()
        mag = math.sqrt(vex ** 2 + vey ** 2)

        # mag=MR
        if (mag != 0):
            vex = vex / mag
            vey = vey / mag
        return (vex, vey)

    # There's a weird error to the pathing right now where it "bounces" when it gets to a goal point: this stops that
    def bou(self, goal):
        if (abs(self.X() - goal.X()) <= 5 and abs(self.Y() - goal.Y()) <= 5):
            return True
        return False


# This is a bounds check for the wall:
def cheBou(ent, cWall):
    if (ent.nDist(cWall) < cWall.radius + ent.rad / 2 and
            ent.dist(cWall) >= cWall.radius + ent.rad / 2):
        return True
    return False


def main():
    # c=Circle(Point(10,10),5)

    c = ent(0, 0, 0, 0, 10)
    c2 = ent(500, 500, 0, 0, 10, "blue")
    goal = ent(250, 250, 0, 0, 30, "yellow")
    ls = []
    win = GraphWin("Update Example", 500, 500, autoflush=False)
    goal.draw(win)
    keDo = False
    te = Text(Point(400, 400), "Press q to start")
    te2 = Text(Point(400, 400), "Crash!")
    te.draw(win)
    ted = False
    while (keDo == False):
        cPo = win.checkMouse()
        if cPo != None:
            ls.append(wallEnt(cPo.getX(), cPo.getY(), 25))
            ls[len(ls) - 1].c.setFill("purple")
            ls[len(ls) - 1].draw(win)

        if win.checkKey() == "q":
            break
    te.undraw()
    for i in range(1000):
        cPo = win.checkMouse()

        if (cPo != None):
            goal.undraw()
            goal = ent(cPo.getX(), cPo.getY(), 0, 0, goal.rad, "yellow")
            goal.draw(win)
        c.undraw()
        c2.undraw()

        # print((1/(c.xco-c2.)**2))
        # print(c.vecTo(c2)[0])

        ve0 = c.vecTo(goal)
        ve1 = c2.vecTo(goal)

        if c.bou(goal) == False:
            # print(decRou(c.vx,3),decRou(ve0[0]*5,3),decRou(c.vy,3),decRou(ve0[1]*5,3))
            # print(decRou(c.vx,3)==-1*decRou(ve0[0]*5,3),decRou(c.vy,3)==-1*decRou(ve0[1]*5,3))
            c.vx = ve0[0] * MR
            c.vy = ve0[1] * MR
        else:
            c.vx = 0
            c.vy = 0

        if c2.bou(goal) == False:
            c2.vx = ve1[0] * MR
            c2.vy = ve1[1] * MR
        else:
            c2.vx = 0
            c2.vy = 0

        for w in ls:
            if cheBou(c, w):
                if ted == False:
                    te2.draw(win)
                    ted = True
                c.vx = 0
                c.vy = 0

                break
        else:
            te2.undraw()

        c.move()
        c2.move()

        c2.draw(win)
        c.draw(win)

        # ve=c.vecTo(c2)
        # ve2=c2.vecTo(c)
        # c.vx-=200*ve[0]*1/((c2.X()-c.X())**2)
        # c.vy-=200*ve[0]*(1/(c.X()-c2.X())**2)
        # c2.vx-=200*ve2[0]*1/((c2.X()-c.X())**2)
        # c2.vy-=200*ve2[0]*(1/(c.X()-c2.X())**2)

        update(30)


main()
