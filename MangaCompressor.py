# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from shutil import rmtree, copytree
from os.path import isdir, splitext, basename, dirname
from os import listdir, unlink, renames
from glob import glob
import re

from os import stat
from PIL import Image

import zipfile

from PyQt5 import QtWidgets
import sys
#from PyQt5 import uic



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Convertir imágenes
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def copymanga(direccion,self):
    app.processEvents()
    try:
        copytree(direccion,dirname(direccion)+'/'+"Backup_"+basename(direccion))
    except:
        self.error_dialog = QtWidgets.QErrorMessage()
        self.error_dialog.showMessage('Algo salió mal con la carpeta backup, tal vez sea que ya exciste.')

def converterInteligente(direccion,self):
    imagenes = glob(direccion + '/' + '*/*.' + 'jpg') + glob(direccion + '/' + '*/*.' + 'jpeg') + glob(direccion + '/' + '*/*.' + 'webp')
    self.powermax = len(imagenes)
    a = 0
    if len(imagenes) == 0:
        return
    for infile in imagenes:
        file, ext = splitext(infile)
        try:
            a = a + 1
            app.processEvents()
            self.ConvertirBar.setMinimum(0)
            self.ConvertirBar.setMaximum(self.powermax)
            self.ConvertirBar.setValue(a)
            img = Image.open(infile).convert('RGB')
            rate = img.size[0]*img.size[1]/stat(infile).st_size
            if rate > 10:
                continue
            elif img.size[0] > 1100:
                img = img.resize((1100,int(img.size[1]/img.size[0]*1100)),
                                  reducing_gap = 3.0)
           					 
            img.save(''.join([file,ext]),optimize = True, quality = int(rate*6 + 40))
        except:
            continue

def converterFijo(direccion,rate,self):
    imagenes = glob(direccion + '/' + '*/*.' + 'jpg') + glob(direccion + '/' + '*/*.' + 'jpeg') + glob(direccion + '/' + '*/*.' + 'webp')
    self.powermax = len(imagenes)
    a = 0
    if len(imagenes) == 0:
        return
    for infile in imagenes:
        file, ext = splitext(infile)
        try:
            a = a + 1
            app.processEvents()
            self.ConvertirBar.setMinimum(0)
            self.ConvertirBar.setMaximum(self.powermax)
            self.ConvertirBar.setValue(a)
            img = Image.open(infile).convert('RGB')
            if img.size[0] > 1100:
                img = img.resize((1100,int(img.size[1]/img.size[0]*1100)),
                                 reducing_gap = 3.0)
            					 
            img.save(''.join([file,ext]),optimize = True, quality = int(rate))
        except:
            continue

            
    
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Borrar archivos repetidos
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def repetidas(direccion,self):
    self.powermax = len(glob(direccion + '/' + '*/*.' + 'jpg') + glob(direccion + '/' + '*/*.' + 'jpeg') + glob(direccion + '/' + '*/*.' + 'webp'))
    q = listdir(direccion)
    l = []
    for j in q:
        l.append(''.join([direccion,'/',j]))
    a = set({})
    b = 0
    
    for i in l:
        if isdir(i) == True:
            w = listdir(i)
            for j in w:
                try:
                    b = b + 1
                    app.processEvents()
                    self.duplicadosBar.setMinimum(0)
                    self.duplicadosBar.setMaximum(self.powermax)
                    self.duplicadosBar.setValue(b)
                    c = open(''.join([i,'/',j]),'rb')
                    s = c.read()
                    if hash(s) not in a:
                        a.add(hash(s))
                    else:
                        c.close()
                        unlink(''.join([i,'/',j]))
                    c.close()
                except:
                    continue
        else:
            continue
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Comprimir carpetas dentro del directorio.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def compresor(direccion,self):
    q = listdir(direccion)
    l = []
    s = []
    for j in q:
        l.append(''.join([direccion,'/',j]))
        s.append(j)
    
    k = 0
    powermax = len(glob(direccion + '/' + '*/*.' + 'jpg') + glob(direccion + '/' + '*/*.' + 'jpeg') + glob(direccion + '/' + '*/*.' + 'webp') + glob(direccion + '/' + '*/*.' + 'png'))
    for i in l:
        if isdir(i) == True and (str(i)+'.zip') not in l:
            w = listdir(i)
            a = zipfile.ZipFile(i + '.zip', "a")
            for j in w:
                k = k + 1
                app.processEvents()
                self.zipBar.setMinimum(0)
                self.zipBar.setMaximum(powermax)
                self.zipBar.setValue(k)
                a.write(i + '\\' + j, s[l.index(i)]+ '\\' + j, compress_type=zipfile.ZIP_DEFLATED)
            a.close()
        else:
            continue
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Transforma archivos zip a cbz.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def cbzConverter(direccion,self):
    if len(glob(direccion + '/' + '*.zip')) == 0:
        return
    k = 0
    powermax = len(glob(direccion + '/' + '*.zip'))
    for infile in glob(direccion + '/' + '*.zip'):
        file, ext = splitext(infile)
        k = k + 1
        app.processEvents()
        self.cbzBar.setMinimum(0)
        self.cbzBar.setMaximum(powermax)
        self.cbzBar.setValue(k)
        try:
            renames(infile,file+'.cbz')
        except:
            continue

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Ordena los capítulos
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def testdesecuencia(l):
    if l == []:
        return True
    c = 0
    m, n = max(l), min(l)
    for i in l:
        c = c + i
    if c == m*(m+1)/2 - (n-1)*(n)/2:
        return True
    else:
        return False
         

