# -*- coding: utf-8 -*-

from qgis.core import QGis 
from qgis.core import QgsMapLayerRegistry, QgsMapLayer
from PyQt4.QtGui import *
from PyQt4.QtCore import QObject, SIGNAL
from PyQt4.QtSql import QSqlDatabase, QSqlQuery
import resources_rc  
from qgis.gui import QgsMessageBar



class MeasureArea:

    def __init__(self, iface):
        
        self.iface = iface

    def initGui(self): 

        self.toolbar = self.iface.addToolBar("My_ToolBar")
        # cria uma ação que iniciará a configuração do plugin 
        pai = self.iface.mainWindow()
        icon_path = ':/plugins/MeasureArea/icon.png'
        self.action = QAction (QIcon (icon_path),u"Calcula em metros quadrados, tamanho da area ou areas.", pai)
        self.action.setObjectName ("Retorna a area do poligono.")
        self.action.setStatusTip(None)
        self.action.setWhatsThis(None)
        self.action.setCheckable(True)
        #Padrões fixados

        self.textbox = QLineEdit(self.iface.mainWindow())
        # Set width
        self.textbox.setFixedWidth(120)
        # Add textbox to toolbar
        self.toolbar.addAction(self.action)
        self.toolbar.addWidget(self.textbox)
        # Set tooltip
        self.action.toggled.connect(self.enableElements)
        self.enableElements(False)
        self.textbox.textChanged.connect(self.enableTool) # acho que é aqui o sinal a ser trabalhado
        self.action.toggled.connect(self.enableTool)                                           
        
        
        

    def unload(self):
        # remove o item de ícone do QGIS GUI.
        del self.toolbar

    def enableElements(self, b):
        self.textbox.setEnabled(b)
       
        
    def enableTool(self, c):
        if c:
            for l in QgsMapLayerRegistry.instance().mapLayers().values():
                if l.type() == QgsMapLayer.VectorLayer: 
                    if l.geometryType() == 1 or l.geometryType() == 2: # Linha ou Poligono
                        l.selectionChanged.connect(self.measureArea) # Conecta
        else:
            for l in QgsMapLayerRegistry.instance().mapLayers().values():
                if l.type() == QgsMapLayer.VectorLayer:
                    if l.geometryType() == 1 or l.geometryType() == 2: # Linha ou Poligono
                        l.selectionChanged.disconnect(self.measureArea) # Desconecta


    def measureArea(self):

        self.layer = self.iface.activeLayer()

        try:
            if self.layer.type() != QgsMapLayer.VectorLayer:
                return

            # Get geometryType(): 0 = points; 1 = lines; 2 = polygons
            if self.layer.geometryType() == 1:
                length = 0
                # Get total length
                for f in self.layer.selectedFeatures():
                    length += f.geometry().length()

                vlength = round(length,2)
                self.textbox.setText( "m = " + str(vlength))
                
                print str(round(length,3)) + u" m"

            elif self.layer.geometryType() == 2:
                area = 0
                # Get total area
                for f in self.layer.selectedFeatures():
                    area += f.geometry().area()
                    
                varea = round(area,2)
                self.textbox.setText(u"m² = " + str(varea) )

            else:
                pass

        except AttributeError:
            self.textbox.setText(u'Não há layer selecionado!')