"""Stuufs utils pour momo, je sais même pas si je vais m'en serveir"""
import math
from typing import Union


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, autrui):
        return math.sqrt((self.x-autrui.x)**2+(self.y-autrui.y)**2)

    def angle(self, autrui):
        return math.atan2(self.y-autrui.y, self.x-autrui.x)

    def tup(self):
        return (self.x, self.y)

    def __add__(self, other):
        return Pos(self.x+other.x, self.y+other.y)

    __sub__ = dist

    def __repr__(self):
        return str(vars(self))


class Vec:
    def __init__(self, x=None, y=None, angle=None, long=None, a=None, b=None):
        self.x = 0
        self.y = 0
        if x != None and y != None:
            self.x = x
            self.y = y
        elif angle != None and long != None:
            self.angle = angle
            self.long = long

        elif type(a) == Pos and type(b) == Pos:
            self.x = a.x-b.x
            self.y = a.y-b.y
        else:
            raise TypeError("No good pair of keywords")

    def __set_angle(self, val):
        long = self.long
        self.x = round(math.cos(val)*long, 9)
        self.y = round(math.sin(val)*long, 9)

    def __set_long(self, val):
        angle = self.angle
        self.x = round(math.cos(angle)*val, 9)
        self.y = round(math.sin(angle)*val, 9)

    angle = property(lambda self: 0 if self.long ==
                     0 else math.atan2(self.y, self.x)+math.pi, __set_angle)
    long = property(lambda self: math.sqrt(self.x**2+self.y**2), __set_long)

    def pointtoo(self, form: Pos, to: Pos):
        self.angle = form.angle(to)

    def __getitem__(self, ind):
        return [self.x, self.y][ind]

    def __add__(self, other):
        return Vec(x=self.x+other.x, y=self.y+other.y)

    def __sub__(self, other):
        return Vec(x=self.x-other.x, y=self.y-other.y)

    def __mul__(self, num):
        return self.x*num.x+self.y*num.y if type(num) == Vec else Vec(x=self.x*num, y=self.y*num)

    def __truediv__(self, num: Union[int, float]):
        return Vec(x=self.x/num, y=self.y/num)

    def __floordiv__(self, num: Union[int, float]):
        return Vec(x=int(self.x/num), y=int(self.y/num))

    def __repr__(self):
        return f"{self.x=} {self.y=}"
    __rmul__ = __mul__
    __radd__ = __add__


class Table:
    def __init__(self, size=(0, 0), default=lambda x, y: (x, y)):
        self.list = [[]]
        self.default = default
        self.addcolumn(size[0])
        self.addline(size[1]-1)

    def __getitem__(self, val):
        try:
            return self.list[val[1]][val[0]]
        except TypeError:
            if type(val) == int:
                return self.list[val]
            else:
                raise

    def __setitem__(self, pos, value):
        if pos[0] >= self.xmax:
            self.addcolumn(pos[0]-self.xmax+1)
        if pos[1] >= self.ymax:
            self.addline(pos[1]-self.ymax)
        self.list[pos[1]][pos[0]] = value

    def addcolumn(self, nb=1):
        for y in range(self.ymax+1):  # For each line
            self.list[y] += [self.default(x, y)
                             for x in range(nb)]  # Ajouter nb colone(s)

    def addline(self, nb=1):
        for y in range(self.ymax+1, self.ymax+nb+1):  # Pour each nouvelle line
            self.list.append([self.default(x, y)
                             for x in range(self.xmax+1)])  # en créer une

    def __repr__(self):
        t = ""
        for y in self.list:
            for x in y:
                t += str(x)+"\t"
        #t+=f"{self.xmax= } {self.ymax= }"
        return t[:-1]

    def __iter__(self):
        self.av = [0, 0]
        return self

    def __next__(self):
        res = self.av[:]
        if self.av == "ended":
            raise StopIteration
        self.av[0] += 1
        if self.av[0] > self.xmax:
            self.av[0] = 0
            self.av[1] += 1
            if self.av[1] > self.ymax:
                self.av = "ended"
                return self[-1, -1], res
        return self[res[0], res[1]], res

    @property
    def xmax(self):
        try:
            val = len(self.list[0])
            return val-1 if val > 0 else 0
        except IndexError:
            return 0

    @property
    def ymax(self):
        val = len(self.list)
        return val-1 if val > 0 else 0


