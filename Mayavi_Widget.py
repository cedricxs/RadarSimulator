import os
from mayavi import mlab
from mayavi.mlab import mesh, surf, contour_surf

os.environ['ETS_TOOLKIT'] = 'qt4'
from pyface.qt import QtGui
from PyQt5.QtCore import Qt 
from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
from SeaDataGenertor import SeaData
from NRL_SigmaSea import NRL_SigmaSea_Calculeur

## create Mayavi Widget and show

class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())
    def __init__(self, sys_info):
        Visualization.plotStatus = 0
        super().__init__()
    @on_trait_change('scene.activated')
    def update_plot(self):
    ## PLot to Show        
        [Visualization.x, Visualization.y , Visualization.z] = SeaData.getInstance().getSeaData()
        f = mlab.gcf()
        
        f.scene.render_window.point_smoothing = True
        f.scene.render_window.line_smoothing = True
        f.scene.render_window.polygon_smoothing = True
        f.scene.render_window.multi_samples = 8 # Try with 4 if you think this is slow
        f.scene.anti_aliasing_frames = True
        mlab.draw()
        
    def plot_static(self):
        mlab.clf()
        if Visualization.plotStatus == 0:
            Visualization.obj = surf(Visualization.x, Visualization.y,Visualization.z, colormap='ocean')
        else:
            nrl = NRL_SigmaSea_Calculeur.getInstance().calculer(Visualization.z)
            Visualization.obj = surf(Visualization.x, Visualization.y,nrl, colormap='blue-red') 
     
    @mlab.animate(delay=100, ui=False)
    def animation():
        while True:
            [Visualization.x, Visualization.y , Visualization.z] = SeaData.getInstance().getSeaData()
            ms = Visualization.obj.mlab_source
            if Visualization.plotStatus == 1:
                nrl = NRL_SigmaSea_Calculeur.getInstance().calculer(Visualization.z)
                ms.scalars = nrl
            else:
                ms.scalars = Visualization.z
            #这里如果是mesh则为z, 如果surf则为scalar
            yield
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=1, width=1, show_label=False),
                resizable=True , x=0, y=0)
    
    

class MayaviQWidget(QtGui.QWidget):
    def __init__(self, sys_info, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.visualization = Visualization(sys_info)

        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        self.ui.setParent(self)
        self.ui.move(0, 0)
        self.resize(parent.size())
        self.ui.resize(parent.size())
    
    def updateSize(self):
        self.resize(self.parent().size())
        self.ui.resize(self.parent().size()) 
    
