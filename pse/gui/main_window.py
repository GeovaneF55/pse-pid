""" Bibliotecas externas. """
from PIL import (Image,
                 ImageQt)
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
                              morph)
from algorithm.interpolation import interpolation
from gui.dialog_filter import DialogFilter
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
        
        # Filtros
        filtersAct = QAction(QIcon(ICONS['filters']), 'Filtros', self.toolbar)
        filtersAct.triggered.connect(self.applyFilter)
        self.toolbar.addAction(filtersAct)

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


    def applyFilter(self):
        (data, ok) = DialogFilter.getResults(self)

        # Se opção foi cancelar ou se nenhuma imagem foi carregada
        # ainda, retornar.
        if not ok or not self.centralWidget.items:
            return

        (row, _) = data['mask'].split('x')
        row = int(row)

        filterFn = None
        label = ''
        
        if data['filter'] in low_pass.Filter:
            filterFn = low_pass.applyFilter
            label = low_pass.FilterLabel[data['filter']] + \
                ' ({})'.format(data['mask'])
            
        elif data['filter'] in morph.Filter:
            filterFn = morph.applyFilter
            label = morph.FilterLabel[data['filter']] + \
                ' ({})'.format(data['mask'])

        lastItem = len(self.centralWidget.items) - 1
        newImage = filterFn(self.centralWidget.items[lastItem]['image'],
                            row, data['filter'])

        label += ' {}'.format(newImage.size)
        self.centralWidget.insertProcessed(newImage, label)
        

    def applyInterpolation(self):
        (data, ok) = DialogInterpolation.getResults(self)

        if not ok or not self.centralWidget.items:
            return

        lastItem = len(self.centralWidget.items) - 1
                                
        newImage = interpolation \
            .nearest_neighbor(self.centralWidget.items[lastItem]['image'],
                              self.centralWidget.items[lastItem]['dim'],
                              data['scale'])

        self.centralWidget.insertProcessed(
            newImage,
            '{} {}'.format(data['type'], newImage.size)
        )
        

    def plotHistogram(self):
        lastItem = len(self.centralWidget.items) - 1

        if lastItem >= 0:
            DialogHistogram.getResults(self.centralWidget.items[lastItem]['image'],
                                       self)

            
    def getImage(self):
        (imagePath, ok) = QFileDialog \
            .getOpenFileName(self, 'Carregar Imagem',
                             filter='Images (*.png *.jpg)')

        if not ok:
            return

        image = Image.open(imagePath)
        self.centralWidget.insertOriginal(image)

   
    def saveImage(self):
        (imagePath, _) = QFileDialog \
            .getSaveFileName(self, 'Salvar Imagem',
                             filter='Images (*.png *.jpg)')

        lastItem = len(self.centralWidget.items) - 1
        if lastItem >= 0:
            self.centralWidget.items[lastItem]['pixmap'].save(imagePath)
