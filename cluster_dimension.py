import os, csv
import numpy as np
import bisect
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button

import HW4lib as HW


L   = [30,40,50,60,70,80,90,100]
nu  = 1
T_c = 2/np.log(1+np.sqrt(2))
T   = 2.7


def fill_histo(l,data):
    bins = np.arange(-np.log10(l**2),1.1,1)
    bins = np.asarray([10**i for i in bins])
    print(bins)
    len_bins = []
    for i in range(1,len(bins)):
        len_bins.append(bins[i]-bins[i-1])
    len_bins = np.asarray(len_bins)
    h_bins = 1/len_bins
    counter = dict()
    for i in range(len(bins)):
        counter[i] = 0
    for i in data:
        try:
            counter[bisect.bisect_right(bins,i)]+=1
        except:
            print(bins)
            print("data: {}, pos: {}".format(i,bisect.bisect_right(bins,i)))
    counter[len(bins)-2]+=counter[len(bins)-1]
    n = [counter[i] for i in range(len(bins)-1)]
    n = np.asarray(n)
    weights = n/h_bins
    return bins,weights,n




fig, ax = plt.subplots(1,1,figsize=(10,10))
ax.set_xscale("log")
plt.subplots_adjust(bottom=0.20,left=0.1,right=0.9,top=0.95)


def read_data(nome,dict_data):
    with open("data_wolf/"+nome, "r") as f:
        T = float(nome.split("_")[2].split(".")[0][1:])/10
        reader = csv.reader(f)
        dict_data[T] = []
        dummy = []
        for row in reader:
            dummy.append(row[0])
            dict_data[T].append(row[1])
        dummy        = np.asarray(dummy[1:],dtype=np.float)
        dict_data[T] = np.asarray(dict_data[T][1:],dtype=np.float)
        
        start_index = np.where(dummy>15)[0][0]

        dict_data[T] = dict_data[T][start_index:]
        if len(dict_data[T]) < 30:
            raise Exception
        
        return dict_data


#READ DATA
data = dict()
for l in L:
    data[l] = dict()
all_files = os.listdir("data_wolf")

for i,l in enumerate(L):
    print("Handling data of configurations with L = {}".format(l))
    filtered_list = filter(lambda x: x.split("_")[1][1:] == str(l),all_files)
    lista_file = []
    for file_name in filtered_list:
        lista_file.append(str(file_name))

    for file_name in lista_file:
        read_data(file_name,data[l])


#PLOTS
plt.sca(ax)
b,w,n = fill_histo(l,data[l][T])
plt.hist(b[:-1],bins=b,weights=w,normed=True)#,bins=50)


#slider
axcolor  = "lightgoldenrodyellow"
axesL   = plt.axes([0.20,0.01,0.60,0.03],axisbg=axcolor)
axesT   = plt.axes([0.20,0.05,0.60,0.03],axisbg=axcolor)


sL    = Slider(axesL,  r"$L$",  30,100,valinit = l,valfmt="%3i")
sT    = Slider(axesT,  r"$T$",  0.1,4.9,valinit = 2.3,valfmt="%1.1f")

def update(val):
    l  = int(round(sL.val,-1))
    T  = round(sT.val,1)
    plt.sca(ax)
    plt.cla()
    bins,weights,labels = fill_histo(l,data[l][T])
    n,bins,patches = plt.hist(bins[:-1],bins,normed=True,weights=weights)
    for patch, label in zip(patches,labels):
        ax.text(patch.get_x()+patch.get_width()/2,patch.get_height(),label,ha="center",va="bottom")
    #n,bins,blabla = plt.hist(data[l][T],bins=10,normed=True) #,bins=50)
    ax.set_xscale("log")
    plt.xticks(bins)#,rotation="vertical")
    fig.canvas.draw_idle()
sL.on_changed(update)
sT.on_changed(update)

plt.sca(ax)
#plt.xlabel(r"$\mathbf{\vert T-T_c\vert L^{1/\nu}}}$",fontsize=15)
#plt.ylabel(r"$\mathbf{m_{abs} L^{\beta/\nu}}$",fontsize=15)
#plt.legend(handles=plots,ncol=2,loc="best")
plt.show()
