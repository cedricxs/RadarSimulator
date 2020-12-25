import os
import PyQt5
dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'Qt','plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
from mayavi import mlab
from mayavi.mlab import surf #contour_surf, mesh

os.environ['ETS_TOOLKIT'] = 'qt4'
from pyface.qt import QtGui
from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
from SeaDataGenerator import SeaData
from NRL_SigmaSea import NRL_SigmaSea_Calculeur

## create Mayavi Widget and show

class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())
    def __init__(self, sys_info, plotType):
        self.plotType = plotType
        self.sys_info = sys_info
        super().__init__()
    
    def getFigure(self):
        return self.figure

    def close(self):
        return mlab.close(all = True)

    @on_trait_change('scene.activated')
    def initialize(self): 
        self.figure = mlab.gcf()
        self.figure.scene.render_window.point_smoothing = True
        self.figure.scene.render_window.line_smoothing = True
        self.figure.scene.render_window.polygon_smoothing = True
        self.figure.scene.render_window.multi_samples = 4
        self.figure.scene.anti_aliasing_frames = True
        self.figure.scene.background = (0, 0, 0)
        self.figure.scene.camera.pitch(45)
        x, y , z = self.sys_info.seaDataGen.getSeaData()
        self.x,self.y,self.z = x, y, z
        nrl = self.sys_info.nrlDataGen.getNrlData(z)
        self.nrl = nrl
        if self.plotType == 0:
            self.obj = surf(x, y,z,colormap=self.sys_info.seafaceColormap)
            #mlab.colorbar(object=self.obj,title='sea surface')
            mlab.title('sea surface',size=0.5,figure = self.figure,line_width = 1.0)
        elif self.plotType == 1:
            self.obj = surf(x, y,nrl,colormap=self.sys_info.radarColormap)
            #mlab.colorbar(object=self.obj,title='return radar')
            mlab.title('return radar',size=0.5,figure = self.figure,line_width = 1.0)
        mlab.orientation_axes()
        mlab.draw()

    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=1, width=1, show_label=False),
                resizable=True , x=0, y=0)
    
    

class MayaviQWidget(QtGui.QWidget):
    def __init__(self, sys_info, parent, plotType):
        QtGui.QWidget.__init__(self, parent)
        
        self.visualization = Visualization(sys_info, plotType)

        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        self.ui.setParent(self)
        self.setParent(parent)
        self.ui.move(0, 0)
        self.resize(parent.size())
        self.ui.resize(parent.size()) 
    def updateSize(self): 
        self.resize(self.parent().size())
        self.ui.resize(self.parent().size()) 
        
    def updateColormap(self,colormap):
        if self.visualization.plotType == 0:
            self.visualization.obj = surf(self.visualization.x, self.visualization.y,self.visualization.z,colormap=colormap)
            mlab.title('sea surface',size=0.5,figure = self.visualization.figure,line_width = 1.0)
        elif self.visualization.plotType == 1:
            self.visualization.obj = surf(self.visualization.x, self.visualization.y,self.visualization.nrl,colormap=colormap)
            mlab.title('return radar',size=0.5,figure = self.visualization.figure,line_width = 1.0)

    def updateStaticView(self, data):
        if self.visualization.plotType == 0:
            self.visualization.z = data
        else:
            self.visualization.nrl = data
        self.visualization.obj.mlab_source.scalars = data

    #here data is z or nrl
    def updateView(self, data):
        self.visualization.obj.mlab_source.scalars = data

    def close(self):
        return self.visualization.close()
