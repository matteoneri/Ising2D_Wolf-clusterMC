import HW4lib as HW
import numpy as np
from matplotlib import pyplot as plt
import csv


L = 20
for T in [1.27]: #np.arange(0.1,5,0.1):
    print(T)

    lattice = HW.SquareSpinLattice(L)

    t_tot_l  = [0.]
    m_l  = [abs(lattice.get_m())]
    E_l  = [lattice.get_E()]

    t=0
    t_tot = 0


    while t_tot<60:
        t = lattice.MCMC(T)
        t_tot += t
        m,m2,m4,E = lattice.update_attributes()
        t_tot_l.append(t_tot)
        m_l.append(abs(m))
        E_l.append(E)

        #writer.writerow([t_tot,t,m,m2,m4,E])
    plt.axis([0,60,0,1.1])
    plt.plot(t_tot_l,m_l,"b--")
    plt.xlabel("t")
    plt.ylabel("m")
    plt.savefig("Tbassa_MCMC_magn.png")
    plt.show()
    plt.close()
    plt.plot(t_tot_l,E_l,"v--")
    plt.xlabel("t")
    plt.ylabel("E")
    plt.savefig("Tbassa_MCMC_energy.png")
    plt.show()
    plt.close()

    fig,ax = plt.subplots(1,1)

    HW.draw_lattice(ax,lattice)
    plt.savefig("Tbassa_MCMC_config.png")
    plt.show()


    
