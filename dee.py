import random as rd

class tabl:

    def __init__(self):
        self.list=[[0]]
        self.xmax=0
        self.ymax=0

    def __getitem__(self,val):
        return self.list[val[1]][val[0]]
    
    def __setitem__(self,val,vil):
        if val[0]>self.xmax-1:
            for ind,xs in enumerate(self.list):
                self.list[ind]=xs+[0 for i in range(abs(self.xmax-val[0]+1))]
            self.xmax=val[0]
        if val[1]>self.ymax-1:
            for i in range(abs(self.ymax-val[1]+1)):
                self.list.append([0 for i in range(self.xmax)])
            self.ymax=val[1]
        self.list[val[1]][val[0]]=vil

    def __repr__(self):
        t="[\n"
        for y in self.list:
            for x in y:
                t+=str(x)+"\t"
            t+="\n"
        t+="]\n"
        t+=f"{self.xmax = } {self.ymax = }"
        return t
try:
    T=tabl()
    T[0,0]=1
    print("all good")
    breakpoint()
except:
    breakpoint()
