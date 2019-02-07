# -*- coding: utf-8 -*-
"""
/***************************************************************************
  
 A QGIS plugin
  
                              -------------------
        begin                : 2016-01-12
        copyright            : Version QGIS 3 (C) 2019 by Jean-Christophe Baudin 
                               
        email                : jeanchristophebaudin@ymail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import unicodedata,sys
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QVariant
from qgis.PyQt.QtWidgets import (QMessageBox)
from qgis.core import  (QgsProject,
                        QgsMapLayer,
                        QgsVectorLayer
                       )
                       


def getVectorLayerByName(NomCouche):
    layermap=QgsProject.instance().mapLayers()
    for name,layer in layermap.items():
        if layer.type()==QgsMapLayer.VectorLayer and layer.name()==NomCouche:
            if layer.isValid():
               return layer
            else:
               return None
            
