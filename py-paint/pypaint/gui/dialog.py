from PyQt5.QtWidgets import (QButtonGroup,
                             QDialog,
                             QDialogButtonBox,
                             QCheckBox,
                             QGridLayout,
                             QHBoxLayout,
                             QLabel,
                             QLayout,
                             QPushButton,
                             QRadioButton,
                             QSpinBox,
                             QDoubleSpinBox,
                             QWidget)
from PyQt5.QtCore import Qt

class TransformDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.initUI()

    def initUI(self):
        """ Cria todos os componentes referentes as transformações. """

        okButton = QPushButton('OK')
        okButton.setDefault(True)
        okButton.clicked \
                .connect(lambda: self.parent.transform(self))

        cancelButton = QPushButton('Cancelar')
        cancelButton.setShortcut('Ctrl+Q')
        cancelButton.clicked \
                    .connect(lambda: self.close())

        buttonBox = QDialogButtonBox(Qt.Horizontal)
        buttonBox.addButton(okButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(cancelButton, QDialogButtonBox.ActionRole)

        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addWidget(buttonBox, 0, 0)

        self.setLayout(mainLayout)
        self.setWindowTitle('Teste')