def cbzOrden(direccion,self, tipo = "inteligente"):
    if tipo == "inteligente":
        capitulos = glob(direccion + '/' + '*.cbz')
        k = 0
        powermax = len(capitulos)
        a = re.compile(r"cap \d\d\d|cap \d\d|cap \d|capitulo \d\d\d|capitulo \d\d|capitulo \d|capítulo \d\d\d|capítulo \d\d|capítulo \d|chapter \d\d\d|chapter \d\d|chapter \d|Capitulo \d\d\d|Capitulo \d\d|Capitulo \d|Capítulo \d\d\d|Capítulo \d\d|Capítulo \d|Chapter \d\d\d|Chapter \d\d|Chapter \d|Ch\.\d\d\d|Ch\.\d\d|Ch\.\d|\d\d\d\-\d\d\d\d|\d\d\-\d\d\d|\d\-\d\d|\d\d\d\d\-\d\d\d\d|\d\d\d-\d\d\d|\d\d-\d\d|\d-\d|\d\d_\d\d|\d_\d|\d\d\d\d\.\d\d|\d\d\d\.\d\d|d\d\.\d\d|d\.\d\d|\d\d\d\d\.\d|\d\d\d\.\d|d\d\.\d|d\.\d|\d\d\d\d|\d\d\d|\d\d|\d")
        t = re.compile(r"Parte \d|parte \d|Vol\.\d\d|Vol\.\d")
        for i in capitulos:
            obj = t.sub('',basename(i))
            k = k + 1
            app.processEvents()
            self.ordenarBar.setMinimum(0)
            self.ordenarBar.setMaximum(powermax)
            self.ordenarBar.setValue(k)
            try:
                b = a.search(obj).group()
                if len(b)<2:
                    b = '0'+ b
                renames(i, ''.join([direccion,'/',b,'.cbz']))
            except:
                continue
        pdfs = glob(direccion + '/' + '*.pdf')
        for i in pdfs:
            try:
                b = a.search(basename(i)).group()
                if len(b)<2:
                    b = '0'+ b
                renames(i, ''.join([direccion,'/',b,'.pdf']))
            except:
                continue
    elif tipo == "bruto":
        capitulos = []
        if len(glob(direccion + '/' + '*.cbz')) == 0:
            return
        for infile in glob(direccion + '/' + '*.cbz'):
            file, ext = splitext(basename(infile))
            try:
                a = re.compile(r"\d\d\d\d\d\d\d\d\d|\d\d\d\d\d\d\d\d|\d\d\d\d\d\d\d|\d\d\d\d\d\d|\d\d\d\d\d|\d\d\d\d|d\d\d|d\d|\d")
                b = a.search(file).group()
                capitulos.append(float(b))
            except:
                continue
        if testdesecuencia(capitulos) == True:
            return
        orden = {}
        a = 0
        for i in range(len(capitulos)):
            orden[min(capitulos)] = str(a + 1)
            capitulos.remove(min(capitulos))
            a = a + 1
            
        k = 0
        powermax = len(glob(direccion + '/' + '*.cbz'))
        for i in orden.keys():
            k = k + 1
            app.processEvents()
            self.ordenarBar.setMinimum(0)
            self.ordenarBar.setMaximum(powermax)
            self.ordenarBar.setValue(k)
            try:
                renames(direccion + '/' + str(int(i))+'.cbz',direccion + '/' + orden[i]+'.cbz')
            except:
                continue
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Eliminar carpetas
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def eliminar(direccion,self):
    k = 0
    s = 0
    l = listdir(direccion)
    for i in l:
        j = direccion + '/' + i
        if isdir(j) == True:
            s += 1
    powermax = s 
    for i in l:
        j = direccion + '/' + i
        if isdir(j) == True:
            rmtree(j)
            k = k + 1
            app.processEvents()
            self.residualesBar.setMinimum(0)
            self.residualesBar.setMaximum(powermax)
            self.residualesBar.setValue(k)
    for i in glob(direccion + '/' + '*.PicsFolder.cbz'):
        file, ext = splitext(i)
        renames(i,file[:len(file)-11] + ext)



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Interfaz Gráfica
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""





