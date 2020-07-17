import numpy as np
#x, y = np.meshgrid(np.arange(-3, 3, 0.05),  np.arange(-2, 2, 0.05))
#x, y = np.transpose(x), np.transpose(y)
#z = x*np.exp(-x**2-y**2)
## View it.
from mayavi import mlab
#s = mlab.surf(x, y, z)
#mlab.show()
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
import numpy as np
from mayavi import mlab
@mlab.show
@mlab.animate(delay = 100, ui = False)
def updateAnimation():
    t = 0.0
    print(1)
    while True:
        ball.mlab_source.set(x = np.cos(t), y = np.sin(t), z = 0)
        
        t += 0.1
        yield

ball = mlab.points3d(np.array(1.), np.array(0.), np.array(0.))

updateAnimation()
mlab.show()
