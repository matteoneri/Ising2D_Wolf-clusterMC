import HW4lib as HW
import numpy as np
from matplotlib import pyplot as plt
import csv


L = 50
for T in [2.27]: #np.arange(0.1,5,0.1):
    print(T)

    lattice   = HW.SquareSpinLattice(L, ordered=True)
    lattice2  = HW.SquareSpinLattice(L, ordered = True)

    t_tot_l  = [0.]
    m_l  = [abs(lattice.get_m())]
    E_l  = [lattice.get_E()]

    t_tot = 0


    while t_tot<200:
        t = lattice.MCMC_DEV(T)
        t_tot += t
        m,m2,m4,E = lattice.update_attributes()
        t_tot_l.append(t_tot)
        m_l.append(abs(m))
        E_l.append(E)


    temp=[t_tot_l,E_l]


        #writer.writerow([t_tot,t,m,m2,m4,E])
    plt.axis([0,200,0,1.1])
    plt.plot(t_tot_l,m_l,"b",label="MCMC",zorder=2)
    t_tot_l  = [0.]
    m_l  = [abs(lattice.get_m())]
    E_l  = [lattice.get_E()]
    t_tot = 0
    while t_tot<200:
        t = lattice2.wolf_cluster_DEV(T)
        t_tot += t
        m,m2,m4,E = lattice2.update_attributes()
        t_tot_l.append(t_tot)
        m_l.append(abs(m))
        E_l.append(E)
    plt.plot(t_tot_l,m_l,"r",label="wolff",zorder=1)
    plt.xlabel("t")
    plt.ylabel("m")
    plt.legend(loc="best")
    plt.savefig("Confronto_Tbassa_magn.png")
    plt.show()
    plt.close()
    plt.plot(t_tot_l,E_l,"r",label="wolff")
    plt.plot(temp[0],temp[1],"b",label="MCMC")
    plt.xlabel("t")
    plt.ylabel("E")
    plt.legend(loc="best")
    plt.savefig("Confronto_Tbassa_energy.png")
    plt.show()
    plt.close()


    fig,ax = plt.subplots(1,1)

    HW.draw_lattice(ax,lattice)
    plt.savefig("Tbassa_MCMC_config_{}.png".format(L))
    plt.show()
    plt.close()

    
    fig,ax = plt.subplots(1,1)

    HW.draw_lattice(ax,lattice)
    plt.savefig("Tbassa_MCMC_config_{}.png".format(L))
    plt.show()
