import os
from mayavi import mlab
from mayavi.mlab import mesh, surf, contour_surf

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
    seaData = SeaData()    
    nRL_SigmaSea_Calculeur = NRL_SigmaSea_Calculeur()
    def __init__(self):
        self.animated = False
        self.plotStatus = 0
        super().__init__()
    @on_trait_change('scene.activated')
    def update_plot(self):
    ## PLot to Show        
        [x, y , z] = Visualization.seaData.getSeaData()
        self.x, self.y, self.z = x, y, z
        self.obj = surf(x, y,z,  colormap='ocean')
        f = mlab.gcf()
        
        f.scene.render_window.point_smoothing = True
        f.scene.render_window.line_smoothing = True
        f.scene.render_window.polygon_smoothing = True
        f.scene.render_window.multi_samples = 8 # Try with 4 if you think this is slow
        f.scene.anti_aliasing_frames = True
        mlab.draw()
        
    def plot_static(self):
        mlab.clf()
        if self.plotStatus == 0:
            self.obj = surf(self.x, self.y,self.z, colormap='ocean')
        else:
            nrl = Visualization.nRL_SigmaSea_Calculeur.calculer(self.z)
            self.obj = surf(self.x, self.y,nrl, colormap='blue-red') 
 
    @mlab.animate(delay=40, ui=True)
    def animation(self):
        self.animated = True
        while True:
            [self.x, self.y , self.z] = Visualization.seaData.getSeaData()
            ms = self.obj.mlab_source
            if self.plotStatus == 1:
                nrl = Visualization.nRL_SigmaSea_Calculeur.calculer(self.z)
                ms.scalars = nrl
            else:
                ms.scalars = self.z
            #这里如果是mesh则为z, 如果surf则为scalar
            yield
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=1, width=1, show_label=False),
                resizable=True , x=0, y=0)
    
    

class MayaviQWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.visualization = Visualization()

        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        self.ui.move(0, -20)
        self.ui.setParent(self)
        self.resize(parent.size())
        self.ui.resize(parent.size())
    
    def updateSize(self):
        self.resize(self.parent().size())
        self.ui.resize(self.parent().size()) 
    
