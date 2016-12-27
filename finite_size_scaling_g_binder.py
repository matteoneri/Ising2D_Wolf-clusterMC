import os, csv
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button

import HW4lib as HW


L   = [30,40,50,60,70,80,90,100]
nu   = 1
T_c = 2/np.log(1+np.sqrt(2))
beta = 1/8


fig, ax = plt.subplots(1,1,figsize=(10,10))
plt.subplots_adjust(bottom=0.20,left=0.1,right=0.9,top=0.95)


def read_data(nome):
    with open(nome, "r") as f:
        reader = csv.reader(f)
        data = [[] for i in range(6)]
        for row in reader:
            for i in range(6):
                data[i].append(row[i])
        for i in range(6):
            data[i] = np.asarray(data[i][1:],dtype=np.float)
                
        try:##### DB
            start_index = np.where(data[0]>15)[0][0]
        except:
            print("CONTROLLARE {}".format(nome))
            from sys import exit
            exit()#### DB
        for i in range(6):
            data[i] = data[i][start_index:]
            if len(data[i]) < 30:
                raise Exception("CONTROLLARE {}. Non >50".format(nome))
        data[3] = data[2]**2
        data[4] = data[2]**4
        
        to_be_returned = []
        to_be_returned.append(np.mean(np.abs(data[2])))
        for array in data[3:]:
            media = np.mean(array)
            to_be_returned.append(media)
        to_be_returned.append(to_be_returned[2]/(3*to_be_returned[1]**2))
        return to_be_returned


#READ DATA
all_data = [[] for i in range(len(L))]
all_files = os.listdir("data_wolf")

for i,l in enumerate(L):
    print("Handling data of configurations with L = {}".format(l))
    filtered_list = filter(lambda x: x.split("_")[1][1:] == str(l),all_files)
    lista_file = []
    for file_name in filtered_list:
        lista_file.append(str(file_name))

    for file_name in lista_file:
        try:
            m,m2,m4,E,g_binder = read_data("data_wolf/"+file_name)
        except:
            print(file_name)
        T = float(file_name.split("_")[2].split(".")[0][1:])/10
        all_data[i].append([T,m,g_binder])

#PLOTS
plots = []
for i,l in enumerate(L):
    data_x = []
    data_y = []
    for v in all_data[i]:
        data_x.append((v[0]-T_c)*l**(1/nu))
        data_y.append(v[2])
    data_x, data_y = zip(*sorted(zip(data_x,data_y)))
    #p, = plt.plot(data_x,data_y,linestyle="-",linewidth=2,marker="s",markersize=3,label="L={}".format(l))
    p, = plt.plot(data_x,data_y,"s",markersize=3,label="L={}".format(l))
    plots.append(p)


#slider
axcolor  = "lightgoldenrodyellow"
axesnu   = plt.axes([0.20,0.01,0.60,0.03],axisbg=axcolor)
axesTc   = plt.axes([0.20,0.05,0.60,0.03],axisbg=axcolor)

snu    = Slider(axesnu,  r"$\nu$",  0.3,3.,valinit = 1)
sTc    = Slider(axesTc,  r"$T_c$",  0.1,4.,valinit = 2/np.log(1+np.sqrt(2)))
def update(val):
    nu   = snu.val
    T_c  = sTc.val
    for i,l in enumerate(L):
        data_x = []
        data_y = []
        for v in all_data[i]:
            data_x.append((v[0]-T_c)*l**(1/nu))
            data_y.append(v[2])
        data_x, data_y = zip(*sorted(zip(data_x,data_y)))
        plots[i].set_xdata(data_x)
        plots[i].set_ydata(data_y)
    fig.canvas.draw_idle()
snu.on_changed(update)
sTc.on_changed(update)

plt.sca(ax)
plt.ticklabel_format(axis='both', style='sci')
plt.grid()
#plt.xlabel(r"$\mathbf{\vert T-T_c\vert L^{\frac{1}{\nu}}}$",fontsize=15)
#plt.ylabel(r"$\mathbf{m_{abs} L^{\frac{\beta}{\nu}}}$",fontsize=15)
plt.xlabel(r"$\mathbf{\vert T-T_c\vert L^{1/\nu}}}$",fontsize=15)
plt.ylabel(r"$\mathbf{g_{binder}}$",fontsize=15)
plt.legend(handles=plots,ncol=2,loc="best")
plt.show()
