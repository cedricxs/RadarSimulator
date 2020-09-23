from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib.animation import FuncAnimation
#from numpy import *
#from matplotlib.text import Text
class Plot_Widget(FigureCanvasQTAgg):
    def __init__(self, parentWidget):
        self.figure = Figure(dpi=100, facecolor='none')
        self.axe = self.figure.add_subplot(111)
        super().__init__(self.figure)
        self.setParent(parentWidget)
        self.resize(parentWidget.size())
        self.setStyleSheet('FigureCanvasQTAgg{background:rgba(0,0,0,0)}')
        #self.mousemove = self.mpl_connect('motion_notify_event', self.mousemove_handler)
        self.clean = True
   
    def update_animation(self, frame):
        print(frame)
        x = range(frame)
        y = [i**2 for i in x]
        self.line[0].set_data(x, y)
        return self.line
    def start_animation(self):
        FuncAnimation(self.figure, self.update_animation, frames=range(100),init_func=None,interval=800, repeat = False,blit=True)
    def setPara(self, axe_title = '', axe_xlabel = '',  axe_ylabel = ''): 
        #self.text = Text(0, 0, '', fontsize=6, fontfamily='黑体')
        #self.axe.add_artist(self.text)
        self.axe.set_title(axe_title, fontsize=9, color='white', fontweight='bold')
        self.axe.set_xlabel(axe_xlabel, fontsize='x-small', color='white', fontweight='semibold')
        self.axe.set_ylabel(axe_ylabel, fontsize='x-small', color='white', fontweight='semibold')
        self.axe.xaxis.set_tick_params(labelsize=6, colors='white')
        self.axe.yaxis.set_tick_params(labelsize=9, colors='white')
        self.axe.grid()
        self.line  = self.axe.plot([], [], '-', color='orange',  linewidth=0.8)
    def updateData(self, data):
        if type(data).__name__=='list':
#            # u and v are parametric variables.
#            # u is an array from 0 to 2*pi, with 100 elements
#            u=r_[0:2*pi:100j]
#            # v is an array from 0 to 2*pi, with 100 elements
#            v=r_[0:pi:100j]
#            # x, y, and z are the coordinates of the points for plotting
#            # each is arranged in a 100x100 array
#            x=10*outer(cos(u),sin(v))
#            y=10*outer(sin(u),sin(v))
#            z=10*outer(ones(size(u)),cos(v))
#            self.axe = p3.Axes3D(self.figure)
#            self.axe.plot3D(ravel(x),ravel(y),ravel(z))
            
            x = data[0]
            y = data[1]
            self.axe.cla()
            self.axe.grid()
            self.axe.plot(x, y, '-', color='orange',  linewidth=1)
            if len(data) == 3:
                y_th = data[2]
                self.axe.plot(x, y_th, '--', color='blue',  linewidth=1)
        else:
            self.axe.plot(data, '-', color='blue', linewidth=0.8)
        self.draw()
        self.clean = False

    def draw_doppler(self, x, y, z, rangebin):
        self.clear()
        self.axe.set_title('time doppler - range{}'.format(rangebin+1), color='white', fontweight='bold');
        self.axe.set_xlabel('time(s)', color='white', fontweight='semibold');
        self.axe.set_ylabel('doppler(m/s)', color='white', fontweight='semibold');
        self.axe.xaxis.set_tick_params( colors='white')
        self.axe.yaxis.set_tick_params(  colors='white')
        self.axe.pcolormesh(x, y, z, cmap='jet')
        self.draw()
    
    def draw_logReturnRadar(self, x, y, z):
        self.clear()
        self.axe.set_title('log return radar', color='white', fontweight='bold');
        self.axe.set_xlabel('time(s)', color='white', fontweight='semibold');
        self.axe.set_ylabel('distance', color='white', fontweight='semibold');
        self.axe.xaxis.set_tick_params( colors='white')
        self.axe.yaxis.set_tick_params(  colors='white')
        self.axe.pcolormesh(x, y, z, cmap='jet')
        self.draw()
    
    def mousemove_handler(self, event):
        'on mouse movement'
        if self.axe.in_axes(event) and self.clean == False:
            x,y = event.xdata, event.ydata
            self.text.set_text( 'x:{0:.2f} y:{1:.2f}'.format(x, y))
            self.draw()
        
    def clear(self):
        self.axe.clear()
        self.clean = True

class Plot_Widget3D_Matplt(Plot_Widget):
    def __init__(self, parentWidget):
        super().__init__(parentWidget)
        self.axe = p3.Axes3D(self.figure)
        self.mpl_disconnect(self.mousemove)
    
    def updateData(self, data, axe_title = '', axe_xlabel = '',  axe_ylabel = ''):
        from matplotlib.colors import LightSource
        from matplotlib import cm
        ls = LightSource(270, 45)
        x, y, z = data[0], data[1], data[2]
        rgb = ls.shade(z, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
        
        self.axe.plot_surface( x, y, z,rstride=1, cstride=1, facecolors=rgb)
        self.axe.set_axis_off()
        self.draw()
        self.clean = False
