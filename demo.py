import numpy as np
import os
import PyQt5
dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'Qt','plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
x, y = np.meshgrid(np.arange(-3, 3, 0.05),  np.arange(-2, 2, 0.05))
x, y = np.transpose(x), np.transpose(y)
z = x*np.exp(-x**2-y**2)
## View it.
from mayavi import mlab
from mpl_toolkits.mplot3d import Axes3D
s = mlab.surf(x, y, z)
mlab.show()
'''
#x, y = np.mgrid[0:3:1,0:3:1]
#s = mlab.surf(x, y, np.asarray(x*0.1, 'd'))
#
#@mlab.animate
#def anim():
#    for i in range(10):
#        s.mlab_source.scalars = x*i
#        yield
#
#anim()
#mlab.show()
# Produce some nice data.
#n_mer, n_long = 6, 11
#pi = np.pi
#dphi = pi/1000.0
#phi = np.arange(0.0, 2*pi + 0.5*dphi, dphi, 'd')
#mu = phi*n_mer
#x = np.cos(mu)*(1+np.cos(n_long*mu/n_mer)*0.5)
#y = np.sin(mu)*(1+np.cos(n_long*mu/n_mer)*0.5)
#z = np.sin(n_long*mu/n_mer)*0.5
#
## View it.
#l = mlab.plot3d(x, y, z, np.sin(mu), tube_radius=0.025, colormap='Spectral')
#
## Now animate the data.
#ms = l.mlab_source
#for i in range(10):
#    x = np.cos(mu)*(1+np.cos(n_long*mu/n_mer +
#                                      np.pi*(i+1)/5.)*0.5)
#    scalars = np.sin(mu + np.pi*(i+1)/5)
#    ms.trait_set(x=x, scalars=scalars)
from logReturnRadar import LogReturnRadar
#from mayavi.mlab import  surf
#@mlab.show
#@mlab.animate(delay = 100, ui = True)
#def updateAnimation():
#    time_count = 0;
#    while True:
#        if time_count+10 >= length:
#            break;
#        else:
#            index = [int(i) for i in ((azi[time_count:time_count+10]-azi_min)/azi_ecart)]
#            for i in range(10):
#                values = datasrc[time_count+i, 0, :, 0]
#                data[:, index[i]] = values;
#        obj.mlab_source.scalars = data;
#        time_count+=10;
#        yield

x = range(0, 77)
y = range(2649, 2845, 15)
x, y = np.mgrid[x, y]
data = [np.zeros((77, 14)) for i in range(8)]
from System_Infomations import System_Infomations
logsrc = LogReturnRadar(System_Infomations())
datasrc = logsrc.data
azi = logsrc.azi
azi_min = 170.150757
azi_ecart = 0.005493
length = logsrc.nsweep

from matplotlib import pyplot as plt
fig = plt.figure()
ax = Axes3D(fig)
time_count = 0

while True:
    if time_count >= length:
        break
    else:
        index = int((azi[time_count]-azi_min)/azi_ecart)
        for i in range(2):
            for j in range(4):
                values = datasrc[time_count, i, :, j]
                data[i*4+j][index, :] = values
    time_count+=1
ax.plot_surface(x, y, data[0], rstride=1, cstride=1, cmap='jet')
ax.set_xlabel('azimuth')
ax.set_ylabel('range')
ax.set_zlabel('amplitude') 
#ax1 = fig.add_subplot(421)
#ax1.pcolormesh(x,y,data[0], cmap='jet')
#ax2 = fig.add_subplot(422)
#ax2.pcolormesh(x,y,data[1], cmap='jet')
#ax3 = fig.add_subplot(423)
#ax3.pcolormesh(x,y,data[2], cmap='jet')
#ax4 = fig.add_subplot(424)
#ax4.pcolormesh(x,y,data[3], cmap='jet')
#ax5 = fig.add_subplot(425)
#ax5.pcolormesh(x,y,data[4], cmap='jet')
#ax6 = fig.add_subplot(426)
#ax6.pcolormesh(x,y,data[5], cmap='jet')
#ax7 = fig.add_subplot(427)
#ax7.pcolormesh(x,y,data[6], cmap='jet')
#ax8 = fig.add_subplot(428)
#ax8.pcolormesh(x,y,data[7], cmap='jet')
#plt.show()
#obj = surf(x, y, data, colormap='blue-red')

#updateAnimation()
#mlab.show()
 '''