from PyQt5 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(595, 562)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ico.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.ConvertirGrupo = QtWidgets.QGroupBox(Dialog)
        self.ConvertirGrupo.setGeometry(QtCore.QRect(50, 60, 531, 151))
        self.ConvertirGrupo.setTitle("")
        self.ConvertirGrupo.setObjectName("ConvertirGrupo")
        self.covertirCheck = QtWidgets.QCheckBox(self.ConvertirGrupo)
        self.covertirCheck.setGeometry(QtCore.QRect(20, 20, 231, 17))
        self.covertirCheck.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.covertirCheck.setChecked(True)
        self.covertirCheck.setTristate(False)
        self.covertirCheck.setObjectName("covertirCheck")
        self.ConvertirBar = QtWidgets.QProgressBar(self.ConvertirGrupo)
        self.ConvertirBar.setGeometry(QtCore.QRect(170, 20, 331, 23))
        self.ConvertirBar.setProperty("value", 0)
        self.ConvertirBar.setTextVisible(True)
        self.ConvertirBar.setInvertedAppearance(False)
        self.ConvertirBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.ConvertirBar.setObjectName("ConvertirBar")
        self.ratebar = QtWidgets.QSlider(self.ConvertirGrupo)
        self.ratebar.setGeometry(QtCore.QRect(70, 120, 160, 19))
        self.ratebar.setAccessibleName("")
        self.ratebar.setAccessibleDescription("")
        self.ratebar.setMinimum(1)
        self.ratebar.setProperty("value", 90)
        self.ratebar.setOrientation(QtCore.Qt.Horizontal)
        self.ratebar.setObjectName("ratebar")
        self.criterio = QtWidgets.QCheckBox(self.ConvertirGrupo)
        self.criterio.setGeometry(QtCore.QRect(390, 120, 81, 17))
        self.criterio.setAccessibleName("")
        self.criterio.setAccessibleDescription("")
        self.criterio.setObjectName("criterio")
        self.label_2 = QtWidgets.QLabel(self.ConvertirGrupo)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 121, 21))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.OtrasGrupo = QtWidgets.QGroupBox(Dialog)
        self.OtrasGrupo.setGeometry(QtCore.QRect(50, 210, 531, 301))
        self.OtrasGrupo.setObjectName("OtrasGrupo")
        self.duplicadosCheck = QtWidgets.QCheckBox(self.OtrasGrupo)
        self.duplicadosCheck.setEnabled(True)
        self.duplicadosCheck.setGeometry(QtCore.QRect(30, 30, 161, 17))
        self.duplicadosCheck.setChecked(True)
        self.duplicadosCheck.setObjectName("duplicadosCheck")
        self.cbzCheck = QtWidgets.QCheckBox(self.OtrasGrupo)
        self.cbzCheck.setGeometry(QtCore.QRect(30, 130, 151, 17))
        self.cbzCheck.setChecked(True)
        self.cbzCheck.setObjectName("cbzCheck")
        self.zipCheck = QtWidgets.QCheckBox(self.OtrasGrupo)
        self.zipCheck.setGeometry(QtCore.QRect(30, 80, 201, 17))
        self.zipCheck.setChecked(True)
        self.zipCheck.setObjectName("zipCheck")
        self.ordenarCheck = QtWidgets.QCheckBox(self.OtrasGrupo)
        self.ordenarCheck.setGeometry(QtCore.QRect(30, 180, 231, 16))
        self.ordenarCheck.setChecked(False)
        self.ordenarCheck.setObjectName("ordenarCheck")
        self.eliminarCheck = QtWidgets.QCheckBox(self.OtrasGrupo)
        self.eliminarCheck.setGeometry(QtCore.QRect(30, 270, 171, 17))
        self.eliminarCheck.setChecked(True)
        self.eliminarCheck.setObjectName("eliminarCheck")
        self.duplicadosBar = QtWidgets.QProgressBar(self.OtrasGrupo)
        self.duplicadosBar.setGeometry(QtCore.QRect(310, 20, 201, 23))
        self.duplicadosBar.setProperty("value", 0)
        self.duplicadosBar.setObjectName("duplicadosBar")
        self.zipBar = QtWidgets.QProgressBar(self.OtrasGrupo)
        self.zipBar.setGeometry(QtCore.QRect(310, 70, 201, 23))
        self.zipBar.setProperty("value", 0)
        self.zipBar.setObjectName("zipBar")
        self.cbzBar = QtWidgets.QProgressBar(self.OtrasGrupo)
        self.cbzBar.setGeometry(QtCore.QRect(310, 120, 201, 23))
        self.cbzBar.setProperty("value", 0)
        self.cbzBar.setObjectName("cbzBar")
        self.ordenarBar = QtWidgets.QProgressBar(self.OtrasGrupo)
        self.ordenarBar.setGeometry(QtCore.QRect(310, 170, 201, 23))
        self.ordenarBar.setProperty("value", 0)
        self.ordenarBar.setObjectName("ordenarBar")
        self.residualesBar = QtWidgets.QProgressBar(self.OtrasGrupo)
        self.residualesBar.setGeometry(QtCore.QRect(320, 270, 201, 23))
        self.residualesBar.setProperty("value", 0)
        self.residualesBar.setObjectName("residualesBar")
        self.inteligenteRadio = QtWidgets.QRadioButton(self.OtrasGrupo)
        self.inteligenteRadio.setGeometry(QtCore.QRect(100, 230, 82, 17))
        self.inteligenteRadio.setChecked(True)
        self.inteligenteRadio.setObjectName("inteligenteRadio")
        self.brutoRadio = QtWidgets.QRadioButton(self.OtrasGrupo)
        self.brutoRadio.setGeometry(QtCore.QRect(260, 230, 82, 17))
        self.brutoRadio.setObjectName("brutoRadio")
        self.manga = QtWidgets.QLineEdit(Dialog)
        self.manga.setGeometry(QtCore.QRect(170, 30, 381, 21))
        self.manga.setInputMethodHints(QtCore.Qt.ImhNone)
        self.manga.setDragEnabled(True)
        self.manga.setClearButtonEnabled(True)
        self.manga.setObjectName("manga")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 30, 121, 21))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.Iniciar = QtWidgets.QPushButton(Dialog)
        self.Iniciar.setGeometry(QtCore.QRect(140, 520, 91, 31))
        self.Iniciar.setObjectName("Iniciar")
        self.Reiniciar = QtWidgets.QPushButton(Dialog)
        self.Reiniciar.setGeometry(QtCore.QRect(360, 520, 91, 31))
        self.Reiniciar.setObjectName("Reiniciar")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Compresor de Mangas S"))
        self.covertirCheck.setText(_translate("Dialog", "Comprimir imagenes"))
        self.criterio.setText(_translate("Dialog", "Por defecto"))
        self.label_2.setText(_translate("Dialog", "Criterio de compresión:"))
        self.OtrasGrupo.setTitle(_translate("Dialog", "GroupBox"))
        self.duplicadosCheck.setText(_translate("Dialog", "Eliminar archivos duplicados"))
        self.cbzCheck.setText(_translate("Dialog", "Transformar de zip a cbz"))
        self.zipCheck.setText(_translate("Dialog", "Comprimir carpetas en el interior a zip"))
        self.ordenarCheck.setText(_translate("Dialog", "Ordenar los cbz en formato numérico"))
        self.eliminarCheck.setText(_translate("Dialog", "Eliminar carpetas residuales"))
        self.inteligenteRadio.setText(_translate("Dialog", "inteligente"))
        self.brutoRadio.setText(_translate("Dialog", "bruto"))
        self.label.setText(_translate("Dialog", "Carpeta Objetivo"))
        self.Iniciar.setText(_translate("Dialog", "Iniciar"))
        self.Reiniciar.setText(_translate("Dialog", "Reiniciar"))


