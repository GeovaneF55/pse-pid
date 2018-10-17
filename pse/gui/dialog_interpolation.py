""" Bibliotecas externas. """
from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QDialog,
                             QDialogButtonBox,
                             QDoubleSpinBox,
                             QComboBox,
                             QFormLayout)

class DialogInterpolation(QDialog):
    def __init__(self, parent = None):
        super(DialogInterpolation, self).__init__(parent)
        #self.setAttribute(Qt.WA_DeleteOnClose)
        self.initUI()


    def initUI(self):
        layout = QFormLayout(self)

        # Input Ampliação/Redução
        self.scale = QDoubleSpinBox()
        self.scale.setRange(-2, 2)
        layout.addRow("Ampliação/Redução: ", self.scale)

	    # Input Tipo de Interpolação
        self.type = QComboBox()
        self.type.addItems(["Vizinho Mais Próximo", "Bilinear", "Bicúbica"])
        self.type.currentIndexChanged.connect(self.selectionchange)
        layout.addRow("Tipo de Interpolação: ", self.type)

        # Botões de OK e Cancel
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)


    def selectionchange(self, i):
        pass


    def getTypeInt(self):
        return self.type.currentText()

    
    def getScale(self):
        return self.scale.text()


    @staticmethod
    def getResults(parent = None):
        """ Método estático que cria o dialog e retorna (type_interpolation, aceito) """
        dialog = DialogInterpolation(parent)
        result = dialog.exec_()
        typeInt = dialog.getTypeInt()
        scale = dialog.getScale()

        return ({'type_inpertpolation':typeInt, 'ampliacao_reducao':scale}, result == QDialog.Accepted)
