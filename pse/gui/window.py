""" Bibliotecas externas. """
from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import (QIcon,
                         QPixmap)
from PyQt5.QtWidgets import (QAction,
                             qApp,
                             QDialog,
                             QHBoxLayout,
                             QDesktopWidget,
                             QFileDialog,
                             QLabel,
                             QMainWindow,
                             QWidget)

""" Bibliotecas locais. """
from gui.dialog_interpolation import (DialogInterpolation)
from gui.dialog_filter import (DialogFilter)
from gui.dialog_histogram import (DialogHistogram)
from gui.toolbar import (ToolBar)
from util.resources import ICONS

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.image = {'original': None, 'processed': None}
        
        exitAct = QAction(self)
        exitAct.triggered.connect(qApp.quit)
        exitAct.setShortcut('Ctrl+Q')
        self.addAction(exitAct)
        
        self.initUI()

        
    def initUI(self):
        """ Inicializa todos os widgets relacionados a janela
        principal do programa.
        """
        
        self.resize(1024, 512)
        self.center()
        self.setWindowTitle('PSE')
        self.createToolBar()

        self.layout = QHBoxLayout()
        
        centralWidget = QWidget()
        centralWidget.setLayout(self.layout)
        
        self.setCentralWidget(centralWidget)
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
        interpAct.triggered.connect(lambda: DialogInterpolation.getResults(self))
        self.toolbar.addAction(interpAct)

        # Histograma
        histAct = QAction(QIcon(ICONS['histogram']), 'Histograma', self.toolbar)
        histAct.triggered.connect(lambda: DialogHistogram.getResults(self))
        self.toolbar.addAction(histAct)

        # Salvar Imagem
        saveAct = QAction(QIcon(ICONS['save']), 'Salvar Imagem', self.toolbar)
        saveAct.triggered.connect(self.saveImage)
        self.toolbar.addAction(saveAct)
        
        self.addToolBar(self.toolbar)


    def applyFilter(self):
        (data, ok) = DialogFilter.getResults(self)

        if ok == QDialog.Rejected:
            return None

        (row, col) = data['mask'].split('x')
        (row, col) = int(row), int(col)
        
        
    def getImage(self):
        (imagePath, _) = QFileDialog.getOpenFileName(self, 'Carregar Imagem',
                                                     filter='Images (*.png *.jpg)')

        print(imagePath)
        if self.image['original']:
            self.layout.removeWidget(self.image['original'])
            self.layout.removeWidget(self.image['processed'])
            
        self.image['original'] = QLabel()
        self.image['original'].setAlignment(Qt.AlignVCenter)
        
        self.image['processed'] = QLabel()
        self.image['processed'].setAlignment(Qt.AlignVCenter)
        
        pixmap = QPixmap(imagePath).scaled(512, 512, Qt.KeepAspectRatio)
        
        self.image['original'].setPixmap(pixmap)
        self.image['processed'].setPixmap(pixmap)
        
        self.layout.addWidget(self.image['original'])
        self.layout.addWidget(self.image['processed'])
        
        
    def saveImage(self):
        (imagePath, _) = QFileDialog.getSaveFileName(self, 'Salvar Imagem',
                                                     filter='Images (*.png *.jpg)')
        self.image['processed'].pixmap().save(imagePath)
