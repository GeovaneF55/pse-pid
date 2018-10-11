from math import sqrt
from PyQt5.QtWidgets import qApp, QDesktopWidget, QMainWindow, QActionGroup
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtCore import Qt

from gui.action import Action
from gui.icon import lineIcon, circIcon, clearIcon, transformIcon, clipIcon, fillIcon
from gui.toolbar import ToolBar
from gui.painter import Painter

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.toolButtons = {}
        
        # Atalho definido para a ação de fechar o programa
        exitAct = Action(qApp.quit, self)
        exitAct.setShortcut('Ctrl+Q')
        self.addAction(exitAct)

        self.initUI()
        
    def initUI(self):
        """ Inicializa todos os widgets relacionados a janela
        principal do programa.
        """
        
        self.resize(1024, 512)
        self.center()
        self.setWindowTitle('Py-Paint')

        self.createMenuBar()        
        self.createToolBar()
        self.show()


    def createMenuBar(self):
        """ Cria o menu superior, adicionando os devidos
        submenus e suas respectivas ações.
        """
        
        self.menubar = self.menuBar()

        menu = self.menubar.addMenu('Algoritmos')

        # Submenu referente aos algoritmos relacionados
        # a construção de retas.
        #submenu = menu.addMenu('Retas')
        #group  = QActionGroup(submenu)

        #action = Action(lambda: self.lines.setFn(bresenham.line),
        #                   group, 'Bresenham', True)
        #action.setChecked(True)
        #submenu.addAction(action)

        #action = Action(lambda: self.lines.setFn(dda.line) , group, 'DDA', True)
        #submenu.addAction(action)

    def createToolBar(self):
        """ Cria o menu de ferramentas lateral, adicionando
        as devidas ferramentas.
        """
        
        self.toolbar = ToolBar(self)
        self.toolbar.setMovable(False)

        # Agrupamento de ações que apresentam como característica
        # o fato de permanecerem marcadas, para serem usadas de forma
        # contínua.
        #group  = QActionGroup(self.toolbar)
        #action = Action(lambda: self.toolbar.chooseAction(ToolBar.TOOLS.line),
        #                group, "Linha", True, lineIcon())
        #self.toolbar.addAction(action, ToolBar.TOOLS.line)

        # Inclusão propriamente dita da barra de ferramentas
        # a janela principal.
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)

        
    def center(self):
        """ Centraliza a janela principal, em relação ao Desktop. """
        
        frame = self.frameGeometry()
        cpoint = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(cpoint)
        self.move(frame.topLeft())