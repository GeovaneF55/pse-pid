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
from gui.spinbox import DoubleTextSpinBox

class DialogFilter(QDialog):
    def __init__(self, parent = None):
        super(DialogFilter, self).__init__(parent)

        self.selectedKey = low_pass.Filter.BOX
        self.selectedFilter = {'filter': self.selectedKey,
                               'opt': '3x3'}
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.initUI()


    def initUI(self):
        """ Cria todos os componentes referentes as transformações. """

        self.setWindowTitle('Filtros')

        # Filtros.
        self.labels = {}
        self.labels[low_pass.Filter.BOX] = QLabel('Box')
        self.labels[low_pass.Filter.MEDIAN] = QLabel('Mediana')
        self.labels[low_pass.Filter.GAUSSIAN] = QLabel('Gaussiano')
        self.labels[morph.Filter.DILATION] = QLabel('Dilatação')
        self.labels[morph.Filter.EROSION] = QLabel('Erosão')
        self.labels[morph.Filter.OPENING] = QLabel('Abertura')
        self.labels[morph.Filter.CLOSING] = QLabel('Fechamento')

        labelsLayout = QVBoxLayout()
        for key, label in self.labels.items():
            if key != low_pass.Filter.BOX:
                label.setEnabled(False)
                
            labelsLayout.addWidget(label)

        labelsWidget = QWidget()
        labelsWidget.setLayout(labelsLayout)

        # Máscaras.
        self.opts = {}
        self.opts[low_pass.Filter.BOX] = QComboBox()
        self.opts[low_pass.Filter.BOX].addItems(['3x3', '5x5', '7x7'])

        self.opts[low_pass.Filter.MEDIAN] = QComboBox()
        self.opts[low_pass.Filter.MEDIAN].addItems(['3x3', '5x5', '7x7'])

        self.opts[low_pass.Filter.GAUSSIAN] = DoubleTextSpinBox()
        self.opts[low_pass.Filter.GAUSSIAN].setSingleStep(0.5)
        self.opts[low_pass.Filter.GAUSSIAN].setRange(1, 11)
        
        self.opts[morph.Filter.DILATION] = QComboBox()
        self.opts[morph.Filter.DILATION].addItems(['3x3', '5x5', '7x7'])

        self.opts[morph.Filter.EROSION] = QComboBox()
        self.opts[morph.Filter.EROSION].addItems(['3x3', '5x5', '7x7'])

        self.opts[morph.Filter.OPENING] = QComboBox()
        self.opts[morph.Filter.OPENING].addItems(['3x3', '5x5', '7x7'])

        self.opts[morph.Filter.CLOSING] = QComboBox()
        self.opts[morph.Filter.CLOSING].addItems(['3x3', '5x5', '7x7'])
                
        optsLayout = QVBoxLayout()
        for key, opt in self.opts.items():
            if key != low_pass.Filter.BOX:
                opt.setEnabled(False)
                
            optsLayout.addWidget(opt)

        optsWidget = QWidget()
        optsWidget.setLayout(optsLayout)

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

        self.radioButtons[low_pass.Filter.GAUSSIAN] = QRadioButton()
        self.radioButtons[low_pass.Filter.GAUSSIAN].setChecked(False)
        self.radioButtons[low_pass.Filter.GAUSSIAN]. \
            clicked.connect(lambda: self.selectFilter(low_pass.Filter.GAUSSIAN))
        
        self.radioButtons[morph.Filter.DILATION]= QRadioButton()
        self.radioButtons[morph.Filter.DILATION].setChecked(False)
        self.radioButtons[morph.Filter.DILATION]. \
            clicked.connect(lambda: self.selectFilter(morph.Filter.DILATION))
        
        self.radioButtons[morph.Filter.EROSION] = QRadioButton()
        self.radioButtons[morph.Filter.EROSION].setChecked(False)
        self.radioButtons[morph.Filter.EROSION]. \
            clicked.connect(lambda: self.selectFilter(morph.Filter.EROSION))

        self.radioButtons[morph.Filter.OPENING]= QRadioButton()
        self.radioButtons[morph.Filter.OPENING].setChecked(False)
        self.radioButtons[morph.Filter.OPENING]. \
            clicked.connect(lambda: self.selectFilter(morph.Filter.OPENING))
        
        self.radioButtons[morph.Filter.CLOSING] = QRadioButton()
        self.radioButtons[morph.Filter.CLOSING].setChecked(False)
        self.radioButtons[morph.Filter.CLOSING]. \
            clicked.connect(lambda: self.selectFilter(morph.Filter.CLOSING))
        
        radioButtonsLayout = QVBoxLayout()
        radioButtonsLayout.setContentsMargins(0, 0, 0, 0)
        for key, button in self.radioButtons.items():
            radioButtonsLayout.addWidget(button)
            
        radioButtonsWidget = QWidget()
        radioButtonsWidget.setLayout(radioButtonsLayout)
        
        # Layout.
        sublayout = QHBoxLayout()
        sublayout.addWidget(labelsWidget)
        sublayout.addWidget(optsWidget)
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
                               'opt': self.opts[self.selectedKey].currentText()}

        return self.accept()
    
    
    def selectFilter(self, selectedKey):
        """ Seta as configurações do filtro selecionado."""
        
        for key, _ in self.radioButtons.items():
            selected = key == selectedKey
            self.labels[key].setEnabled(selected)
            self.opts[key].setEnabled(selected)

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
