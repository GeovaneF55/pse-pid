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
from algorithm.filter import (low_pass)
from gui.spinbox import DoubleTextSpinBox

class DialogLowPass(QDialog):
    def __init__(self, parent = None):
        super(DialogLowPass, self).__init__(parent)

        self.selectedKey = low_pass.Filter.BOX
        self.selectedFilter = {'filter': self.selectedKey,
                               'opt': '3x3'}
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.initUI()


    def initUI(self):
        """ Cria todos os componentes referentes as transformações. """

        self.setWindowTitle('Filtros Passa-Baixa')

        # Filtros (F).
        self.labels = {}
        # F: Passa-Baixa
        self.labels[low_pass.Filter.BOX] = QLabel('Box')
        self.labels[low_pass.Filter.MEDIAN] = QLabel('Mediana')
        self.labels[low_pass.Filter.GAUSSIAN] = QLabel('Gaussiano')

        labelsLayout = QVBoxLayout()
        for key, label in self.labels.items():
            if key != low_pass.Filter.BOX:
                label.setEnabled(False)
                
            labelsLayout.addWidget(label)

        labelsWidget = QWidget()
        labelsWidget.setLayout(labelsLayout)

        # Máscaras(M).
        self.opts = {}
        # M: Passa-Baixa
        self.opts[low_pass.Filter.BOX] = QComboBox()
        self.opts[low_pass.Filter.BOX].addItems(['3x3', '5x5', '7x7'])

        self.opts[low_pass.Filter.MEDIAN] = QComboBox()
        self.opts[low_pass.Filter.MEDIAN].addItems(['3x3', '5x5', '7x7'])

        self.opts[low_pass.Filter.GAUSSIAN] = DoubleTextSpinBox()
        self.opts[low_pass.Filter.GAUSSIAN].setSingleStep(0.5)
        self.opts[low_pass.Filter.GAUSSIAN].setRange(1, 11)
                
        optsLayout = QVBoxLayout()
        for key, opt in self.opts.items():
            if key != low_pass.Filter.BOX:
                opt.setEnabled(False)
                
            optsLayout.addWidget(opt)

        optsWidget = QWidget()
        optsWidget.setLayout(optsLayout)

        # Seleção do Filtro (S).
        self.radioButtons = {}
        # S: Passa-Baixa
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

        dialog = DialogLowPass(parent)
        result = dialog.exec_()

        return (dialog.selectedFilter, result)
