# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'About_Dialog.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(489, 235)
        Dialog.setStyleSheet(_fromUtf8(""))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(170, 90, 171, 20))
        self.label_2.setBaseSize(QtCore.QSize(0, 0))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(170, 150, 62, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(170, 110, 311, 20))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(170, 10, 191, 61))
        self.label_5.setText(_fromUtf8(""))
        self.label_5.setPixmap(QtGui.QPixmap(_fromUtf8(":/symbol.png")))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(170, 130, 131, 21))
        self.label_7.setObjectName(_fromUtf8("label_7"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Acerca de VAL 518", None))
        self.label_2.setText(_translate("Dialog", "Versión 3.0", None))
        self.label_3.setText(_translate("Dialog", "2018", None))
        self.label_4.setText(_translate("Dialog", "Desarrollador: Francisco Rafael Huesca M.", None))
        self.label_7.setText(_translate("Dialog", "CIDES/ Tecnología", None))

import resources_rc
