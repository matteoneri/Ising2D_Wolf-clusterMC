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
        m,m2,m4,E,g_binder = read_data("data_wolf/"+file_name)
        T = float(file_name.split("_")[2].split(".")[0][1:])/10
        all_data[i].append([T,m,E])


#PLOT MAGNETIZATION
plots = []
for i,l in enumerate(L):
    data_x = []
    data_y = []
    for v in all_data[i]:
        data_x.append(v[0])
        data_y.append(abs(v[1]))
    data_x, data_y = zip(*sorted(zip(data_x,data_y)))
    p, = plt.plot(data_x,data_y,linestyle="-",linewidth=2,marker="s",markersize=3,label="L={}".format(l))
    #p, = plt.plot(data_x,data_y,"s",markersize=3,label="L={}".format(l))
    plots.append(p)


plt.sca(ax)
plt.ticklabel_format(axis='both', style='sci')
plt.grid()
#plt.xlabel(r"$\mathbf{\vert T-T_c\vert L^{\frac{1}{\nu}}}$",fontsize=15)
#plt.ylabel(r"$\mathbf{m_{abs} L^{\frac{\beta}{\nu}}}$",fontsize=15)
plt.xlabel(r"$\mathbf{T}$",fontsize=15)
plt.ylabel(r"$\mathbf{m_{abs}}$",fontsize=15)
plt.legend(handles=plots,ncol=2,loc="best")
plt.show()
plt.close()


#PLOT ENERGY
plots = []
for i,l in enumerate(L):
    data_x = []
    data_y = []
    for v in all_data[i]:
        data_x.append(v[0])
        data_y.append(v[2])
    data_x, data_y = zip(*sorted(zip(data_x,data_y)))
    p, = plt.plot(data_x,data_y,linestyle="-",linewidth=2,marker="s",markersize=3,label="L={}".format(l))
    plots.append(p)


plt.ticklabel_format(axis='both', style='sci')
plt.grid()
#plt.xlabel(r"$\mathbf{\vert T-T_c\vert L^{\frac{1}{\nu}}}$",fontsize=15)
#plt.ylabel(r"$\mathbf{m_{abs} L^{\frac{\beta}{\nu}}}$",fontsize=15)
plt.xlabel(r"$\mathbf{T}$",fontsize=15)
plt.ylabel(r"$\mathbf{E}$",fontsize=15)
plt.legend(handles=plots,ncol=2,loc="best")
plt.show()
