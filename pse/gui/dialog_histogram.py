""" Bibliotecas externas. """
import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QDialog,
                             QDialogButtonBox,
                             QFormLayout,
                             QHBoxLayout,
                             QLabel,                             
                             QRadioButton)

""" Biliotecas locais. """
from util.resources import HIST
                             
class DialogHistogram(QDialog):
    def __init__(self, origImage, procImage, parent = None):
        super(DialogHistogram, self).__init__(parent)
        
        # Salvar imagem temporariamente
        origImage.save(HIST + 'orig_tmp.jpg')

        # Salvar última imagem processada temporariamente
        procImage.save(HIST + 'proc_tmp.jpg')

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.initUI()


    def initUI(self):          
        self.saveHistograms()      
        rButtons = QHBoxLayout()
        
        self.b1 = QRadioButton('RGB')
        self.b1.setChecked(True)
        self.b1.toggled.connect(lambda:self.btnState(self.b1))
        rButtons.addWidget(self.b1) 

        self.b2 = QRadioButton('RED')
        self.b2.toggled.connect(lambda:self.btnState(self.b2))
        rButtons.addWidget(self.b2)

        self.b3 = QRadioButton('GREEN')
        self.b3.toggled.connect(lambda:self.btnState(self.b3))
        rButtons.addWidget(self.b3) 

        self.b4 = QRadioButton('BLUE')
        self.b4.toggled.connect(lambda:self.btnState(self.b4))
        rButtons.addWidget(self.b4)    

        layout = QFormLayout(self)
        layout.addRow(rButtons) 

        #Adcionar o Histograma à Widget
        hLayout = QHBoxLayout()
        self.imgLabel = QLabel()
        pixmap = QPixmap(HIST + 'hist.png')
        self.imgLabel.setPixmap(pixmap)
        self.imgLabel.show()
        hLayout.addWidget(self.imgLabel)
        layout.addRow(hLayout)

        # Butões de OK e Cancel
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok, Qt.Horizontal, self)
        buttons.accepted.connect(self.btnOkPressed)
        layout.addRow(buttons)
        
        self.setLayout(layout)
        self.setWindowTitle('Histograms')


    def btnState(self, b):
        if b.text() == 'RGB':
            if b.isChecked() == True:
                pixmap = QPixmap(HIST + 'hist.png')
                self.imgLabel.setPixmap(pixmap)
                self.imgLabel.show()
                
        if b.text() == 'RED':
            if b.isChecked() == True:
                pixmap = QPixmap(HIST + 'red.png')
                self.imgLabel.setPixmap(pixmap)
                self.imgLabel.show()

        if b.text() == 'GREEN':
            if b.isChecked() == True:
                pixmap = QPixmap(HIST + 'green.png')
                self.imgLabel.setPixmap(pixmap)
                self.imgLabel.show()

        if b.text() == 'BLUE':
            if b.isChecked() == True:
                pixmap = QPixmap(HIST + 'blue.png')
                self.imgLabel.setPixmap(pixmap)
                self.imgLabel.show()

    def btnOkPressed(self):
        if os.path.exists(HIST + 'orig_tmp.jpg'):
            os.remove(HIST + 'orig_tmp.jpg')
            os.remove(HIST + 'hist.png')
            os.remove(HIST + 'red.png')
            os.remove(HIST + 'green.png')
            os.remove(HIST + 'blue.png')
        self.accept()


    def saveHistograms(self):
        img = cv2.imread(HIST + 'orig_tmp.jpg')
        plt.hist(img.ravel(), 256, [0,256])
        plt.savefig(HIST + 'hist.png')
        plt.clf()

        histr = cv2.calcHist([img],[0],None,[256],[0,256])
        plt.plot(histr, color = 'b')
        plt.xlim([0,256])
        plt.savefig(HIST + 'blue.png')
        plt.clf()

        histr = cv2.calcHist([img],[1],None,[256],[0,256])
        plt.plot(histr, color = 'g')
        plt.xlim([0,256])
        plt.savefig(HIST + 'green.png')
        plt.clf()

        histr = cv2.calcHist([img],[2],None,[256],[0,256])
        plt.plot(histr, color = 'r')
        plt.xlim([0,256])
        plt.savefig(HIST + 'red.png')
        plt.clf()


    @staticmethod
    def getResults(origImage, parent = None):
        """ Método estático que cria o dialog e retorna true com sua finalização """
        dialog = DialogHistogram(origImage, parent)
        result = dialog.exec_()
        return True
