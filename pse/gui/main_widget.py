""" Bibliotecas externas. """
from PIL import (Image,
                 ImageQt)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QGridLayout,
                             QLabel,
                             QSizePolicy,
                             QVBoxLayout,
                             QWidget)

class MainWidget(QWidget):
    IMAGE_DIM = 256
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
                
        self.grid = {'rows': self.parent.height() // MainWidget.IMAGE_DIM,
                     'cols': self.parent.width() // MainWidget.IMAGE_DIM}
        
        self.items = []

        self.replicate = -1
        self.initUI()
        

    def initUI(self):
        """ Inicializa o widget principal do programa, que
        contém todas as imagens - original e processadas.
        """
        
        layout = QGridLayout()
        self.setLayout(layout)

        
    def resizeEvent(self, event):
        super().resizeEvent(event)

        oldGrid = self.grid
        self.grid = {'rows': self.parent.height() // MainWidget.IMAGE_DIM,
                     'cols': self.parent.width() // MainWidget.IMAGE_DIM}

        
        # Caso grid não tenha mudado ou nenhuma imagem tenha sido carrregada,
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
        """ Preencha o grid com as imagens e seus respectivos labels. """

        # Caso imagem ainda não tenha sido carregada ou imagem original
        # não exista, retornar.
        if not items:
            return

        # Limpa todo o grid antes de repreencher.
        self.clearGrid()

        # Preenche grid de forma que, caso a quantidade de itens não
        # seja suficiente para ocupar todo o grid, replique a ultima
        # imagem.
        gridSize = (self.grid['rows'] * self.grid['cols'])
        numItems = len(items)
        item = 0

        # Caso tenha mais itens do que posições no grid, descartar
        # as imagems mais antigas (com execessão da original)
        if numItems > gridSize:
            start = numItems - gridSize + 1
            items = [items[0]] + items[start:]

        for i in range(self.grid['rows']):
            for j in range(self.grid['cols']):
                text = items[item]['label']
                imageQt = ImageQt.ImageQt(items[item]['image'])
                pixmap = QPixmap.fromImage(imageQt)

                self.addGridItem(text, pixmap, i, j)

                item += 1 and item != self.replicate


    def undo(self):
        """ Retira a útima imagem processada da lista e
        recalcula a posição de réplica. Ação só é realizada
        caso exista alguma imagem diferente da original.
        """

        if len(self.items) > 1:
            self.items.pop()
            self.replicate -= 1
            self.fillGrid(self.items)


    def insertOriginal(self, image):
        """ Insere a nova imagem em todas as posições do grid.

        @param image PIL.Image
        """

        image = image.resize((MainWidget.IMAGE_DIM, MainWidget.IMAGE_DIM),
                             Image.BICUBIC).convert('RGB')

        dim = image.size
        item = {'label': 'Original {}'.format(dim), 'image': image, 'dim': dim}

        self.items = [item]
        self.replicate = 0
                      
        self.fillGrid(self.items)


    def insertProcessed(self, image, label):
        """ Insere uma imagem recém processada no grid.
        
        @param image PIL.Image
        """
        
        # Variável usada para, caso grid não tenha sido completamente preenchido
        # ainda (contém cópias de alguma imagem), setar a nova imagem como a que
        # será replicada.
        self.replicate += 1

        dim = image.size
        image = image.resize((MainWidget.IMAGE_DIM, MainWidget.IMAGE_DIM),
                             Image.BICUBIC).convert('RGB')

        self.items.append({'label': label, 'image': image, 'dim': dim})
        self.fillGrid(self.items)
