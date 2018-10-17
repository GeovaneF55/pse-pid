""" Bibliotecas externas. """
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QComboBox,
                             QDialogButtonBox,
                             QDialog,
                             QHBoxLayout,
                             QLabel,
                             QRadioButton,
                             QVBoxLayout,
                             QWidget)


""" Biliotecas locais. """
from algorithm.filter import (low_pass,
                              morph)

class DialogFilter(QDialog):
    def __init__(self, parent = None):
        super(DialogFilter, self).__init__(parent)

        self.selectedKey = low_pass.Filter.BOX
        self.selectedFilter = {'filter': self.selectedKey,
                               'mask': '3x3'}
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.initUI()


    def initUI(self):
        """ Cria todos os componentes referentes as transformações. """

        self.setWindowTitle('Filtros')

        # Filtros.
        self.labels = {}
        self.labels[low_pass.Filter.BOX] = QLabel('Box')
        self.labels[low_pass.Filter.MEDIAN] = QLabel('Mediana')
        self.labels[morph.Filter.MIN] = QLabel('Mínimo')
        self.labels[morph.Filter.MAX] = QLabel('Máximo')

        labelsLayout = QVBoxLayout()
        for key, label in self.labels.items():
            if key != low_pass.Filter.BOX:
                label.setEnabled(False)
                
            labelsLayout.addWidget(label)

        labelsWidget = QWidget()
        labelsWidget.setLayout(labelsLayout)

        # Máscaras.
        self.masks = {}
        self.masks[low_pass.Filter.BOX] = QComboBox()
        self.masks[low_pass.Filter.BOX].addItems(['3x3', '5x5', '7x7'])

        self.masks[low_pass.Filter.MEDIAN] = QComboBox()
        self.masks[low_pass.Filter.MEDIAN].addItems(['3x3', '5x5', '7x7'])
        
        self.masks[morph.Filter.MIN] = QComboBox()
        self.masks[morph.Filter.MIN].addItems(['3x3', '5x5', '7x7'])

        self.masks[morph.Filter.MAX] = QComboBox()
        self.masks[morph.Filter.MAX].addItems(['3x3', '5x5', '7x7'])

        masksLayout = QVBoxLayout()
        for key, mask in self.masks.items():
            if key != low_pass.Filter.BOX:
                mask.setEnabled(False)
                
            masksLayout.addWidget(mask)

        masksWidget = QWidget()
        masksWidget.setLayout(masksLayout)

        # Seleção do filtro.
        self.radioButtons = {}
        self.radioButtons[low_pass.Filter.BOX] = QRadioButton()
        self.radioButtons[low_pass.Filter.BOX].setChecked(True)
        self.radioButtons[low_pass.Filter.BOX]. \
            clicked.connect(lambda: self.selectFilter(low_pass.Filter.BOX))

        self.radioButtons[low_pass.Filter.MEDIAN] = QRadioButton()
        self.radioButtons[low_pass.Filter.MEDIAN].setChecked(False)
        self.radioButtons[low_pass.Filter.MEDIAN]. \
            clicked.connect(lambda: self.selectFilter(low_pass.Filter.MEDIAN))
        
        self.radioButtons[morph.Filter.MIN] = QRadioButton()
        self.radioButtons[morph.Filter.MIN].setChecked(False)
        self.radioButtons[morph.Filter.MIN]. \
            clicked.connect(lambda: self.selectFilter(morph.Filter.MIN))        
        
        self.radioButtons[morph.Filter.MAX]= QRadioButton()
        self.radioButtons[morph.Filter.MAX].setChecked(False)
        self.radioButtons[morph.Filter.MAX]. \
            clicked.connect(lambda: self.selectFilter(morph.Filter.MAX))
        
        radioButtonsLayout = QVBoxLayout()
        for key, button in self.radioButtons.items():
            radioButtonsLayout.addWidget(button)
            
        radioButtonsWidget = QWidget()
        radioButtonsWidget.setLayout(radioButtonsLayout)
        
        # Layout.
        sublayout = QHBoxLayout()
        sublayout.addWidget(labelsWidget)
        sublayout.addWidget(masksWidget)
        sublayout.addWidget(radioButtonsWidget)

        # Botões de OK e Cancel.
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.getFilter)
        buttons.rejected.connect(self.reject)

        subwidget = QWidget()
        subwidget.setLayout(sublayout)

        # Layout principal.
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(subwidget)
        mainLayout.addWidget(buttons)
        
        self.setLayout(mainLayout)


    def getFilter(self):
        self.selectedFilter = {'filter': self.selectedKey,
                               'mask': self.masks[self.selectedKey].currentText()}

        return self.accept()
    
    
    def selectFilter(self, selectedKey):
        """ Seta as configurações do filtro selecionado."""
        
        for key, _ in self.radioButtons.items():
            selected = key == selectedKey
            self.labels[key].setEnabled(selected)
            self.masks[key].setEnabled(selected)

        self.selectedKey = selectedKey

        
    @staticmethod
    def getResults(parent = None):
        """ Método estático que cria o dialog e retorna uma tupla contendo:
        1- dicionário com as configurações do filtro selecionado
        2- dialog aceito/cancelado
        """

        dialog = DialogFilter(parent)
        result = dialog.exec_()

        return (dialog.selectedFilter, result)
