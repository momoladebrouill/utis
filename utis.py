"""Stuufs utils pour momo, je sais même pas si je vais m'en serveir"""
print("Services offerts par votre bien aimé captiane µ")
from typing import Union
import math
class Pos:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def dist(self,autrui):
        return math.sqrt((self.x-autrui.x)**2+(self.y-autrui.y)**2)
    def angle(self,autrui):
        return math.atan2(self.y-autrui.y,self.x-autrui.x)
    def tup(self):
        return (self.x,self.y)
    
    def __add__(self,other):
        return Pos(self.x+other.x,self.y+other.y)
    
    __sub__=dist
    
    def __repr__(self):
        return str(vars(self))


class Vec:
    def __init__(self,**args):
        """duo: x=0 + y=0 ou angle=0 + long=1 ou a=Pos() + b=Pos()
        Un super vecteur"""
        self._x=args.get('x')
        self._y=args.get('y')
        self._angle=args.get('angle')
        self._long=args.get('long')
        
        if self._x!=None and self._y!=None:
            self.__set_polaire()
            
        elif self._angle!=None and self._long!=None:
            self.__set_cartesian()
            
        elif type(args.get("a"))==Pos and type(args.get("b"))==Pos:
            self._x=args.get("a").x-args.get("b").x
            self._y=args.get("a").y-args.get("b").y
            self.__set_polaire()
            
        else:
            raise TypeError("Arguments must be x= and y= or angle= and long= or a= and b=")
            
    
    def __set_angle(self,val):
        self._angle=val
        self.__set_cartesian()

    def __set_long(self,val):
        self._long=val
        self.__set_cartesian()

    def __set_x(self,val):
        self._x=val
        self.__set_polaire()
    def __set_y(self,val):
        self._y=val
        self.__set_polaire()
    def __set_by_iter(self,tup:iter):
        self._x=tup[0]
        self._y=tup[1]
        self.__set_polaire()
    def __set_cartesian(self):
        self._x=round(math.cos(self.angle)*self.long,9)
        self._y=round(math.sin(self.angle)*self.long,9)
        
    def __set_polaire(self):
        self._long=math.sqrt(self.x**2+self.y**2)
        if self.long==0:
            self._angle=0
        else:
            self._angle=math.atan2(self.y,self.x)+math.pi
        
    def __getitem__(self,ind):
        return [self.x,self.y,self.angle,self.long][ind]
    def pointtoo(self,form:Pos,to:Pos):
        self.angle=form.angle(to)
        
    def __add__(self,other):
        return Vec(x=self.x+other.x,y=self.y+other.y)
    
    def __sub__(self,other):
        return Vec(x=self.x-other.x,y=self.y-other.y)
    
    def __mul__(self,num):
        if type(num)==Vec:
            return self.x*num.x+self.y*num.y
        else:
            return Vec(x=self.x*num,y=self.y*num)
    
    def __truediv__(self,num:Union[int,float]):
        return Vec(x=self.x/num,y=self.y/num)
    def __floordiv__(self,num:Union[int,float]):
        return Vec(x=int(self.x/num),y=int(self.y/num))
    def __repr__(self):
        return str((self.x,self.y,self.long,self.angle))
    __rmul__=__mul__
    __radd__=__add__
    angle=property(lambda self: self._angle,__set_angle)
    long=property(lambda self: self._long,__set_long)
    x=property(lambda self:self._x,__set_x)
    y=property(lambda self:self._y,__set_y)
    c=property(lambda self:(self.x,self.y),__set_by_iter,doc="Tuple cartesien (x,y)")
    
if __name__=="__main__":
    a=Vec(x=1,y=0)
    b=Vec(long=1,angle=math.tau)
    c=Pos(0,10)
    d=Pos(20,20)
            
