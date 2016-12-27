import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches

class LatticeRow:
    def __init__(self,L,ordered):
        self._L      = L
        self._getmap = {self._L:0,
                        -1:self._L-1}
        for i in range(self._L):
            self._getmap[i] = i
        if ordered:
            self._row = np.ones(L,dtype=np.bool)
        else:
            self._row = np.array(np.random.binomial(1,0.5,size=L),dtype=np.bool)

    def __getitem__(self,key):
        """Ottiene il valore di uno spin nella riga.
        Tiene conto delle boundary"""
        return self._row[self._getmap[key]]

    def __setitem__(self,key,value):
        """Cambia uno spin"""
        self._row[self._getmap[key]] = value

    def __add__(self, x):
        if isinstance(x, LatticeRow):
            return np.sum(self._row) + x._sum
        elif isinstance(x, int):
            return np.sum(self._row) + x
        else:
            return NotImplemented

    def __radd__(self,x):
        if isinstance(x,int):
            return np.sum(self._row) + x
        else:
            return NotImplemented


class SquareSpinLattice:
    def __init__(self,L,ordered=False):
        self._L = L
        self._N = L**2
        dummy   = []
        self._spins = np.array([LatticeRow(L,ordered) for i in range(L)])
        self._getmap = {self._L:0,
                        -1:self._L-1}
        for i in range(self._L):
            self._getmap[i] = i
        self._E = 0
        for i in range(L):
            for j in range(L):
                if self._spins[i][j] == self._spins[i][j+1]:
                    self._E -= 1
                else:
                    self._E += 1
                if self._spins[i][j] == self._spins[self._getmap[i+1]][j]:
                    self._E -= 1
                else:
                    self._E += 1
        self._m  = (2*sum(self._spins) - self._N)/self._N
        self._m2 = self._m**2
        self._m4 = self._m**4
        self._updated = True
        
    def __getitem__(self,key):
        """Ottiene il valore di uno spin"""
        return self._spins[self._getmap[key]]

    def __repr__(self):
        string = ""
        for i in range(self._L):
            string += str([self[i][j] for j in range(self._L)])+"\n"
        return string


    def flip_spin(self,row,col):
        """Flippa uno spin.
        Ritorna l'incremento di tempo"""
        self[row][col] = not self[row][col]
        deltaE = 2*self.get_Ei(row,col)
        self._E += deltaE
        self._m += self[row][col]*2/self._N
        return 1/self._N

    def update_E(self):
        if self._updated:
            return self._E
        self._E = 0
        for i in range(self._L):
            for j in range(self._L):
                if self._spins[i][j] == self._spins[i][j+1]:
                    self._E -= 1
                else:
                    self._E += 1
                if self._spins[i][j] == self._spins[self._getmap[i+1]][j]:
                    self._E -= 1
                else:
                    self._E += 1
        return self._E


    def get_E(self):
        return self._E

    def get_Ei(self,row,col):
        """Ritorna l'energia del cluster formato da (row,col) e i suoi vicini"""
        S             = -1+2*self[row][col]
        sum_neighbors = 0
        for i in (-1,1):
            sum_neighbors += (-1+2*self[row][col+i])*S
            sum_neighbors += (-1+2*self[row+i][col])*S
        return -sum_neighbors

    def get_m(self):
        return self._m

    def update_m(self):
        self._m = (2*sum(self._spins) - self._N)/self._N
        return self._m

    def get_m2(self):
        return self._m2

    def get_m4(self):
        return self._m4


    def update_attributes(self):
        if self._updated:
            return self._m,self._m2,self._m4,self._E
        self._m  = (2*sum(self._spins) - self._N)/self._N
        self._m2 = self._m**2
        self._m4 = self._m**4
        self.update_E()
        return self._m,self._m2,self._m4,self._E



    def get_neighbors(self,x,y):
        return [
                (self._getmap[x-1],y),
                (x,self._getmap[y-1]),
                (x,self._getmap[y+1]),
                (self._getmap[x+1],y)
               ]
    def MCMC(self,T,x=None,y=None):
        if x==None:
            x = np.random.randint(self._L)
        if y==None:
            y = np.random.randint(self._L)
        E_old = self.get_Ei(x,y)
        E_new = -E_old
        if E_new<E_old or np.random.rand()<np.exp((E_old-E_new)/T):
            self[x][y] = not self[x][y]
        self._updated = False
        return 1/self._N

    def MCMC_DEV(self,T,x=None,y=None):
        if x==None:
            x = np.random.randint(self._L)
        if y==None:
            y = np.random.randint(self._L)
        E_old = self.get_Ei(x,y)
        S     = self[x][y]
        E_new = -E_old
        if E_new<E_old or np.random.rand()<np.exp((E_old-E_new)/T):
            self[x][y] = not S
            self._E -= 2*E_old
            self._m -= (4*S-2)/self._N
        return 1/self._N

    def wolf_cluster(self,T,x=None,y=None):
        if x==None:
            x = np.random.randint(self._L)
        if y==None:
            y = np.random.randint(self._L)
        S = self[x][y]
        self[x][y] = not S
        counter = 1
        frontiera_old = {(x,y)}
        while frontiera_old != set():
            frontiera_new = set()
            for i in frontiera_old:
                for j in self.get_neighbors(*i):
                    if S == self[j[0]][j[1]] and np.random.rand()<1-np.exp(-2/T):
                            frontiera_new.add(j)
                            self[j[0]][j[1]] = not S
                            counter += 1
            frontiera_old = frontiera_new
        self._updated = False
        return counter/self._N

    def wolf_cluster_DEV(self,T,x=None,y=None):
        if x==None:
            x = np.random.randint(self._L)
        if y==None:
            y = np.random.randint(self._L)
        S = self[x][y]
        self[x][y] = not S
        deltaE = 2*self.get_Ei(x,y)
        self._E += deltaE
        self._m -= (4*S-2)/self._N
        counter = 1
        frontiera_old = {(x,y)}
        while frontiera_old != set():
            frontiera_new = set()
            for i in frontiera_old:
                for j in self.get_neighbors(*i):
                    if S == self[j[0]][j[1]] and np.random.rand()<1-np.exp(-2/T):
                            frontiera_new.add(j)
                            self[j[0]][j[1]] = not S
                            deltaE = 2*self.get_Ei(*j)
                            self._E += deltaE
                            self._m -= (4*S-2)/self._N
                            counter += 1
            frontiera_old = frontiera_new
        self._m2 = self._m**2
        self._m4 = self._m**4
        return counter/self._N

