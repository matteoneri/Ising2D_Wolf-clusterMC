import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

import HW4lib as HW


T_c   = 2.2
T     = T_c
L     = 30
n     = L**2
t_max = 100
L     = [10,20,30,40]

lattice = dict()
for l in L:
    lattice[l] = HW.SquareSpinLattice(l, ordered=True)

plt.ion()
fig_m, ax_m  = plt.subplots(1,1,figsize = (10,10))
fig_E, ax_E  = plt.subplots(1,1,figsize = (10,10))

fig = [fig_m,fig_E]
ax  = [ax_m,ax_E]


fig_panel, ax_panel = plt.subplots(1,1,figsize = (5,4))
#slider
axestemp = plt.axes([0.2,0.8, 0.8, 0.03], axisbg='lightgoldenrodyellow')
stemp    = Slider(axestemp, "T", 0.,5, valinit = T_c)

def update(val):
    global T
    T = stemp.val
    fig_panel.canvas.draw_idle()
stemp.on_changed(update)

#reset button
resetaxes = plt.axes([0.7,0.6,0.1,0.04])
button    = Button(resetaxes, "Reset") 

def reset(event):
    lattice = [HW.SquareSpinLattice(l, ordered=True) for l in L]
button.on_clicked(reset)

#L radio button

axesradio = []
radio   = []
L_drawn = [True for l in L]


def showL(label):
    global L_drawn
    L_drawn[label] = not L_drawn[label]
    fig_panel.canvas.draw_idle()
    return lambda x: None

for i,l in enumerate(L):
    axesradio.append(plt.axes([0.25,0.5-i*0.1,0.2,0.1],axisbg="lightgoldenrodyellow"))
    radio.append(Button(axesradio[i],str(l)))
    radio[i].on_clicked(showL(i))

#m radio button
axesradio2 = plt.axes([0.5,0.1,0.2,0.1], axisbg="lightgoldenrodyellow")
radio2     = RadioButtons(axesradio2,
            ("Magnetization",
             "Energy"),active=0)
graph   = "Magnetization"

def choosegraph(label):
    global graph
    graph = label
    fig_panel.canvas.draw_idle()
radio2.on_clicked(choosegraph)



t_wolf = np.zeros(len(L))
m = np.array([lattice[l].get_m() for l in L])
E = np.array([lattice[l].get_E() for l in L])
t_wolf_l   = [np.zeros(len(L))]
m_l        = [m]
E_l        = [E]
while any(t_wolf<t_max):
    t_wolf += np.array([lattice[l].wolf_cluster(T) for l in L])
    m = np.array([lattice[l].update_m() for l in L])
    E = np.array([lattice[l].update_E() for l in L])
    
    t_wolf_l.append(t_wolf)
    m_l.append(np.abs(m))
    E_l.append(E)
    
    plt.sca(ax_m)
    ax_m.plot(t_wolf_l,m_l,"o")
    plt.axis([0,max(t_wolf),0,1.1])
    plt.sca(ax_E)
    ax_E.plot(t_wolf_l,E_l,"o")
    plt.axis([0,max(t_wolf),0,1.1])
        

    plt.pause(5.01)
    plt.sca(ax_m) 
    plt.cla()
    plt.sca(ax_E)
    plt.cla()


