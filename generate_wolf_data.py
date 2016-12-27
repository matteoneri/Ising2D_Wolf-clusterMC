import HW4lib as HW
import numpy as np
from matplotlib import pyplot as plt
import csv

T_c = 2/np.log(1+np.sqrt(2))

L = 500
for T in np.arange(3.3,5.0,0.1):
    print("DEV:{} - {}".format(round(T,1),L))

    lattice = HW.SquareSpinLattice(L)


    t=0
    t_tot = 0

    with open("data_wolf/data_L{}_T{}.csv".format(L,int(T*10)),"w") as f:
        writer = csv.writer(f)
        writer.writerow(["t_tot","t","m","m2","m4","E"])
        
#        it = 0
        while t_tot<50:
#            if it%10==0:
#                print("{}\t{}".format(it,t_tot))
            t = lattice.wolf_cluster_DEV(T)
            t_tot += t
            m,m2,m4,E = lattice.update_attributes()

            writer.writerow([t_tot,t,m,m2,m4,E])
    
#            it+=1




