""" Bibliotecas externas. """
from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QComboBox,
                             QDialogButtonBox,
                             QDialog,
                             QHBoxLayout,
                             QLabel,
                             QRadioButton,
                             QVBoxLayout,
                             QWidget)


""" Biliotecas locais. """
from algorithm.filter.low_pass import (LowPassFilter)

class DialogFilter(QDialog):
    def __init__(self, parent = None):
        super(DialogFilter, self).__init__(parent)

        self.selectedKey = LowPassFilter.BOX
        self.selectedFilter = {'filter': self.selectedKey,
                               'mask': '3x3'}
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.initUI()


    def initUI(self):
        """ Cria todos os componentes referentes as transformações. """

        self.setWindowTitle('Filtros')

        # Filtros.
        self.labels = {}
        self.labels[LowPassFilter.BOX] = QLabel('Box')
        self.labels[LowPassFilter.MEDIAN] = QLabel('Mediana')
        self.labels[LowPassFilter.MODE] = QLabel('Moda')
        self.labels[LowPassFilter.MIN] = QLabel('Mínimo')
        self.labels[LowPassFilter.MAX] = QLabel('Máximo')

        labelsLayout = QVBoxLayout()
        for key, label in self.labels.items():
            if key != LowPassFilter.BOX:
                label.setEnabled(False)
                
            labelsLayout.addWidget(label)

        labelsWidget = QWidget()
        labelsWidget.setLayout(labelsLayout)

        # Máscaras.
        self.masks = {}
        self.masks[LowPassFilter.BOX] = QComboBox()
        self.masks[LowPassFilter.BOX].addItems(['3x3', '5x5', '7x7'])

        self.masks[LowPassFilter.MEDIAN] = QComboBox()
        self.masks[LowPassFilter.MEDIAN].addItems(['3x3', '5x5', '7x7'])

        self.masks[LowPassFilter.MODE] = QComboBox()
        self.masks[LowPassFilter.MODE].addItems(['3x3', '5x5', '7x7'])
        
        self.masks[LowPassFilter.MIN] = QComboBox()
        self.masks[LowPassFilter.MIN].addItems(['3x3', '5x5', '7x7'])

        self.masks[LowPassFilter.MAX] = QComboBox()
        self.masks[LowPassFilter.MAX].addItems(['3x3', '5x5', '7x7'])

        masksLayout = QVBoxLayout()
        for key, mask in self.masks.items():
            if key != LowPassFilter.BOX:
                mask.setEnabled(False)
                
            masksLayout.addWidget(mask)

        masksWidget = QWidget()
        masksWidget.setLayout(masksLayout)

        # Seleção do filtro.
        self.radioButtons = {}
        self.radioButtons[LowPassFilter.BOX] = QRadioButton()
        self.radioButtons[LowPassFilter.BOX].setChecked(True)
        self.radioButtons[LowPassFilter.BOX]. \
            clicked.connect(lambda: self.selectFilter(LowPassFilter.BOX))

        self.radioButtons[LowPassFilter.MEDIAN] = QRadioButton()
        self.radioButtons[LowPassFilter.MEDIAN].setChecked(False)
        self.radioButtons[LowPassFilter.MEDIAN]. \
            clicked.connect(lambda: self.selectFilter(LowPassFilter.MEDIAN))

        self.radioButtons[LowPassFilter.MODE] = QRadioButton()
        self.radioButtons[LowPassFilter.MODE].setChecked(False)
        self.radioButtons[LowPassFilter.MODE]. \
            clicked.connect(lambda: self.selectFilter(LowPassFilter.MODE))
        
        self.radioButtons[LowPassFilter.MIN] = QRadioButton()
        self.radioButtons[LowPassFilter.MIN].setChecked(False)
        self.radioButtons[LowPassFilter.MIN]. \
            clicked.connect(lambda: self.selectFilter(LowPassFilter.MIN))        
        
        self.radioButtons[LowPassFilter.MAX]= QRadioButton()
        self.radioButtons[LowPassFilter.MAX].setChecked(False)
        self.radioButtons[LowPassFilter.MAX]. \
            clicked.connect(lambda: self.selectFilter(LowPassFilter.MAX))
        
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
