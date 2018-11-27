""" Bibliotecas externas. """
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDialog,
                             QDialogButtonBox,
                             QDoubleSpinBox,
                             QComboBox,
                             QFormLayout)

class DialogInterpolation(QDialog):
    MIN_SCALE = 0.1
    MAX_SCALE = 0.9
    
    def __init__(self, parent = None):
        super(DialogInterpolation, self).__init__(parent)

        self.data = {'type': 'Nearest', 'scale': DialogInterpolation.MIN_SCALE}
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.initUI()


    def initUI(self):

        self.setWindowTitle('Interpolações')

        layout = QFormLayout(self)

        # Input Ampliação/Redução
        self.scaleBox = QDoubleSpinBox()
        self.scaleBox.setSingleStep(DialogInterpolation.MIN_SCALE)
        self.scaleBox.setRange(DialogInterpolation.MIN_SCALE,
                               DialogInterpolation.MAX_SCALE)
        self.scaleBox.valueChanged.connect(self.updateScale)
        layout.addRow("Ampliação/Redução: ", self.scaleBox)

	    # Input Tipo de Interpolação
        self.typeBox = QComboBox()
        self.typeBox.addItems(["Vizinho Mais Próximo", "Bilinear", "Bicúbica"])
        self.typeBox.currentIndexChanged.connect(self.updateType)
        layout.addRow("Tipo de Interpolação: ", self.typeBox)

        # Botões de OK e Cancel
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)


    def updateScale(self):
        self.data['scale'] = self.scaleBox.value()

        
    def updateType(self):
        self.data['type'] = self.typeBox.currentText()


    @staticmethod
    def getResults(parent = None):
        """ Método estático que cria o dialog e retorna (type_interpolation, aceito) """
        dialog = DialogInterpolation(parent)
        result = dialog.exec_()        

        return (dialog.data, result)
