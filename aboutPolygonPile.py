# -*- coding: utf-8 -*-

import os
import os.path
from qgis.core import QgsProject, QgsMapLayer, QgsWkbTypes
from qgis.PyQt.QtCore import QFileInfo, QSettings, QCoreApplication
from qgis.PyQt.QtCore import QTranslator, qVersion
from qgis.PyQt.QtGui import QIcon,QFont,QPalette,QBrush,QColor
from PyQt5 import QtCore
from qgis.PyQt.QtWidgets import QAction, QMessageBox,QDialog, QDialogButtonBox,QAction,QGridLayout,QLabel,QTextEdit,QPushButton,QFrame,QSpacerItem,QSizePolicy,QApplication
# Import libs 

import sys

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,320,360).size()).expandedTo(Dialog.minimumSizeHint()))

        self.gridlayout = QGridLayout(Dialog)
        self.gridlayout.setObjectName("gridlayout")

        font = QFont()
        font.setPointSize(15) 
        font.setWeight(50) 
        font.setBold(True)
        
        self.label_2 = QLabel(Dialog)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,1,1,1,2)
         
        self.textEdit = QTextEdit(Dialog)

        palette = QPalette()

        brush = QBrush(QColor(0,0,0,0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Active,QPalette.Base,brush)

        brush = QBrush(QColor(0,0,0,0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive,QPalette.Base,brush)

        brush = QBrush(QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled,QPalette.Base,brush)
        self.textEdit.setPalette(palette)
        self.textEdit.setAutoFillBackground(True)
        self.textEdit.width = 320
        self.textEdit.height = 360
        self.textEdit.setFrameShape(QFrame.NoFrame)
        self.textEdit.setFrameShadow(QFrame.Plain)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
       
        self.gridlayout.addWidget(self.textEdit,2,1,5,2) 

        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.gridlayout.addWidget(self.pushButton,4,2,1,1) 

        spacerItem = QSpacerItem(20,40,QSizePolicy.Minimum,QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem,3,1,1,1)

        self.retranslateUi(Dialog)
        self.pushButton.clicked.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QApplication.translate("Dialog", "Polygons_Pile", None))
        self.label_2.setText(QApplication.translate("Dialog", "Polygons_Pile 3.1", None))
        self.textEdit.setHtml(QApplication.translate("Dialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><span style=\" font-weight:600;\">"
        "Polygons_Pile :  </span>"
        " This plugin orders the polygons of a layer, making a pyramid of them, with the smallest ont top and the largest at the bottom.                                                                   "
        " It makes a new layer with polygons in pyramid order.                                                                                                  </b>"
        " The new layer contains attributes values from original layer plus 3 extras:                                                                               </b>"
        " - area ( in current projection units),                                                                                                                 </b>"
        " - rank : first is the largest polygon and last the smallest,                                                                                          </b>"
        " - id_poly : the feature's id - it's the row number minus one in original attribute table.                                                                           </b>"  
        " NOTA BENE: all rasters should be unchecked in layer panel or the plugin won't work !                                                                          </b>" 
        " This plugin is not a part of Qgis engine and any problems should be reported only to the author. </p></td></tr></table>"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
        "<p style=\"margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
        "                   "
        "<br><b>jeanchristophebaudin@ymail.com</b><br>"
        "<br><br><i>code 3.1 (07 février 2019).</i></p></body></html>", None))
        self.pushButton.setText(QApplication.translate("Dialog", "OK", None))

