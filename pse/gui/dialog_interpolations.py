from PyQt5.QtWidgets import (QDialog,
                            QDialogButtonBox,
                            QComboBox,
                            QFormLayout)
from PyQt5.QtCore import (Qt)

class DialogInterpolations(QDialog):


    def __init__(self, parent = None):
        super(DialogInterpolations, self).__init__(parent)
        #self.setAttribute(Qt.WA_DeleteOnClose)
        self.initUI()


    def initUI(self):
        layout = QFormLayout(self)

		# Input Tipo de Interpolação
        self.type = QComboBox()
        self.type.addItems(["Vizinho Mais Próximo", "Bilinear", "Bicúbica"])
        self.type.currentIndexChanged.connect(self.selectionchange)
        layout.addRow("Tipo de Interpolação: ", self.type)

        # Butões de OK e Cancel
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)


    def selectionchange(self, i):
        pass


    def getAxis(self):
        return self.type.currentText()


    @staticmethod
    def getResults(parent = None):
        """ Método estático que cria o dialog e retorna (type_interpolation, aceito) """
        dialog = DialogInterpolations(parent)
        result = dialog.exec_()
        type_interpolation = dialog.getAxis()
        return (type_interpolation, result == QDialog.Accepted)