# class Ui(QtWidgets.QDialog):
#     def __init__(self):
#         super(Ui, self).__init__()
#         uic.loadUi('Ventana.ui', self)


class Ui(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        
        self.manga = self.findChild(QtWidgets.QLineEdit, 'manga')
        self.covertirCheck = self.findChild(QtWidgets.QCheckBox, 'covertirCheck')
        self.ratebar = self.findChild(QtWidgets.QSlider, 'ratebar')
        self.criterio = self.findChild(QtWidgets.QCheckBox, 'criterio')
        self.duplicadosCheck = self.findChild(QtWidgets.QCheckBox, 'duplicadosCheck')
        self.zipCheck = self.findChild(QtWidgets.QCheckBox, 'zipCheck')
        self.cbzCheck = self.findChild(QtWidgets.QCheckBox, 'cbzCheck')
        self.ordenarCheck = self.findChild(QtWidgets.QCheckBox, 'ordenarCheck')
        self.eliminarCheck = self.findChild(QtWidgets.QCheckBox, 'eliminarCheck')
        self.ConvertirBar = self.findChild(QtWidgets.QProgressBar, 'ConvertirBar')
        self.duplicadosBar = self.findChild(QtWidgets.QProgressBar, 'duplicadosBar')
        self.zipBar = self.findChild(QtWidgets.QProgressBar, 'zipBar')
        self.cbzBar = self.findChild(QtWidgets.QProgressBar, 'cbzBar')
        self.ordenarBar = self.findChild(QtWidgets.QProgressBar, 'ordenarBar')
        self.inteligenteRadio = self.findChild(QtWidgets.QRadioButton, 'inteligenteRadio')
        self.brutoRadio = self.findChild(QtWidgets.QRadioButton, 'brutoRadio')
        self.residualesBar = self.findChild(QtWidgets.QProgressBar, 'residualesBar')
        
        
        self.Iniciar = self.findChild(QtWidgets.QPushButton, 'Iniciar')
        self.Iniciar.clicked.connect(self.IniciarPresionado)
        self.Reiniciar = self.findChild(QtWidgets.QPushButton, 'Reiniciar')
        self.Reiniciar.clicked.connect(self.ReiniciarPresionado)
        
        self.covertirCheck.stateChanged.connect(self.checkchange)
        self.criterio.stateChanged.connect(self.checkchange)
        self.ordenarCheck.stateChanged.connect(self.checkchange)
        
        self.inteligenteRadio.setEnabled(False)
        self.brutoRadio.setEnabled(False)
        
        self.show()
    
    def checkchange(self):
        if not self.covertirCheck.isChecked() == True:
            self.ratebar.setEnabled(False)
            self.criterio.setEnabled(False)
        else:
            self.criterio.setEnabled(True)
            if self.criterio.isChecked() == True:
                self.ratebar.setEnabled(False)
            else:
                self.ratebar.setEnabled(True)
        
        if not self.ordenarCheck.isChecked() == True:
            self.inteligenteRadio.setEnabled(False)
            self.brutoRadio.setEnabled(False)
        else:
            self.inteligenteRadio.setEnabled(True)
            self.brutoRadio.setEnabled(True)
    
    def IniciarPresionado(self):
        
        #copymanga(self.manga.text(),self)
        self.destino = self.manga.text()
        
        if self.duplicadosCheck.isChecked() == True:
            repetidas(self.destino,self)
        
        if self.covertirCheck.isChecked() == True:
            if self.criterio.isChecked() == True:
                converterInteligente(self.destino,self)
            else:
                converterFijo(self.destino,self.ratebar.value(),self)
        
        if self.zipCheck.isChecked() == True:
            compresor(self.destino,self)
            
        if self.cbzCheck.isChecked() == True:
            cbzConverter(self.destino,self)

        if self.ordenarCheck.isChecked() == True:
            if self.inteligenteRadio.isChecked() == True:
                cbzOrden(self.destino,self, "inteligente")
            elif self.brutoRadio.isChecked() == True:
                cbzOrden(self.destino,self, "bruto")
        
        if self.eliminarCheck.isChecked() == True:
            eliminar(self.destino,self)
    
    def ReiniciarPresionado(self):
        self.manga.setText('')
        self.ConvertirBar.setMinimum(0)
        self.ConvertirBar.setMaximum(100)
        self.ConvertirBar.setValue(0)
        
        self.duplicadosBar.setMinimum(0)
        self.duplicadosBar.setMaximum(100)
        self.duplicadosBar.setValue(0)
        
        self.zipBar.setMinimum(0)
        self.zipBar.setMaximum(100)
        self.zipBar.setValue(0)
        
        self.cbzBar.setMinimum(0)
        self.cbzBar.setMaximum(100)
        self.cbzBar.setValue(0)
        
        self.ordenarBar.setMinimum(0)
        self.ordenarBar.setMaximum(100)
        self.ordenarBar.setValue(0)
        
        self.residualesBar.setMinimum(0)
        self.residualesBar.setMaximum(100)
        self.residualesBar.setValue(0)
        app.exec_()
        
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()