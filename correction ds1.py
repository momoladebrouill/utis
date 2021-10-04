# Parcours en largeur

def parcours(racine):
    now=[racine]
    nex=[]
    while len(now):
        for ammal in now:
            nex+=ammal.childs
        now=nex[:]
    return now

# Classe entier relatif

class IntRel():
    def __init__(self,val:int,signe):
        self.signe = signe
        self.val = val

    def __mul__(self,other):
        return IntRel(self.val*other.val, "+" if self.signe == other.signe else "-")
    
    def __add__(self,other):
        if self.signe == other.signe:
            return IntRel(self.val+other.val,self.signe)
        
        else:
            if self.val>other.val:
                return IntRel(self.val-other.val,self.signe)
            
            else:
                return IntRel(other.val-self.val,other.signe)
            
    __abs__ = lambda self:IntRel(self.val,"+")
    __repr__ = lambda self: f"{self.signe if self.signe!='+' else ''}{self.val}"
    

    
    
