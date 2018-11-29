""" Bibliotecas externas. """
import cv2
from matplotlib         import pyplot as plt
import numpy as np
import os
from PyQt5.QtCore       import (Qt,
                            QRect)
from PyQt5.QtGui        import (QPixmap,
                            QFont)
from PyQt5.QtWidgets    import (QDialog,
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
        
        self.b1 = QRadioButton('Escala de Cinza')
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

        rButtons.setAlignment(Qt.AlignCenter)
        layout = QFormLayout(self)
        layout.addRow(rButtons) 

        l1 = QLabel()
        l2 = QLabel()

        #Adcionar o Histograma Img Original à Widget
        l1.setText("Imagem Original")
        layout.addRow(l1)
        l1.setFont(QFont("Arial", 14, 75, False))
        l1.setAlignment(Qt.AlignCenter)
        hLayout = QHBoxLayout()
        self.imgLabelOri = QLabel()
        pixmap = QPixmap(HIST + 'hist_ori.png')
        self.imgLabelOri.setPixmap(pixmap)
        self.imgLabelOri.show()
        hLayout.addWidget(self.imgLabelOri)
        layout.addRow(hLayout)

        #Adcionar o Histograma Img Processada à Widget
        l2.setText("Última Imagem Processada")
        layout.addRow(l2)
        l2.setFont(QFont("Arial", 14, 75, False))
        l2.setAlignment(Qt.AlignCenter)
        hLayout = QHBoxLayout()
        self.imgLabelProc = QLabel()
        pixmap = QPixmap(HIST + 'hist_proc.png')
        self.imgLabelProc.setPixmap(pixmap)
        self.imgLabelProc.show()
        hLayout.addWidget(self.imgLabelProc)
        layout.addRow(hLayout)

        # Butões de OK e Cancel
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok, Qt.Horizontal, self)
        buttons.accepted.connect(self.btnOkPressed)
        layout.addRow(buttons)
        
        self.setLayout(layout)
        self.setWindowTitle('Histograms')


    def btnState(self, b):
        if b.text() == 'Escala de Cinza':
            if b.isChecked() == True:
                pixmap = QPixmap(HIST + 'hist_ori.png')
                self.imgLabelOri.setPixmap(pixmap)
                self.imgLabelOri.show()

                pixmap = QPixmap(HIST + 'hist_proc.png')
                self.imgLabelProc.setPixmap(pixmap)
                self.imgLabelProc.show()
                
        if b.text() == 'RED':
            if b.isChecked() == True:
                pixmap = QPixmap(HIST + 'red_ori.png')
                self.imgLabelOri.setPixmap(pixmap)
                self.imgLabelOri.show()

                pixmap = QPixmap(HIST + 'red_proc.png')
                self.imgLabelProc.setPixmap(pixmap)
                self.imgLabelProc.show()

        if b.text() == 'GREEN':
            if b.isChecked() == True:
                pixmap = QPixmap(HIST + 'green_ori.png')
                self.imgLabelOri.setPixmap(pixmap)
                self.imgLabelOri.show()

                pixmap = QPixmap(HIST + 'green_proc.png')
                self.imgLabelProc.setPixmap(pixmap)
                self.imgLabelProc.show()

        if b.text() == 'BLUE':
            if b.isChecked() == True:
                pixmap = QPixmap(HIST + 'blue_ori.png')
                self.imgLabelOri.setPixmap(pixmap)
                self.imgLabelOri.show()

                pixmap = QPixmap(HIST + 'blue_proc.png')
                self.imgLabelProc.setPixmap(pixmap)
                self.imgLabelProc.show()


    def btnOkPressed(self):
        if os.path.exists(HIST + 'orig_tmp.jpg'):
            os.remove(HIST + 'orig_tmp.jpg')
            os.remove(HIST + 'hist_ori.png')
            os.remove(HIST + 'red_ori.png')
            os.remove(HIST + 'green_ori.png')
            os.remove(HIST + 'blue_ori.png')
            os.remove(HIST + 'proc_tmp.jpg')
            os.remove(HIST + 'hist_proc.png')
            os.remove(HIST + 'red_proc.png')
            os.remove(HIST + 'green_proc.png')
            os.remove(HIST + 'blue_proc.png')
        self.accept()


    def saveHistograms(self):
        img = cv2.imread(HIST + 'orig_tmp.jpg')
        plt.hist(img.ravel(), 256, [0,256])
        plt.savefig(HIST + 'hist_ori.png', dpi = 70)
        plt.clf()

        histr = cv2.calcHist([img],[0],None,[256],[0,256])
        plt.plot(histr, color = 'b')
        plt.xlim([0,256])
        plt.savefig(HIST + 'blue_ori.png', dpi = 70)
        plt.clf()

        histr = cv2.calcHist([img],[1],None,[256],[0,256])
        plt.plot(histr, color = 'g')
        plt.xlim([0,256])
        plt.savefig(HIST + 'green_ori.png', dpi = 70)
        plt.clf()

        histr = cv2.calcHist([img],[2],None,[256],[0,256])
        plt.plot(histr, color = 'r')
        plt.xlim([0,256])
        plt.savefig(HIST + 'red_ori.png', dpi = 70)
        plt.clf()

        img = cv2.imread(HIST + 'proc_tmp.jpg')
        plt.hist(img.ravel(), 256, [0,256])
        plt.savefig(HIST + 'hist_proc.png', dpi = 70)
        plt.clf()

        histr = cv2.calcHist([img],[0],None,[256],[0,256])
        plt.plot(histr, color = 'b')
        plt.xlim([0,256])
        plt.savefig(HIST + 'blue_proc.png', dpi = 70)
        plt.clf()

        histr = cv2.calcHist([img],[1],None,[256],[0,256])
        plt.plot(histr, color = 'g')
        plt.xlim([0,256])
        plt.savefig(HIST + 'green_proc.png', dpi = 70)
        plt.clf()

        histr = cv2.calcHist([img],[2],None,[256],[0,256])
        plt.plot(histr, color = 'r')
        plt.xlim([0,256])
        plt.savefig(HIST + 'red_proc.png', dpi = 70)
        plt.clf()


    @staticmethod
    def getResults(origImage, procImage, parent = None):
        """ Método estático que cria o dialog e retorna true com sua finalização """
        dialog = DialogHistogram(origImage, procImage, parent)
        result = dialog.exec_()
        return True
