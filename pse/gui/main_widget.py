""" Bibliotecas externas. """
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QGridLayout,
                             QLabel,
                             QSizePolicy,
                             QVBoxLayout,
                             QWidget)

class MainWidget(QWidget):
    PIXMAP_DIM = 256
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
                
        self.grid = {'rows': self.parent.height() // MainWidget.PIXMAP_DIM,
                     'cols': self.parent.width() // MainWidget.PIXMAP_DIM}
        
        self.items = []

        self.replicate = -1
        self.initUI()
        

    def initUI(self):
        """ Inicializa o widget principal do programa, que
        contém todas as pixmapns - original e processadas.
        """
        
        layout = QGridLayout()
        self.setLayout(layout)

        
    def resizeEvent(self, event):
        super().resizeEvent(event)

        oldGrid = self.grid
        self.grid = {'rows': self.parent.height() // MainWidget.PIXMAP_DIM,
                     'cols': self.parent.width() // MainWidget.PIXMAP_DIM}

        
        # Caso grid não tenha mudado ou nenhuma pixmapm tenha sido carrregada,
        # nada a fazer.
        if self.grid == oldGrid or not self.items:
            return
 
        # Repreenche o grid, de acordo com as novas dimensões.
        self.fillGrid(self.items)
        

    def addGridItem(self, text, pixmap, i, j):
        """ Add an item to the grid.

        @param text String
        @param pixmap QPixmap
        @param i int
        @param j int
        """

        textLabel = QLabel(text)
        textLabel.setStyleSheet('QColor {color: #424242;}')
        
        pixmapLabel = QLabel()
        pixmapLabel.setPixmap(pixmap)
        pixmapLabel.setMinimumSize(1, 1)

        itemLayout = QVBoxLayout()
        itemLayout.addWidget(textLabel)
        itemLayout.addWidget(pixmapLabel)
        
        itemWidget = QWidget()
        itemWidget.setLayout(itemLayout)
        
        self.layout().addWidget(itemWidget, i, j)
                        
        
    def clearGrid(self):
        """ Limpa todos os items da tela. """

        for i in reversed(range(self.layout().count())):
            self.layout().itemAt(i).widget().setParent(None)

        
    def fillGrid(self, items):
        """ Preencha o grid com as pixmapns e seus respectivos labels. """

        # Caso pixmapm ainda não tenha sido carregada ou pixmapm original
        # não exista, retornar.
        if not items:
            return

        # Limpa todo o grid antes de repreencher.
        self.clearGrid()

        # Preenche grid de forma que, caso a quantidade de itens não
        # seja suficiente para ocupar todo o grid, replique a ultima
        # pixmapm.
        gridSize = (self.grid['rows'] * self.grid['cols'])
        numItems = len(items)
        item = 0

        # Caso tenha mais itens do que posições no grid, descartar
        # as pixmapms mais antigas (com execessão da original)
        if numItems > gridSize:
            start = numItems - gridSize + 1
            items = [items[0]] + items[start:]

        for i in range(self.grid['rows']):
            for j in range(self.grid['cols']):
                text = items[item]['label']
                # pixmapQt = PixmapQt.PixmapQt(items[item]['pixmap'])
                # pixmap = QPixmap.fromPixmap(pixmapQt)
                pixmap = items[item]['pixmap']

                self.addGridItem(text, pixmap, i, j)

                item += 1 and item != self.replicate


    def undo(self):
        """ Retira a útima pixmapm processada da lista e
        recalcula a posição de réplica. Ação só é realizada
        caso exista alguma pixmapm diferente da original.
        """

        if len(self.items) > 1:
            self.items.pop()
            self.replicate -= 1
            self.fillGrid(self.items)


    def insertOriginal(self, pixmap):
        """ Insere a nova pixmapm em todas as posições do grid.

        @param pixmap PIL.Pixmap
        """

        pixmap = pixmap.scaled(256, 256, Qt.IgnoreAspectRatio,
                               Qt.SmoothTransformation)
        dim = (pixmap.width(), pixmap.height())
        item = {'label': 'Original {}'.format(dim), 'pixmap': pixmap}

        self.items = [item]
        self.replicate = 0
                      
        self.fillGrid(self.items)


    def insertProcessed(self, pixmap, label):
        """ Insere uma pixmapm recém processada no grid.
        
        @param pixmap PIL.Pixmap
        """
        
        # Variável usada para, caso grid não tenha sido completamente preenchido
        # ainda (contém cópias de alguma pixmapm), setar a nova pixmapm como a que
        # será replicada.
        
        self.replicate += 1

        pixmap = pixmap.scaled(256, 256, Qt.IgnoreAspectRatio,
                               Qt.SmoothTransformation)
        dim = (pixmap.width(), pixmap.height())

        self.items.append({'label': label, 'pixmap': pixmap})
        self.fillGrid(self.items)
