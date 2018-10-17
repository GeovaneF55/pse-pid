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
from algorithm.filter.space_ops import (SpaceOps)

class DialogFilter(QDialog):
    def __init__(self, parent = None):
        super(DialogFilter, self).__init__(parent)

        self.selectedKey = SpaceOps.BOX
        self.selectedFilter = {'filter': self.selectedKey,
                               'mask': '3x3'}
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.initUI()


    def initUI(self):
        """ Cria todos os componentes referentes as transformações. """

        self.setWindowTitle('Filtros')

        # Filtros.
        self.labels = {}
        self.labels[SpaceOps.BOX] = QLabel('Box')
        self.labels[SpaceOps.MEDIAN] = QLabel('Mediana')
        self.labels[SpaceOps.MIN] = QLabel('Mínimo')
        self.labels[SpaceOps.MAX] = QLabel('Máximo')

        labelsLayout = QVBoxLayout()
        for key, label in self.labels.items():
            if key != SpaceOps.BOX:
                label.setEnabled(False)
                
            labelsLayout.addWidget(label)

        labelsWidget = QWidget()
        labelsWidget.setLayout(labelsLayout)

        # Máscaras.
        self.masks = {}
        self.masks[SpaceOps.BOX] = QComboBox()
        self.masks[SpaceOps.BOX].addItems(['3x3', '5x5', '7x7'])

        self.masks[SpaceOps.MEDIAN] = QComboBox()
        self.masks[SpaceOps.MEDIAN].addItems(['3x3', '5x5', '7x7'])
        
        self.masks[SpaceOps.MIN] = QComboBox()
        self.masks[SpaceOps.MIN].addItems(['3x3', '5x5', '7x7'])

        self.masks[SpaceOps.MAX] = QComboBox()
        self.masks[SpaceOps.MAX].addItems(['3x3', '5x5', '7x7'])

        masksLayout = QVBoxLayout()
        for key, mask in self.masks.items():
            if key != SpaceOps.BOX:
                mask.setEnabled(False)
                
            masksLayout.addWidget(mask)

        masksWidget = QWidget()
        masksWidget.setLayout(masksLayout)

        # Seleção do filtro.
        self.radioButtons = {}
        self.radioButtons[SpaceOps.BOX] = QRadioButton()
        self.radioButtons[SpaceOps.BOX].setChecked(True)
        self.radioButtons[SpaceOps.BOX]. \
            clicked.connect(lambda: self.selectFilter(SpaceOps.BOX))

        self.radioButtons[SpaceOps.MEDIAN] = QRadioButton()
        self.radioButtons[SpaceOps.MEDIAN].setChecked(False)
        self.radioButtons[SpaceOps.MEDIAN]. \
            clicked.connect(lambda: self.selectFilter(SpaceOps.MEDIAN))
        
        self.radioButtons[SpaceOps.MIN] = QRadioButton()
        self.radioButtons[SpaceOps.MIN].setChecked(False)
        self.radioButtons[SpaceOps.MIN]. \
            clicked.connect(lambda: self.selectFilter(SpaceOps.MIN))        
        
        self.radioButtons[SpaceOps.MAX]= QRadioButton()
        self.radioButtons[SpaceOps.MAX].setChecked(False)
        self.radioButtons[SpaceOps.MAX]. \
            clicked.connect(lambda: self.selectFilter(SpaceOps.MAX))
        
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