################## GRAFICA ####

def draw_lattice(ax, lattice):
    plt.sca(ax)
    ax.axis((0,lattice._L,0,lattice._L))
    ## TICKS
    labels = range(lattice._L)
    ticks = np.arange(0.5,lattice._L,1)
    plt.xticks(ticks,labels)
    plt.yticks(ticks,labels)
    for i in range(lattice._L):
        for j in range(lattice._L):
            if lattice[i][j] == True:
                rect = patches.Rectangle(
                        (i,j),
                        1,1,
                        fill=True,
                        facecolor = "#003333",
                        edgecolor = "black",
                        linewidth = 1
                        )
            else:
                rect = patches.Rectangle(
                        (i,j),
                        1,1,
                        fill=False,
                        edgecolor = "black",
                        linewidth = 1
                        )
            ax.add_patch(rect)

def update_lattice_single_spin(ax,i,j,value):
    plt.sca(ax)
    if value == True:
        rect = patches.Rectangle(
                (i,j),
                1,1,
                fill=True,
                facecolor = "#003333",
                edgecolor = "black",
                linewidth = 1
                )
    else:
        rect = patches.Rectangle(
                (i,j),
                1,1,
                fill=True,
                facecolor = "white",
                edgecolor = "black",
                linewidth = 1
                )
    ax.add_patch(rect)

def update_lattice(ax,lattice):
    plt.sca(ax)
    plt.cla()
    ## TICKS
    labels = range(lattice._L)
    ticks = np.arange(0.5,lattice._L,1)
    plt.xticks(ticks,labels)
    plt.yticks(ticks,labels)
    for i in range(lattice._L):
        for j in range(lattice._L):
            if lattice[i][j] == True:
                rect = patches.Rectangle(
                        (i,j),
                        1,1,
                        fill=True,
                        facecolor = "#003333",
                        edgecolor = "black",
                        linewidth = 1
                        )
            else:
                rect = patches.Rectangle(
                        (i,j),
                        1,1,
                        fill=True,
                        facecolor = "white",
                        edgecolor = "black",
                        linewidth = 1
                        )
            ax.add_patch(rect)

    