class Plan:

    def __init__(self, inter=(-5, -5, 5, 5), default=lambda x, y: (x, y)):
        self.default = default
        self.list = []

        self.ouest, self.nord, self.est, self.sud = 0, 0, 0, 0

        self.addlineDown(abs(inter[3]))
        self.addlineUp(abs(inter[1]))
        self.addcolumnLeft(abs(inter[0]))
        self.addcolumnRight(abs(inter[2]))

    def __getitem__(self, val):
        if type(val) == tuple:
            return self.list[val[1]][abs(self.ouest)+val[0]]
        else:
            print(f"Bad index for type Plan: {val}")

    def addcolumnRight(self, nb=1):
        for index, y in enumerate(range(self.nord, self.sud)):
            self.list[index] = self.list[index] + \
                [self.default(x, y) for x in range(self.est, self.est+nb)]
        self.est += nb

    def addcolumnLeft(self, nb=1):
        for index, y in enumerate(range(self.nord, self.sud)):
            self.list[index] = [self.default(x, y) for x in range(
                self.ouest-nb, self.ouest)]+self.list[index]
        self.ouest -= nb

    def addlineUp(self, nb=1):
        self.list = [[self.default(x, y) for x in range(
            self.ouest, self.est)] for y in range(self.nord-nb, self.nord)]+self.list
        self.nord -= nb

    def addlineDown(self, nb):
        self.list = self.list+[[self.default(x, y) for x in range(
            self.ouest, self.est)] for y in range(self.sud, self.sud+nb)]
        self.sud += nb

    def __setitem__(self, pos, value):
        x, y = pos
        if not self.ouest < x < self.est:
            if x < self.ouest:
                self.addcolumnLeft(abs(x-self.ouest))
            if self.est < x:
                self.addcolumnRight(abs(x-self.est))

        if not self.nord < y < self.sud:
            if y < self.nord:
                self.addlineUp(abs(y-self.nord))
            if self.sud < y:
                self.addlineDown(abs(y-self.sud))
        self.list[abs(self.nord)+y][abs(self.ouest)+x] = value

    def __repr__(self):
        t = ""
        for y in self.list:
            t += str(y)+"\n"
        return t

    def __iter__(self):
        self.av = [self.ouest, self.nord]
        return self

    def __next__(self):
        if self.av == "end":
            raise StopIteration
        else:
            res = self[self.av[0], self.av[1]], self.av[:]
            self.av[0] += 1
            if self.av[0] > self.est:
                self.av[1] += 1
                if self.av[1] > self.sud:
                    self.av = 'end'
        return res


class Complex:
    def __new__(cls,a,b):
        if b==0:
            return type(a).__new__(type(a),a)
        else:
            return super(Complex,cls).__new__(cls)
    def __init__(self, Re, Im):
        if Im:
            self.re = Re
            self.im = Im
        else:
            self.__class__=int

    def __add__(self, other):
        return Complex(self.re+other.re, self.im+other.im)

    def __repr__(self):
        return f"{self.re}{'+' if self.im>=0 else ''}{self.im}i"

    @property
    def bar(self):
        return Complex(self.re, -self.im)

    def set_im(self, val):
        if val == 0:
            del self.im
        else:
            self._im = val

    def del_im(self):
        self._im=0
        self.__init__(self.re,0)
    def intoger(int):pass
    im = property(lambda self: self._im, set_im, del_im)


if __name__ == "__main__":
    a = Vec(x=1, y=1)
    b = Vec(long=1, angle=math.tau)
    c = Pos(0, 10)
    d = Pos(20, 20)
    S = Plan()
    T = Table(default=lambda x, y: 0)
    D = Table(size=(10, 10), default=lambda x, y: x*y)
    a = Complex(1, 2)
    ...
else:
    print('Services offerts par votre bien aimé capitaine µ uwu')
