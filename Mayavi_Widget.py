import os
from mayavi import mlab
from mayavi.mlab import surf #contour_surf, mesh

os.environ['ETS_TOOLKIT'] = 'qt4'
from pyface.qt import QtGui
from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
from SeaDataGenertor import SeaData
from NRL_SigmaSea import NRL_SigmaSea_Calculeur

## create Mayavi Widget and show

class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())
    def __init__(self, sys_info, plotType):
        self.plotType = plotType
        super().__init__()
    @on_trait_change('scene.activated')
    def initialize(self):
        f = mlab.gcf()
        f.scene.render_window.point_smoothing = True
        f.scene.render_window.line_smoothing = True
        f.scene.render_window.polygon_smoothing = True
        f.scene.render_window.multi_samples = 8 # Try with 4 if you think this is slow
        f.scene.anti_aliasing_frames = True
        f.scene.background = (0, 0, 0)
        x, y , z = SeaData.getInstance().getSeaData()
        nrl = NRL_SigmaSea_Calculeur.getInstance().calculer(z)
        if self.plotType == 0:
            self.obj = surf(x, y,z, colormap='ocean')
        elif self.plotType == 1:
            self.obj = surf(x, y,nrl, colormap='blue-red')
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
        
    #here data is z or nrl
    def update(self, data):
        self.visualization.obj.mlab_source.scalars = data
