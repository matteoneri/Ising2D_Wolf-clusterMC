import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

import HW4lib as HW


T_c   = 2.2692
T     = T_c
L     = 20
n     = L**2
t_max = 100

lattice = HW.SquareSpinLattice(L, ordered=False)

plt.ion()
fig, (ax_lattice, ax_graphs) = plt.subplots(1,2,figsize = (20,10))

plt.subplots_adjust(bottom=0.25)

#slider
axestemp = plt.axes([0.2,0.1, 0.4, 0.03], axisbg='lightgoldenrodyellow')
stemp  = Slider(axestemp, "T", 0.,5, valinit = T)

def update(val):
    global T
    T = stemp.val
    fig.canvas.draw_idle()
stemp.on_changed(update)

#reset button
resetaxes = plt.axes([0.2,0.025,0.1,0.04])
button    = Button(resetaxes, "Reset") 

def reset(event):
    stemp.reset()
button.on_clicked(reset)

#radio button
axesradio = plt.axes([0.65,0.025,0.2,0.1], axisbg="lightgoldenrodyellow")
radio   = RadioButtons(axesradio,
            ("Magnetization",
             "Energy"),active=0)
graph   = "Magnetization"

def choosegraph(label):
    global graph
    graph = label
    fig.canvas.draw_idle()
radio.on_clicked(choosegraph)

HW.draw_lattice(ax_lattice,lattice)



m,m2,m4,E = lattice.update_attributes()
t_l        = [0.]
m_l        = [abs(m)]
m2_l       = [m2] 
m4_l       = [m4] 
E_l        = [E]

t = 0

while t<t_max:
    t += lattice.wolf_cluster(T)
    t += lattice.MCMC(T)
    m,m2,m4,E = lattice.update_attributes()
    
    t_l.append(t)
    E_l.append(E)
    m_l.append(abs(m))
    m2_l.append(m2)
    m4_l.append(m4)
    
    
    HW.update_lattice(ax_lattice, lattice)

    if graph == "Magnetization":
        plt.sca(ax_graphs)
        ax_graphs.plot(t_l,m_l,"b")
        #ax_graphs.plot(t_l,m2_l,"r+")
        #ax_graphs.plot(t_l,m4_l,"k^")
        plt.axis([0,t,0,1.1])
    elif graph == "Energy":
        ax_graphs.plot(t_l,E_l,color="g",linewidth=3)
        

    plt.pause(2.01)
    plt.sca(ax_graphs) 
    plt.cla()


