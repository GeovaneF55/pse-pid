""" Bibliotecas externas. """
from PyQt5.QtWidgets import (QCheckBox,
                             QComboBox,
                             QDialog,
                             QHBoxLayout,
                             QLabel,
                             QVBoxLayout,
                             QWidget)
from PyQt5.QtCore import (Qt)


class DialogFilters(QDialog):
    def __init__(self, parent = None):
        super(DialogFilters, self).__init__(parent)

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.initUI()


    def initUI(self):
        """ Cria todos os componentes referentes as transformações. """

        self.setWindowTitle('Filtros')

        # Filtros
        minLabel = QLabel('Mínimo')
        maxLabel = QLabel('Máximo')

        labelsLayout = QVBoxLayout()
        labelsLayout.addWidget(minLabel)
        labelsLayout.addWidget(maxLabel)

        labelsWidget = QWidget()
        labelsWidget.setLayout(labelsLayout)

        # Máscaras
        minMask = QComboBox()
        minMask.addItems(['3x3', '5x5', '7x7', '9x9', '11x11'])

        maxMask = QComboBox()
        maxMask.addItems(['3x3', '5x5', '7x7', '9x9', '11x11'])

        masksLayout = QVBoxLayout()
        masksLayout.addWidget(minMask)
        masksLayout.addWidget(maxMask)

        masksWidget = QWidget()
        masksWidget.setLayout(masksLayout)

        # Checkbox
        minCheckBox = QCheckBox()
        minCheckBox.setChecked(False)

        maxCheckBox = QCheckBox()
        maxCheckBox.setChecked(False)

        checkBoxesLayout = QVBoxLayout()
        checkBoxesLayout.addWidget(minCheckBox)
        checkBoxesLayout.addWidget(maxCheckBox)        

        checkBoxesWidget = QWidget()
        checkBoxesWidget.setLayout(checkBoxesLayout)
        
        # Layout principal
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(labelsWidget)
        mainLayout.addWidget(masksWidget)
        mainLayout.addWidget(checkBoxesWidget)
        
        self.setLayout(mainLayout)


    @staticmethod
    def getResults(parent = None):
        """ Método estático que cria o dialog e retorna uma tupla contendo:
        1- dicionário com todos os filtros selecionados e suas respectivas
        configurações.
        2- dialog aceito/cancelado
        """

        dialog = DialogFilters(parent)
        result = dialog.exec_()
        return ({}, result)
