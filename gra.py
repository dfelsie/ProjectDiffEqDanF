from graphics import *
import time
import math

MR = 5


# Remember that 0,0 (x,y) is the upper left corner
# P1 is the upper left point
# P2 is the lower right


# For rounding, but I didn't use this
def decRou(x, place):
    num = 10 ** place
    return int((x * num)) / num


def mag(vec):
    return math.sqrt(vec[0] ** 2 + vec[1] ** 2)


def chaMag(vec, nMag):
    m = mag(vec)
    vec[0] = vec[0] * nMag / m
    vec[1] = vec[1] * nMag / m
    return vec

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

    #Obviously, like above, but with current v added
    def nDist(self, other):
        return math.sqrt((self.X() + self.vx - other.X()) ** 2 + (self.Y() + self.vy - other.Y()) ** 2)

    def eq(self, other):
        return self is other

    def repulsion(self, other):
        A = 10
        B = 2.5
        ve = self.vecTo(other)
        r = self.rad + other.rad
        d = self.dist(other)
        res = A * math.exp((r - d) / B)
        # print(res)
        ve[0] = res * ve[0]
        ve[1] = res * ve[1]
        return ve




    # Finds the best path from one ent to another
    def vecTo(self, other):
        vex = other.X() - self.X()
        vey = other.Y() - self.Y()
        mag = math.sqrt(vex ** 2 + vey ** 2)

        # mag=MR
        if (mag != 0):
            vex = vex / mag
            vey = vey / mag
        return [vex, vey]

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


#ibid, but for an array of walls
def cheBouArr(ent, arrCWall):
    for cWall in arrCWall:
        if cheBou(ent, cWall):
            return False
    return True


#Rotates a vector by the degrees given
def Rot(vec, deg):
    deg = deg * (math.pi / 180)
    x, y = vec
    v = [0, 0]
    v[0] = x * math.cos(deg) - y * math.sin(deg);
    v[1] = x * math.sin(deg) + y * math.cos(deg);
    return v;

def main():
    # c=Circle(Point(10,10),5)

    c = ent(0, 100, 0, 0, 10)
    c2 = ent(0, 120, 0, 0, 10, "blue")
    w = wallEnt(470, 220, 10)
    w2 = wallEnt(480, 210, 10)
    w3 = wallEnt(490, 200, 10)
    w4 = wallEnt(470, 280, 10)
    w5 = wallEnt(480, 290, 10)
    w6 = wallEnt(490, 300, 10)
    w7 = wallEnt(500, 190, 10)
    w8 = wallEnt(500, 310, 10)
    w9 = wallEnt(460, 230, 10)
    w10 = wallEnt(460, 270, 10)
    goal = ent(500, 250, 0, 0, 30, "yellow")
    lw = []
    lw.append(w)
    lw.append(w2)
    lw.append(w3)
    lw.append(w4)
    lw.append(w5)
    lw.append(w6)
    lw.append(w7)
    lw.append(w8)
    lw.append(w9)
    lw.append(w10)
    le = []
    le.append(c)
    le.append(c2)
    win = GraphWin("Update Example", 500, 500, autoflush=False)
    goal.draw(win)
    for w0 in lw:
        w0.c.setFill("purple")
        w0.draw(win)
    keDo = False
    te = Text(Point(400, 400), "Press q to start")
    te1 = Text(Point(400, 400), "Press q to start (again)")

    te2 = Text(Point(400, 400), "Crash!")
    te.draw(win)
    ted = False
    while (keDo == False):
        cPo = win.checkMouse()
        if cPo != None:
            lw.append(wallEnt(cPo.getX(), cPo.getY(), 10))
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

    staTim = time.time()

    for i in range(8000):
        cPo = win.checkMouse()

        if (cPo != None):
            goal.undraw()
            goal = ent(cPo.getX(), cPo.getY(), 0, 0, goal.rad, "yellow")
            goal.draw(win)


        for e in le:
            e.undraw()
            v = chaMag(e.vecTo(goal), 5)
            if (e.bou(goal) == False):

                for e2 in le:
                    dis = e.dist(e2)
                    if (dis > 250 or dis == 0 or e.eq(e2)):
                        e.vx += (v[0] - e.vx) * .333
                        e.vy += (v[1] - e.vy) * .333
                        continue

                    rep = e.repulsion(e2)
                    e.vx += (v[0] - e.vx) * .333
                    e.vy += (v[1] - e.vy) * .333
                    e.vx -= rep[0]
                    e.vy -= rep[1]
            else:

                e.vx = 0
                e.vy = 0

        for e in le:
            while (cheBouArr(e, lw) == False):
                lsp = [e.vx, e.vy]
                v15 = Rot(lsp, 15)
                e.vx = v15[0]
                e.vy = v15[1]

        for e in le:
            e.move()
            if (e.dist(goal) > goal.rad):
                e.draw(win)
                continue
            else:
                le[:] = [e2 for e2 in le if not e2.eq(e)]
                print(len(le))

        if (len(le) == 0):
            print(time.time() - staTim)
            break


        update(30)


main()
