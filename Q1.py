import HW4lib as HW

import numpy as np
from matplotlib import pyplot as plt

T_crit = 2.2692
T      = 2.3
L      = [10,20,30,40]
t_max  = 10

lattices = [HW.SquareSpinLattice(l,ordered=True) for l in L]

t_l = [[0.] for l in L]
m_l = [[lattices[i].get_m()] for i in range(len(L))]
E_l = [[lattices[i].get_E()] for i in range(len(L))]


plt.ion()
fig, (ax_m,ax_E) = plt.subplots(1,2)

while  min([l[-1] for l in t_l]) < t_max:
    for i,l in enumerate([1]):
        t_l[i].append(t_l[i][-1]+lattices[i].wolf_cluster(T))
        m_l[i].append(abs(lattices[i].update_m()))
        E_l[i].append(lattices[i].update_E())
        

        ax_m.plot(t_l[i],m_l[i],"o",linewidth=3)
        ax_E.plot(t_l[i],E_l[i],"o",linewidth=3)

    plt.pause(0.3)
    plt.sca(ax_m)
    plt.cla()
    plt.sca(ax_E)
    plt.cla()




