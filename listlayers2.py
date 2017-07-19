# -*- coding: utf-8 -*-
#necessaire pour les connections signals / slots
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from osgeo import ogr
# pour ordonner des dictionnaires
from collections import OrderedDict

# import de QGIS
from qgis import *
from qgis.core import *
from qgis.gui import *
from qgis.gui import QgsMapCanvas
from qgis.utils import iface

import processing
from processing import *

import os
import os.path

import fonctionsF
import doAbout

class Ui_Dialog(object):
    def __init__(self, iface):
        self.iface = iface
    
    def setupUi(self, Dialog):
        self.iface = iface
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,340,200).size()).expandedTo(Dialog.minimumSizeHint()))
        Dialog.setWindowTitle("Polygons_Pile")
        
        # QLabel lancer recherche
        self.label10 = QtGui.QLabel(Dialog)
        self.label10.setGeometry(QtCore.QRect(15,20,300,18))
        self.label10.setObjectName("label10")
        self.label10.setText("Select a layer of polygons:  ")

        ListeCouchesPoly=[""]
        NbCouches=self.iface.mapCanvas().layerCount()
        if NbCouches==0: QMessageBox.information(None,"information: ","No Layers ! ")
        else:
            for i in range(0,NbCouches):
                couche=self.iface.mapCanvas().layer(i)
                # 0 pour point
                if couche.geometryType()== 2 or couche.geometryType()==5 :
                    if couche.isValid():
                       ListeCouchesPoly.append(couche.name())
                    else:
                       QMessageBox.information(None,"information: ","No layers with polygons ! ")
                       return None
        self.ComboBoxPolygones = QtGui.QComboBox(Dialog)
        self.ComboBoxPolygones.setMinimumSize(QtCore.QSize(300, 25))
        self.ComboBoxPolygones.setMaximumSize(QtCore.QSize(300, 25))
        self.ComboBoxPolygones.setGeometry(QtCore.QRect(10, 45, 300,25))
        self.ComboBoxPolygones.setObjectName("ComboBoxPolygones")
        for i in range(len(ListeCouchesPoly)):  self.ComboBoxPolygones.addItem(ListeCouchesPoly[i])

        #Exemple de QPushButton
        self.DoButton = QtGui.QPushButton(Dialog)
        self.DoButton.setMinimumSize(QtCore.QSize(200, 20))
        self.DoButton.setMaximumSize(QtCore.QSize(200, 20))        
        self.DoButton.setGeometry(QtCore.QRect(60,80, 200, 20))
        self.DoButton.setObjectName("DoButton")
        self.DoButton.setText(" Let's do it ... being patient !")

        #Exemple de QPushButton
        self.aboutButton = QtGui.QPushButton(Dialog)
        self.aboutButton.setMinimumSize(QtCore.QSize(70, 20))
        self.aboutButton.setMaximumSize(QtCore.QSize(70, 20))        
        self.aboutButton.setGeometry(QtCore.QRect(30, 110, 70, 23))
        self.aboutButton.setObjectName("aboutButton")
        self.aboutButton.setText(" Read me ")
        
        self.PushButton = QtGui.QPushButton(Dialog)
        self.PushButton.setMinimumSize(QtCore.QSize(100, 20))
        self.PushButton.setMaximumSize(QtCore.QSize(100, 20))
        self.PushButton.setGeometry(QtCore.QRect(185, 110, 100,23))
        self.PushButton.setObjectName("PushButton")
        self.PushButton.setText("Quit")
         
        #ProgressBar
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setMinimumSize(QtCore.QSize(260, 15))
        self.progressBar.setMaximumSize(QtCore.QSize(260, 15))
        self.progressBar.setGeometry(QtCore.QRect(30,145,260,15))
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setStyleSheet(
            """QProgressBar {border: 2px solid grey; border-radius: 5px; text-align: center;}"""
            """QProgressBar::chunk {background-color: 6C96C6; width: 20px;}"""
        )
        #Pose a minima une valeur de la barre de progression / slide contrôle
        self.progressBar.setValue(0)
         
        # actions
        QtCore.QObject.connect(self.PushButton,QtCore.SIGNAL("clicked()"),Dialog.reject)
        QtCore.QObject.connect(self.ComboBoxPolygones,QtCore.SIGNAL("currentIndexChanged(QString)"),self.onComboP)
        QtCore.QObject.connect(self.aboutButton, SIGNAL("clicked()"), self.doAbout)
        QtCore.QObject.connect(self.DoButton, SIGNAL("clicked()"), self.Run)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
                                                             
    def onComboP(self):
        global zdim
        SelectionP = self.ComboBoxPolygones.currentText()
        #QMessageBox.information(None,"information:","couche selectionnee: "+ (SelectionP))
        CoucheP=fonctionsF.getVectorLayerByName(SelectionP)
        counterP=zdim=0
        for featP in CoucheP.getFeatures(QgsFeatureRequest()):
            counterP+=1
            zdim+=1
        if counterP==0:
            QMessageBox.information(None,"information:","Layer "+ str(CoucheP.name())+"  do not contain polygons!")
               
    def doAbout(self):
        d = doAbout.Dialog()
        d.exec_()
    
    def Run(self):
        SelectionP = self.ComboBoxPolygones.currentText()
        CoucheP=fonctionsF.getVectorLayerByName(SelectionP)
        featP=QgsFeature()
        counterP=0
        #global DicoP_non_classe,DicoP_classe
        DicoP_non_classe={}
        # on charge les données dans un dictionnaire
        for featP in CoucheP.getFeatures():
            # to create final attribute table we store attributes values in attributs
            # pour recreer les tables finales on met dans attributs
            # les valeurs des  attributs des objets de la couche de lignes
            attributs = featP.attributes()
            #QMessageBox.information(None,"DEBUG attributs %s ", "%s"%attributs)
            Poly_id = featP.id()
            counterP+=1
            geomP=featP.geometry()
            #QMessageBox.information(None,"geomP type:",str(geomP.type()))
            surfP=geomP.area()
            DicoP_non_classe[counterP]=[surfP,Poly_id]
        #QMessageBox.information(None,"DEBUG DicoP_non_classe ", str(DicoP_non_classe))
        n=0
        DicoP_classe={}
        # to class polygons with extract and delete them from a first dicom:DicoP_non_classe after
        # adding them to a second:DicoP_classe
        # pour classer on procede par extraction /suppression des minimums 
        # de DicoP_non_classe et ajout dans DicoP_classe
        
        for c in range(1,counterP+1):
            n+=1
            #QMessageBox.information(None,"DEBUG n ", str(n)+ '  et c  : '+str(c))
            first=True
            maxi=0
            id_maxi=0
            for k in DicoP_non_classe.keys():
                surfP=DicoP_non_classe[k][0]
                if first:
                    first=False
                    id_maxi=k
                    maxi=surfP
                else:
                    if maxi < surfP:
                        maxi=surfP
                        id_maxi=k
            surfPc=DicoP_non_classe[id_maxi][0]
            poly_id=DicoP_non_classe[id_maxi][1]
            DicoP_classe[n]=[surfPc,poly_id]
            del DicoP_non_classe[id_maxi] # supprime le minimum identifie
            zPercent = int(2* counterP / zdim)
            self.progressBar.setValue(zPercent)
        #QMessageBox.information(None,"DEBUG DicoP_classe ", str(DicoP_classe)+' compteurPnc :'+ str(c))
        Pyramide=QgsVectorLayer("Polygon",'Pile_of_'+ str(CoucheP.name()), "memory")
        QgsMapLayerRegistry.instance().addMapLayer(Pyramide)
        prPyramide = Pyramide.dataProvider()
        ListeChamps=[]
        ProviderP=CoucheP.dataProvider()
        Champs=ProviderP.fields()
        for f in Champs:
            znameField= f.name()
            Type=str(f.typeName())
            if Type == 'Integer': ListeChamps.append(QgsField(znameField, QVariant.Int))
            if Type == 'Real': ListeChamps.append(QgsField(znameField, QVariant.Double))
            if Type == 'String': ListeChamps.append(QgsField(znameField, QVariant.String))
            else:ListeChamps.append(QgsField(znameField, QVariant.String))
        ListeChamps.append(QgsField("area", QVariant.Double))
        ListeChamps.append(QgsField("rank", QVariant.Int))
        ListeChamps.append(QgsField("poly_id", QVariant.Int))
        prPyramide.addAttributes(ListeChamps)
        Pyramide.startEditing()
        attributsF=[]
        surfF=0 
        ID=0
        classement=""
        Liste=[]
        ListeClasse=[]
        counter=0
        #QMessageBox.information(None,"DEBUG  ", " DicoP_classe" + str(DicoP_classe))
        for key in DicoP_classe.keys():
            I=DicoP_classe[key][1]
            counter+=1
            zPercent = int(2+(98 * counter / zdim))
            self.progressBar.setValue(zPercent)
            for featP in CoucheP.getFeatures():
                Poly_id = featP.id()
                if I==Poly_id:
                    newfeat = QgsFeature()
                    attributsF = featP.attributes()
                    geomP=featP.geometry()
                    surfF=DicoP_classe[key][0]
                    classement=int(key)
                    ID=Poly_id
                    Values=[]
                    Values.extend(attributsF)
                    Values.append(surfF)
                    Values.append(classement)                       
                    Values.append(ID)
                    newfeat.setGeometry(geomP)
                    newfeat.setAttributes(Values)
                    prPyramide.addFeatures([newfeat])
            
        Pyramide.commitChanges()
        #iface.mapCanvas().refresh()                     
        self.iface.mapCanvas().refresh()    
 
              
    
