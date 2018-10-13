""" Bibliotecas externas. """
from enum import Enum
from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QComboBox,
                             QDialogButtonBox,
                             QDialog,
                             QHBoxLayout,
                             QLabel,
                             QRadioButton,
                             QVBoxLayout,
                             QWidget)

class DialogFilter(QDialog):
    Filter = Enum('Filter', 'MIN MAX')
    
    def __init__(self, parent = None):
        super(DialogFilter, self).__init__(parent)

        self.selectedFilter = {'filter': DialogFilter.Filter.MIN,
                               'mask': '3x3'}
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.initUI()


    def initUI(self):
        """ Cria todos os componentes referentes as transformações. """

        self.setWindowTitle('Filtros')

        # Filtros.
        self.labels = {}
        self.labels[DialogFilter.Filter.MIN] = QLabel('Mínimo')
        self.labels[DialogFilter.Filter.MAX] = QLabel('Máximo')

        labelsLayout = QVBoxLayout()
        for key, label in self.labels.items():
            if key != DialogFilter.Filter.MIN:
                label.setEnabled(False)
                
            labelsLayout.addWidget(label)

        labelsWidget = QWidget()
        labelsWidget.setLayout(labelsLayout)

        # Máscaras.
        self.masks = {}
        self.masks[DialogFilter.Filter.MIN] = QComboBox()
        self.masks[DialogFilter.Filter.MIN].addItems(['3x3', '5x5', '7x7',
                                                      '9x9', '11x11'])

        self.masks[DialogFilter.Filter.MAX] = QComboBox()
        self.masks[DialogFilter.Filter.MAX].addItems(['3x3', '5x5', '7x7',
                                                      '9x9', '11x11'])

        masksLayout = QVBoxLayout()
        for key, mask in self.masks.items():
            if key != DialogFilter.Filter.MIN:
                mask.setEnabled(False)
                
            masksLayout.addWidget(mask)

        masksWidget = QWidget()
        masksWidget.setLayout(masksLayout)

        # Seleção do filtro.
        self.radioButtons = {}
        self.radioButtons[DialogFilter.Filter.MIN] = QRadioButton()
        self.radioButtons[DialogFilter.Filter.MIN].setChecked(True)
        self.radioButtons[DialogFilter.Filter.MIN].\
            clicked.connect(lambda: self.selectFilter(DialogFilter.Filter.MIN))        
        
        self.radioButtons[DialogFilter.Filter.MAX]= QRadioButton()
        self.radioButtons[DialogFilter.Filter.MAX].setChecked(False)
        self.radioButtons[DialogFilter.Filter.MAX].\
            clicked.connect(lambda: self.selectFilter(DialogFilter.Filter.MAX))
        
        radioButtonsLayout = QVBoxLayout()
        for key, button in self.radioButtons.items():
            radioButtonsLayout.addWidget(button)
            
        radioButtonsWidget = QWidget()
        radioButtonsWidget.setLayout(radioButtonsLayout)
        
        # Layout intermediário.
        sublayout = QHBoxLayout()
        sublayout.addWidget(labelsWidget)
        sublayout.addWidget(masksWidget)
        sublayout.addWidget(radioButtonsWidget)

        # Botões de OK e Cancel.
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        subwidget = QWidget()
        subwidget.setLayout(sublayout)

        # Layout principal.
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(subwidget)
        mainLayout.addWidget(buttons)
        
        self.setLayout(mainLayout)


    def selectFilter(self, selectedKey):
        """ Seta as configurações do filtro selecionado."""
        
        for key, _ in self.radioButtons.items():
            selected = key == selectedKey
            self.labels[key].setEnabled(selected)
            self.masks[key].setEnabled(selected)

        self.selectedFilter = {'filter': selectedKey,
                               'mask': self.masks[key].currentText()}


    @staticmethod
    def getResults(parent = None):
        """ Método estático que cria o dialog e retorna uma tupla contendo:
        1- dicionário com as configurações do filtro selecionado
        2- dialog aceito/cancelado
        """

        dialog = DialogFilter(parent)
        result = dialog.exec_()

        return (dialog.selectedFilter, result)
