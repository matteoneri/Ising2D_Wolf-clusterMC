import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches

class LatticeRow:
    def __init__(self,L):
        self._L      = L
        self._getmap = {self._L:0,
                        -1:self._L-1}
        for i in range(self._L):
            self._getmap[i] = i
        self._row    = np.array(np.random.binomial(1,0.5,size=L),dtype=np.bool)
        self._sum    = np.sum(self._row)

    def __getitem__(self,key):
        """Ottiene il valore di uno spin nella riga.
        Tiene conto delle boundary"""
        return self._row[self._getmap[key]]

    def __setitem__(self,key,value):
        """Cambia uno spin"""
        self._row[self._getmap[key]] = value

    def __add__(self, x):
        if isinstance(x, LatticeRow):
            return self._sum + x._sum
        elif isinstance(x, int):
            return self._sum + x
        else:
            return NotImplemented

    def __radd__(self,x):
        if isinstance(x,int):
            return self._sum + x
        else:
            return NotImplemented


class SquareSpinLattice:
    def __init__(self,L):
        self._L = L
        self._N = L**2
        dummy   = []
        self._spins = np.array([LatticeRow(L) for i in range(L)])
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
        self.m = sum(self._spins)/self._N 
        
    def __getitem__(self,key):
        """Ottiene il valore di uno spin"""
        return self._spins[key]

    def __repr__(self):
        string = ""
        for i in range(self._L):
            string += str([self[i][j] for j in range(self._L)])+"\n"
        return string


    def flip_spin(self,row,col):
        """Flippa uno spin.
        Ritarna la variazione di energia"""
        self[row][col] = not self[row][col]
        deltaE = 2*self.get_Ei(row,col)
        self._E += deltaE
        return 1/self._N

    def recompute_E(self):
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
        return self._E


    def get_total_E(self):
        return self._E

    def get_Ei(self,row,col):
        """Ritorna l'energia del cluster formato da (row,col) e i suoi vicini"""
        S             = -1+2*self[row][col]
        sum_neighbors = 0
        for i in (-1,1):
            sum_neighbors += (-1+2*self[row][col+i])*S
            sum_neighbors += (-1+2*self[row+1][col])*S
        return -sum_neighbors

    def get_m(self):
        return self._m

    def

    def get_neighbors(self,x,y):
        return [
                (self._getmap[x-1],y),
                (x,self._getmap[y-1]),
                (x,self._getmap[y+1]),
                (self._getmap[x+1],y)
               ]
    
    def wolf_cluster(self,x,y,T):
        S = self[x][y]
        cluster       = {(x,y)}
        frontiera_old = {(x,y)}
        while frontiera_old != set():
            frontiera_new = set()
            for i in frontiera_old:
                for j in self.get_neighbors(*i):
                    if self[i[0]][i[1]] == self[j[0]][j[1]] and j not in cluster:
                        if np.random.rand()<1-np.exp(-2/T):
                            frontiera_new.add(j)
                            cluster.add(j)
            frontiera_old = frontiera_new
        for i in cluster:
            self[i[0]][i[1]] = not S
        return len(cluster)/self._N


    def flip_cluster(self,cluster):
        pass









class SquareSpinLattice_OLD:
    def __init__(self,L):
        self._L = L
        self._N = L**2
        self._spins = np.array(np.random.binomial(1,0.5,size=(L,L)),dtype=np.bool)
        self._E = 0
        for i in range(L):
            for j in range(L):
                if self._spins[i][j] == self._spins[i][(j+1)%self._L]:
                    self._E-=1
                else:
                    self._E+=1
                if self._spins[i][j] == self._spins[(i+1)%self._L][j]:
                    self._E-=1
                else:
                    self._E+=1

    def __getitem__(self,key):
        """Ottiene il valore di uno spin"""
        return self._spins[key//self._L][key%self._L]

    def __setitem__(self,key,value):
        """Cambia uno spin. Ritorna la variazione di energia"""
        if self[key] != value:
            self._spins[key//self._L][key%self._L] = np.bool(value)
            return 2*self.get_Ei(key)
        else:
            return 0

    def n2coord(self,n):
        pass

    def coord2n(self,coord):
        pass

    def get_neighbors_n(self,key):
        pass

    def create_cluster(self,key):
        #TODO
        pass

    def flip_cluster(self,cluster):
        """Un cluster e' un insieme di indici (numeri interi)"""
        #TODO
        pass

    def get_neighbors_ENWS(self,key):
        """Ritorna i vicini del key-esimo spin.
        [Est,Nord,West,Sud] in senso orario"""
#        print((key//self._L,(key+1)%self._L),\
#              (((key//self._L)-1)%self._L,key%self._L),\
#              (key//self._L,(key-1)%self._L),\
#              (((key//self._L)+1)%self._L,key%self._L)
#              )
        return np.array((self._spins[key//self._L][(key+1)%self._L],\
                        self._spins[((key//self._L)+1)%self._L][key%self._L],\
                        self._spins[key//self._L][(key-1)%self._L],\
                        self._spins[((key//self._L)-1)%self._L][key%self._L]
                        ))
    
    def get_total_E(self):
        """Ritorna l'energia totale del sistema"""
        return self._E

    def get_Ei(self,key):
        """Ritorna l'esergia dei 5 spin: key e i suoi vicini"""
        return (4-2*np.sum(self.get_neighbors_ENWS(key)))*(-1+2*self[key])





################## GRAFICA ####

def draw_lattice(lattice):
    """Ritorna fig, ax"""
    fig, ax = plt.subplots(figsize = (10,10))
    plt.axis((0,lattice._L,0,lattice._L))
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
    return fig, ax

def update_lattice_single_spin(ax,i,j,value):
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

    
