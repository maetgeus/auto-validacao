from qgis.core import QgsProject
from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.PyQt.QtWidgets import QAction
from qgis.utils import iface

class AutoVal:
    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.listener = None

    def initGui(self):
        self.action = QAction("Monitorar Geometria", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&AutoVal", self.action)

    def unload(self):
        if self.listener:
            del self.listener
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginMenu("&AutoVal", self.action)

    def run(self):
        layer = self.iface.activeLayer()
        if layer:
            self.listener = GeometryChangeListener(layer)

class GeometryChangeListener(QObject):
    feature_moved = pyqtSignal()

    def __init__(self, layer):
        super().__init__()
        self.layer = layer
        self.layer.geometryChanged.connect(self.on_geometry_changed)

    def on_geometry_changed(self, fid, geom):
        feature = self.layer.getFeature(fid)
        if feature:
            if not self.layer.isEditable():
                self.layer.startEditing()
            feature["Status"] = "Validado"
            self.layer.updateFeature(feature)
            # Remover o commitChanges para manter o modo de edição ativo
