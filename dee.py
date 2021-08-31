from random import random

class Table:
    def __init__(self):
        self.list=[[0]]
        self.xmax=0
        self.ymax=0

    def __getitem__(self,val):
        if type(val)==tuple:
            return self.list[val[1]][val[0]]
        elif type(val)==int:
            return self.list[val]
        else:
            print(f"Bad index for type Table: {val}")
    def __setitem__(self,pos,value):
        if pos[0]>=self.xmax:
            for ind,xs in enumerate(self.list):
                self.list[ind]=xs+[0 for i in range(pos[0]-self.xmax)]
            self.xmax=len(self.list[0])
        if pos[1]>=self.ymax:
            for i in range(pos[1]-self.ymax):
                self.list.append([0 for i in range(self.xmax)])
            self.ymax=len(self.list)
        self.list[pos[1]][pos[0]]=value

    def __repr__(self):
        t=""
        for y in self.list:t+=str(y)+"\n" 
        #t+=f"Width: {self.xmax} items Height: {self.ymax} items"
        return t
    def __iter__(self):
        self.av=[0,0]
        return self
    def __next__(self):
        res=self.av[:]
        if self.av=="ended":
                raise StopIteration
        self.av[0]+=1
        if self.av[0]>=self.xmax:
            self.av[0]=0
            self.av[1]+=1
            if self.av[1]>=self.ymax:
                self.av="ended"
                return self[-1,-1],res
        return self[res[0],res[1]],res
            
class Plan:

    def __init__(self):
        self.list=[[0]]
        self.xinter=[0,0]
        self.yinter=[0,0]

    def __getitem__(self,val):
        if type(val)==tuple:
            return self.list[val[1]][abs(self.xinter[0])+val[0]]
        else:
            print(f"Bad index for type Plan: {val}")
    def __setitem__(self,pos,value):
        x,y=pos
        
        if not self.xinter[0]<x<self.xinter[1]:
            if x<self.xinter[0]:
                for ligne in range(len(self.list)):
                    self.list[ligne]=[None for to_add_before in range(abs(x-self.xinter[0]))]+self.list[ligne]
                self.xinter[0]-=abs(x-self.xinter[0])
            if self.xinter[1]<x:
                for ligne in range(len(self.list)):
                    self.list[ligne]=self.list[ligne]+[None for to_add_after in range(x-self.xinter[1])]
                self.xinter[1]+=abs(x-self.xinter[1])+1
                
        if not self.yinter[0]<y<self.yinter[1]:
            emptyline=[None for x in range(abs(self.xinter[0])+self.xinter[1])]
            if y<self.yinter[0]:
                self.list=[emptyline[:] for y in range(abs(y-self.yinter[0]))]+self.list
                self.yinter[0]-=abs(y-self.yinter[0])
            if self.yinter[1]<y:
                self.list=self.list+[emptyline[:] for y in range(abs(y-self.yinter[1]))]
                self.yinter[1]+=abs(y-self.yinter[1])
        self.list[abs(self.yinter[0])+y][abs(self.xinter[0])+x]=value
    def __repr__(self):
        t=""
        for y in self.list:t+=str(y)+"\n"
        #t+=f"Width: {self.xmax} items Height: {self.ymax} items"
        return t


S=Plan()
T=Table()
T[10,10]="bout"

