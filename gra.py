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

    def eq(self, other):
        return self is other

    def starVec(self, goal, cost):
        return 0;

    def bug(self, wall):
        ra = wall.rad

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


def cheBouArr(ent, arrCWall):
    for cWall in arrCWall:
        if cheBou(ent, cWall):
            return False
    return True


def Rot(vec, deg):
    deg = deg * (math.pi / 180)
    x, y = vec
    v = [0, 0]
    v[0] = x * math.cos(deg) - y * math.sin(deg);
    v[1] = x * math.sin(deg) + y * math.cos(deg);
    return v;

def main():
    # c=Circle(Point(10,10),5)

    c = ent(0, 0, 0, 0, 10)
    c2 = ent(500, 500, 0, 0, 10, "blue")
    goal = ent(250, 250, 0, 0, 30, "yellow")
    lw = []
    le = []
    lv = []
    le.append(c)
    le.append(c2)
    win = GraphWin("Update Example", 500, 500, autoflush=False)
    goal.draw(win)
    keDo = False
    te = Text(Point(400, 400), "Press q to start")
    te1 = Text(Point(400, 400), "Press q to start (again)")

    te2 = Text(Point(400, 400), "Crash!")
    te.draw(win)
    ted = False
    while (keDo == False):
        cPo = win.checkMouse()
        if cPo != None:
            lw.append(wallEnt(cPo.getX(), cPo.getY(), 25))
            lw[len(lw) - 1].c.setFill("purple")
            lw[len(lw) - 1].draw(win)

        if win.checkKey() == "q":
            break
    te.undraw()
    te1.draw(win)

    while (True):
        cPo = win.checkMouse()
        if (cPo != None):
            le.append(ent(cPo.getX(), cPo.getY(), 0, 0, 10, col="green"))
            le[len(le) - 1].draw(win)
        if win.checkKey() == "q":
            break
    te1.undraw()

    for i in range(8000):
        cPo = win.checkMouse()

        if (cPo != None):
            goal.undraw()
            goal = ent(cPo.getX(), cPo.getY(), 0, 0, goal.rad, "yellow")
            goal.draw(win)


        # print((1/(c.xco-c2.)**2))
        # print(c.vecTo(c2)[0])

        for e in le:
            e.undraw()
            v = e.vecTo(goal)
            if (e.bou(goal) == False):
                e.vx = v[0] * MR
                e.vy = v[1] * MR
                for e2 in le:
                    if e is e2:
                        continue
                    dis = e.dist(e2)
                    if (dis > 250 or dis == 0):
                        continue
                    ve = e.vecTo(e2)
                    # ve1=e2.vecTo(e)

                    e.vx -= 200 * ve[0] * 1 / dis ** 2
                    e.vy -= 200 * ve[1] * 1 / dis ** 2
                    e2.vx -= 200 * -ve[0] * 1 / dis ** 2
                    e2.vy -= 200 * -ve[1] * 1 / dis ** 2
            else:
                e.vx = 0
                e.vy = 0

        # if c.bou(goal) == False:
            # print(decRou(c.vx,3),decRou(ve0[0]*5,3),decRou(c.vy,3),decRou(ve0[1]*5,3))
            # print(decRou(c.vx,3)==-1*decRou(ve0[0]*5,3),decRou(c.vy,3)==-1*decRou(ve0[1]*5,3))
        #   c.vx = ve0[0] * MR
        #   c.vy = ve0[1] * MR
        #else:
        #    c.vx = 0
        #    c.vy = 0

        #if c2.bou(goal) == False:
        #    c2.vx = ve1[0] * MR
        #    c2.vy = ve1[1] * MR
        #else:
        #    c2.vx = 0
        #    c2.vy = 0

        for e in le:
            while (cheBouArr(e, lw) == False):
                lsp = [e.vx, e.vy]
                v15 = Rot(lsp, 15)
                print(v15)
                e.vx = v15[0]
                e.vy = v15[1]

        ve2 = c.vecTo(c2)
        ve3 = c2.vecTo(c)
        # c.vx-=200*ve2[0]*1/c.dist(c2)**2
        # c.vy-=200*ve2[1]*1/c.dist(c2)**2
        # c2.vx-=200*ve3[0]*1/c2.dist(c)**2
        # c2.vy-=200*ve3[1]*1/c2.dist(c)**2

        # c.move()
        # c2.move()

        # c2.draw(win)
        #c.draw(win)

        for e in le:
            e.move()
            if (e.dist(goal) > goal.rad):
                e.draw(win)
                continue
            else:
                le[:] = [e2 for e2 in le if not e2.eq(e)]
                print(len(le))
        # ve=c.vecTo(c2)
        # ve2=c2.vecTo(c)
        if (len(le) == 0):
            print("Done!")
            break


        update(30)


main()
