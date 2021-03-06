""" Bibliotecas externas. """
import numpy
from qimage2ndarray import (rgb_view,
                            array2qimage)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (QIcon,
                         QPixmap)
from PyQt5.QtWidgets import (QAction,
                             qApp,
                             QDialog,
                             QDesktopWidget,
                             QFileDialog,
                             QLabel,
                             QMainWindow)

""" Bibliotecas locais. """
from algorithm.filter import (low_pass,
                              high_pass,
                              morph)
from algorithm.interpolation import interpolation
from gui.dialog_high_pass import DialogHighPass
from gui.dialog_low_pass import DialogLowPass
from gui.dialog_morph import DialogMorph
from gui.dialog_histogram import DialogHistogram
from gui.dialog_interpolation import DialogInterpolation
from gui.main_widget import MainWidget
from gui.toolbar import ToolBar
from util.resources import ICONS

class MainWindow(QMainWindow):
    MIN_WIDTH = 512
    MIN_HEIGHT = 256
    
    WIDTH = 1024
    HEIGHT = 512
    
    def __init__(self):
        super().__init__()
        
        exitAct = QAction(self)
        exitAct.triggered.connect(qApp.quit)
        exitAct.setShortcut('Ctrl+Q')
        self.addAction(exitAct)
        
        self.initUI()
        
        
    def initUI(self):
        """ Inicializa todos os widgets relacionados a janela
        principal do programa.
        """

        self.centralWidget = MainWidget(self)
        self.setCentralWidget(self.centralWidget)
        
        self.resize(MainWindow.WIDTH, MainWindow.HEIGHT)
        self.setMinimumSize(MainWindow.MIN_WIDTH, MainWindow.MIN_HEIGHT)
        self.center()
        self.setWindowTitle('PSE')
        self.setWindowIcon(QIcon(ICONS['pse']))
        self.createToolBar()

        self.show()
    

    def center(self):
        """ Centraliza a janela principal, em relação ao Desktop. """
        
        frame = self.frameGeometry()
        cpoint = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(cpoint)
        self.move(frame.topLeft())


    def createToolBar(self):
        """ Cria o menu de ferramentas. """

        self.toolbar = ToolBar(self)

        # Carregar imagem
        openAct = QAction(QIcon(ICONS['open']), 'Carregar Imagem', self.toolbar)
        openAct.triggered.connect(self.getImage)
        openAct.setShortcut('Ctrl+N')
        self.toolbar.addAction(openAct)
        
        # Filtros (F)
        # F: Passa-Alta
        highpassAct = QAction(QIcon(ICONS['high_pass']), 'Passa-Alta', self.toolbar)
        highpassAct.triggered.connect(self.applyHighPass)
        self.toolbar.addAction(highpassAct)

        # F: Passa-Baixa
        lowpassAct = QAction(QIcon(ICONS['low_pass']), 'Passa-Baixa', self.toolbar)
        lowpassAct.triggered.connect(self.applyLowPass)
        self.toolbar.addAction(lowpassAct)

        # F: Morfológico
        morphAct = QAction(QIcon(ICONS['morph']), 'Morfológico', self.toolbar)
        morphAct.triggered.connect(self.applyMorph)
        self.toolbar.addAction(morphAct)

        # Interpolação
        interpAct = QAction(QIcon(ICONS['interpolation']), 'Interpolação',
                            self.toolbar)
        interpAct.triggered.connect(self.applyInterpolation)
        self.toolbar.addAction(interpAct)

        # Histograma
        histAct = QAction(QIcon(ICONS['histogram']), 'Histograma', self.toolbar)
        histAct.triggered.connect(self.plotHistogram)
        self.toolbar.addAction(histAct)

        # Desfazer última ação
        undoAct = QAction(QIcon(ICONS['undo']), 'Desfazer', self.toolbar)
        undoAct.triggered.connect(lambda: self.centralWidget.undo())
        self.toolbar.addAction(undoAct)

        # Salvar Imagem
        saveAct = QAction(QIcon(ICONS['save']), 'Salvar Imagem', self.toolbar)
        saveAct.triggered.connect(self.saveImage)
        self.toolbar.addAction(saveAct)
        
        self.addToolBar(self.toolbar)


    def applyFilter(self, data, ok):

        # Se opção foi cancelar ou se nenhuma imagem foi carregada
        # ainda, retornar.
        if not ok or not self.centralWidget.items:
            return

        row = data['opt']
        filterFn = None
        label = ''
        
        if data['filter'] in low_pass.Filter:
            filterFn = low_pass.applyFilter
            label = low_pass.FilterLabel[data['filter']] + \
                ' ({})'.format(data['opt'])

        elif data['filter'] in high_pass.Filter:
            filterFn = high_pass.applyFilter
            label = high_pass.FilterLabel[data['filter']]

            if data['filter'] == high_pass.Filter.GAUSSIAN_LAPLACE:
                label += ' ({})'.format(data['opt'])
            
        elif data['filter'] in morph.Filter:
            filterFn = morph.applyFilter
            label = morph.FilterLabel[data['filter']] + \
                ' ({})'.format(data['opt'])

        lastItem = len(self.centralWidget.items) - 1
        image = self.centralWidget.items[lastItem]['pixmap'].toImage()
        imageMatrix = rgb_view(image)

        newImage = QPixmap.fromImage(
            array2qimage(filterFn(imageMatrix, row, data['filter']))
        )

        label += ' {}'.format((newImage.width(), newImage.height()))
        self.centralWidget.insertProcessed(newImage, label)


    def applyHighPass(self):
        (data, ok) = DialogHighPass.getResults(self)

        if data['opt'] and data['filter'] == high_pass.Filter.GAUSSIAN_LAPLACE:
            data['opt'] = float(data['opt'])
            
        self.applyFilter(data, ok)
        

    def applyLowPass(self):
        (data, ok) = DialogLowPass.getResults(self)

        if data['opt'] and data['filter'] == low_pass.Filter.GAUSSIAN:
            data['opt'] = float(data['opt'])
            
        self.applyFilter(data, ok)

        
    def applyMorph(self):
        (data, ok) = DialogMorph.getResults(self)

        self.applyFilter(data, ok)

        
    def applyInterpolation(self):
        (data, ok) = DialogInterpolation.getResults(self)

        if not ok or not self.centralWidget.items:
            return

        if data['scale']:
            scale = float(data['scale'])

            order = self.interpolationOrder(data['order']) if data['order'] else 0
            
            lastItem = len(self.centralWidget.items) - 1
            proc = rgb_view(self.centralWidget.items[lastItem]['pixmap'].toImage())
            
            newImage = QPixmap.fromImage(
                array2qimage(interpolation.nearest_neighbor(proc, scale, order))
            )

            self.centralWidget.insertProcessed(
                newImage,
                '{} {}'.format(data['order'], (newImage.width(), newImage.height()))
            )
        

    def plotHistogram(self):
        lastItem = len(self.centralWidget.items) - 1

        if lastItem >= 0:
            orig = self.centralWidget.items[0]['pixmap'].toImage()
            proc = self.centralWidget.items[lastItem]['pixmap'].toImage()
            DialogHistogram.getResults(orig, proc, self)

    def interpolationOrder(self, order):
        if 'Vizinho Mais Próximo' == order:
            ord = 0
        elif 'Bilinear' == order:
            ord = 1
        elif 'Bicúbica' == order:
            ord = 2
        else:
            ord = 0

        return ord
            
    def getImage(self):
        (imagePath, ok) = QFileDialog \
            .getOpenFileName(self, 'Carregar Imagem',
                             filter='Images (*.png *.jpg *.jpeg)')

        if not ok:
            return

        image = QPixmap(imagePath)
        self.centralWidget.insertOriginal(image)

   
    def saveImage(self):
        (imagePath, _) = QFileDialog \
            .getSaveFileName(self, 'Salvar Imagem',
                             filter='Images (*.png *.jpg *.jpeg)')

        lastItem = len(self.centralWidget.items) - 1
        if lastItem >= 0:
            self.centralWidget.items[lastItem]['pixmap'].save(imagePath)
