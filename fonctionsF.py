# -*- coding: utf-8 -*-
"""
/***************************************************************************
  
 A QGIS plugin
  
                              -------------------
        begin                : 2016-01-12
        copyright            : (C) 2016 by Jean-Christophe Baudin 
                               
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
from PyQt4 import QtCore
from PyQt4 import QtGui
from qgis.core import *
from qgis.gui import *

def getVectorLayerByName(NomCouche):
    layermap=QgsMapLayerRegistry.instance().mapLayers()
    for name, layer in layermap.iteritems():
        if layer.type()==QgsMapLayer.VectorLayer and layer.name()==NomCouche:
            if layer.isValid():
               return layer
            else:
               return None
            
